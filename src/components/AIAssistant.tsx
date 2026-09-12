'use client';

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { X, Send, Bot, Sparkles } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

const PRESET_QUESTIONS = [
  '人脸一致性评测该选什么指标？',
  '为什么全局色偏下 PSNR 暴跌但 LPIPS 良好？',
  '小样本生成分布评估用 FID 还是 KID？',
];

const INITIAL_MESSAGES: Message[] = [
  {
    id: 'welcome',
    role: 'assistant',
    content: '您好！我是 Image Evaluator AI 评测助手，已注入 Level 0 领域知识库（涵盖 Aesthetic, CLIP, ArcFace, LPIPS, SSIM, PSNR, FID, KID, PickScore 9 大核心指标与复现指令）。\n\n您可以直接输入评测疑问，或点击上方预设问题快速提问。',
  },
];

function getFallbackAnswer(query: string): string {
  const q = query.toLowerCase();

  // Preset 1: Face consistency / ArcFace
  if (q.includes('人脸') || q.includes('一致性') || q.includes('arcface') || q.includes('face') || q.includes('身份')) {
    return `[人脸一致性评测选型建议]

1. 核心推荐指标: arcface
- 原理机制: 基于 InsightFace buffalo_l 模型提取人脸 512 维归一化深度特征，计算待测图与参考图人脸向量的余弦距离。
- 取值范围与判定: 取值范围为 [0, 2]，数值越小代表身份越一致。通常以 0.40 - 0.50 作为判决阈值；余弦距离小于 0.40 表明高度一致。

2. 互补感知评估: lpips (局部人脸裁剪)
- 若除身份高层特征外，还需评估面部微观纹理、局部几何拉伸与表情保真度，建议裁剪人脸区域并使用 lpips 辅助评估。

3. CLI 快速复现命令:
\`\`\`bash
image-evaluator --metrics arcface --image generated_face.png --reference real_face.png

\`\`\``;
  }

  // Preset 2: Global color shift / PSNR vs LPIPS
  if (q.includes('色偏') || q.includes('psnr') || q.includes('lpips') || q.includes('暴跌') || q.includes('像素')) {
    return `[全局色偏下 PSNR 暴跌与 LPIPS 良好的数学机理]

1. PSNR (峰值信噪比) 机制与缺陷:
- 计算公式: PSNR = 10 * log10(MAX^2 / MSE)，完全基于逐像素均方误差 (MSE)。
- 暴跌原因: 当图像出现全局轻微色彩偏移（如色调微调）或微小位移时，全图所有像素均产生固定残差，MSE 迅速在整幅图像累积放大，导致对数空间内的 PSNR 出现断崖式暴跌。

2. LPIPS (深度感知特征相似度) 鲁棒性:
- 计算机制: LPIPS 在深度卷积神经网络 (AlexNet) 的多层归一化激活特征空间中计算感知距离。
- 良好原因: 深度卷积特征关注的是结构轮廓、纹理分布和语义拓扑，对全局常量亮度与色彩平移具有天然的不变性与鲁棒性，真实反映人眼的主观良好感知。

3. 选型建议:
- 评估生成图像的感知质量时应以 LPIPS 为主指标；PSNR 仅用于评估严格无损压缩或像素级重构基准。`;
  }

  // Preset 3: Small sample distribution / FID vs KID
  if (q.includes('小样本') || q.includes('kid') || q.includes('fid') || q.includes('分布') || q.includes('样本量')) {
    return `[小样本生成分布评估指标选型: FID vs KID]

1. 推荐结论: 强烈推荐使用 kid (Kernel Inception Distance)。

2. 核心数学机理与差异:
- FID 缺陷: FID 依赖经验协方差矩阵和均值向量的高斯拟合。在样本量不足（如 N < 2048 甚至几百张）时，存在显著的正向经验估计偏差 (Empirical Bias)，导致计算出的 FID 显著虚高且方差极大。
- KID 优势: KID 采用多项式核的最大均值差异 (MMD) 无偏 U 统计量 (Unbiased U-Statistic)。无论样本规模大小，其期望值均严格无偏，并采用千张子集多次重采样计算均值和标准差，评测结果高度可信。

3. CLI 快速复现命令:
\`\`\`bash
image-evaluator --metrics kid --image generated_folder/ --reference real_folder/

\`\`\``;
  }

  // Aesthetic
  if (q.includes('aesthetic') || q.includes('美学') || q.includes('单图')) {
    return `[单图美学质量评估 (Aesthetic)]

- 核心机制: 基于 OpenCLIP ViT-L-14 归一化多模态特征，接轻量级线性回归头预测人类美学评分。
- 取值范围: 约 1 到 10 分，数值越高代表视觉美学质量越优。
- 适用场景: 无参考图生成图像筛选、生成多样性过滤与高质量图库排序。
- CLI 复现命令:
\`\`\`bash
image-evaluator --metrics aesthetic --image sample.png

\`\`\``;
  }

  // CLIP / Text-image alignment
  if (q.includes('clip') || q.includes('文本') || q.includes('语义') || q.includes('prompt') || q.includes('对齐')) {
    return `[图文语义匹配度评估 (CLIP Score)]

- 核心机制: 基于 OpenAI clip-vit-base-patch32 模型，分别提取提示词与生成图像的归一化特征，计算余弦相似度。
- 取值范围: [0, 1]，数值越高代表图像与文本提示词的语义吻合度越高。
- CLI 复现命令:
\`\`\`bash
image-evaluator --metrics clip --image sample.png --prompt "an astronaut on mars"

\`\`\``;
  }

  // PickScore
  if (q.includes('pickscore') || q.includes('人类偏好') || q.includes('偏好')) {
    return `[人类主观偏好评估 (PickScore)]

- 核心机制: 基于真实人类选择数据集 (Pick-a-Pic) 大规模微调的 CLIP ViT-H-14 视觉模型。
- 核心优势: 相比标准 CLIP 仅判断语义覆盖，PickScore 深入捕获人类审美直觉、负面伪影敏感度与构图完整性。
- CLI 复现命令:
\`\`\`bash
image-evaluator --metrics pickscore --image sample.png --prompt "prompt text"

\`\`\``;
  }

  // SSIM
  if (q.includes('ssim') || q.includes('结构')) {
    return `[结构相似度评估 (SSIM)]

- 核心机制: 采用 11x11 高斯加权滑动窗口，综合评估局部亮度、对比度与结构三要素。
- 取值范围: [-1, 1]，1.0 代表完全一致。
- CLI 复现命令:
\`\`\`bash
image-evaluator --metrics ssim --image generated.png --reference reference.png

\`\`\``;
  }

  // Default summary response
  return `[Image Evaluator 9 大核心指标与技术矩阵速查]

1. 感知视觉质量: aesthetic (OpenCLIP ViT-L-14 特征回归，数值越高越优)
2. 图文语义对齐: clip (文本与图像余弦相似度), pickscore (人类主观偏好微调模型)
3. 主体身份一致: arcface (InsightFace buffalo_l 512 维余弦距离，< 0.50 同人)
4. 成对保真度: lpips (深度感知距离，越低越好), ssim (结构相似度), psnr (像素信噪比)
5. 数据集分布: fid (大样本高斯距离，N >= 2048), kid (小样本无偏核多项式距离)

多指标 CLI 联合复现命令:
\`\`\`bash
# 成对全维度对比
image-evaluator --metrics lpips ssim psnr --image gen.png --reference ref.png

# 数据集分布全量评测
image-evaluator --metrics fid kid --image gen_folder/ --reference real_folder/

\`\`\``;
}

