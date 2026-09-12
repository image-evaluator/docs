'use client';

import React, { useState } from 'react';
import { ImageComparison } from './ImageComparison';
import { Terminal, Copy, Check, Info, Layers } from 'lucide-react';

interface MetricItem {
  name: string;
  value: string;
  tendency: string;
  verdict: string;
  isFavorable: boolean;
  description: string;
}

interface CaseData {
  id: string;
  tabLabel: string;
  title: string;
  subtitle: string;
  badge: string;
  badgeColor: string;
  resolution: string;
  beforeImage: string;
  afterImage: string;
  metrics: MetricItem[];
  analysis: string;
  command: string;
}

const CASES_DATA: CaseData[] = [
  {
    id: 'case_01',
    tabLabel: '用例一：严重感知失真',
    title: '用例一：局部结构位移与严重感知失真',
    subtitle: '画面边缘发生重度几何拓扑形变，多尺度指标全线一致告警',
    badge: '多指标一致判决退化',
    badgeColor: 'border-red-200 bg-red-50 text-red-700 dark:border-red-900/50 dark:bg-red-950/30 dark:text-red-400',
    resolution: '64 × 64 像素',
    beforeImage: '/demo/cases/reference/case_01.png',
    afterImage: '/demo/cases/generated/case_01.png',
    metrics: [
      {
        name: 'LPIPS (AlexNet)',
        value: '0.7219',
        tendency: '越低越优（0.0 完全重合）',
        verdict: '严重失真',
        isFavorable: false,
        description: '深度卷积激活特征空间距离高企，纹理与几何感知发生重度撕裂。',
      },
      {
        name: 'SSIM',
        value: '0.4368',
        tendency: '越高越优（1.0 结构相同）',
        verdict: '结构高度退化',
        isFavorable: false,
        description: '高斯滑动窗口局部协方差统计极低，边缘轮廓与结构相关性断裂。',
      },
      {
        name: 'PSNR',
        value: '18.05 dB',
        tendency: '越高越优（+∞ 像素重合）',
        verdict: '信噪比偏低',
        isFavorable: false,
        description: '逐像素能量均方误差显著，底层色彩与亮度信号衰减严重。',
      },
    ],
    analysis:
      '画面存在局部结构位移与重度几何形变。三大成对指标（深度特征 LPIPS 0.7219、结构统计 SSIM 0.4368、底层信号 PSNR 18.05 dB）形成完全一致的负面判决，证实样本在语义、结构与像素三重尺度均遭受不可逆质量退化。',
    command:
      'image-evaluator --metrics lpips ssim psnr --reference reference/case_01.png --image generated/case_01.png',
  },
  {
    id: 'case_02',
    tabLabel: '用例二：全局色偏扰动',
    title: '用例二：全局暖色温色偏与学术互补实证',
    subtitle: '传统像素/结构指标严重受挫，深度特征准确识别语义拓扑高度完好',
    badge: '多尺度互补典型实证',
    badgeColor:
      'border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-900/50 dark:bg-amber-950/30 dark:text-amber-400',
    resolution: '64 × 64 像素',
    beforeImage: '/demo/cases/reference/case_02.png',
    afterImage: '/demo/cases/generated/case_02.png',
    metrics: [
      {
        name: 'LPIPS (AlexNet)',
        value: '0.1376',
        tendency: '越低越优（0.0 完全重合）',
        verdict: '感知高度保真',
        isFavorable: true,
        description: '深度特征准确提取几何拓扑与语义骨架，滤除全局色偏干扰，呈现极低感知距离。',
      },
      {
        name: 'SSIM',
        value: '0.2959',
        tendency: '越高越优（1.0 结构相同）',
        verdict: '统计指标误判',
        isFavorable: false,
        description: '局部均值与对比度受大面积色温漂移严重污染，局部统计量出现假阳性剧降。',
      },
      {
        name: 'PSNR',
        value: '13.87 dB',
        tendency: '越高越优（+∞ 像素重合）',
        verdict: '像素能量偏移',
        isFavorable: false,
        description: '整幅画面像素强度系统性偏离，均方误差大幅上升，信噪比仅录得 13.87 dB。',
      },
    ],
    analysis:
      '存在全局暖色阶色偏。像素级 PSNR 与局部结构 SSIM 严重受挫，但基于 AlexNet 深层感知特征的 LPIPS 准确识别出几何拓扑与语义完全一致，呈现极低距离 (0.1376)。这是经典计算机视觉学术界揭示的多尺度成对指标互补性铁证。',
    command:
      'image-evaluator --metrics lpips ssim psnr --reference reference/case_02.png --image generated/case_02.png',
  },
  {
    id: 'case_03',
    tabLabel: '用例三：高清人脸局部编辑',
    title: '用例三：真实高清人脸局部微调多模态全景评测',
    subtitle: '真实人脸增配眼镜局部操作，身份特征不漂移，全维度指标综合打分',
    badge: '全量多模态评测范例',
    badgeColor:
      'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-900/50 dark:bg-emerald-950/30 dark:text-emerald-400',
    resolution: '1024 × 1024 像素',
    beforeImage: '/demo/cases/reference/case_03.png',
    afterImage: '/demo/cases/generated/case_03.png',
    metrics: [
      {
        name: 'LPIPS',
        value: '0.0901',
        tendency: '越低越优',
        verdict: '极高保真',
        isFavorable: true,
        description: '全局深度感知特征高度重合，微小差异仅来自于局部新增的眼镜。',
      },
      {
        name: 'SSIM',
        value: '0.9172',
        tendency: '越高越优',
        verdict: '结构极优',
        isFavorable: true,
        description: '除眼镜微小区域外，大面积面部轮廓、发丝与背景结构完全完好。',
      },
      {
        name: 'PSNR',
        value: '22.30 dB',
        tendency: '越高越优',
        verdict: '基底对齐良好',
        isFavorable: true,
        description: '大部分背景与人像未修改区域逐像素严格对齐，重构信噪比处于高位。',
      },
      {
        name: 'ArcFace',
        value: '0.4481',
        tendency: '余弦距离越低越优（< 0.68 确认为同人）',
        verdict: '身份严格一致',
        isFavorable: true,
        description: '人脸生物特征嵌入向量比对，确认为同一人，未发生身份特征漂移。',
      },
      {
        name: 'CLIP Score',
        value: '0.2353',
        tendency: '图文对齐度越大越优',
        verdict: '指令精确遵从',
        isFavorable: true,
        description: '精准响应文本提示词 "give the man glasses"，语义对齐度达标。',
      },
      {
        name: 'Aesthetic',
        value: '6.7540',
        tendency: '美学质量越优（区间 1.0 - 10.0）',
        verdict: '高品质人像',
        isFavorable: true,
        description: '预训练美学评分器打分，面部光影细腻真实，无伪影与噪点。',
      },
    ],
    analysis:
      '真实 MagicBrush 人像加眼镜编辑（1024x1024），除眼部微调外其余区域像素与身份完全保真。ArcFace 确认身份未发生漂移（0.4481），CLIP 验证眼镜添加成功（0.2353），成对保真度三指标（LPIPS 0.0901 / SSIM 0.9172 / PSNR 22.30 dB）全面证实背景与未修改区域完美保留。',
    command:
      'image-evaluator --metrics aesthetic clip arcface lpips ssim psnr --reference reference/case_03.png --image generated/case_03.png --prompt "give the man glasses"',
  },
];

