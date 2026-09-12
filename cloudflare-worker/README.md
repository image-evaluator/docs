# Image Evaluator AI Assistant Cloudflare Worker

This directory contains the Cloudflare Worker proxy that connects the Image Evaluator documentation site to the Agnes API (`agnes-2.5-flash`). It injects Level 0 evaluation domain knowledge and streams responses back with CORS support.

## Architecture

- **Runtime**: Cloudflare Workers (V8 edge isolates)
- **Model**: `agnes-2.5-flash`
- **Upstream API**: `https://api.agnes.ai/v1/chat/completions`
- **Features**:
  - Full CORS headers (`OPTIONS` preflight and `POST` responses)
  - Level 0 system prompt injection (covering all 9 metrics, formulas, and CLI reproduction commands)
  - Native `text/event-stream` Server-Sent Events (SSE) streaming proxy
  - Clean error reporting and graceful status codes

## Setup and Deployment

### 1. Install Dependencies

```bash
cd docs-site/cloudflare-worker
bun install

```

### 2. Configure Secrets

Set your Agnes API key as an encrypted Cloudflare secret:

```bash
npx wrangler secret put AGNES_API_KEY

```

When prompted, paste your secret key.

### 3. Local Development

Run the worker locally on `http://localhost:8787`:

```bash
npx wrangler dev

```

You can test the endpoint using curl:

```bash
curl -X POST http://localhost:8787/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "How do I evaluate face consistency?"}
    ],
    "stream": false
  }'

```

### 4. Production Deployment

Deploy the worker to your Cloudflare account:

```bash
npx wrangler deploy

```

Once deployed, copy your assigned worker URL (e.g. `https://image-evaluator-ai-assistant.<subdomain>.workers.dev`) and set it in your documentation site environment:

```env
NEXT_PUBLIC_AI_WORKER_URL=https://image-evaluator-ai-assistant.<subdomain>.workers.dev

```

