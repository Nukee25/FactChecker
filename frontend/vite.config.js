import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const apiTarget = process.env.VITE_API_PROXY_TARGET || 'http://yatharth.duckdns.org/api' || 'http://172.24.0.2:8000'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // listen on all interfaces
    port: 5173,      // comma here is essential
    allowedHosts: [
      'yatharth.duckdns.org'
    ],
    proxy: {
      '/api': apiTarget
    }
  }
})
