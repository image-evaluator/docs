export interface Env {
  AI?: {
    run: (model: string, options: Record<string, unknown>) => Promise<unknown>;
  };
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

const SYSTEM_PROMPT = `You are the technical AI Assistant for Image Evaluator, a production-grade multidimensional evaluation toolkit for AI image generation covering 9 core metrics.

Core Metrics & Mathematical Formulations:
1. aesthetic: LAION aesthetic predictor using OpenCLIP ViT-L-14 embeddings + MLP linear regression head. Range [1, 10]; higher is better. Measures overall visual aesthetic appeal.
2. clip: CLIP Score measuring text-to-image semantic cosine alignment:
$$\\text{CLIP}(I, T) = \\max(100 \\cdot \\cos(\\mathbf{e}_I, \\mathbf{e}_T), 0)$$
Range [0, 100]; higher is better.
3. arcface: Face identity cosine distance via InsightFace buffalo_l (512-dim embedding):
$$\\text{Distance}(f_1, f_2) = 1 - \\frac{f_1 \\cdot f_2}{\\|f_1\\|_2 \\|f_2\\|_2}$$
Range [0, 2]; lower is better (< 0.40 indicates high identity consistency).
4. lpips: Learned Perceptual Image Patch Similarity using AlexNet multi-scale features:
$$d(x, x_0) = \\sum_{l} \\frac{1}{H_l W_l} \\sum_{h, w} \\left\\| w_l \\odot (\\hat{y}^l_{hw} - \\hat{y}^{0l}_{hw}) \\right\\|_2^2$$
Range [0, 1+]; lower is better. Robust against slight spatial shifts and global color shifts where MSE fails.
5. ssim: Structural Similarity Index Measure evaluated across luminance, contrast, and structure:
$$\\text{SSIM}(x, y) = \\frac{(2\\mu_x \\mu_y + C_1)(2\\sigma_{xy} + C_2)}{(\\mu_x^2 + \\mu_y^2 + C_1)(\\sigma_x^2 + \\sigma_y^2 + C_2)}$$
Range [-1, 1]; higher is better (1.0 = identical). Constants $C_1 = (K_1 L)^2, C_2 = (K_2 L)^2$.
6. psnr: Peak Signal-to-Noise Ratio (dB) computed from pixel-wise MSE:
$$\\text{PSNR} = 10 \\cdot \\log_{10}\\left(\\frac{\\text{MAX}_I^2}{\\text{MSE}}\\right)$$
where $\\text{MSE} = \\frac{1}{mn}\\sum_{i=0}^{m-1}\\sum_{j=0}^{n-1}[I(i,j) - K(i,j)]^2$. Higher is better. Highly sensitive to global pixel shifts or subtle tints.
7. fid: Fréchet Inception Distance evaluating generative distribution distance in Inception-v3 pool3 feature space:
$$\\text{FID} = \\|\\mu_r - \\mu_g\\|_2^2 + \\text{Tr}(\\Sigma_r + \\Sigma_g - 2(\\Sigma_r \\Sigma_g)^{1/2})$$
Lower is better. Biased for small sample sizes, recommended $N \\ge 2048$.
8. kid: Kernel Inception Distance using polynomial kernel MMD squared U-statistic:
$$k(x, y) = \\left(\\frac{1}{d} x^T y + 1\\right)^3$$
Lower is better. Unbiased estimator, ideal for small sample evaluation (e.g. subsets of 1000 or fewer).
9. pickscore: Fine-tuned CLIP ViT-H-14 based on large-scale human preference data (Pick-a-Pic). Higher is better. Reflects subjective human preference and prompt compliance.

CLI Commands:
- Single image aesthetic: image-evaluator --metrics aesthetic --image sample.png
- Text-image alignment: image-evaluator --metrics clip pickscore --image sample.png --prompt "prompt text"
- Paired comparison: image-evaluator --metrics lpips ssim psnr --image gen.png --reference ref.png
- Dataset distribution: image-evaluator --metrics fid kid --image gen_dir/ --reference real_dir/

CRITICAL MATHEMATICAL FORMATTING RULES (STRICTLY ENFORCED):
- ALWAYS format all mathematical equations, formulas, and expressions using standard LaTeX syntax.
- Standalone / display equations MUST be wrapped in double dollar signs $$...$$ on their own lines.
- Inline mathematical variables, parameters, constants, and short math expressions MUST be wrapped in single dollar signs $...$ (e.g. $x$, $y$, $\\mu_x$, $\\sigma_{xy}$, $C_1$, $C_2$, $\\text{MSE}$, $\\log_{10}$, $N \\ge 2048$).
- NEVER output raw ASCII pseudo-formulas (e.g. NEVER write "mu_a * mu_b", "SSIM = (2 * ...)", or "10 * log10(...)").
- NEVER use unescaped underscores in math symbols outside of LaTeX delimiters.

Response Guidelines:
- Answer questions concisely, accurately, and authoritatively based on Image Evaluator documentation.
- Provide mathematical principles, trade-offs, diagnostic suggestions, and reproduction commands.
- Respond in the same language as the user's inquiry (Simplified Chinese for Chinese queries, English for English queries).
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
    const apiKey = env.AI_API_KEY || env.OPENAI_API_KEY || env.AGNES_API_KEY;

    // Mode 1: External API proxy (OpenAI, DeepSeek, Minimax, etc.)
    if (apiKey) {
      const apiBase = (env.AI_API_BASE || env.AGNES_API_BASE || 'https://api.openai.com/v1').replace(/\/+$/, '');
      const model = env.AI_MODEL || env.AGNES_MODEL || 'gpt-4o-mini';

      const upstreamPayload = {
        model,
        messages: [
          { role: 'system', content: SYSTEM_PROMPT },
          ...messages,
        ],
        stream: shouldStream,
        max_tokens: 2048,
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
    }

    // Mode 2: Native Cloudflare Workers AI (Zero-key fallback)
    if (env.AI) {
      try {
        const cfModel = env.AI_MODEL && env.AI_MODEL.startsWith('@cf/')
          ? env.AI_MODEL
          : '@cf/meta/llama-3.2-3b-instruct';

        const stream = await env.AI.run(cfModel, {
          messages: [
            { role: 'system', content: SYSTEM_PROMPT },
            ...messages,
          ],
          stream: shouldStream,
          max_tokens: 2048,
        });

        if (shouldStream) {
          return new Response(stream as BodyInit, {
            status: 200,
            headers: {
              ...CORS_HEADERS,
              'Content-Type': 'text/event-stream',
              'Cache-Control': 'no-cache',
            },
          });
        }

        return jsonResponse(stream, 200);
      } catch (err: unknown) {
        const errorMessage = err instanceof Error ? err.message : String(err);
        return jsonResponse(
          {
            error: {
              message: 'Cloudflare Workers AI execution failed.',
              type: 'ai_error',
              details: errorMessage,
            },
          },
          500
        );
      }
    }

    // Neither configured
    return jsonResponse(
      {
        error: {
          message: 'Neither AI_API_KEY nor Workers AI binding is configured.',
          type: 'configuration_error',
        },
      },
      503
    );
  },
};

