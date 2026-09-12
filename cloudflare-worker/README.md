# Image Evaluator AI Assistant Cloudflare Worker

Cloudflare Worker 反向代理，支持任何 OpenAI 兼容 API（DeepSeek, OpenAI, Minimax, Groq 等），为文档站提供流式 SSE 问答与指标诊断。

## 环境变量配置

在 `wrangler.toml` 或 Cloudflare Dashboard 中配置：
- `AI_API_BASE`: 上游 API 地址，如 `https://api.deepseek.com/v1` 或 `https://api.openai.com/v1`
- `AI_MODEL`: 模型标识，如 `deepseek-chat` 或 `gpt-4o-mini`

密钥配置：
```bash
npx wrangler secret put AI_API_KEY
```

## 部署流程

```bash
cd docs-site/cloudflare-worker
npx wrangler login
npx wrangler deploy
```

部署完成后，将生成的 Worker URL 配置到 GitHub 仓库（`image-evaluator/docs`）的 Actions Secret：
`AI_WORKER_URL = https://image-evaluator-ai-assistant.<subdomain>.workers.dev`