export function MetricVisualShowcase() {
  const [activeTab, setActiveTab] = useState<string>('case_01');
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const activeCase = CASES_DATA.find((c) => c.id === activeTab) || CASES_DATA[0];

  const handleCopy = (command: string, id: string) => {
    if (typeof navigator !== 'undefined' && navigator.clipboard) {
      navigator.clipboard.writeText(command);
      setCopiedId(id);
      setTimeout(() => {
        setCopiedId(null);
      }, 2000);
    }
  };

  return (
    <div className="my-8 rounded-2xl border border-neutral-200 bg-white/70 backdrop-blur-md p-4 sm:p-6 shadow-sm dark:border-neutral-800 dark:bg-neutral-900/60">
      {/* 顶部用例选项卡导航 */}
      <div className="flex flex-wrap items-center gap-2 border-b border-neutral-200 pb-4 dark:border-neutral-800">
        {CASES_DATA.map((item) => {
          const isActive = item.id === activeCase.id;
          return (
            <button
              key={item.id}
              type="button"
              onClick={() => setActiveTab(item.id)}
              className={`px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-medium transition-all cursor-pointer ${
                isActive
                  ? 'bg-neutral-900 text-white shadow-xs dark:bg-neutral-100 dark:text-neutral-900'
                  : 'bg-neutral-100 text-neutral-600 hover:bg-neutral-200/80 hover:text-neutral-900 dark:bg-neutral-800 dark:text-neutral-400 dark:hover:bg-neutral-700 dark:hover:text-neutral-200'
              }`}
            >
              {item.tabLabel}
            </button>
          );
        })}
      </div>

      {/* 用例标题与元数据说明 */}
      <div className="mt-5 flex flex-col gap-2">
        <div className="flex flex-wrap items-center gap-2">
          <h3 className="text-base sm:text-lg font-bold text-neutral-900 dark:text-neutral-100">
            {activeCase.title}
          </h3>
          <span
            className={`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border ${activeCase.badgeColor}`}
          >
            {activeCase.badge}
          </span>
          <span className="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-mono text-neutral-500 bg-neutral-100 dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700">
            {activeCase.resolution}
          </span>
        </div>
        <p className="text-xs sm:text-sm text-neutral-600 dark:text-neutral-400 leading-relaxed">
          {activeCase.subtitle}
        </p>
      </div>

      {/* 交互式对比组件 */}
      <ImageComparison
        beforeImage={activeCase.beforeImage}
        afterImage={activeCase.afterImage}
        beforeLabel="参考原图（Reference）"
        afterLabel="待测生成图（Generated）"
        alt={activeCase.title}
      />

      {/* 指标卡片矩阵 */}
      <div className="mt-6 flex flex-col gap-3">
        <div className="flex items-center gap-2 text-xs font-semibold text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">
          <Layers className="h-3.5 w-3.5" />
          <span>实测指标结果矩阵</span>
        </div>

        <div
          className={`grid gap-3 ${
            activeCase.metrics.length > 3
              ? 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3'
              : 'grid-cols-1 sm:grid-cols-3'
          }`}
        >
          {activeCase.metrics.map((metric) => (
            <div
              key={metric.name}
              className="flex flex-col justify-between p-3.5 rounded-xl border border-neutral-200/80 bg-neutral-50/70 dark:border-neutral-800 dark:bg-neutral-900/40"
            >
              <div>
                <div className="flex items-center justify-between gap-2">
                  <span className="text-xs font-bold text-neutral-700 dark:text-neutral-300 font-mono">
                    {metric.name}
                  </span>
                  <span
                    className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium border ${
                      metric.isFavorable
                        ? 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-900/50 dark:bg-emerald-950/30 dark:text-emerald-400'
                        : 'border-red-200 bg-red-50 text-red-700 dark:border-red-900/50 dark:bg-red-950/30 dark:text-red-400'
                    }`}
                  >
                    {metric.verdict}
                  </span>
                </div>
                <div className="mt-2 text-2xl font-bold font-mono tracking-tight text-neutral-900 dark:text-neutral-100">
                  {metric.value}
                </div>
                <div className="mt-0.5 text-[11px] text-neutral-500 font-sans">
                  {metric.tendency}
                </div>
              </div>

              <div className="mt-3 pt-2.5 border-t border-neutral-200/60 dark:border-neutral-800/60 text-xs text-neutral-600 dark:text-neutral-400 leading-normal">
                {metric.description}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 专家诊断分析面板 */}
      <div className="mt-5 rounded-xl border border-blue-200/60 bg-blue-50/50 p-4 dark:border-blue-900/40 dark:bg-blue-950/20">
        <div className="flex items-start gap-2.5">
          <Info className="h-4 w-4 text-blue-600 dark:text-blue-400 shrink-0 mt-0.5" />
          <div className="flex flex-col gap-1">
            <span className="text-xs font-semibold text-blue-900 dark:text-blue-300">
              实测分析与指标机理解析
            </span>
            <p className="text-xs sm:text-sm text-neutral-700 dark:text-neutral-300 leading-relaxed">
              {activeCase.analysis}
            </p>
          </div>
        </div>
      </div>

      {/* 本地 CLI 复现代码栏 */}
      <div className="mt-4 rounded-xl border border-neutral-200 bg-neutral-950 p-3.5 text-neutral-200 dark:border-neutral-800">
        <div className="flex items-center justify-between pb-2 mb-2 border-b border-neutral-800 text-xs text-neutral-400">
          <div className="flex items-center gap-1.5 font-mono">
            <Terminal className="h-3.5 w-3.5 text-neutral-400" />
            <span>命令行复现评测</span>
          </div>
          <button
            type="button"
            onClick={() => handleCopy(activeCase.command, activeCase.id)}
            className="flex items-center gap-1 px-2 py-0.5 rounded-md hover:bg-neutral-800 text-neutral-300 hover:text-white transition-colors cursor-pointer"
          >
            {copiedId === activeCase.id ? (
              <>
                <Check className="h-3 w-3 text-emerald-400" />
                <span className="text-emerald-400">已复制</span>
              </>
            ) : (
              <>
                <Copy className="h-3 w-3" />
                <span>复制命令</span>
              </>
            )}
          </button>
        </div>
        <div className="font-mono text-xs sm:text-sm text-neutral-300 overflow-x-auto whitespace-pre py-1">
          <span className="text-emerald-400 select-none">$ </span>
          {activeCase.command}
        </div>
      </div>
    </div>
  );
}

