export interface Env {
  AI_API_KEY?: string;
  AI_API_BASE?: string;
  AI_MODEL?: string;
  // Backward compatibility
  OPENAI_API_KEY?: string;
  AGNES_API_KEY?: string;
  AGNES_API_BASE?: string;
  AGNES_MODEL?: string;
}

interface ChatMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

interface ChatRequestBody {
  messages?: ChatMessage[];
  stream?: boolean;
}

const CORS_HEADERS: Record<string, string> = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

const SYSTEM_PROMPT = `You are the technical AI Assistant for Image Evaluator, a production-grade multidimensional evaluation toolkit for AI image generation covering 9 core metrics:

1. aesthetic: LAION aesthetic predictor using OpenCLIP ViT-L-14 embeddings + linear regression head. Range [1, 10]; higher is better. Measures overall visual perceptual appeal.
2. clip: CLIP Score measuring text-to-image semantic alignment using OpenAI clip-vit-base-patch32 cosine similarity. Range [0, 1]; higher is better.
3. arcface: Face identity consistency using InsightFace buffalo_l (512-dim embedding cosine distance). Range [0, 2]; lower is better (distance < 0.5 indicates same identity).
4. lpips: Learned Perceptual Image Patch Similarity using AlexNet multi-scale features. Range [0, 1+]; lower is better. Robust against slight spatial shifts and global color shifts where MSE fails.
5. ssim: Structural Similarity Index Measure using 11x11 Gaussian window. Range [-1, 1]; higher is better (1.0 = identical).
6. psnr: Peak Signal-to-Noise Ratio (dB) computed from pixel-wise MSE: 10 * log10(MAX^2 / MSE). Higher is better. Highly sensitive to global pixel shifts or subtle tints.
7. fid: Frechet Inception Distance evaluating generative distribution distance via Inception-v3 pool3 features. Lower is better. Biased for small samples, recommended sample size N >= 2048.
8. kid: Kernel Inception Distance using polynomial kernel MMD U-statistic. Lower is better. Unbiased estimator, ideal for small sample evaluation (e.g., subsets of 1000 or fewer).
9. pickscore: Fine-tuned CLIP ViT-H-14 based on large-scale human preference data (Pick-a-Pic). Higher is better. Reflects subjective human preference and prompt compliance.

CLI Commands:
- Single image aesthetic: image-evaluator --metrics aesthetic --image sample.png
- Text-image alignment: image-evaluator --metrics clip pickscore --image sample.png --prompt "prompt text"
- Paired comparison: image-evaluator --metrics lpips ssim psnr --image gen.png --reference ref.png
- Dataset distribution: image-evaluator --metrics fid kid --image gen_dir/ --reference real_dir/

Guidelines:
- Answer questions concisely, accurately, and authoritatively based on Image Evaluator documentation.
- Provide mathematical principles, trade-offs, diagnostic suggestions, and reproduction commands.
- Do not use any emojis.`;

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      ...CORS_HEADERS,
      'Content-Type': 'application/json',
    },
  });
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: CORS_HEADERS,
      });
    }

    const url = new URL(request.url);
    const pathname = url.pathname;

    if (request.method !== 'POST' || (pathname !== '/' && pathname !== '/chat')) {
      return jsonResponse({ error: { message: 'Method not allowed. Use POST / or POST /chat.', type: 'invalid_request' } }, 405);
    }

    const apiKey = env.AI_API_KEY || env.OPENAI_API_KEY || env.AGNES_API_KEY;

    if (!apiKey) {
      return jsonResponse(
        {
          error: {
            message: 'AI_API_KEY is not configured on this Cloudflare Worker.',
            type: 'configuration_error',
          },
        },
        503
      );
    }

    let requestBody: ChatRequestBody;
    try {
      requestBody = await request.json() as ChatRequestBody;
    } catch {
      return jsonResponse({ error: { message: 'Invalid JSON body.', type: 'invalid_request' } }, 400);
    }

    const messages = Array.isArray(requestBody.messages) ? requestBody.messages : [];
    if (messages.length === 0) {
      return jsonResponse({ error: { message: 'messages array is required and cannot be empty.', type: 'invalid_request' } }, 400);
    }

    const shouldStream = Boolean(requestBody.stream);
    const apiBase = (env.AI_API_BASE || env.AGNES_API_BASE || 'https://api.openai.com/v1').replace(/\/+$/, '');
    const model = env.AI_MODEL || env.AGNES_MODEL || 'gpt-4o-mini';

    const upstreamPayload = {
      model,
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        ...messages,
      ],
      stream: shouldStream,
    };

    try {
      const upstreamResponse = await fetch(`${apiBase}/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`,
        },
        body: JSON.stringify(upstreamPayload),
      });

      if (!upstreamResponse.ok) {
        let errorDetails: unknown = null;
        try {
          errorDetails = await upstreamResponse.json();
        } catch {
          errorDetails = await upstreamResponse.text();
        }
        return jsonResponse(
          {
            error: {
              message: 'Upstream AI API returned an error.',
              status: upstreamResponse.status,
              details: errorDetails,
            },
          },
          upstreamResponse.status
        );
      }

      if (shouldStream) {
        return new Response(upstreamResponse.body, {
          status: 200,
          headers: {
            ...CORS_HEADERS,
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
          },
        });
      }

      const responseJson = await upstreamResponse.json();
      return jsonResponse(responseJson, 200);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : String(err);
      return jsonResponse(
        {
          error: {
            message: 'Failed to proxy request to upstream AI API.',
            type: 'proxy_error',
            details: errorMessage,
          },
        },
        502
      );
    }
  },
};

