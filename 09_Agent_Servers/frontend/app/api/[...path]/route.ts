import { initApiPassthrough } from "langgraph-nextjs-api-passthrough";

export const { GET, POST, PUT, PATCH, DELETE, OPTIONS, runtime } =
  initApiPassthrough({
    apiUrl: process.env.LANGGRAPH_API_URL,
    apiKey: process.env.LANGSMITH_API_KEY,
    runtime: "edge",
    // Force uncompressed upstream so the edge proxy can't forward a stale
    // `content-encoding: gzip` header on a decompressed body (browser then
    // fails with ERR_CONTENT_DECODING_FAILED).
    headers: () => ({ "accept-encoding": "identity" }),
  });