export function AIAssistant() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>(INITIAL_MESSAGES);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const activeStreamRef = useRef<boolean>(false);
  const abortControllerRef = useRef<AbortController | null>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [isOpen, messages, scrollToBottom]);

  // Unmount cleanup: cancel any active stream or network request
  useEffect(() => {
    return () => {
      activeStreamRef.current = false;
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  // Handle local simulated typewriter streaming for fallback answers
  const simulateStreaming = useCallback(
    (fullText: string, targetMessageId: string) => {
      activeStreamRef.current = true;
      let currentIndex = 0;
      const chunkSize = 8;
      const intervalMs = 25;

      const timer = setInterval(() => {
        if (!activeStreamRef.current) {
          clearInterval(timer);
          setIsLoading(false);
          return;
        }

        currentIndex += chunkSize;
        if (currentIndex >= fullText.length) {
          clearInterval(timer);
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === targetMessageId ? { ...msg, content: fullText } : msg
            )
          );
          setIsLoading(false);
          activeStreamRef.current = false;
        } else {
          const partial = fullText.slice(0, currentIndex);
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === targetMessageId ? { ...msg, content: partial } : msg
            )
          );
        }
      }, intervalMs);
    },
    []
  );

  const handleSend = useCallback(
    async (textToSend: string) => {
      const trimmed = textToSend.trim();
      if (!trimmed || isLoading) return;

      // Abort any preceding in-flight fetch
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      const abortController = new AbortController();
      abortControllerRef.current = abortController;

      const userMsgId = `user-${Date.now()}`;
      const botMsgId = `bot-${Date.now()}`;

      const newMessages: Message[] = [
        ...messages,
        { id: userMsgId, role: 'user', content: trimmed },
        { id: botMsgId, role: 'assistant', content: '' },
      ];

      setMessages(newMessages);
      setInputValue('');
      setIsLoading(true);

      const workerUrl = process.env.NEXT_PUBLIC_AI_WORKER_URL;

      // If worker URL is configured, attempt real proxy streaming
      if (workerUrl && workerUrl.trim() !== '') {
        try {
          const endpoint = workerUrl.replace(/\/+$/, '') + '/chat';
          const payloadMessages = newMessages
            .filter((m) => m.id !== botMsgId)
            .map((m) => ({ role: m.role, content: m.content }));

          const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages: payloadMessages, stream: true }),
            signal: abortController.signal,
          });

          if (!response.ok || !response.body) {
            throw new Error(`Worker HTTP status ${response.status}`);
          }

          const reader = response.body.getReader();
          const decoder = new TextDecoder('utf-8');
          let accumulated = '';
          let doneReading = false;
          let buffer = '';

          activeStreamRef.current = true;

          while (!doneReading && activeStreamRef.current) {
            const { value, done } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop() || '';

            for (const line of lines) {
              const trimmedLine = line.trim();
              if (!trimmedLine || trimmedLine.startsWith(':')) continue;
              if (trimmedLine === 'data: [DONE]') {
                doneReading = true;
                break;
              }
              if (trimmedLine.startsWith('data: ')) {
                const jsonStr = trimmedLine.slice(6);
                try {
                  const parsed = JSON.parse(jsonStr);
                  const contentDelta =
                    parsed.choices?.[0]?.delta?.content ||
                    parsed.choices?.[0]?.message?.content ||
                    '';
                  if (contentDelta) {
                    accumulated += contentDelta;
                    setMessages((prev) =>
                      prev.map((msg) =>
                        msg.id === botMsgId
                          ? { ...msg, content: accumulated }
                          : msg
                      )
                    );
                  }
                } catch {
                  // Silently ignore non-JSON SSE frames
                }
              }
            }
          }

          setIsLoading(false);
          activeStreamRef.current = false;
          return;
        } catch {
          // If the request was intentionally aborted, exit cleanly
          if (abortController.signal.aborted) {
            setIsLoading(false);
            return;
          }
          // Otherwise gracefully fall through to local fallback knowledge engine
        }
      }

      // Offline / Local Level 0 fallback engine
      const fallbackContent = getFallbackAnswer(trimmed);
      simulateStreaming(fallbackContent, botMsgId);
    },
    [messages, isLoading, simulateStreaming]
  );

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      void handleSend(inputValue);
    }
  };

  return (
    <>
      {/* Floating trigger button */}
      {!isOpen && (
        <button
          type="button"
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-50 flex items-center gap-2.5 rounded-full bg-blue-600 px-4 py-2.5 text-sm font-medium text-white shadow-xl transition-all duration-200 hover:bg-blue-700 hover:shadow-2xl focus:outline-none focus:ring-2 focus:ring-blue-400"
          aria-label="打开 AI 评测问答浮窗"
        >
          <Bot className="h-4 w-4" />
          <span>AI 评测问答</span>
        </button>
      )}

      {/* Floating chat panel */}
      {isOpen && (
        <div
          role="dialog"
          aria-labelledby="ai-assistant-title"
          className="fixed bottom-6 right-4 sm:right-6 z-50 flex h-[560px] max-h-[calc(100vh-5rem)] w-[calc(100vw-2rem)] sm:w-96 flex-col overflow-hidden rounded-2xl border border-fd-border bg-fd-card text-fd-foreground shadow-2xl transition-all duration-200"
        >
          {/* Header */}
          <div className="flex items-center justify-between border-b border-fd-border bg-fd-muted/60 px-4 py-3">
            <div className="flex items-center gap-2.5">
              <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-blue-600 text-white shadow-sm">
                <Bot className="h-4 w-4" />
              </div>
              <div>
                <h3
                  id="ai-assistant-title"
                  className="text-sm font-semibold leading-none text-fd-foreground"
                >
                  AI 评测助手
                </h3>
                <p className="mt-1 text-[11px] leading-none text-fd-muted-foreground">
                  Agnes 2.5 Flash / Level 0 文档增强
                </p>
              </div>
            </div>
            <button
              type="button"
              onClick={() => {
                activeStreamRef.current = false;
                if (abortControllerRef.current) {
                  abortControllerRef.current.abort();
                }
                setIsOpen(false);
              }}
              className="rounded-lg p-1.5 text-fd-muted-foreground hover:bg-fd-accent hover:text-fd-foreground transition-colors"
              aria-label="关闭问答浮窗"
            >
              <X className="h-4 w-4" />
            </button>
          </div>

          {/* Preset question chips */}
          <div className="border-b border-fd-border/70 bg-fd-muted/30 p-2.5">
            <div className="flex items-center gap-1.5 text-[11px] font-medium text-fd-muted-foreground mb-1.5">
              <Sparkles className="h-3 w-3 text-blue-500" />
              <span>快速提问预设</span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {PRESET_QUESTIONS.map((question) => (
                <button
                  key={question}
                  type="button"
                  disabled={isLoading}
                  onClick={() => void handleSend(question)}
                  className="rounded-md border border-fd-border bg-fd-card px-2 py-1 text-left text-xs text-fd-muted-foreground hover:border-blue-400 hover:text-blue-600 hover:bg-blue-50/50 dark:hover:bg-blue-950/30 transition-colors disabled:opacity-50"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>

          {/* Messages container */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((msg) => {
              const isUser = msg.role === 'user';
              return (
                <div
                  key={msg.id}
                  className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[88%] rounded-2xl px-3.5 py-2.5 text-xs leading-relaxed ${
                      isUser
                        ? 'rounded-tr-sm bg-blue-600 text-white shadow-sm'
                        : 'rounded-tl-sm border border-fd-border bg-fd-muted/70 text-fd-foreground'
                    }`}
                  >
                    {!isUser && isLoading && msg.content === '' ? (
                      <div className="flex items-center gap-1.5 py-1 text-fd-muted-foreground">
                        <span className="inline-block h-1.5 w-1.5 animate-bounce rounded-full bg-blue-600" />
                        <span className="inline-block h-1.5 w-1.5 animate-bounce rounded-full bg-blue-600 [animation-delay:0.2s]" />
                        <span className="inline-block h-1.5 w-1.5 animate-bounce rounded-full bg-blue-600 [animation-delay:0.4s]" />
                        <span className="text-[11px] ml-1">思考检索中...</span>
                      </div>
                    ) : (
                      <div className="whitespace-pre-wrap font-sans">
                        {msg.content}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
            <div ref={messagesEndRef} />
          </div>

          {/* Input bar */}
          <div className="border-t border-fd-border bg-fd-card p-3">
            <div className="flex items-center gap-2">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="请输入评测疑问或指标选型..."
                disabled={isLoading}
                className="flex-1 rounded-xl border border-fd-border bg-fd-muted/50 px-3.5 py-2 text-xs text-fd-foreground placeholder:text-fd-muted-foreground focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:opacity-50"
              />
              <button
                type="button"
                disabled={isLoading || !inputValue.trim()}
                onClick={() => void handleSend(inputValue)}
                className="flex h-8 w-8 items-center justify-center rounded-xl bg-blue-600 text-white transition-all duration-150 hover:bg-blue-700 disabled:opacity-40 disabled:hover:bg-blue-600 focus:outline-none"
                aria-label="发送消息"
              >
                <Send className="h-3.5 w-3.5" />
              </button>
            </div>
            <div className="mt-1.5 flex items-center justify-between text-[10px] text-fd-muted-foreground px-0.5">
              <span>按 Enter 发送 / 支持 9 大指标诊断</span>
              <span>Level 0 离线高可用</span>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

