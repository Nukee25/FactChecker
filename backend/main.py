import asyncio
import json

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from services.ai_detector import detect_ai_content
from services.claim_extractor import extract_claims
from services.evidence_retriever import retrieve_evidence
from services.media_checker import check_media_authenticity, check_media_from_url
from services.url_extractor import extract_url_content
from services.verifier import verify_claim

TRUE_CLAIM_WEIGHT = 100
PARTIAL_CLAIM_WEIGHT = 50

app = FastAPI(title="FactChecker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VerifyRequest(BaseModel):
    input: str
    input_type: str = "text"


def sse(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.post("/api/check-media")
async def check_media(
    file: UploadFile | None = File(default=None),
    url: str | None = Form(default=None),
):
    if file is not None:
        image_data = await file.read()
        result = await check_media_authenticity(image_data)
    elif url:
        result = await check_media_from_url(url)
    else:
        return {"error": "Provide either a file or a url"}
    return result


@app.post("/api/verify")
async def verify(request: VerifyRequest):
    async def stream():
        try:
            yield sse({"stage": "extracting", "progress": 5, "message": "Extracting content..."})

            if request.input_type == "url":
                content = await extract_url_content(request.input)
                if not content:
                    content = request.input
            else:
                content = request.input

            yield sse({"stage": "extracting", "progress": 15, "message": "Content extracted. Analyzing for claims..."})

            ai_detection = await detect_ai_content(content)
            yield sse({"stage": "ai_detection", "progress": 25, "message": "AI detection complete.", "ai_detection": ai_detection})

            claims = await asyncio.get_event_loop().run_in_executor(None, extract_claims, content)
            yield sse({"stage": "claims_extracted", "progress": 35, "message": f"Found {len(claims)} claims to verify.", "claims_count": len(claims)})

            verified_claims = []
            total = len(claims)

            for i, claim in enumerate(claims):
                progress = 35 + int((i / max(total, 1)) * 55)
                yield sse({
                    "stage": "verifying",
                    "progress": progress,
                    "message": f"Verifying claim {i + 1} of {total}: {claim[:80]}...",
                    "current_claim": i + 1,
                    "total_claims": total,
                })

                evidence = await retrieve_evidence(claim)
                result = await verify_claim(claim, evidence)
                result["claim"] = claim
                verified_claims.append(result)

                yield sse({
                    "stage": "claim_verified",
                    "progress": progress + 2,
                    "message": f"Claim {i + 1} verified: {result.get('verdict', 'Unverifiable')}",
                    "claim_result": result,
                })

            true_count = sum(1 for c in verified_claims if c.get("verdict") == "True")
            false_count = sum(1 for c in verified_claims if c.get("verdict") == "False")
            partial_count = sum(1 for c in verified_claims if c.get("verdict") == "Partially True")
            unverifiable_count = sum(1 for c in verified_claims if c.get("verdict") == "Unverifiable")
            overall_score = (true_count * TRUE_CLAIM_WEIGHT + partial_count * PARTIAL_CLAIM_WEIGHT) / max(total, 1)

            report = {
                "overall_score": round(overall_score, 1),
                "total_claims": total,
                "true_count": true_count,
                "false_count": false_count,
                "partial_count": partial_count,
                "unverifiable_count": unverifiable_count,
                "claims": verified_claims,
                "ai_detection": ai_detection,
                "content_preview": content[:500],
            }

            yield sse({"stage": "complete", "progress": 100, "message": "Verification complete!", "report": report})

        except Exception as exc:
            yield sse({"stage": "error", "progress": 0, "message": str(exc)})

    return StreamingResponse(stream(), media_type="text/event-stream")
