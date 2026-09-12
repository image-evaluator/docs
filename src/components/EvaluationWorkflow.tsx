'use client';

import React from 'react';
import Link from 'next/link';

interface WorkflowProps {
  lang?: 'en' | 'zh';
}

export function EvaluationWorkflow({ lang = 'en' }: WorkflowProps) {
  const isZh = lang === 'zh';
  const prefix = isZh ? '/zh' : '';

  const workflows = [
    {
      title: isZh ? '单图无参考质量' : 'No-Reference Quality',
      badge: '--image',
      metrics: [
        { name: 'aesthetic', label: isZh ? 'LAION 美学评分' : 'LAION Aesthetic', href: `${prefix}/no-reference/aesthetic`, dir: '↑' },
      ],
    },
    {
      title: isZh ? '跨模态图文对齐' : 'Text-to-Image Alignment',
      badge: '--image + --prompt',
      metrics: [
        { name: 'clip', label: isZh ? 'CLIP 语义余弦相似度' : 'CLIP Cosine Sim', href: `${prefix}/text-image/clip`, dir: '↑' },
        { name: 'pickscore', label: isZh ? 'PickScore 人类偏好' : 'PickScore Preference', href: `${prefix}/text-image/pickscore`, dir: '↑' },
      ],
    },
    {
      title: isZh ? '成对保真与主体一致' : 'Pairwise Fidelity & Identity',
      badge: '--image + --reference',
      metrics: [
        { name: 'lpips', label: isZh ? 'LPIPS 深度感知距离' : 'LPIPS Perceptual', href: `${prefix}/pairwise/lpips`, dir: '↓' },
        { name: 'ssim', label: isZh ? 'SSIM 结构相似度' : 'SSIM Structure', href: `${prefix}/pairwise/ssim`, dir: '↑' },
        { name: 'psnr', label: isZh ? 'PSNR 峰值信噪比' : 'PSNR Ratio', href: `${prefix}/pairwise/psnr`, dir: '↑' },
        { name: 'arcface', label: isZh ? 'ArcFace 人脸身份距离' : 'ArcFace Identity', href: `${prefix}/pairwise/arcface`, dir: '↓' },
      ],
    },
    {
      title: isZh ? '群体生成分布差异' : 'Dataset Distribution',
      badge: '--image <dir> + --reference <dir>',
      metrics: [
        { name: 'fid', label: isZh ? 'FID 弗雷歇距离' : 'FID Distance', href: `${prefix}/distribution/fid`, dir: '↓' },
        { name: 'kid', label: isZh ? 'KID 多项式核 MMD' : 'KID U-Statistic', href: `${prefix}/distribution/kid`, dir: '↓' },
      ],
    },
  ];

  return (
    <div className="my-8 rounded-2xl border border-fd-border bg-fd-card/40 p-5 shadow-xs">
      <div className="text-sm font-semibold text-fd-foreground mb-1">
        {isZh ? '评测决策流与输入契约' : 'Evaluation Decision Flow & Input Contracts'}
      </div>
      <p className="text-xs text-fd-muted-foreground mb-4">
        {isZh
          ? '根据评测目标与输入数据结构，选择对应的指标集合与命令行参数：'
          : 'Select the optimal metric suite based on input parameters and task objectives:'}
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {workflows.map((wf, idx) => (
          <div
            key={idx}
            className="flex flex-col rounded-xl border border-fd-border/70 bg-fd-background/70 p-3.5 transition-colors hover:border-fd-primary/40"
          >
            <div className="flex items-center justify-between pb-2 border-b border-fd-border/50">
              <span className="text-xs font-bold text-fd-foreground">{wf.title}</span>
              <code className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-fd-secondary text-fd-secondary-foreground border border-fd-border/50">
                {wf.badge}
              </code>
            </div>

            <div className="flex flex-wrap gap-2 pt-3 mt-auto">
              {wf.metrics.map((m, mIdx) => (
                <Link
                  key={mIdx}
                  href={m.href}
                  className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium bg-fd-accent/40 text-fd-accent-foreground hover:bg-fd-accent hover:text-fd-primary transition-all border border-fd-border/40"
                >
                  <span className="font-mono font-bold text-fd-primary">{m.name}</span>
                  <span className="text-[11px] text-fd-muted-foreground">({m.label})</span>
                  <span className="text-[10px] opacity-70">{m.dir}</span>
                </Link>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

