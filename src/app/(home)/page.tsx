import Link from 'next/link';
import { ArrowRight, BookOpen, Terminal, Layers, Sparkles } from 'lucide-react';

const METRIC_CARDS = [
  {
    title: '单图感知美学',
    metrics: 'Aesthetic Predictor V2',
    description: '无需参考图，基于 CLIP 特征与多层感知机预测人类视觉审美与质量打分。',
    href: '/docs/aesthetic',
  },
  {
    title: '图文语义匹配',
    metrics: 'CLIP Score (ViT-B/32)',
    description: '多模态嵌入余弦相似度，客观评测生成图像与文本提示词的语义对齐程度。',
    href: '/docs/clip',
  },
  {
    title: '主体身份保真',
    metrics: 'ArcFace Cosine Similarity',
    description: 'InsightFace 512 维特征余弦距离，精准衡量人脸与主体身份一致性。',
    href: '/docs/arcface',
  },
  {
    title: '深度感知失真',
    metrics: 'LPIPS (AlexNet)',
    description: '多尺度深层感知卷积特征加权距离，贴合人类真实视觉感知判断。',
    href: '/docs/lpips',
  },
  {
    title: '结构相似性',
    metrics: 'SSIM (11x11 Gaussian)',
    description: '基于局部滑动窗口高斯协方差统计的亮度、对比度与结构三分量相似度。',
    href: '/docs/ssim',
  },
  {
    title: '逐像素信噪比',
    metrics: 'PSNR (Peak SNR)',
    description: '基于均方误差对数尺度的底层物理级信号能量重构保真度度量。',
    href: '/docs/psnr',
  },
  {
    title: '生成分布距离',
    metrics: 'FID (Clean-FID Inception-v3)',
    description: '高斯协方差二次型距离，标准抗混叠重采样度量群体生成分布。',
    href: '/docs/fid',
  },
  {
    title: '核最大均值差异',
    metrics: 'KID (Polynomial MMD)',
    description: '三次多项式核最大均值差异无偏估计量，专精小样本分布评估。',
    href: '/docs/kid',
  },
  {
    title: '人类偏好对齐',
    metrics: 'PickScore (Pick-a-Pic)',
    description: '基于真实人类成对偏好反馈微调，评估最符合人类直觉审美的生成结果。',
    href: '/docs/pickscore',
  },
];

export default function HomePage() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden px-6 pt-16 pb-20 md:pt-24 md:pb-28 text-center">
        <div className="mx-auto max-w-4xl">
          <div className="inline-flex items-center gap-2 rounded-full border border-fd-border bg-fd-secondary/60 px-3.5 py-1 text-xs font-medium text-fd-secondary-foreground mb-6 backdrop-blur">
            <Sparkles className="w-3.5 h-3.5 text-fd-primary" />
            <span>开源图像生成多维评测套件 · 覆盖 9 大核心指标</span>
          </div>

          <h1 className="text-4xl font-extrabold tracking-tight sm:text-6xl text-fd-foreground">
            统一图像质量与多维对齐评估
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-fd-muted-foreground max-w-2xl mx-auto leading-relaxed">
            生产级、零黑盒的图像生成评测套件。覆盖美学感知、图文对齐、主体保真、成对失真、分布差异与人类偏好全维度。
          </p>

          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Link
              href="/docs"
              className="inline-flex items-center gap-2 rounded-lg bg-fd-primary px-6 py-3 font-semibold text-fd-primary-foreground shadow transition hover:opacity-90"
            >
              <BookOpen className="w-4 h-4" />
              <span>浏览文档中心</span>
              <ArrowRight className="w-4 h-4" />
            </Link>

            <Link
              href="/docs/visual-demo"
              className="inline-flex items-center gap-2 rounded-lg border border-fd-border bg-fd-card px-6 py-3 font-semibold text-fd-card-foreground shadow-sm transition hover:bg-fd-accent hover:text-fd-accent-foreground"
            >
              <Layers className="w-4 h-4 text-fd-primary" />
              <span>交互式演练 Demo</span>
            </Link>
          </div>
        </div>

        {/* Quickstart Terminal Card */}
        <div className="mx-auto max-w-2xl mt-12 text-left">
          <div className="rounded-xl border border-fd-border bg-fd-card shadow-lg overflow-hidden">
            <div className="flex items-center justify-between px-4 py-2.5 bg-fd-secondary/40 border-b border-fd-border text-xs text-fd-muted-foreground font-mono">
              <div className="flex items-center gap-2">
                <Terminal className="w-3.5 h-3.5" />
                <span>快速开始</span>
              </div>
              <span>bash</span>
            </div>
            <div className="p-4 font-mono text-sm space-y-2 bg-fd-secondary/10">
              <div className="text-fd-muted-foreground"># 安装官方发布包</div>
              <div className="text-fd-foreground font-semibold select-all">$ pip install image-evaluator</div>
              <div className="text-fd-muted-foreground pt-2"># 单行 CLI 执行多维评测</div>
              <div className="text-fd-foreground font-semibold select-all">
                $ image-evaluator --metrics aesthetic clip --image sample.png --prompt "a scenic landscape"
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Metrics Cards Grid */}
      <section className="px-6 py-16 bg-fd-secondary/20 border-t border-fd-border">
        <div className="mx-auto max-w-5xl">
          <div className="text-center mb-12">
            <h2 className="text-2xl font-bold tracking-tight sm:text-3xl text-fd-foreground">
              全维度 9 大权威评测指标体系
            </h2>
            <p className="mt-3 text-sm sm:text-base text-fd-muted-foreground">
              每个指标均提供数学理论推导、官方基准对齐测试与边界约束指南。
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {METRIC_CARDS.map((card) => (
              <Link
                key={card.href}
                href={card.href}
                className="group relative flex flex-col justify-between rounded-xl border border-fd-border bg-fd-card p-6 shadow-sm transition hover:shadow-md hover:border-fd-primary/50"
              >
                <div>
                  <div className="text-xs font-mono font-semibold text-fd-primary mb-1">
                    {card.metrics}
                  </div>
                  <h3 className="text-lg font-bold text-fd-card-foreground group-hover:text-fd-primary transition-colors">
                    {card.title}
                  </h3>
                  <p className="mt-2.5 text-sm text-fd-muted-foreground leading-relaxed">
                    {card.description}
                  </p>
                </div>
                <div className="mt-4 pt-3 border-t border-fd-border/50 flex items-center text-xs font-medium text-fd-primary">
                  <span>阅读详细文档</span>
                  <ArrowRight className="w-3.5 h-3.5 ml-1 transition-transform group-hover:translate-x-1" />
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto border-t border-fd-border px-6 py-8 text-center text-xs text-fd-muted-foreground">
        <p>Apache-2.0 License · Maintained by image-evaluator community</p>
      </footer>
    </div>
  );
}
