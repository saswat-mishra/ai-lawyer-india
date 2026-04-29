/** @type {import('next').NextConfig} */
const isDev = process.env.NODE_ENV !== "production";
const nextConfig = {
  reactStrictMode: true,
  // In dev, the FastAPI backend runs on :8000.
  // In prod (Vercel), /api/* is served by api/index.py serverless function on the same origin
  // — no rewrite needed.
  async rewrites() {
    if (!isDev) return [];
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000"}/api/:path*`,
      },
    ];
  },
};
module.exports = nextConfig;
