import os

DOCS_DIR = "content/docs"

def save(path, content):
    full_path = os.path.join(DOCS_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {path}")

# ==============================================================================
# SINGLE-IMAGE: AESTHETIC
# ==============================================================================
save("single-image/aesthetic.mdx", """---
title: Aesthetic (Visual Quality Score)
description: Aesthetic Predictor V2 - Zero-reference aesthetic evaluation with OpenCLIP ViT-L-14
---

# Aesthetic (Visual Quality Score)

LAION AI Aesthetic Score estimates perceived visual quality using an OpenCLIP `ViT-L-14` backbone coupled with a linear regression head trained on human ratings from aesthetic datasets (such as SAC and AVA). It is widely utilized for automated image filtering, curated gallery ranking, and analyzing prompt engineering quality.

---

## Technical Specifications

| Parameter | Specification |
| :--- | :--- |
| **CLI Argument** | `--metrics aesthetic` |
| **Input Constraint** | `--image` (single image file or directory) |
| **Output Type** | Continuous scalar float (typical range `[1.0, 10.0]`) |
| **Direction** | **Higher is better** |
| **Backbone Architecture** | OpenCLIP `ViT-L-14` (`openai` weights, `force_quick_gelu=True`) + linear regression head |
| **Source Implementation** | [LAION-AI/aesthetic-predictor](https://github.com/LAION-AI/aesthetic-predictor) (`sa_0_4_vit_l_14_linear.pth`) |

---

## Formulation & Architectural Alignment

The predictor extracts a 768-dimensional normalized visual embedding $\\mathbf{z} \\in \\mathbb{R}^{768}$ from the input image $I$, then applies a learned linear projection:

```math
\\text{Score}(I) = \\mathbf{w}^T \\left( \\frac{\\Phi(I)}{\\|\\Phi(I)\\|_2} \\right) + b
```

### QuickGELU Activation Alignment

The predictor explicitly instantiates OpenCLIP with `force_quick_gelu=True`. This preserves exact consistency with the official OpenAI pre-trained weights and the historical reference implementation (`open_clip==1.3.0`). While modern `open_clip` releases defaulted to standard PyTorch `nn.GELU()`, triggering weight mismatch warnings, our explicit activation alignment eliminates warnings and guarantees deterministic embedding reproducibility.

---

## Usage Examples

<Steps>
  <Step>
    ### Single Image Evaluation

    Compute the aesthetic score for a single generated image:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics aesthetic --image sample.png
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.laion_ai_aesthetic_predictor import LaionAiAestheticPredictor

        predictor = LaionAiAestheticPredictor()
        score = predictor.evaluate_aesthetic_score("sample.png")
        print(f"Aesthetic Score: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Directory Batch Evaluation

    Compute the arithmetic mean aesthetic score across an entire image directory:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics aesthetic --image path/to/images_dir/
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.laion_ai_aesthetic_predictor import LaionAiAestheticPredictor

        predictor = LaionAiAestheticPredictor()
        mean_score = predictor.evaluate_folder_aesthetic_score("path/to/images_dir/")
        print(f"Mean Aesthetic Score: {mean_score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

save("single-image/aesthetic.zh.mdx", """---
title: Aesthetic (单图美学评分)
description: Aesthetic Predictor V2 - 零参考图视觉美学评分预测
---

# Aesthetic (单图美学评分)

LAION AI Aesthetic Score 是一项无需参考原图的单图视觉审美质量评估指标。该指标基于在海量图文数据上预训练的 OpenCLIP `ViT-L-14` 视觉模型提取高维特征，并结合在人类主观审美标注数据集（SAC、AVA）上拟合的线性回归预测头，将抽象的美学感受量化为连续数值。

---

## 核心规格与指标特性

| 参数维度 | 规范与技术事实 |
| :--- | :--- |
| **命令行参数** | `--metrics aesthetic` |
| **输入约束** | `--image`（单个图像文件或图像文件夹） |
| **输出形式** | 位于区间 $$[1.0, 10.0]$$ 的连续标量浮点数 |
| **数值导向** | **越高越优**（分值越高代表画面主观审美品质越好） |
| **预训练骨干** | OpenCLIP `ViT-L-14`（官方 `openai` 权重，`force_quick_gelu=True`） |
| **回归权重头** | `sa_0_4_vit_l_14_linear.pth`（768 维特征线性回归层） |

---

## 数学原理与架构对齐

模型首先将输入图像 $I$ 缩放至 $224 \\times 224$ 分辨率并送入 ViT-L-14 提取 768 维特征向量，对其执行 $L_2$ 单位范数归一化，最终经由线性回归权重计算标量得分：

```math
\\text{Score}(I) = \\mathbf{w}^T \\left( \\frac{\\Phi(I)}{\\|\\Phi(I)\\|_2} \\right) + b
```

### QuickGELU 激活函数对齐机制

本套件在初始化 OpenCLIP 骨干网络时显式指定 `force_quick_gelu=True`：
- **权重原生兼容**：官方 OpenAI 原始权重在训练期间严格使用 QuickGELU 激活函数。后继高版本 `open_clip` 默认退化为标准 `nn.GELU()`，会触发结构不匹配告警并造成特征偏移。
- **消减数值扰动**：显式对齐激活函数根除了上游权重加载警告，确保评分与官方基准测试结果具有 100% 确定性的一致性。

---

## 调用范例 (CLI 与 Python API)

<Steps>
  <Step>
    ### 单图美学质量打分

    计算单张生成图像的美学分值：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics aesthetic --image sample.png
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.laion_ai_aesthetic_predictor import LaionAiAestheticPredictor

        predictor = LaionAiAestheticPredictor()
        score = predictor.evaluate_aesthetic_score("sample.png")
        print(f"单图美学评分: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### 目录批量美学打分

    对图库目录中所有有效图片执行批量美学预测并返回算术均值：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics aesthetic --image path/to/images_dir/
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.laion_ai_aesthetic_predictor import LaionAiAestheticPredictor

        predictor = LaionAiAestheticPredictor()
        mean_score = predictor.evaluate_folder_aesthetic_score("path/to/images_dir/")
        print(f"图库平均美学分: {mean_score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

# ==============================================================================
# SINGLE-IMAGE: CLIP
# ==============================================================================
save("single-image/clip.mdx", """---
title: CLIP Score (Text-Image Alignment)
description: Objective cosine similarity in multimodal embedding space via clip-vit-base-patch32
---

# CLIP Score (Text-Image Alignment)

CLIP Score measures the semantic alignment between a generated image and its guiding text prompt. It evaluates whether the visual concepts described in the prompt are faithfully manifested in the synthesized output by projecting both modalities into a shared normalized embedding space.

---

## Technical Specifications

| Parameter | Specification |
| :--- | :--- |
| **CLI Argument** | `--metrics clip` |
| **Input Constraint** | `--image` (file/directory) and `--prompt` (text or prompt file) |
| **Output Type** | Continuous float in `[0.0, 100.0]` |
| **Direction** | **Higher is better** |
| **Backbone Architecture** | OpenAI `clip-vit-base-patch32` |
| **Formula Reference** | Hessel et al., "CLIPScore: A Reference-free Evaluation Metric for Image Captioning", EMNLP 2021 |

---

## Formulation

Let $\\mathbf{e}_I = \\frac{\\Phi_{\\text{visual}}(I)}{\\|\\Phi_{\\text{visual}}(I)\\|_2}$ and $\\mathbf{e}_T = \\frac{\\Phi_{\\text{text}}(T)}{\\|\\Phi_{\\text{text}}(T)\\|_2}$ be the $L_2$-normalized visual and text embeddings:

```math
\\text{CLIP-Score}(I, T) = \\max(100 \\cdot \\cos(\\mathbf{e}_I, \\mathbf{e}_T), 0) = \\max(100 \\cdot (\\mathbf{e}_I \\cdot \\mathbf{e}_T), 0)
```

---

## Usage Examples

<Steps>
  <Step>
    ### Single Image Alignment

    Evaluate how closely an image follows a given text prompt:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics clip \\
            --image sample.png \\
            --prompt "an astronaut riding a horse on mars"
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.clip_score_predictor import ClipScorePredictor

        predictor = ClipScorePredictor()
        score = predictor.evaluate_clip_score(
            image_path="sample.png",
            prompt="an astronaut riding a horse on mars"
        )
        print(f"CLIP Score: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Directory Batch Evaluation

    Evaluate an entire directory against a shared prompt:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics clip \\
            --image path/to/images_dir/ \\
            --prompt "photorealistic landscape at sunset"
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.clip_score_predictor import ClipScorePredictor

        predictor = ClipScorePredictor()
        mean_score = predictor.evaluate_folder_clip_score(
            folder_path="path/to/images_dir/",
            prompt="photorealistic landscape at sunset"
        )
        print(f"Mean CLIP Score: {mean_score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

save("single-image/clip.zh.mdx", """---
title: CLIP Score (图文语义对齐)
description: 多模态嵌入空间图文余弦相似度客观评测
---

# CLIP Score (图文语义对齐)

CLIP Score 用于客观量化生成图像与其指导文本提示词（Prompt）之间的跨模态语义匹配度。该指标基于 OpenAI 预训练的对比学习图文模型，分别将图像与文本映射至统一维度的归一化超球面向量空间，并通过余弦距离度量两者语义吻合程度。

---

## 核心规格与指标特性

| 参数维度 | 规范与技术事实 |
| :--- | :--- |
| **命令行参数** | `--metrics clip` |
| **输入约束** | 必须同时提供 `--image` 与 `--prompt`（支持文本字符串或包含提示词的文本文件） |
| **输出形式** | 位于区间 $$[0.0, 100.0]$$ 的标量浮点数（底层为余弦相似度放大 100 倍） |
| **数值导向** | **越高越优**（分值越高代表图像与提示词所描述的语义内容越契合） |
| **预训练骨干** | OpenAI `clip-vit-base-patch32` |
| **学术出处** | Hessel et al., "CLIPScore: A Reference-free Evaluation Metric for Image Captioning", EMNLP 2021 |

---

## 数学原理与计算公式

设输入图像为 $I$，文本提示词为 $T$。特征抽取器分别计算归一化视觉向量 $\\mathbf{e}_I$ 与文本向量 $\\mathbf{e}_T$：

```math
\\text{CLIP-Score}(I, T) = \\max(100 \\cdot \\cos(\\mathbf{e}_I, \\mathbf{e}_T), 0) = \\max(100 \\cdot (\\mathbf{e}_I \\cdot \\mathbf{e}_T), 0)
```

---

## 调用范例 (CLI 与 Python API)

<Steps>
  <Step>
    ### 单图提示词对齐度评测

    评估单幅生成图像对文本指令的遵循程度：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics clip \\
            --image sample.png \\
            --prompt "an astronaut riding a horse on mars"
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.clip_score_predictor import ClipScorePredictor

        predictor = ClipScorePredictor()
        score = predictor.evaluate_clip_score(
            image_path="sample.png",
            prompt="an astronaut riding a horse on mars"
        )
        print(f"CLIP 语义对齐分: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### 图库批量对齐度评测

    评测文件夹内所有生成图像对公共提示词的平均遵从表现：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics clip \\
            --image path/to/images_dir/ \\
            --prompt "photorealistic landscape at sunset"
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.clip_score_predictor import ClipScorePredictor

        predictor = ClipScorePredictor()
        mean_score = predictor.evaluate_folder_clip_score(
            folder_path="path/to/images_dir/",
            prompt="photorealistic landscape at sunset"
        )
        print(f"平均 CLIP 对齐分: {mean_score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

# ==============================================================================
# SINGLE-IMAGE: ARCFACE
# ==============================================================================
save("single-image/arcface.mdx", """---
title: ArcFace (Subject Identity Fidelity)
description: Face identity cosine distance evaluation via InsightFace buffalo_l 512-dimensional embeddings
---

# ArcFace (Subject Identity Fidelity)

ArcFace evaluates subject facial identity preservation across personalization, face-swapping, and subject-driven generation tasks. Powered by InsightFace `buffalo_l`, it extracts 512-dimensional deep facial representations and calculates the angular cosine distance between the generated subject and a ground-truth reference photo.

---

## Technical Specifications

| Parameter | Specification |
| :--- | :--- |
| **CLI Argument** | `--metrics arcface` |
| **Input Constraint** | Paired `--image` and `--reference` (files or directories with matching stems) |
| **Output Type** | Continuous scalar float in `[0.0, 2.0]` |
| **Direction** | **Lower is better** (< 0.40 indicates high identity consistency, 0.0 = identical face) |
| **Backbone Model** | InsightFace `buffalo_l` (ResNet-50 / ArcFace loss) |
| **Threshold Guidance** | Cosine distance < 0.40 indicates same identity; > 0.60 indicates identity drift |

---

## Formulation

Let $\\mathbf{f}_1, \\mathbf{f}_2 \\in \\mathbb{R}^{512}$ be the $L_2$-normalized facial feature vectors:

```math
\\text{Distance}(\\mathbf{f}_1, \\mathbf{f}_2) = 1 - \\frac{\\mathbf{f}_1 \\cdot \\mathbf{f}_2}{\\|\\mathbf{f}_1\\|_2 \\|\\mathbf{f}_2\\|_2}
```

If multiple faces are detected, the detector automatically selects the dominant face based on bounding-box area and landmark confidence.

---

## Usage Examples

<Steps>
  <Step>
    ### Single Pair Face Identity Check

    Verify whether an edited or generated portrait preserves the reference person's identity:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics arcface \\
            --reference real_face.png \\
            --image generated_face.png
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.arcface_dist_predictor import ArcFaceDistPredictor

        predictor = ArcFaceDistPredictor()
        distance = predictor.evaluate_arcface_distance(
            reference_path="real_face.png",
            generated_path="generated_face.png"
        )
        print(f"ArcFace Cosine Distance: {distance:.4f}")
        print("Verdict: " + ("Same Identity" if distance < 0.45 else "Identity Drift Detected"))
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Directory Batch Evaluation

    Evaluate facial identity preservation across pairs of images with matching stems:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics arcface \\
            --reference path/to/real_faces/ \\
            --image path/to/generated_faces/
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.arcface_dist_predictor import ArcFaceDistPredictor

        predictor = ArcFaceDistPredictor()
        mean_dist = predictor.evaluate_folder_arcface_distance(
            reference_folder="path/to/real_faces/",
            generated_folder="path/to/generated_faces/"
        )
        print(f"Mean ArcFace Distance: {mean_dist:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

save("single-image/arcface.zh.mdx", """---
title: ArcFace (主体身份保真)
description: 深度人脸特征空间余弦距离与身份一致性度量
---

# ArcFace (主体身份保真)

ArcFace 专注于衡量人像个性化定制（Personalization）、LoRA 角色重绘以及人脸替换（Face-Swap）算法中的主体生物特征一致性。该指标基于成熟的人脸深度表征框架 InsightFace `buffalo_l`，提取两幅图像中目标人脸的 512 维深度嵌入特征向量，并计算其余弦距离。

---

## 核心规格与指标特性

| 参数维度 | 规范与技术事实 |
| :--- | :--- |
| **命令行参数** | `--metrics arcface` |
| **输入约束** | 必须成对提供包含清晰人脸的 `--image` 与 `--reference` |
| **输出形式** | 位于区间 $$[0.0, 2.0]$$ 的无量纲余弦距离浮点数 |
| **数值导向** | **越低越优**（数值越小代表身份越吻合；0.0 代表人脸特征完全一致） |
| **预训练骨干** | InsightFace `buffalo_l`（ResNet-50 主干网络，ArcFace 角度边界损失） |
| **同人判定阈值** | 通常建议取 **0.40 - 0.50** 为同人判决线；大于 0.60 判定为身份漂移 |

---

## 数学原理与计算公式

设待测图与参考图检测出的人脸 512 维特征向量分别为 $\\mathbf{f}_1$ 与 $\\mathbf{f}_2$：

```math
\\text{Distance}(\\mathbf{f}_1, \\mathbf{f}_2) = 1 - \\frac{\\mathbf{f}_1 \\cdot \\mathbf{f}_2}{\\|\\mathbf{f}_1\\|_2 \\|\\mathbf{f}_2\\|_2}
```

若画面中存在多人脸，检测器依据人脸检测置信度与边界框面积自动选择主面孔执行特征抽取与对齐。

---

## 调用范例 (CLI 与 Python API)

<Steps>
  <Step>
    ### 单对人脸身份保真度校验

    比对编辑或生成的人脸是否与基准原图为同一人：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics arcface \\
            --reference real_face.png \\
            --image generated_face.png
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.arcface_dist_predictor import ArcFaceDistPredictor

        predictor = ArcFaceDistPredictor()
        distance = predictor.evaluate_arcface_distance(
            reference_path="real_face.png",
            generated_path="generated_face.png"
        )
        print(f"ArcFace 余弦距离: {distance:.4f}")
        print("判决结果: " + ("高度一致 (同人)" if distance < 0.45 else "身份发生漂移"))
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### 图库批量人像配对校验

    对两个目录中同名文件逐对提取人脸并计算平均距离：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics arcface \\
            --reference path/to/real_faces/ \\
            --image path/to/generated_faces/
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.arcface_dist_predictor import ArcFaceDistPredictor

        predictor = ArcFaceDistPredictor()
        mean_dist = predictor.evaluate_folder_arcface_distance(
            reference_folder="path/to/real_faces/",
            generated_folder="path/to/generated_faces/"
        )
        print(f"批处理平均 ArcFace 距离: {mean_dist:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

# ==============================================================================
# PAIRWISE: LPIPS
# ==============================================================================
save("pairwise/lpips.mdx", """---
title: LPIPS (Perceptual Distance)
description: Learned Perceptual Image Patch Similarity using AlexNet multi-scale deep features
---

# LPIPS (Perceptual Distance)

Learned Perceptual Image Patch Similarity (LPIPS) by Zhang et al. (CVPR 2018) evaluates perceptual fidelity across generated and reference images. By extracting multi-scale activations from a deep neural network and applying learned channel weights, it correlates strongly with human subjective judgments of image similarity.

---

## Technical Specifications

| Parameter | Specification |
| :--- | :--- |
| **CLI Argument** | `--metrics lpips` |
| **Input Constraint** | Paired `--image` and `--reference` (identical spatial dimensions required) |
| **Output Type** | Continuous scalar float in `[0.0, +inf)` |
| **Direction** | **Lower is better** (0.0 represents identical perceptual features) |
| **Backbone Architecture** | Official `lpips` v0.1 (AlexNet trunk) |
| **Dynamic Range** | Normalized to `[-1.0, 1.0]` internally |
| **Academic Citation** | Zhang et al., "The Unreasonable Effectiveness of Deep Features as a Perceptual Metric", CVPR 2018 |

---

## Formulation

LPIPS extracts feature activations across $L$ layers from reference $x$ and generated $x_0$. Within each layer $l$, feature channels are normalized by $L_2$ norm, scaled by learned vector $w_l$, and spatially averaged:

```math
d(x, x_0) = \\sum_l \\frac{1}{H_l W_l} \\sum_{h, w} \\left\\| w_l \\odot \\left( \\hat{y}^l_{hw} - \\hat{y}_{0, hw}^l \\right) \\right\\|_2^2
```

---

## Strict Dimension Check & Fail-Fast Policy

- **No Silent Resizing**: Input pairs must strictly match in dimensions ($H_{\\text{ref}} = H_{\\text{gen}}$ and $W_{\\text{ref}} = W_{\\text{gen}}$). The engine strictly terminates with a `ValueError` on size mismatch to prevent high-frequency interpolation distortion.
- **Exact Stem Alignment**: In directory mode, files pair strictly by case-sensitive stem across formats. Any unpaired file triggers an immediate halt.

---

## Usage Examples

<Steps>
  <Step>
    ### Single Pair Evaluation

    Measure deep perceptual distance between a generated sample and ground truth:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics lpips \\
            --reference path/to/reference.png \\
            --image path/to/generated.png
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.lpips_predictor import LPIPSPredictor

        predictor = LPIPSPredictor()
        distance = predictor.evaluate_lpips(
            reference_path="path/to/reference.png",
            generated_path="path/to/generated.png"
        )
        print(f"LPIPS Distance: {distance:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Directory Batch Evaluation

    Compute pairwise perceptual distance across directories of matching files:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics lpips \\
            --reference path/to/reference_folder/ \\
            --image path/to/generated_folder/
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.lpips_predictor import LPIPSPredictor

        predictor = LPIPSPredictor()
        mean_dist = predictor.evaluate_folder_lpips(
            reference_folder="path/to/reference_folder/",
            generated_folder="path/to/generated_folder/"
        )
        print(f"Mean LPIPS: {mean_dist:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

# ==============================================================================
# PAIRWISE: SSIM
# ==============================================================================
save("pairwise/ssim.mdx", """---
title: SSIM (Structural Similarity)
description: Structural Similarity Index Measure via 11x11 Gaussian window decomposition
---

# SSIM (Structural Similarity)

The Structural Similarity Index Measure (SSIM) evaluates the structural degradation between two images. Developed by Wang et al. (IEEE TIP 2004), it decouples image similarity into luminance, contrast, and structural covariance across localized sliding Gaussian patches.

---

## Technical Specifications

| Parameter | Specification |
| :--- | :--- |
| **CLI Argument** | `--metrics ssim` |
| **Input Constraint** | Paired `--image` and `--reference` (dimensions $\\ge 11 \\times 11$) |
| **Output Type** | Continuous float in `[-1.0, 1.0]` |
| **Direction** | **Higher is better** (1.0 = identical structure) |
| **Kernel Specification** | $11 \\times 11$ Gaussian sliding window, $\\sigma = 1.5$ |
| **Multi-Channel Rule** | Computed independently per RGB channel, unweighted arithmetic mean returned |

---

## Formulation

For local patches $x$ and $y$, SSIM evaluates:

```math
\\text{SSIM}(x, y) = \\frac{(2\\mu_x \\mu_y + C_1)(2\\sigma_{xy} + C_2)}{(\\mu_x^2 + \\mu_y^2 + C_1)(\\sigma_x^2 + \\sigma_y^2 + C_2)}
```

where $C_1 = (K_1 L)^2, C_2 = (K_2 L)^2$ with $K_1 = 0.01, K_2 = 0.03, L = 1.0$.

---

## Usage Examples

<Steps>
  <Step>
    ### Single Pair SSIM

    Measure structural statistical similarity between two registered images:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics ssim \\
            --reference path/to/reference.png \\
            --image path/to/generated.png
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.ssim_predictor import SSIMPredictor

        predictor = SSIMPredictor()
        similarity = predictor.evaluate_ssim(
            reference_path="path/to/reference.png",
            generated_path="path/to/generated.png"
        )
        print(f"SSIM: {similarity:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Directory Batch Evaluation

    Compute pairwise mean structural similarity across directories:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics ssim \\
            --reference path/to/reference_folder/ \\
            --image path/to/generated_folder/
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.ssim_predictor import SSIMPredictor

        predictor = SSIMPredictor()
        mean_ssim = predictor.evaluate_folder_ssim(
            reference_folder="path/to/reference_folder/",
            generated_folder="path/to/generated_folder/"
        )
        print(f"Mean SSIM: {mean_ssim:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

save("pairwise/ssim.zh.mdx", """---
title: SSIM (结构相似性)
description: 局部高斯滑动窗口亮度、对比度与结构三分量统计相似度
---

# SSIM (结构相似性)

结构相似性度量（Structural Similarity Index Measure，简称 SSIM）由 Zhou Wang 等人于 IEEE TIP 2004 提出。与仅衡量绝对数值差异的传统均方误差不同，SSIM 模拟人类视觉系统对结构信息的感知敏感性，将图像解耦为亮度均值、对比度方差与结构协方差三个独立分量。

---

## 核心规格与指标特性

| 参数维度 | 规范与技术事实 |
| :--- | :--- |
| **命令行参数** | `--metrics ssim` |
| **输入约束** | 必须成对提供 `--image` 与 `--reference`（图像尺寸不得低于 $$11 \\times 11$$ 像素） |
| **输出形式** | 位于区间 $$[-1.0, 1.0]$$ 的标量浮点数 |
| **数值导向** | **越高越优**（1.0 代表结构完全一致） |
| **滑动窗口** | $$11 \\times 11$$ 高斯局部加权滑动窗口，标准差 $$\\sigma = 1.5$$ |
| **多通道协议** | RGB 三个通道分别独立计算 SSIM，返回三通道非加权算术均值 |

---

## 理论推导与数学形式

对于局部图像块 $x$ 与 $y$，SSIM 综合亮度分量 $l(x, y)$、对比度分量 $c(x, y)$ 与结构分量 $s(x, y)$：

```math
\\text{SSIM}(x, y) = \\frac{(2\\mu_x \\mu_y + C_1)(2\\sigma_{xy} + C_2)}{(\\mu_x^2 + \\mu_y^2 + C_1)(\\sigma_x^2 + \\sigma_y^2 + C_2)}
```

其中 $C_1 = (K_1 L)^2, C_2 = (K_2 L)^2$，默认参数为 $K_1 = 0.01, K_2 = 0.03, L = 1.0$。

---

## 调用范例 (CLI 与 Python API)

<Steps>
  <Step>
    ### 单对图像结构相似性打分

    评估单幅生成图像相对基准真值的结构相似度：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics ssim \\
            --reference path/to/reference.png \\
            --image path/to/generated.png
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.ssim_predictor import SSIMPredictor

        predictor = SSIMPredictor()
        similarity = predictor.evaluate_ssim(
            reference_path="path/to/reference.png",
            generated_path="path/to/generated.png"
        )
        print(f"SSIM 结构相似度: {similarity:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### 目录批量逐对评测

    对两个目录中同名文件执行逐对 SSIM 计算并统计均值：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics ssim \\
            --reference path/to/reference_folder/ \\
            --image path/to/generated_folder/
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.ssim_predictor import SSIMPredictor

        predictor = SSIMPredictor()
        mean_ssim = predictor.evaluate_folder_ssim(
            reference_folder="path/to/reference_folder/",
            generated_folder="path/to/generated_folder/"
        )
        print(f"平均 SSIM: {mean_ssim:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

# ==============================================================================
# PAIRWISE: PSNR
# ==============================================================================
save("pairwise/psnr.mdx", """---
title: PSNR (Peak Signal-to-Noise Ratio)
description: Pixel-level reconstruction fidelity computed from Mean Squared Error
---

# PSNR (Peak Signal-to-Noise Ratio)

Peak Signal-to-Noise Ratio (PSNR) is the classical baseline metric in digital signal processing and image restoration. Measuring the ratio between maximum signal energy and reconstruction noise, it quantifies strict pixel-level ground-truth fidelity.

---

## Technical Specifications

| Parameter | Specification |
| :--- | :--- |
| **CLI Argument** | `--metrics psnr` |
| **Input Constraint** | Paired `--image` and `--reference` (exact matching spatial dimensions) |
| **Output Type** | Logarithmic decibels (dB) in `[0.0, +inf)` |
| **Direction** | **Higher is better** (typical high quality: 30-50 dB; identical: `+inf`) |
| **Input Range** | Floats normalized to `[0.0, 1.0]`, $\\text{MAX}_I = 1.0$ |
| **Zero-MSE Behavior** | Strictly returns `float("inf")` when images are identical |

---

## Formulation

Given ground-truth $I$ and generated $K$ of dimensions $m \\times n$:

```math
\\text{MSE} = \\frac{1}{3mn} \\sum_{c=1}^3 \\sum_{i=0}^{m-1} \\sum_{j=0}^{n-1} [I(i, j, c) - K(i, j, c)]^2
```

```math
\\text{PSNR} = 10 \\cdot \\log_{10}\\left( \\frac{\\text{MAX}_I^2}{\\text{MSE}} \\right)
```

---

## Usage Examples

<Steps>
  <Step>
    ### Single Pair PSNR

    Evaluate reconstruction signal-to-noise ratio:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics psnr \\
            --reference path/to/reference.png \\
            --image path/to/generated.png
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.psnr_predictor import PSNRPredictor

        predictor = PSNRPredictor()
        psnr_val = predictor.evaluate_psnr(
            reference_path="path/to/reference.png",
            generated_path="path/to/generated.png"
        )
        print(f"PSNR: {psnr_val:.2f} dB")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Directory Batch Evaluation

    Compute pairwise mean PSNR across directories:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics psnr \\
            --reference path/to/reference_folder/ \\
            --image path/to/generated_folder/
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.psnr_predictor import PSNRPredictor

        predictor = PSNRPredictor()
        mean_psnr = predictor.evaluate_folder_psnr(
            reference_folder="path/to/reference_folder/",
            generated_folder="path/to/generated_folder/"
        )
        print(f"Mean PSNR: {mean_psnr:.2f} dB")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

save("pairwise/psnr.zh.mdx", """---
title: PSNR (峰值信噪比)
description: 基于逐像素均方误差的底层物理级信号能量重构保真度
---

# PSNR (峰值信噪比)

峰值信噪比（Peak Signal-to-Noise Ratio，简称 PSNR）是数字信号处理、图像编码与底层图像恢复领域的底线基准指标。该指标通过均方误差（MSE）量化生成图像相对参考原图在每一个像素通道上的绝对能量差值。

---

## 核心规格与指标特性

| 参数维度 | 规范与技术事实 |
| :--- | :--- |
| **命令行参数** | `--metrics psnr` |
| **输入约束** | 必须成对提供 `--image` 与 `--reference`（尺寸必须完全一致） |
| **输出形式** | 位于区间 $$[0.0, +\\infty)$$ 的分贝（dB）数值 |
| **数值导向** | **越高越优**（高品质重构通常在 30-50 dB 之间；完全无损时为 `+inf`） |
| **信号极大值** | 输入张量归一化至 $$[0.0, 1.0]$$，对应最大信号能量 $$\\text{MAX}_I = 1.0$$ |
| **零误差行为** | 当成对两图完全一致时，MSE = 0，系统严格返回 `float("inf")` |

---

## 理论推导与数学形式

设三通道 RGB 图像分辨率为 $m \\times n$：

```math
\\text{MSE} = \\frac{1}{3mn} \\sum_{c=1}^3 \\sum_{i=0}^{m-1} \\sum_{j=0}^{n-1} [I(i, j, c) - K(i, j, c)]^2
```

```math
\\text{PSNR} = 10 \\cdot \\log_{10}\\left( \\frac{\\text{MAX}_I^2}{\\text{MSE}} \\right)
```

---

## 调用范例 (CLI 与 Python API)

<Steps>
  <Step>
    ### 单对图像重构信噪比评测

    计算生成图像相对基准真值的重构分贝：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics psnr \\
            --reference path/to/reference.png \\
            --image path/to/generated.png
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.psnr_predictor import PSNRPredictor

        predictor = PSNRPredictor()
        psnr_val = predictor.evaluate_psnr(
            reference_path="path/to/reference.png",
            generated_path="path/to/generated.png"
        )
        print(f"PSNR 峰值信噪比: {psnr_val:.2f} dB")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### 目录批量逐对评测

    对两个目录中同名文件逐对计算 PSNR 并统计均值：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics psnr \\
            --reference path/to/reference_folder/ \\
            --image path/to/generated_folder/
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.psnr_predictor import PSNRPredictor

        predictor = PSNRPredictor()
        mean_psnr = predictor.evaluate_folder_psnr(
            reference_folder="path/to/reference_folder/",
            generated_folder="path/to/generated_folder/"
        )
        print(f"平均 PSNR: {mean_psnr:.2f} dB")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

# ==============================================================================
# DISTRIBUTION: FID
# ==============================================================================
save("distribution/fid.mdx", """---
title: FID (Fréchet Inception Distance)
description: Generative distribution distance evaluated in Inception-v3 pool3 feature space
---

# FID (Fréchet Inception Distance)

Fréchet Inception Distance (FID), introduced by Heusel et al. (NeurIPS 2017), is the standard benchmark for evaluating the quality and diversity of generative models (GANs, Diffusion Models). It fits continuous multivariate Gaussians to deep feature representations extracted by Inception-v3 and computes the Wasserstein-2 distance between the real and generated distributions.

---

## Technical Specifications

| Parameter | Specification |
| :--- | :--- |
| **CLI Argument** | `--metrics fid` |
| **Input Constraint** | Two existing directories via `--image` and `--reference` |
| **Output Type** | Continuous scalar float in `[0.0, +inf)` |
| **Direction** | **Lower is better** (0.0 represents identical distributions) |
| **Feature Layer** | Official Inception-v3 (2048-dimensional activations from `pool3`) |
| **Sample Size Rule** | Biased estimator. Sample size $N \\ge 2048$ strongly recommended for publication |

---

## Formulation

Let $(\\mu_r, \\Sigma_r)$ and $(\\mu_g, \\Sigma_g)$ represent the empirical mean and covariance matrices of Inception-v3 pool3 feature representations:

```math
\\text{FID} = \\|\\mu_r - \\mu_g\\|_2^2 + \\text{Tr}\\left( \\Sigma_r + \\Sigma_g - 2(\\Sigma_r \\Sigma_g)^{1/2} \\right)
```

The matrix square root $(\\Sigma_r \\Sigma_g)^{1/2}$ is resolved using robust Schur decomposition, with imaginary residuals eliminated if numerical conditioning issues arise.

---

## Usage Examples

<Steps>
  <Step>
    ### Dataset Generative Distribution Evaluation

    Compute the FID score between a folder of synthesized samples and real reference data:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics fid \\
            --reference path/to/real_dataset/ \\
            --image path/to/generated_dataset/
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.fid_predictor import FIDPredictor

        predictor = FIDPredictor()
        fid_score = predictor.evaluate_fid(
            reference_folder="path/to/real_dataset/",
            generated_folder="path/to/generated_dataset/"
        )
        print(f"FID Score: {fid_score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

save("distribution/fid.zh.mdx", """---
title: FID (弗雷歇感知距离)
description: Inception-v3 特征空间高斯协方差二次型距离
---

# FID (弗雷歇感知距离)

弗雷歇初始距离（Fréchet Inception Distance，简称 FID）由 Martin Heusel 等人于 NeurIPS 2017 提出。它是度量生成对抗网络（GAN）与扩散模型（Diffusion Models）生成图像集合质量与多样性的学术界黄金标准。

---

## 核心规格与指标特性

| 参数维度 | 规范与技术事实 |
| :--- | :--- |
| **命令行参数** | `--metrics fid` |
| **输入约束** | 双方输入 `--image` 与 `--reference` 必须均为包含图像的已存在文件夹 |
| **输出形式** | 位于区间 $$[0.0, +\\infty)$$ 的无量纲标量浮点数 |
| **数值导向** | **越低越优**（数值越小代表生成图库与真实图库的分布越一致） |
| **特征提取器** | 官方 Inception-v3 模型（倒数第二层 `pool3` 提取的 2048 维特征） |
| **样本量约束** | 存在小样本正向偏差，学术严谨对比强烈建议样本量 $$N \\ge 2048$$ |

---

## 理论推导与数学形式

将真实图片集与生成图片集分别输入 Inception-v3，计算提取出的 2048 维特征向量的均值向量 $\\mu_r, \\mu_g$ 以及经验协方差矩阵 $\\Sigma_r, \\Sigma_g$：

```math
\\text{FID} = \\|\\mu_r - \\mu_g\\|_2^2 + \\text{Tr}\\left( \\Sigma_r + \\Sigma_g - 2(\\Sigma_r \\Sigma_g)^{1/2} \\right)
```

---

## 调用范例 (CLI 与 Python API)

<Steps>
  <Step>
    ### 数据集生成分布距离计算

    对比生成数据集与基准真实数据集的特征高斯距离：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics fid \\
            --reference path/to/real_dataset/ \\
            --image path/to/generated_dataset/
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.fid_predictor import FIDPredictor

        predictor = FIDPredictor()
        fid_score = predictor.evaluate_fid(
            reference_folder="path/to/real_dataset/",
            generated_folder="path/to/generated_dataset/"
        )
        print(f"FID 分布距离: {fid_score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

# ==============================================================================
# DISTRIBUTION: KID
# ==============================================================================
save("distribution/kid.mdx", """---
title: KID (Kernel Inception Distance)
description: Polynomial kernel Maximum Mean Discrepancy unbiased U-statistic for small-sample evaluation
---

# KID (Kernel Inception Distance)

Kernel Inception Distance (KID), proposed by Bińkowski et al. (ICLR 2018), measures generative distribution similarity using the squared Maximum Mean Discrepancy (MMD) with a polynomial kernel on Inception representations. Unlike FID, KID is an **unbiased estimator**, delivering statistically reliable benchmarks even on small subsets (e.g. 100 to 1000 samples).

---

## Technical Specifications

| Parameter | Specification |
| :--- | :--- |
| **CLI Argument** | `--metrics kid` |
| **Input Constraint** | Two directories via `--image` and `--reference` |
| **Output Type** | Mean and standard deviation floats (e.g. `mean +/- std`) |
| **Direction** | **Lower is better** (0.0 represents matching distributions) |
| **Estimator Type** | Unbiased U-statistic (may yield minute negative values due to sample variance) |
| **Resampling Strategy** | Repeated random subset sampling ($N=1000$ per fold) |

---

## Formulation

For Inception features $x, y \\in \\mathbb{R}^{2048}$, KID utilizes a cubic polynomial kernel:

```math
k(x, y) = \\left( \\frac{1}{d} x^T y + 1 \\right)^3, \\quad d = 2048
```

The unbiased squared MMD U-statistic between sample batches $X$ and $Y$ of size $m$ is given by:

```math
\\text{MMD}_u^2(X, Y) = \\frac{1}{m(m-1)} \\sum_{i \\neq j}^m k(x_i, x_j) + \\frac{1}{m(m-1)} \\sum_{i \\neq j}^m k(y_i, y_j) - \\frac{2}{m^2} \\sum_{i, j}^m k(x_i, y_j)
```

---

## Usage Examples

<Steps>
  <Step>
    ### Small-Sample Generative Distribution Evaluation

    Compute unbiased KID mean and standard deviation:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics kid \\
            --reference path/to/real_dataset/ \\
            --image path/to/generated_dataset/
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.kid_predictor import KIDPredictor

        predictor = KIDPredictor()
        mean_kid, std_kid = predictor.evaluate_folder_kid(
            reference_folder="path/to/real_dataset/",
            generated_folder="path/to/generated_dataset/"
        )
        print(f"KID: {mean_kid:.6f} (+/- {std_kid:.6f})")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

save("distribution/kid.zh.mdx", """---
title: KID (核最大均值差异)
description: 三次多项式核无偏 U 统计量，专精小样本分布评估
---

# KID (核最大均值差异)

核初始距离（Kernel Inception Distance，简称 KID）由 Mikołaj Bińkowski 等人于 ICLR 2018 提出。与 FID 强依赖经验协方差矩阵的高斯拟合不同，KID 采用非参数的多项式核最大均值差异（MMD）无偏 U 统计量，专为解决**小样本场景下的分布评估**而设计。

---

## 核心规格与指标特性

| 参数维度 | 规范与技术事实 |
| :--- | :--- |
| **命令行参数** | `--metrics kid` |
| **输入约束** | 双方输入 `--image` 与 `--reference` 必须均为包含图像的已存在文件夹 |
| **输出形式** | 返回均值与标准差浮点数（形如 `mean +/- std`） |
| **数值导向** | **越低越优**（数值越小代表生成分布与真实分布越接近） |
| **统计性质** | **严格无偏估计量**（在真实分布重合时可能因样本方差产生微小负值，属正常现象） |
| **重采样策略** | 采用 1000 个样本的子集进行多轮重抽样计算均值与标准差 |

---

## 理论推导与数学形式

对于 Inception-v3 提取的 2048 维特征向量 $x, y$，KID 采用三次多项式核函数：

```math
k(x, y) = \\left( \\frac{1}{d} x^T y + 1 \\right)^3, \\quad d = 2048
```

设样本量大小为 $m$，无偏 U 统计量形式如下：

```math
\\text{MMD}_u^2(X, Y) = \\frac{1}{m(m-1)} \\sum_{i \\neq j}^m k(x_i, x_j) + \\frac{1}{m(m-1)} \\sum_{i \\neq j}^m k(y_i, y_j) - \\frac{2}{m^2} \\sum_{i, j}^m k(x_i, y_j)
```

---

## 调用范例 (CLI 与 Python API)

<Steps>
  <Step>
    ### 小样本生成分布评测

    即使在几百张小样本图像下，依然获得可信的无偏分布统计量：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics kid \\
            --reference path/to/real_dataset/ \\
            --image path/to/generated_dataset/
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.kid_predictor import KIDPredictor

        predictor = KIDPredictor()
        mean_kid, std_kid = predictor.evaluate_folder_kid(
            reference_folder="path/to/real_dataset/",
            generated_folder="path/to/generated_dataset/"
        )
        print(f"KID 无偏均值: {mean_kid:.6f} (+/- {std_kid:.6f})")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

# ==============================================================================
# PREFERENCE: PICKSCORE
# ==============================================================================
save("preference/pickscore.mdx", """---
title: PickScore (Human Preference Alignment)
description: Fine-tuned CLIP ViT-H-14 scoring model trained on large-scale human choice data
---

# PickScore (Human Preference Alignment)

PickScore, introduced by Kirstain et al. (NeurIPS 2023), measures how well generated images align with real-world human preferences. Fine-tuned on the large-scale Pick-a-Pic dataset containing over 500,000 empirical human choices, it goes beyond pure semantic coverage to capture visual aesthetics, artifact avoidance, and compositional balance.

---

## Technical Specifications

| Parameter | Specification |
| :--- | :--- |
| **CLI Argument** | `--metrics pickscore` |
| **Input Constraint** | `--image` and `--prompt` required |
| **Output Type** | Continuous scalar float (higher indicates stronger human preference) |
| **Direction** | **Higher is better** |
| **Backbone Model** | Fine-tuned `yuvalkirstain/PickScore_v1` (based on OpenCLIP `ViT-H-14`) |
| **Training Basis** | > 500k real user preference comparisons from Pick-a-Pic |

---

## Formulation

Given text prompt $y$ and candidate image $x$, PickScore computes the preference logit via normalized visual and textual embeddings:

```math
s(x, y) = \\cos(\\Phi_{\\text{visual}}(x), \\Phi_{\\text{text}}(y))
```

The probability that image $x_1$ is preferred over $x_2$ given prompt $y$ models the Bradley-Terry choice probability:

```math
P(x_1 \\succ x_2 \\mid y) = \\frac{\\exp(s(x_1, y) / \\tau)}{\\exp(s(x_1, y) / \\tau) + \\exp(s(x_2, y) / \\tau)}
```

---

## Usage Examples

<Steps>
  <Step>
    ### Single Image Human Preference Score

    Evaluate synthetic image appeal against human preference standards:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics pickscore \\
            --image sample.png \\
            --prompt "a photorealistic oil painting of a cottage by a lake"
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.pickscore_predictor import PickScorePredictor

        predictor = PickScorePredictor()
        score = predictor.evaluate_pickscore(
            image_or_folder="sample.png",
            prompt="a photorealistic oil painting of a cottage by a lake"
        )
        print(f"PickScore: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Directory Batch Evaluation

    Evaluate an entire directory against a prompt:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics pickscore \\
            --image path/to/images_dir/ \\
            --prompt "cinematic lighting portrait of an elderly wizard"
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.pickscore_predictor import PickScorePredictor

        predictor = PickScorePredictor()
        mean_score = predictor.evaluate_pickscore(
            image_or_folder="path/to/images_dir/",
            prompt="cinematic lighting portrait of an elderly wizard"
        )
        print(f"Mean PickScore: {mean_score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

save("preference/pickscore.zh.mdx", """---
title: PickScore (真实偏好对齐)
description: 基于真实人类成对偏好反馈微调的生成质量打分
---

# PickScore (真实偏好对齐)

PickScore 由 Yuval Kirstain 等人于 NeurIPS 2023 提出。与传统的 CLIP 仅仅关注文本关键词是否在画面中出现不同，PickScore 基于大规模真实人类选择数据集 Pick-a-Pic（包含超过 50 万条人类在真实文生图应用中两两比对的选择记录），微调自 OpenCLIP `ViT-H-14`，能够敏锐捕捉人类真实审美喜好、负面瑕疵厌恶以及构图完整性。

---

## 核心规格与指标特性

| 参数维度 | 规范与技术事实 |
| :--- | :--- |
| **命令行参数** | `--metrics pickscore` |
| **输入约束** | 必须同时提供 `--image` 与 `--prompt`（文本或文件） |
| **输出形式** | 连续标量浮点数 |
| **数值导向** | **越高越优**（分值越高代表越贴近人类大众在相同提示词下的主流偏好） |
| **微调骨干** | `yuvalkirstain/PickScore_v1`（OpenCLIP `ViT-H-14` 大规模微调模型） |
| **核心优势** | 深度捕捉画面微观伪影、过饱和失真与光影不合理，避免指标“刷分假象” |

---

## 数学原理与计算形式

给定提示词 $y$ 与生成候选图 $x$，PickScore 计算归一化特征余弦相似度作为偏好对数几率（Logit）：

```math
s(x, y) = \\cos(\\Phi_{\\text{visual}}(x), \\Phi_{\\text{text}}(y))
```

在两张候选生成图 $x_1$ 与 $x_2$ 之间，人类偏好 $x_1$ 的概率服从 Bradley-Terry 模型：

```math
P(x_1 \\succ x_2 \\mid y) = \\frac{\\exp(s(x_1, y) / \\tau)}{\\exp(s(x_1, y) / \\tau) + \\exp(s(x_2, y) / \\tau)}
```

---

## 调用范例 (CLI 与 Python API)

<Steps>
  <Step>
    ### 单图人类偏好打分

    评估单幅图像是否符合人类主观审美偏好：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics pickscore \\
            --image sample.png \\
            --prompt "a photorealistic oil painting of a cottage by a lake"
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.pickscore_predictor import PickScorePredictor

        predictor = PickScorePredictor()
        score = predictor.evaluate_pickscore(
            image_or_folder="sample.png",
            prompt="a photorealistic oil painting of a cottage by a lake"
        )
        print(f"PickScore 偏好得分: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### 目录批量偏好评测

    对图库执行批量偏好打分并返回算术均值：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics pickscore \\
            --image path/to/images_dir/ \\
            --prompt "cinematic lighting portrait of an elderly wizard"
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.pickscore_predictor import PickScorePredictor

        predictor = PickScorePredictor()
        mean_score = predictor.evaluate_pickscore(
            image_or_folder="path/to/images_dir/",
            prompt="cinematic lighting portrait of an elderly wizard"
        )
        print(f"平均 PickScore: {mean_score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

# ==============================================================================
# BENCHMARK: VISUAL-DEMO
# ==============================================================================
save("benchmark/visual-demo.mdx", """---
title: Visual Benchmark (Interactive Demo)
description: Interactive multi-metric dashboard and dual-image slider comparative inspection
---

# Visual Benchmark (Interactive Demo)

This interactive evaluation benchmark demonstrates how different metric layers respond across three representative generative scenarios: **severe perceptual distortion**, **global warm color tint shift**, and **high-resolution portrait localized editing**. Use the slider or side-by-side view to visually inspect localized differences and compare metric scores.

---

## Interactive Metric Showcase

<MetricVisualShowcase />

---

## Architectural Complementarity

1. **LPIPS (Perceptual Deep Feature Layer)**: Highly robust against global uniform tint or minor sub-pixel shifts, but fires an alarm upon textural destruction or geometric contour tears.
2. **SSIM (Structural Statistical Layer)**: Evaluates local covariance across an $11 \\times 11$ window. Highly sensitive to contour blurs and edge artifacts.
3. **PSNR (Physical Pixel Layer)**: Evaluates absolute mean squared error on pixel intensity. Highly sensitive to subtle global luminance shifts.
""")

save("benchmark/visual-demo.zh.mdx", """---
title: Visual Benchmark (实测演练)
description: 交互式多维指标看板与双图对比实测
---

# Visual Benchmark (实测演练)

本演练中心通过真实算法生成的代表性图像样本，提供可交互的双图拖拽滑块与并排比对能力，将抽象的多维评估分值转化为直观的视觉差异。通过深入剖析不同失真场景下的指标反馈，揭示多尺度、多模态评估体系的互补机制与工程约束。

---

## 交互式多维指标看板

以下交互看板汇集了三个典型评测场景：**局部结构位移与严重感知失真**、**全局暖色温色偏与学术互补实证**以及**真实高清人脸局部微调多模态全景评测**。您可以通过滑块拖拽或切换并排视图，直观探查图像局部差异与指标得分。

<MetricVisualShowcase />

---

## 指标互补性机理与判决权衡

1. **LPIPS (深度特征感知层)**: 对全局均匀微色偏或亚像素微移具备极强稳健性，但在画面出现局部纹理破坏、边缘撕裂或几何形变时会产生高灵敏度响应。
2. **SSIM (中观结构统计层)**: 通过高斯滑动窗口捕获局部结构协方差，对轮廓模糊与边缘退化高度敏感。
3. **PSNR (底层物理像素层)**: 基于逐像素均方误差，对全局光照平移极其敏感，是衡量数值无损重构精度的基底底线。
""")

print("All metrics docs generated successfully!")
