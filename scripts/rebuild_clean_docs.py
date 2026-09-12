import os

docs_dir = "content/docs"

def save(rel_path, content):
    full_path = os.path.join(docs_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n\n")
    print(f"Wrote: {full_path}")

# ==============================================================================
# 1. INDEX
# ==============================================================================
save("index.mdx", """---
title: Quickstart
description: Lightweight unified evaluation toolkit for generative image quality and alignment
---

# Quickstart

`image-evaluator` is a lightweight evaluation toolkit designed for generative AI researchers and practitioners. Under a unified interface, it systematically covers **nine core evaluation dimensions**: single-image aesthetic score, cross-modal text-image semantic alignment, subject facial identity fidelity, pairwise fidelity triad (deep perceptual distance, structural similarity, and peak signal-to-noise ratio), dataset generative distribution distance (Fréchet Inception Distance and Kernel Inception Distance), and human preference alignment.

---

## Metric Architecture Matrix

The toolkit structures its nine core metrics across four functional dimensions based on evaluation input interface:

| Category | Metric | Required Options | Output Scale | Direction | Documentation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **No-Reference Quality** | `aesthetic` | `--image` | `[1.0, 10.0]` | Higher is better | [Aesthetic Score](/no-reference/aesthetic) |
| **Text-to-Image Alignment** | `clip` | `--image`, `--prompt` | `[0.0, 100.0]` | Higher is better | [CLIP Score](/text-image/clip) |
| **Text-to-Image Alignment** | `pickscore` | `--image`, `--prompt` | Logits $\\approx [15, 25]$ | Higher is better | [PickScore](/text-image/pickscore) |
| **Pairwise Comparison** | `lpips` | `--image`, `--reference` | `[0.0, +inf)` | Lower is better | [LPIPS Distance](/pairwise/lpips) |
| **Pairwise Comparison** | `ssim` | `--image`, `--reference` | `[-1.0, 1.0]` | Higher is better | [SSIM Similarity](/pairwise/ssim) |
| **Pairwise Comparison** | `psnr` | `--image`, `--reference` | dB $\\in [0.0, +inf)$ | Higher is better | [PSNR Ratio](/pairwise/psnr) |
| **Pairwise Comparison** | `arcface` | `--image`, `--reference` | `[0.0, 2.0]` | Lower is better | [ArcFace Distance](/pairwise/arcface) |
| **Dataset Distribution** | `fid` | `--image <dir>`, `--reference <dir>` | `[0.0, +inf)` | Lower is better | [FID Score](/distribution/fid) |
| **Dataset Distribution** | `kid` | `--image <dir>`, `--reference <dir>` | U-stat $\\approx [-0.01, 0.10]$ | Lower is better | [KID Score](/distribution/kid) |

---

## Core Capability Highlights

<Cards>
  <Card title="No-Reference Quality" href="/no-reference/aesthetic" description="Evaluate standalone aesthetic appeal and visual composition without ground-truth reference." />
  <Card title="Text-to-Image Alignment" href="/text-image/clip" description="Evaluate semantic prompt compliance and fine-tuned human subjective preference." />
  <Card title="Pairwise Comparison" href="/pairwise/lpips" description="Measure perceptual distortion (LPIPS), structural fidelity (SSIM), pixel SNR (PSNR), and facial identity (ArcFace)." />
  <Card title="Dataset Distribution" href="/distribution/fid" description="Quantify population-level distribution shift via large-sample FID and unbiased small-sample KID." />
  <Card title="Interactive Benchmark" href="/benchmark/visual-demo" description="Explore interactive split-screen comparisons across extreme distortion and color-shift cases." />
</Cards>

---

## Quickstart Tutorial

<Steps>
  <Step>
    ### Environment Installation

    Install `image-evaluator` in your Python 3.11+ environment:

    ```bash
    pip install image-evaluator
    ```
  </Step>

  <Step>
    ### Single-Image Aesthetic Evaluation

    Score standalone visual appeal using LAION aesthetic predictor:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics aesthetic --image path/to/sample.png
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.laion_ai_aesthetic_predictor import LaionAiAestheticPredictor

        predictor = LaionAiAestheticPredictor()
        score = predictor.evaluate_aesthetic_score("path/to/sample.png")
        print(f"Aesthetic Score: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Text-Image Alignment and Preference Scoring

    Verify text prompt alignment and subjective human preference simultaneously:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics clip pickscore \\
            --image path/to/sample.png \\
            --prompt "an astronaut riding a horse on mars"
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.clip_score_predictor import ClipScorePredictor
        from image_evaluator.pickscore_predictor import PickScorePredictor

        clip_pred = ClipScorePredictor()
        pick_pred = PickScorePredictor()

        prompt = "an astronaut riding a horse on mars"
        clip_val = clip_pred.evaluate_clip_score("path/to/sample.png", prompt=prompt)
        pick_val = pick_pred.evaluate_pickscore("path/to/sample.png", prompt=prompt)

        print(f"CLIP Score: {clip_val:.4f}, PickScore: {pick_val:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Pairwise Fidelity Triad Evaluation

    Quantify perceptual, structural, and numerical differences against a reference ground truth:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics lpips ssim psnr \\
            --reference path/to/reference.png \\
            --image path/to/generated.png
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.lpips_predictor import LPIPSPredictor
        from image_evaluator.ssim_predictor import SSIMPredictor
        from image_evaluator.psnr_predictor import PSNRPredictor

        lpips_p = LPIPSPredictor()
        ssim_p = SSIMPredictor()
        psnr_p = PSNRPredictor()

        ref, gen = "path/to/reference.png", "path/to/generated.png"
        print(f"LPIPS: {lpips_p.evaluate_lpips(ref, gen):.4f}")
        print(f"SSIM:  {ssim_p.evaluate_ssim(ref, gen):.4f}")
        print(f"PSNR:  {psnr_p.evaluate_psnr(ref, gen):.2f} dB")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Generative Dataset Distribution Distances

    Compare feature distribution shifts between generated and ground-truth directories:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics fid kid \\
            --reference path/to/real_folder/ \\
            --image path/to/generated_folder/
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.fid_predictor import FIDPredictor
        from image_evaluator.kid_predictor import KIDPredictor

        fid_p = FIDPredictor()
        kid_p = KIDPredictor()

        real_dir, gen_dir = "path/to/real_folder/", "path/to/generated_folder/"
        print(f"FID: {fid_p.evaluate_fid(real_dir, gen_dir):.4f}")

        mean_kid, std_kid = kid_p.evaluate_kid(real_dir, gen_dir)
        print(f"KID: {mean_kid:.6f} (+/- {std_kid:.6f})")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

save("index.zh.mdx", """---
title: 快速开始
description: 统一图像质量与多维对齐评估套件
---

# 快速开始

`image-evaluator` 是一套面向生成式人工智能研究员与工程实践者的轻量级统一评估套件。该工具在统一的接口规范下，系统性覆盖了生成图像质量的**九大核心评估维度**：单图视觉美学质量预测、文本图像跨模态语义对齐、主体人脸身份保真度、成对图像保真度三元组（深度感知特征距离、结构统计相似度、峰值信噪比）、数据集分布保真度（双特征空间弗雷歇距离与核感知距离）以及人类主观偏好对齐评分。

---

## 评估维度与指标矩阵

本套件严格基于评测输入参数契约，将九项核心指标划分为四大体系：

| 评测类别 | 指标名称 | 必填参数选项 | 标度范围 | 取值方向 | 对应文档 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **单图无参考质量** | `aesthetic` | `--image` | `[1.0, 10.0]` | 数值越高越优 | [Aesthetic (单图美学)](/zh/no-reference/aesthetic) |
| **跨模态图文对齐** | `clip` | `--image`, `--prompt` | `[0.0, 100.0]` | 数值越高越优 | [CLIP Score (图文对齐)](/zh/text-image/clip) |
| **跨模态图文对齐** | `pickscore` | `--image`, `--prompt` | Logits $\\approx [15, 25]$ | 数值越高越优 | [PickScore (偏好对齐)](/zh/text-image/pickscore) |
| **成对保真与主体** | `lpips` | `--image`, `--reference` | `[0.0, +inf)` | 数值越低越优 | [LPIPS (深度感知)](/zh/pairwise/lpips) |
| **成对保真与主体** | `ssim` | `--image`, `--reference` | `[-1.0, 1.0]` | 数值越高越优 | [SSIM (结构相似)](/zh/pairwise/ssim) |
| **成对保真与主体** | `psnr` | `--image`, `--reference` | dB $\\in [0.0, +inf)$ | 数值越高越优 | [PSNR (峰值信噪比)](/zh/pairwise/psnr) |
| **成对保真与主体** | `arcface` | `--image`, `--reference` | `[0.0, 2.0]` | 数值越低越优 | [ArcFace (主体保真)](/zh/pairwise/arcface) |
| **群体生成分布差异** | `fid` | `--image <dir>`, `--reference <dir>` | `[0.0, +inf)` | 数值越低越优 | [FID (弗雷歇距离)](/zh/distribution/fid) |
| **群体生成分布差异** | `kid` | `--image <dir>`, `--reference <dir>` | U-stat $\\approx [-0.01, 0.10]$ | 数值越低越优 | [KID (核最大均值)](/zh/distribution/kid) |

---

## 核心能力矩阵导览

<Cards>
  <Card title="单图无参考质量" href="/zh/no-reference/aesthetic" description="无须参考底图，评估单图美学构图、质感与纯视觉质量得分。" />
  <Card title="跨模态图文对齐" href="/zh/text-image/clip" description="基于提示词语义遵从度 (CLIP) 与真实人类主观审美偏好 (PickScore) 进行联合评估。" />
  <Card title="成对保真与主体一致" href="/zh/pairwise/lpips" description="解耦深层感知纹理 (LPIPS)、结构轮廓 (SSIM)、像素信噪比 (PSNR) 以及人脸主体身份 (ArcFace)。" />
  <Card title="群体生成分布差异" href="/zh/distribution/fid" description="度量大样本分布距离 (FID) 与千张小样本无偏统计量 (KID)。" />
  <Card title="交互式实测演练" href="/zh/benchmark/visual-demo" description="探查严重几何撕裂、全局暖色温色偏与人脸编辑下的多维指标联动。" />
</Cards>

---

## 快速开始教程

<Steps>
  <Step>
    ### 环境安装

    在 Python 3.11+ 环境中安装发布版本：

    ```bash
    pip install image-evaluator
    ```
  </Step>

  <Step>
    ### 单图视觉美学评分

    计算单张图像或目录的 LAION 视觉美学评分：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics aesthetic --image path/to/sample.png
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.laion_ai_aesthetic_predictor import LaionAiAestheticPredictor

        predictor = LaionAiAestheticPredictor()
        score = predictor.evaluate_aesthetic_score("path/to/sample.png")
        print(f"美学评分: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### 图文语义匹配与人类偏好评估

    同时评估生成图片与提示词的吻合度以及人类主观审美偏好：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics clip pickscore \\
            --image path/to/sample.png \\
            --prompt "an astronaut riding a horse on mars"
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.clip_score_predictor import ClipScorePredictor
        from image_evaluator.pickscore_predictor import PickScorePredictor

        clip_pred = ClipScorePredictor()
        pick_pred = PickScorePredictor()

        prompt = "an astronaut riding a horse on mars"
        clip_val = clip_pred.evaluate_clip_score("path/to/sample.png", prompt=prompt)
        pick_val = pick_pred.evaluate_pickscore("path/to/sample.png", prompt=prompt)

        print(f"CLIP 图文对齐: {clip_val:.4f}, PickScore 偏好: {pick_val:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### 成对图像保真度三元组评测

    对比生成图相对参考原图的多尺度重构精度：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics lpips ssim psnr \\
            --reference path/to/reference.png \\
            --image path/to/generated.png
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.lpips_predictor import LPIPSPredictor
        from image_evaluator.ssim_predictor import SSIMPredictor
        from image_evaluator.psnr_predictor import PSNRPredictor

        lpips_p = LPIPSPredictor()
        ssim_p = SSIMPredictor()
        psnr_p = PSNRPredictor()

        ref, gen = "path/to/reference.png", "path/to/generated.png"
        print(f"LPIPS 感知距离: {lpips_p.evaluate_lpips(ref, gen):.4f}")
        print(f"SSIM 结构相似:   {ssim_p.evaluate_ssim(ref, gen):.4f}")
        print(f"PSNR 峰值信噪比: {psnr_p.evaluate_psnr(ref, gen):.2f} dB")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### 数据集生成分布距离评测

    评估生成图库与真实图库之间的特征分布距离：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics fid kid \\
            --reference path/to/real_folder/ \\
            --image path/to/generated_folder/
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.fid_predictor import FIDPredictor
        from image_evaluator.kid_predictor import KIDPredictor

        fid_p = FIDPredictor()
        kid_p = KIDPredictor()

        real_dir, gen_dir = "path/to/real_folder/", "path/to/generated_folder/"
        print(f"FID 分布距离: {fid_p.evaluate_fid(real_dir, gen_dir):.4f}")

        mean_kid, std_kid = kid_p.evaluate_kid(real_dir, gen_dir)
        print(f"KID 无偏统计量: {mean_kid:.6f} (+/- {std_kid:.6f})")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

# ==============================================================================
# 2. NO-REFERENCE: AESTHETIC
# ==============================================================================
save("no-reference/aesthetic.mdx", """---
title: Aesthetic Score
description: LAION aesthetic predictor using OpenCLIP ViT-L-14 visual embeddings and linear projection
---

# Aesthetic Score

The LAION Aesthetic Predictor estimates the visual appeal and compositional beauty of a standalone image without requiring a ground-truth reference. It extracts normalized feature embeddings using OpenCLIP `ViT-L-14` and projects them through a lightweight linear head trained on the SAC (Simulacra Aesthetic Captions) and LAION-Aesthetics benchmark datasets.

---

## Technical Specifications

| Property | Specification |
| :--- | :--- |
| **Category** | No-Reference Image Quality |
| **CLI Metric** | `aesthetic` |
| **Input Options** | `--image <file_or_dir>` (required) |
| **Prohibited Options** | `--reference`, `--prompt` |
| **Output Scale** | Continuous scalar float in `[1.0, 10.0]` |
| **Direction** | **Higher is better** |
| **Model Backbone** | OpenCLIP `ViT-L-14` + linear MLP regression head |
| **Upstream Source** | [LAION-AI/aesthetic-predictor](https://github.com/LAION-AI/aesthetic-predictor) |

---

## Mathematical Formulation

The predictor computes a 768-dimensional normalized visual embedding $\\mathbf{z} \\in \\mathbb{R}^{768}$ from image $I$, followed by an affine projection with learned weights $\\mathbf{w}$ and bias $b$:

```math
s_{\\text{aesthetic}} = \\mathbf{w}^T \\left( \\frac{\\Phi(I)}{\\|\\Phi(I)\\|_2} \\right) + b
```

The resulting scalar output ranges in $[1.0, 10.0]$, where higher values reflect superior perceived artistic quality.

---

## Interpretation & Guidance

- **Score Distribution**: On general web and natural photography benchmarks, typical photos score between $4.5$ and $6.0$. High-grade professional photography and curated artwork typically score above $6.5$.
- **No Ground-Truth Required**: Evaluates the image in isolation, ignoring semantic alignment with any prompt. Pair with **CLIP** or **PickScore** to assess prompt adherence.
- **Protocol Consistency**: Compare aesthetic scores only between models evaluated under the identical OpenCLIP ViT-L-14 backbone weights.

---

## Usage Examples

<Steps>
  <Step>
    ### Single Image Evaluation

    Evaluate standalone visual appeal for a synthetic image:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics aesthetic --image path/to/sample.png
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.laion_ai_aesthetic_predictor import LaionAiAestheticPredictor

        predictor = LaionAiAestheticPredictor()
        score = predictor.evaluate_aesthetic_score("path/to/sample.png")
        print(f"Aesthetic Score: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Batch Directory Evaluation

    Compute the mean aesthetic score across an entire folder of generated outputs:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics aesthetic --image path/to/folder/
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.laion_ai_aesthetic_predictor import LaionAiAestheticPredictor

        predictor = LaionAiAestheticPredictor()
        mean_score = predictor.evaluate_folder_aesthetic_score("path/to/folder/")
        print(f"Dataset Mean Aesthetic: {mean_score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>

---

## References

- **Model Repository**: [LAION-AI/aesthetic-predictor](https://github.com/LAION-AI/aesthetic-predictor)
- **Dataset**: Schuhmann et al., 2022, *LAION-Aesthetics: Predictor Training and Datasets* ([LAION Blog](https://laion.ai/blog/laion-aesthetics/))
- **Backbone**: Ilharco et al., 2021, *OpenCLIP* ([GitHub Repository](https://github.com/mlfoundations/open_clip))
""")

save("no-reference/aesthetic.zh.mdx", """---
title: Aesthetic (单图美学评分)
description: 基于 OpenCLIP ViT-L-14 视觉特征与线性回归头的 LAION 视觉美学质量预测
---

# Aesthetic (单图美学评分)

LAION Aesthetic 美学评估器用于度量单张图像的构图美学与视觉吸引力，全程无需任何参考底图。该模型通过 OpenCLIP `ViT-L-14` 骨干网络提取图像的归一化特征向量，输入经过 SAC (Simulacra Aesthetic Captions) 与 LAION-Aesthetics 真实人类审美标注微调的轻量级线性回归头输出评分。

---

## 核心规格

| 属性 | 规范定义 |
| :--- | :--- |
| **评测体系** | 单图无参考质量 (No-Reference Quality) |
| **命令行参数** | `--metrics aesthetic` |
| **输入要求** | `--image <路径>` (单图或图片目录) |
| **禁止参数** | `--reference`, `--prompt` (传入将直接报错) |
| **标度范围** | 标量连续浮点数 `[1.0, 10.0]` |
| **取值方向** | **数值越高越优** |
| **骨干网络** | OpenCLIP `ViT-L-14` + SAC 线性打分头 |
| **权威源** | [LAION-AI/aesthetic-predictor](https://github.com/LAION-AI/aesthetic-predictor) |

---

## 理论公式推导

美学模型首先使用图像编码器 $\\Phi$ 提取 768 维归一化特征向量 $\\mathbf{z}$，随后通过权重矩阵 $\\mathbf{w}$ 与偏置项 $b$ 完成打分：

```math
s_{\\text{aesthetic}} = \\mathbf{w}^T \\left( \\frac{\\Phi(I)}{\\|\\Phi(I)\\|_2} \\right) + b
```

该指标取值范围为 $[1.0, 10.0]$，分值越高代表模型判断的艺术美感越强。

---

## 评测阈值与解读建议

- **分布区间参考**：在自然摄影与通用图库上，普通自然照片分值多落在 $4.5$ 至 $6.0$ 之间；高品质专业摄影作品与优质精选生成图通常达到 $6.5$ 分以上。
- **无参考限制**：该指标独立评测图像构图，不感知任何文字提示词。若需评估图片对提示词的还原度，请联合使用 **CLIP** 或 **PickScore**。
- **基准一致性**：不同实验对比时，必须保证运行在同一套 OpenCLIP ViT-L-14 预训练权重之下。

---

## 调用示例

<Steps>
  <Step>
    ### 单张图像美学评估

    计算单张生成图像的美学分值：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics aesthetic --image path/to/sample.png
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.laion_ai_aesthetic_predictor import LaionAiAestheticPredictor

        predictor = LaionAiAestheticPredictor()
        score = predictor.evaluate_aesthetic_score("path/to/sample.png")
        print(f"美学评分: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### 目录批量均值评测

    批量评估生成图库并输出整体美学平均分：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics aesthetic --image path/to/folder/
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.laion_ai_aesthetic_predictor import LaionAiAestheticPredictor

        predictor = LaionAiAestheticPredictor()
        mean_score = predictor.evaluate_folder_aesthetic_score("path/to/folder/")
        print(f"图库平均美学分: {mean_score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>

---

## 参考文献与项目源

- **官方模型仓库**: [LAION-AI/aesthetic-predictor](https://github.com/LAION-AI/aesthetic-predictor)
- **训练数据发布**: Schuhmann et al., 2022, *LAION-Aesthetics: Predictor Training and Datasets* ([LAION Blog](https://laion.ai/blog/laion-aesthetics/))
- **骨干网络实现**: Ilharco et al., 2021, *OpenCLIP* ([GitHub 仓库](https://github.com/mlfoundations/open_clip))
""")

