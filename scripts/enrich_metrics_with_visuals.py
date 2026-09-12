import os

docs_dir = "content/docs"

def update_file(rel_path, content):
    full_path = os.path.join(docs_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n\n")
    print(f"Updated: {full_path}")

# ==============================================================================
# 2. TEXT-IMAGE: CLIP
# ==============================================================================
update_file("text-image/clip.mdx", """---
title: CLIP Score
description: Text-to-image cross-modal semantic cosine alignment using CLIP ViT-B/32
---

# CLIP Score

CLIP Score by Hessel et al. (EMNLP 2021) evaluates the semantic consistency between a synthetic image and its descriptive text prompt. By projecting both text tokens and visual patches into a joint multimodal embedding space via `clip-vit-base-patch32`, it computes cosine similarity calibrated to $[0, 100]$.

---

## Benchmark Diagnostic Scale

<MetricScale
  min={0.0}
  max={100.0}
  unit=" pts"
  direction="higher"
  segments={[
    { label: "High Alignment", range: [28.0, 100.0], color: "emerald", note: "Strong adherence to prompt concepts & styles" },
    { label: "Moderate Match", range: [20.0, 28.0], color: "amber", note: "Core subject present, attributes may drift" },
    { label: "Semantic Mismatch", range: [0.0, 20.0], color: "rose", note: "Missing primary objects or hallucinated content" }
  ]}
/>

---

## Parameter Contract

<TypeTable
  type={{
    "--metrics": {
      type: "string",
      description: "Must include 'clip'.",
      default: "required"
    },
    "--image": {
      type: "string (path)",
      description: "Path to input image file or directory of images.",
      default: "required"
    },
    "--prompt": {
      type: "string",
      description: "Text prompt string (or path to text file containing prompt).",
      default: "required"
    },
    "--reference": {
      type: "string",
      description: "Not allowed for CLIP evaluation.",
      default: "none"
    }
  }}
/>

---

## Mathematical Formulation

Given an image $I$ and prompt text $T$, the image encoder $\\mathbf{E}_I$ and text encoder $\\mathbf{E}_T$ produce $L_2$-normalized embeddings. The score is computed as:

```math
\\text{CLIP}(I, T) = \\max\\left( 100 \\cdot \\cos(\\mathbf{e}_I, \\mathbf{e}_T), 0 \\right) = 100 \\cdot \\max\\left( \\frac{\\mathbf{E}_I(I) \\cdot \\mathbf{E}_T(T)}{\\|\\mathbf{E}_I(I)\\|_2 \\|\\mathbf{E}_T(T)\\|_2}, 0 \\right)
```

Values scale in $[0.0, 100.0]$, where higher scores indicate stronger semantic compliance.

---

## Usage Examples

<Steps>
  <Step>
    ### Single Image Evaluation

    Evaluate text adherence for a single generated image:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics clip \
            --image path/to/sample.png \
            --prompt "an astronaut riding a horse on mars"
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.clip_score_predictor import ClipScorePredictor

        predictor = ClipScorePredictor()
        score = predictor.evaluate_clip_score(
            image_path="path/to/sample.png",
            prompt="an astronaut riding a horse on mars"
        )
        print(f"CLIP Score: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Folder Evaluation Against Shared Prompt

    Evaluate all images in a folder against a single benchmark prompt:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics clip \
            --image path/to/folder/ \
            --prompt "photorealistic portrait of a cyberpunk detective"
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.clip_score_predictor import ClipScorePredictor

        predictor = ClipScorePredictor()
        mean_score = predictor.evaluate_folder_clip_score(
            folder_path="path/to/folder/",
            prompt="photorealistic portrait of a cyberpunk detective"
        )
        print(f"Mean CLIP Score: {mean_score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

update_file("text-image/clip.zh.mdx", """---
title: CLIP Score (图文语义对齐)
description: 基于 CLIP ViT-B/32 多模态联合嵌入空间的文本与图像余弦相似度评测
---

# CLIP Score (图文语义对齐)

CLIP Score (Hessel et al., EMNLP 2021) 用于评估生成图像与输入文本提示词（Prompt）之间的跨模态语义吻合度。该指标通过 `clip-vit-base-patch32` 将文本词元与图像像素映射至对齐的多模态超球面，计算余弦相似度并缩放至 $[0, 100]$ 区间。

---

## 指标诊断区间标尺

<MetricScale
  min={0.0}
  max={100.0}
  unit=" 分"
  direction="higher"
  segments={[
    { label: "高度语义遵从", range: [28.0, 100.0], color: "emerald", note: "准确呈现提示词描述的核心主体、修饰属性与风格" },
    { label: "中度语义关联", range: [20.0, 28.0], color: "amber", note: "出现主要对象，但存在属性漂移或细节漏生成" },
    { label: "严重图文失配", range: [0.0, 20.0], color: "rose", note: "主体遗漏、虚假幻觉或严重语义偏离" }
  ]}
/>

---

## 接口参数契约

<TypeTable
  type={{
    "--metrics": {
      type: "string",
      description: "声明评测指标，必须包含 'clip'。",
      default: "必填"
    },
    "--image": {
      type: "string (路径)",
      description: "待评估图片文件路径或目录。",
      default: "必填"
    },
    "--prompt": {
      type: "string",
      description: "用于对齐比对的文本提示词字符串或包含提示词的文本文件路径。",
      default: "必填"
    },
    "--reference": {
      type: "string",
      description: "图文对齐不依赖配对参考底图，禁止传入。",
      default: "禁止"
    }
  }}
/>

---

## 理论公式推导

给定图像 $I$ 与文本提示词 $T$，图像编码器 $\\mathbf{E}_I$ 与文本编码器 $\\mathbf{E}_T$ 提取单位超球面上的 $L_2$ 归一化向量：

```math
\\text{CLIP}(I, T) = 100 \\cdot \\max\\left( \\frac{\\mathbf{E}_I(I) \\cdot \\mathbf{E}_T(T)}{\\|\\mathbf{E}_I(I)\\|_2 \\|\\mathbf{E}_T(T)\\|_2}, 0 \\right)
```

分值范围在 $[0.0, 100.0]$ 之间，分值越高表明生成图像越贴合提示词的语义描述。

---

## 调用示例

<Steps>
  <Step>
    ### 单张图像图文语义评估

    计算单张图片对提示词的遵从得分：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics clip \
            --image path/to/sample.png \
            --prompt "an astronaut riding a horse on mars"
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.clip_score_predictor import ClipScorePredictor

        predictor = ClipScorePredictor()
        score = predictor.evaluate_clip_score(
            image_path="path/to/sample.png",
            prompt="an astronaut riding a horse on mars"
        )
        print(f"CLIP 图文对齐分: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### 目录批量图文对齐评估

    针对整个生成图库批量计算同一基准提示词的平均对齐分：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics clip \
            --image path/to/folder/ \
            --prompt "photorealistic portrait of a cyberpunk detective"
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.clip_score_predictor import ClipScorePredictor

        predictor = ClipScorePredictor()
        mean_score = predictor.evaluate_folder_clip_score(
            folder_path="path/to/folder/",
            prompt="photorealistic portrait of a cyberpunk detective"
        )
        print(f"平均 CLIP 图文对齐分: {mean_score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

# ==============================================================================
# 3. TEXT-IMAGE: PICKSCORE
# ==============================================================================
update_file("text-image/pickscore.mdx", """---
title: PickScore
description: Fine-tuned CLIP ViT-H-14 human preference reward scoring trained on the Pick-a-Pic benchmark
---

# PickScore

PickScore by Kirstain et al. (NeurIPS 2023) evaluates text-to-image synthesis quality against human subjective preferences. While standard CLIP evaluates objective semantic similarity, PickScore is fine-tuned on over 500,000 empirical human choices from the Pick-a-Pic dataset (`yuvalkirstain/PickScore_v1`), predicting which synthetic generation humans prefer.

---

## Benchmark Diagnostic Scale

<MetricScale
  min={10.0}
  max={30.0}
  unit=" logit"
  direction="higher"
  segments={[
    { label: "Top-Tier Choice", range: [21.0, 30.0], color: "emerald", note: "Strong human preference & high generation appeal" },
    { label: "Standard Quality", range: [17.0, 21.0], color: "amber", note: "Typical baseline generative outputs" },
    { label: "Human Dislike", range: [10.0, 17.0], color: "rose", note: "Obvious anatomy flaws, blur, or prompt deviation" }
  ]}
/>

---

## Parameter Contract

<TypeTable
  type={{
    "--metrics": {
      type: "string",
      description: "Must include 'pickscore'.",
      default: "required"
    },
    "--image": {
      type: "string (path)",
      description: "Path to input image file or directory of images.",
      default: "required"
    },
    "--prompt": {
      type: "string",
      description: "Required text prompt describing the image generation context.",
      default: "required"
    },
    "--reference": {
      type: "string",
      description: "Not allowed for PickScore evaluation.",
      default: "none"
    }
  }}
/>

---

## Mathematical Formulation

PickScore projects image $I$ and prompt $T$ through fine-tuned CLIP ViT-H-14 encoders into normalized 1024-dimensional space, computing a temperature-calibrated softmax preference logit:

```math
s_{\\text{pick}} = 100 \\cdot \\frac{\\Phi_{\\text{image}}(I) \\cdot \\Phi_{\\text{text}}(T)}{\\|\\Phi_{\\text{image}}(I)\\|_2 \\|\\Phi_{\\text{text}}(T)\\|_2}
```

On empirical test sets, real outputs typically score in $[15.0, 25.0]$. Higher values indicate stronger alignment with human aesthetic choices.

---

## Usage Examples

<Steps>
  <Step>
    ### Single Image Evaluation

    Score human aesthetic preference against a target prompt:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics pickscore \
            --image path/to/sample.png \
            --prompt "an oil painting of a cottage in the woods at twilight"
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.pickscore_predictor import PickScorePredictor

        predictor = PickScorePredictor()
        score = predictor.evaluate_pickscore(
            image_path="path/to/sample.png",
            prompt="an oil painting of a cottage in the woods at twilight"
        )
        print(f"PickScore Preference: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Comparative Candidate Ranking

    Compare multiple generated candidates to determine which one humans are most likely to select:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics pickscore \
            --image path/to/candidate_folder/ \
            --prompt "portrait of an ancient warrior, detailed cinematic lighting"
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.pickscore_predictor import PickScorePredictor

        predictor = PickScorePredictor()
        mean_score = predictor.evaluate_folder_pickscore(
            folder_path="path/to/candidate_folder/",
            prompt="portrait of an ancient warrior, detailed cinematic lighting"
        )
        print(f"Mean Candidate PickScore: {mean_score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

update_file("text-image/pickscore.zh.mdx", """---
title: PickScore (人类审美偏好对齐)
description: 基于 Pick-a-Pic 真实人类成对反馈数据集微调的 CLIP ViT-H-14 偏好奖励打分模型
---

# PickScore (人类审美偏好对齐)

PickScore (Kirstain et al., NeurIPS 2023) 专门用于评测文本生成图像在人类主观审美维度下的偏好程度。常规 CLIP 衡量的是客观图文特征几何距离，而 PickScore 在包含超 50 万条真实人类二选一打分数据的 Pick-a-Pic 数据集 (`yuvalkirstain/PickScore_v1`) 上进行了深度微调，能够直接预测人类评委更倾向选择哪张生成结果。

---

## 指标诊断区间标尺

<MetricScale
  min={10.0}
  max={30.0}
  unit=" 分 (Logit)"
  direction="higher"
  segments={[
    { label: "极高人类偏好", range: [21.0, 30.0], color: "emerald", note: "高度符合人类审美、构图出众、无明显形变瑕疵" },
    { label: "中位基准生成", range: [17.0, 21.0], color: "amber", note: "标准扩散模型平均表现，符合提示词但质感普通" },
    { label: "人类明显倾向淘汰", range: [10.0, 17.0], color: "rose", note: "肢体崩坏、语义偏离、画面噪点或光影严重失真" }
  ]}
/>

---

## 接口参数契约

<TypeTable
  type={{
    "--metrics": {
      type: "string",
      description: "声明评测指标，必须包含 'pickscore'。",
      default: "必填"
    },
    "--image": {
      type: "string (路径)",
      description: "待评测图片路径或候选图片文件夹路径。",
      default: "必填"
    },
    "--prompt": {
      type: "string",
      description: "生成该图像所依据的文本提示词，必填。",
      default: "必填"
    },
    "--reference": {
      type: "string",
      description: "人类偏好模型直接评估 (Image, Prompt)，禁止传入参考底图。",
      default: "禁止"
    }
  }}
/>

---

## 理论公式推导

PickScore 使用经过人类反馈微调的 ViT-H-14 编码器，分别提取图像特征 $\\Phi_{\\text{image}}(I)$ 与文本特征 $\\Phi_{\\text{text}}(T)$，计算带温度缩放的对数几率评分：

```math
s_{\\text{pick}} = 100 \\cdot \\frac{\\Phi_{\\text{image}}(I) \\cdot \\Phi_{\\text{text}}(T)}{\\|\\Phi_{\\text{image}}(I)\\|_2 \\|\\Phi_{\\text{text}}(T)\\|_2}
```

在主流生成测试集上，分值主要集中在 $[15.0, 25.0]$ 范围。数值越大，代表人类评测者偏好该生成图像的概率越高。

---

## 调用示例

<Steps>
  <Step>
    ### 单张图像人类偏好评分

    评估单张生成样本与提示词的人类偏好对齐度：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics pickscore \
            --image path/to/sample.png \
            --prompt "an oil painting of a cottage in the woods at twilight"
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.pickscore_predictor import PickScorePredictor

        predictor = PickScorePredictor()
        score = predictor.evaluate_pickscore(
            image_path="path/to/sample.png",
            prompt="an oil painting of a cottage in the woods at twilight"
        )
        print(f"PickScore 人类偏好分: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### 候选生成图库择优评测

    批量计算候选生成图集的偏好得分以进行择优排序：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics pickscore \
            --image path/to/candidate_folder/ \
            --prompt "portrait of an ancient warrior, detailed cinematic lighting"
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.pickscore_predictor import PickScorePredictor

        predictor = PickScorePredictor()
        mean_score = predictor.evaluate_folder_pickscore(
            folder_path="path/to/candidate_folder/",
            prompt="portrait of an ancient warrior, detailed cinematic lighting"
        )
        print(f"候选集平均 PickScore: {mean_score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

# ==============================================================================
# 4. PAIRWISE: LPIPS
# ==============================================================================
update_file("pairwise/lpips.mdx", """---
title: LPIPS (Perceptual Distance)
description: Learned Perceptual Image Patch Similarity using AlexNet multi-scale deep features
---

# LPIPS (Perceptual Distance)

Learned Perceptual Image Patch Similarity (LPIPS) by Zhang et al. (CVPR 2018) evaluates perceptual fidelity across generated and reference images. By extracting multi-scale activations from a deep neural network and applying learned channel weights, it correlates strongly with human subjective judgments of image similarity.

---

## Benchmark Diagnostic Scale

<MetricScale
  min={0.0}
  max={1.0}
  unit=""
  direction="lower"
  segments={[
    { label: "High Fidelity", range: [0.0, 0.15], color: "emerald", note: "Imperceptible perceptual difference against reference" },
    { label: "Moderate Drift", range: [0.15, 0.35], color: "amber", note: "Noticeable style, texture, or fine detail shift" },
    { label: "Heavy Distortion", range: [0.35, 1.0], color: "rose", note: "Severe structural corruption or semantic divergence" }
  ]}
/>

---

## Parameter Contract

<TypeTable
  type={{
    "--metrics": {
      type: "string",
      description: "Must include 'lpips'.",
      default: "required"
    },
    "--image": {
      type: "string (path)",
      description: "Path to generated image file or folder.",
      default: "required"
    },
    "--reference": {
      type: "string (path)",
      description: "Path to ground-truth reference image file or folder.",
      default: "required"
    },
    "--prompt": {
      type: "string",
      description: "Not allowed for pairwise image fidelity.",
      default: "none"
    }
  }}
/>

<Callout type="warn">
  **Spatial Dimension Contract**: LPIPS strictly enforces that input pairs share identical dimensions ($H_{\\text{ref}} = H_{\\text{gen}}$ and $W_{\\text{ref}} = W_{\\text{gen}}$). The library strictly raises `ValueError` on size mismatch to prevent high-frequency interpolation artifacts.
</Callout>

---

## Mathematical Formulation

LPIPS extracts feature activations across $L$ layers from reference $x$ and generated $x_0$. Within each layer $l$, feature channels are normalized by $L_2$ norm, scaled by learned vector $w_l$, and spatially averaged:

```math
d(x, x_0) = \\sum_l \\frac{1}{H_l W_l} \\sum_{h, w} \\left\\| w_l \\odot \\left( \\hat{y}^l_{hw} - \\hat{y}_{0, hw}^l \\right) \\right\\|_2^2
```

---

## Usage Examples

<Steps>
  <Step>
    ### Single Pair Evaluation

    Measure deep perceptual distance between a generated sample and ground truth:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics lpips \
            --reference path/to/reference.png \
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
        image-evaluator --metrics lpips \
            --reference path/to/reference_folder/ \
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

update_file("pairwise/lpips.zh.mdx", """---
title: LPIPS (深度感知距离)
description: 基于 AlexNet 多尺度深层激活特征的感知相似度度量
---

# LPIPS (深度感知距离)

LPIPS (Zhang et al., CVPR 2018) 是一种利用深度神经网络隐藏层激活值评估图像感知保真度的经典指标。传统的像素级比较（如 MSE、PSNR）极易受到轻微空间位移和全局色温偏移的干扰，而 LPIPS 能够准确捕捉高层纹理与结构语义，与人类主观感知具有极强的一致性。

---

## 指标诊断区间标尺

<MetricScale
  min={0.0}
  max={1.0}
  unit=""
  direction="lower"
  segments={[
    { label: "极高感知保真", range: [0.0, 0.15], color: "emerald", note: "人眼几乎无法察觉生成图与原图的质感差异" },
    { label: "中度风格漂移", range: [0.15, 0.35], color: "amber", note: "肉眼可见轻微色调、微观纹理或细节平滑" },
    { label: "严重感知劣变", range: [0.35, 1.0], color: "rose", note: "轮廓破坏、结构撕裂或伪影大面积扩散" }
  ]}
/>

---

## 接口参数契约

<TypeTable
  type={{
    "--metrics": {
      type: "string",
      description: "声明评测指标，必须包含 'lpips'。",
      default: "必填"
    },
    "--image": {
      type: "string (路径)",
      description: "待测生成图像文件或目录路径。",
      default: "必填"
    },
    "--reference": {
      type: "string (路径)",
      description: "作为对照基准的真实参考图像文件或目录路径。",
      default: "必填"
    },
    "--prompt": {
      type: "string",
      description: "成对保真度评测不涉及提示词，禁止传入。",
      default: "禁止"
    }
  }}
/>

<Callout type="warn">
  **空间尺寸绝对一致原则**：成对评测严格要求两张输入图像的长宽尺寸完全匹配 ($H_{\\text{ref}} = H_{\\text{gen}}$ 且 $W_{\\text{ref}} = W_{\\text{gen}}$)。底层拒绝执行隐式双线性插值，遇到尺寸不匹配时直接抛出 `ValueError`，以杜绝重采样引入的高频伪影污染。
</Callout>

---

## 理论公式推导

LPIPS 从参考图 $x$ 与生成图 $x_0$ 的 $L$ 个深度网络层中提取特征，在每一层 $l$ 内对通道向量执行 $L_2$ 归一化，乘以经过人类打分标定的可学习通道权重 $w_l$，并计算空间均方误差均值：

```math
d(x, x_0) = \\sum_l \\frac{1}{H_l W_l} \\sum_{h, w} \\left\\| w_l \\odot \\left( \\hat{y}^l_{hw} - \\hat{y}_{0, hw}^l \\right) \\right\\|_2^2
```

取值越接近 $0.0$，代表两张图像的深层感知特征越趋于一致。

---

## 调用示例

<Steps>
  <Step>
    ### 单对图像感知距离评估

    比较单张生成图像相对原图的感知距离：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics lpips \
            --reference path/to/reference.png \
            --image path/to/generated.png
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.lpips_predictor import LPIPSPredictor

        predictor = LPIPSPredictor()
        distance = predictor.evaluate_lpips(
            reference_path="path/to/reference.png",
            generated_path="path/to/generated.png"
        )
        print(f"LPIPS 感知距离: {distance:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### 目录批量配对评测

    批量计算两组配对目录的平均感知距离：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics lpips \
            --reference path/to/reference_folder/ \
            --image path/to/generated_folder/
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.lpips_predictor import LPIPSPredictor

        predictor = LPIPSPredictor()
        mean_dist = predictor.evaluate_folder_lpips(
            reference_folder="path/to/reference_folder/",
            generated_folder="path/to/generated_folder/"
        )
        print(f"平均 LPIPS 距离: {mean_dist:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

# ==============================================================================
# 5. PAIRWISE: ARCFACE
# ==============================================================================
update_file("pairwise/arcface.mdx", """---
title: ArcFace Distance
description: Facial identity preservation using InsightFace buffalo_l 512-dimensional cosine feature distance
---

# ArcFace Distance

ArcFace Distance (Deng et al., CVPR 2019) measures facial identity consistency between a generated portrait and a reference photo. By extracting 512-dimensional deep facial embeddings using InsightFace (`buffalo_l`), it computes normalized cosine feature distance. This is the gold-standard metric for evaluating identity retention in LoRA, InstantID, PhotoMaker, and DreamBooth personalized generation.

---

## Benchmark Diagnostic Scale

<MetricScale
  min={0.0}
  max={2.0}
  unit=""
  direction="lower"
  segments={[
    { label: "Same Identity", range: [0.0, 0.40], color: "emerald", note: "High identity retention (InstantID / LoRA verification standard)" },
    { label: "Ambiguous Drift", range: [0.40, 0.60], color: "amber", note: "Facial expression or lighting causing boundary drift" },
    { label: "Different Identity", range: [0.60, 2.0], color: "rose", note: "Identity lost or incorrect biometric features" }
  ]}
/>

---

## Parameter Contract

<TypeTable
  type={{
    "--metrics": {
      type: "string",
      description: "Must include 'arcface'.",
      default: "required"
    },
    "--image": {
      type: "string (path)",
      description: "Path to generated facial image or folder.",
      default: "required"
    },
    "--reference": {
      type: "string (path)",
      description: "Path to reference ground-truth facial image or folder.",
      default: "required"
    },
    "--prompt": {
      type: "string",
      description: "Not allowed for facial identity evaluation.",
      default: "none"
    }
  }}
/>

<Callout type="warn">
  **Face Detection Prerequisite**: ArcFace requires successful face detection in **both** the reference and generated images via InsightFace RetinaFace (`buffalo_l`). If no face is detected in either image, the metric returns `None`.
</Callout>

---

## Mathematical Formulation

The cosine distance between $L_2$-normalized 512-dimensional face embeddings $\\mathbf{f}_1$ and $\\mathbf{f}_2$ is defined as:

```math
\\text{Distance}(\\mathbf{f}_1, \\mathbf{f}_2) = 1 - \\frac{\\mathbf{f}_1 \\cdot \\mathbf{f}_2}{\\|\\mathbf{f}_1\\|_2 \\|\\mathbf{f}_2\\|_2}
```

Scale ranges in $[0.0, 2.0]$, where lower values indicate stronger facial resemblance ($0.0$ denotes exact mathematical identity).

---

## Usage Examples

<Steps>
  <Step>
    ### Single Pair Face Identity Evaluation

    Compare facial identity retention between generated output and real photo:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics arcface \
            --reference path/to/reference_face.png \
            --image path/to/generated_face.png
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.arcface_dist_predictor import ArcFaceDistPredictor

        predictor = ArcFaceDistPredictor()
        distance = predictor.evaluate_arcface(
            reference_path="path/to/reference_face.png",
            generated_path="path/to/generated_face.png"
        )
        print(f"ArcFace Distance: {distance:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Personalized Generation Benchmark

    Batch evaluate personalization testsets across folders:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics arcface \
            --reference path/to/reference_faces/ \
            --image path/to/generated_faces/
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.arcface_dist_predictor import ArcFaceDistPredictor

        predictor = ArcFaceDistPredictor()
        mean_dist = predictor.evaluate_folder_arcface(
            reference_folder="path/to/reference_faces/",
            generated_folder="path/to/generated_faces/"
        )
        print(f"Mean Face Distance: {mean_dist:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

update_file("pairwise/arcface.zh.mdx", """---
title: ArcFace (主体人脸一致性)
description: 基于 InsightFace buffalo_l 512 维特征余弦距离的人脸主体身份保持度评测
---

# ArcFace (主体人脸一致性)

ArcFace 人脸距离 (Deng et al., CVPR 2019) 用于度量生成人像与真实人物参考照之间的人脸生物特征一致性。通过 InsightFace (`buffalo_l`) 骨干网络提取主面部 512 维深度人脸嵌入特征，计算其余弦特征距离。该指标是评估 InstantID、PhotoMaker、LoRA 与 DreamBooth 等个性化人脸保持算法的核心度量工具。

---

## 指标诊断区间标尺

<MetricScale
  min={0.0}
  max={2.0}
  unit=""
  direction="lower"
  segments={[
    { label: "同一人物确认", range: [0.0, 0.40], color: "emerald", note: "人脸身份高度保持（主流 LoRA 与 InstantID 达标门槛）" },
    { label: "疑似身份漂移", range: [0.40, 0.60], color: "amber", note: "表情剧烈变化、光照干扰或五官存在模糊漂移" },
    { label: "不同人物判定", range: [0.60, 2.0], color: "rose", note: "人脸特征丢失，判定为完全不同的人物面孔" }
  ]}
/>

---

## 接口参数契约

<TypeTable
  type={{
    "--metrics": {
      type: "string",
      description: "声明评测指标，必须包含 'arcface'。",
      default: "必填"
    },
    "--image": {
      type: "string (路径)",
      description: "待测生成人像图片文件或目录路径。",
      default: "必填"
    },
    "--reference": {
      type: "string (路径)",
      description: "真实人物参考原图文件或目录路径。",
      default: "必填"
    },
    "--prompt": {
      type: "string",
      description: "人脸身份比对基于两图特征，禁止传入提示词。",
      default: "禁止"
    }
  }}
/>

<Callout type="warn">
  **人脸前置检测门禁**：ArcFace 必须在参考图与生成图中均成功检测到人脸（基于 RetinaFace 模型）。若任一图片未检测到人脸或置信度不足，该测试对将返回 `None`。
</Callout>

---

## 理论公式推导

两个 $L_2$ 归一化的 512 维人脸特征向量 $\\mathbf{f}_1$ 与 $\\mathbf{f}_2$ 之间的余弦距离定义为：

```math
\\text{Distance}(\\mathbf{f}_1, \\mathbf{f}_2) = 1 - \\frac{\\mathbf{f}_1 \\cdot \\mathbf{f}_2}{\\|\\mathbf{f}_1\\|_2 \\|\\mathbf{f}_2\\|_2}
```

取值范围为 $[0.0, 2.0]$，分值越低代表面部五官生物特征越相似。

---

## 调用示例

<Steps>
  <Step>
    ### 单对人脸身份保真度评估

    评估单张生成人像与人物原照的面部特征距离：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics arcface \
            --reference path/to/reference_face.png \
            --image path/to/generated_face.png
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.arcface_dist_predictor import ArcFaceDistPredictor

        predictor = ArcFaceDistPredictor()
        distance = predictor.evaluate_arcface(
            reference_path="path/to/reference_face.png",
            generated_path="path/to/generated_face.png"
        )
        print(f"ArcFace 人脸距离: {distance:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### 个性化人像批量测试

    批量评测微调模型在人物图库上的平均面孔一致性：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics arcface \
            --reference path/to/reference_faces/ \
            --image path/to/generated_faces/
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.arcface_dist_predictor import ArcFaceDistPredictor

        predictor = ArcFaceDistPredictor()
        mean_dist = predictor.evaluate_folder_arcface(
            reference_folder="path/to/reference_faces/",
            generated_folder="path/to/generated_faces/"
        )
        print(f"平均人脸距离: {mean_dist:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

# ==============================================================================
# 6. DISTRIBUTION: FID
# ==============================================================================
update_file("distribution/fid.mdx", """---
title: FID (Fréchet Inception Distance)
description: Generative distribution distance evaluated in Inception-v3 pool3 feature space
---

# FID (Fréchet Inception Distance)

Fréchet Inception Distance (Heusel et al., NeurIPS 2017) measures the statistical distance between a generated image distribution and a real-world dataset. By fitting multivariate Gaussians to the 2048-dimensional `pool3` features of an Inception-v3 network, it assesses both visual realism and sample diversity.

---

## Benchmark Diagnostic Scale

<MetricScale
  min={0.0}
  max={100.0}
  unit=""
  direction="lower"
  segments={[
    { label: "State of the Art", range: [0.0, 15.0], color: "emerald", note: "Commercial-grade diffusion realism & rich diversity" },
    { label: "Acceptable Realism", range: [15.0, 40.0], color: "amber", note: "Standard generative research baseline" },
    { label: "Mode Collapse", range: [40.0, 100.0], color: "rose", note: "Severe artifacts, blur, or severe loss of sample diversity" }
  ]}
/>

---

## Directory Layout Contract

FID requires directory inputs on both generated and reference sides. Unlike pairwise metrics, filenames do not need to match and sample counts may differ ($N_{\\text{ref}} \\neq N_{\\text{gen}}$):

<Files>
  <Folder name="real_dataset" defaultOpen>
    <File name="real_0001.png" />
    <File name="real_0002.png" />
    <File name="... (>= 2048 recommended)" />
  </Folder>
  <Folder name="generated_dataset" defaultOpen>
    <File name="synth_0001.png" />
    <File name="synth_0002.png" />
    <File name="... (>= 2048 recommended)" />
  </Folder>
</Files>

<Callout type="warn">
  **Sample Size Bias Warning**: FID is a biased estimator. Evaluating with small sample sizes ($N < 2048$) systematically overestimates the true distribution distance and triggers a runtime warning. For sample sizes under 2000, consider using the unbiased **KID** metric instead.
</Callout>

---

## Mathematical Formulation

The Wasserstein-2 distance between two multivariate Gaussians $(\\mu_r, \\Sigma_r)$ and $(\\mu_g, \\Sigma_g)$ is computed as:

```math
\\text{FID} = \\|\\mu_r - \\mu_g\\|_2^2 + \\text{Tr}\\left( \\Sigma_r + \\Sigma_g - 2\\left(\\Sigma_r \\Sigma_g\\right)^{1/2} \\right)
```

Lower values indicate closer fidelity and diversity to the ground-truth distribution.

---

## Usage Examples

<Steps>
  <Step>
    ### Dataset Distribution Evaluation

    Compute CleanFID between generated and ground-truth directories:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics fid \
            --reference path/to/real_images/ \
            --image path/to/generated_images/
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.fid_predictor import FIDPredictor

        predictor = FIDPredictor()
        score = predictor.evaluate_fid(
            reference_folder="path/to/real_images/",
            generated_folder="path/to/generated_images/"
        )
        print(f"CleanFID Score: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

update_file("distribution/fid.zh.mdx", """---
title: FID (弗雷歇距离)
description: 基于 Inception-v3 pool3 特征空间高斯二阶统计量的生成分布距离评测
---

# FID (弗雷歇距离)

弗雷歇 Inception 距离 (Heusel et al., NeurIPS 2017) 用于评估生成图片群体与真实图片数据集之间的整体统计分布差异。该指标将真实图集与生成图集分别输入 Inception-v3 网络提取 2048 维 `pool3` 深层特征，拟合多元高斯分布并计算 Wasserstein-2 统计距离，能够同时反映生成样本的保真度与多样性（防模式崩塌）。

---

## 指标诊断区间标尺

<MetricScale
  min={0.0}
  max={100.0}
  unit=""
  direction="lower"
  segments={[
    { label: "前沿生成质感", range: [0.0, 15.0], color: "emerald", note: "商业级生图质感、细节真实且分布覆盖多样" },
    { label: "标准基准水平", range: [15.0, 40.0], color: "amber", note: "学术研究标准 Baseline 表现" },
    { label: "模式崩塌或失真", range: [40.0, 100.0], color: "rose", note: "样本单一性严重、伪影频发或特征严重漂移" }
  ]}
/>

---

## 数据集目录组织规范

FID 评测必须传入两个已存在的文件夹目录。与成对指标不同，两边无需文件名配对，图片数量亦可不相等 ($N_{\\text{ref}} \\neq N_{\\text{gen}}$)：

<Files>
  <Folder name="real_dataset (真实参考库)" defaultOpen>
    <File name="real_0001.png" />
    <File name="real_0002.png" />
    <File name="... (建议 >= 2048 张)" />
  </Folder>
  <Folder name="generated_dataset (生成待测库)" defaultOpen>
    <File name="synth_0001.png" />
    <File name="synth_0002.png" />
    <File name="... (建议 >= 2048 张)" />
  </Folder>
</Files>

<Callout type="warn">
  **样本量有偏估计陷阱**：FID 属于有偏估计量，样本量过小 ($N < 2048$) 时会系统性虚高偏大，运行中会触发警告。当受测样本集小于 2000 张时，强烈建议使用无偏估计指标 **KID** 进行衡量。
</Callout>

---

## 理论公式推导

两个多元高斯分布 $(\\mu_r, \\Sigma_r)$ 与 $(\\mu_g, \\Sigma_g)$ 之间的弗雷歇距离公式为：

```math
\\text{FID} = \\|\\mu_r - \\mu_g\\|_2^2 + \\text{Tr}\\left( \\Sigma_r + \\Sigma_g - 2\\left(\\Sigma_r \\Sigma_g\\right)^{1/2} \\right)
```

分值越低，代表生成样本集的特征分布与真实样本集越接近。

---

## 调用示例

<Steps>
  <Step>
    ### 数据集群体分布距离计算

    计算生成图库与真实图库的 CleanFID 分值：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics fid \
            --reference path/to/real_images/ \
            --image path/to/generated_images/
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.fid_predictor import FIDPredictor

        predictor = FIDPredictor()
        score = predictor.evaluate_fid(
            reference_folder="path/to/real_images/",
            generated_folder="path/to/generated_images/"
        )
        print(f"CleanFID 分布距离: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

# ==============================================================================
# 7. DISTRIBUTION: KID
# ==============================================================================
update_file("distribution/kid.mdx", """---
title: KID (Kernel Inception Distance)
description: Unbiased polynomial kernel maximum mean discrepancy (MMD) in Inception feature space
---

# KID (Kernel Inception Distance)

Kernel Inception Distance (Bińkowski et al., ICLR 2018) is an unbiased metric for evaluating generative image distributions. Unlike FID, which fits a parametric Gaussian distribution and suffers from heavy small-sample bias, KID computes the squared Maximum Mean Discrepancy (MMD) with a cubic polynomial kernel via a U-statistic, providing reliable evaluation on subsets of 1,000 images or fewer.

---

## Benchmark Diagnostic Scale

<MetricScale
  min={-0.005}
  max={0.08}
  unit=""
  direction="lower"
  segments={[
    { label: "Optimal Distribution", range: [-0.005, 0.005], color: "emerald", note: "Distribution shift near theoretical zero" },
    { label: "Acceptable Divergence", range: [0.005, 0.025], color: "amber", note: "Standard generative divergence" },
    { label: "Severe Mismatch", range: [0.025, 0.08], color: "rose", note: "High distribution discrepancy or mode failure" }
  ]}
/>

---

## Dataset Directory Layout

KID operates over directories of images. Like FID, filenames do not need to match and counts can differ:

<Files>
  <Folder name="reference_dir" defaultOpen>
    <File name="real_01.png" />
    <File name="... (100 - 1000 samples)" />
  </Folder>
  <Folder name="generated_dir" defaultOpen>
    <File name="gen_01.png" />
    <File name="... (100 - 1000 samples)" />
  </Folder>
</Files>

<Callout type="info">
  **Small-Sample Unbiasedness & Negative Values**: Because the U-statistic is an unbiased estimator of squared MMD, sample variance around zero can yield small negative values (e.g. `-0.0004`). These reflect unbiased statistical variance and must **never** be manually clamped to zero.
</Callout>

---

## Mathematical Formulation

KID computes MMD with a cubic polynomial kernel $k(x, y) = \\left(\\frac{1}{d} x^T y + 1\\right)^3$ across Inception feature representations:

```math
\\text{KID} = \\text{MMD}^2(P_r, P_g) = \\mathbb{E}[k(x, x')] + \\mathbb{E}[k(y, y')] - 2\\mathbb{E}[k(x, y)]
```

The evaluator returns the mean and standard deviation: $\\text{Mean} \\pm \\text{Std}$. Lower values reflect superior fidelity.

---

## Usage Examples

<Steps>
  <Step>
    ### Dataset Distribution Evaluation

    Compute unbiased KID between generated and reference folders:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics kid \
            --reference path/to/reference_dir/ \
            --image path/to/generated_dir/
        ```
      </Tab>
      <Tab value="Python API">
        ```python
        from image_evaluator.kid_predictor import KIDPredictor

        predictor = KIDPredictor()
        mean_kid, std_kid = predictor.evaluate_kid(
            reference_folder="path/to/reference_dir/",
            generated_folder="path/to/generated_dir/"
        )
        print(f"KID: {mean_kid:.6f} (+/- {std_kid:.6f})")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

update_file("distribution/kid.zh.mdx", """---
title: KID (核最大均值差异)
description: 基于 Inception 特征空间多项式核最大均值差异 (MMD) 的无偏生成分布距离
---

# KID (核最大均值差异)

核最大均值差异 (Bińkowski et al., ICLR 2018) 是一种面向生成式图像群体分布的无偏评测指标。相较于必须拟合多元高斯分布且严重依赖大样本量（易出现小样本虚高）的 FID，KID 基于三次多项式核并通过无偏 U 统计量计算分布的最大均值差异（MMD），在千张以内的小样本场景下依然保持客观稳定。

---

## 指标诊断区间标尺

<MetricScale
  min={-0.005}
  max={0.08}
  unit=""
  direction="lower"
  segments={[
    { label: "极佳分布吻合", range: [-0.005, 0.005], color: "emerald", note: "生成分布与真实分布在特征空间几无差异" },
    { label: "常规基准漂移", range: [0.005, 0.025], color: "amber", note: "日常模型迭代常见可接受分布偏差" },
    { label: "显著分布偏离", range: [0.025, 0.08], color: "rose", note: "高维特征分布明显失配，生成质感严重欠缺" }
  ]}
/>

---

## 数据集目录组织规范

KID 支持两个独立文件夹输入，两边无须保持文件名配对与张数一致：

<Files>
  <Folder name="reference_dir (真实对照集)" defaultOpen>
    <File name="real_01.png" />
    <File name="... (100 - 1000 张小样本)" />
  </Folder>
  <Folder name="generated_dir (生成测试集)" defaultOpen>
    <File name="gen_01.png" />
    <File name="... (100 - 1000 张小样本)" />
  </Folder>
</Files>

<Callout type="info">
  **小样本无偏性与负值原理**：由于无偏 U 统计量的数学性质，当两个分布极其接近（真实 MMD 为 0）时，有限样本抽样波动可能产生极小的负数（例如 `-0.0004`）。这属于无偏估计的正常统计方差现象，**严禁**强行截断为 0。
</Callout>

---

## 理论公式推导

KID 采用三次多项式核函数 $k(x, y) = \\left(\\frac{1}{d} x^T y + 1\\right)^3$ 衡量 Inception 特征空间距离：

```math
\\text{KID} = \\text{MMD}^2(P_r, P_g) = \\mathbb{E}[k(x, x')] + \\mathbb{E}[k(y, y')] - 2\\mathbb{E}[k(x, y)]
```

评测器输出均值与标准差 $\\text{Mean} \\pm \\text{Std}$。数值越低越优。

---

## 调用示例

<Steps>
  <Step>
    ### 小样本数据集分布评测

    计算生成图库与真实图库之间的无偏 KID 统计量：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics kid \
            --reference path/to/reference_dir/ \
            --image path/to/generated_dir/
        ```
      </Tab>
      <Tab value="Python API 代码">
        ```python
        from image_evaluator.kid_predictor import KIDPredictor

        predictor = KIDPredictor()
        mean_kid, std_kid = predictor.evaluate_kid(
            reference_folder="path/to/reference_dir/",
            generated_folder="path/to/generated_dir/"
        )
        print(f"KID: {mean_kid:.6f} (+/- {std_kid:.6f})")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
""")

