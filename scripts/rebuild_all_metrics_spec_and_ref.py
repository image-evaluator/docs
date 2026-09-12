import os

docs_dir = "content/docs"

def save(rel_path, content):
    full_path = os.path.join(docs_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n\n")
    print(f"Wrote: {full_path}")

# ==============================================================================
# CLIP
# ==============================================================================
save("text-image/clip.mdx", """---
title: CLIP Score
description: Text-to-image cross-modal semantic cosine alignment using CLIP ViT-B/32
---

# CLIP Score

CLIP Score by Hessel et al. (EMNLP 2021) evaluates the semantic consistency between a synthetic image and its descriptive text prompt. By projecting both text tokens and visual patches into a joint multimodal embedding space via `clip-vit-base-patch32`, it computes cosine similarity calibrated to $[0, 100]$.

---

## Technical Specifications

| Property | Specification |
| :--- | :--- |
| **Category** | Cross-Modal Text-to-Image Alignment |
| **CLI Metric** | `clip` |
| **Input Options** | `--image <file_or_dir>`, `--prompt "<text_or_file>"` (both required) |
| **Prohibited Options** | `--reference` (not applicable for text-to-image alignment) |
| **Output Scale** | Continuous scalar in `[0.0, 100.0]` |
| **Direction** | **Higher is better** |
| **Model Backbone** | OpenAI CLIP `clip-vit-base-patch32` |
| **Upstream Source** | [openai/CLIP](https://github.com/openai/CLIP) |

---

## Mathematical Formulation

Given an image $I$ and prompt text $T$, the image encoder $\\mathbf{E}_I$ and text encoder $\\mathbf{E}_T$ produce $L_2$-normalized embeddings. The score is computed as:

```math
\\text{CLIP}(I, T) = 100 \\cdot \\max\\left( \\frac{\\mathbf{E}_I(I) \\cdot \\mathbf{E}_T(T)}{\\|\\mathbf{E}_I(I)\\|_2 \\|\\mathbf{E}_T(T)\\|_2}, 0 \\right)
```

Values scale in $[0.0, 100.0]$, where higher scores indicate stronger semantic compliance.

---

## Interpretation & Guidance

- **Benchmark Scores**: Typical diffusion outputs (Stable Diffusion, Midjourney) on MS-COCO prompts score between $25.0$ and $33.0$. Scores above $30.0$ denote high semantic fidelity.
- **Lexical Overlap Sensitivity**: CLIP evaluates high-level visual semantic features. Negations (e.g. *"a cat without hat"*) and spatial relations (*"cube on top of cylinder"*) remain known challenge areas.
- **Combined Evaluation**: Pair with **PickScore** to measure both objective semantic alignment and subjective aesthetic preference.

---

## Usage Examples

<Steps>
  <Step>
    ### Single Image Evaluation

    Evaluate text adherence for a single generated image:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics clip \\
            --image path/to/sample.png \\
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
        image-evaluator --metrics clip \\
            --image path/to/folder/ \\
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

---

## References

- **Paper**: Hessel et al., 2021, *CLIPScore: A Reference-free Evaluation Metric for Image Captioning* (EMNLP 2021, [arXiv:2104.08718](https://arxiv.org/abs/2104.08718))
- **Model & Implementation**: [openai/CLIP](https://github.com/openai/CLIP)
- **Foundation Paper**: Radford et al., 2021, *Learning Transferable Visual Models From Natural Language Supervision* (ICML 2021, [arXiv:2103.00020](https://arxiv.org/abs/2103.00020))
""")

save("text-image/clip.zh.mdx", """---
title: CLIP Score (图文语义对齐)
description: 基于 CLIP ViT-B/32 多模态联合嵌入空间的文本与图像余弦相似度评测
---

# CLIP Score (图文语义对齐)

CLIP Score (Hessel et al., EMNLP 2021) 用于评估生成图像与输入文本提示词（Prompt）之间的跨模态语义吻合度。该指标通过 `clip-vit-base-patch32` 将文本词元与图像像素映射至对齐的多模态超球面，计算余弦相似度并缩放至 $[0, 100]$ 区间。

---

## 核心规格

| 属性 | 规范定义 |
| :--- | :--- |
| **评测体系** | 跨模态图文对齐 (Text-to-Image Alignment) |
| **命令行参数** | `--metrics clip` |
| **输入要求** | `--image <图片或目录>`, `--prompt "<文本或文件>"` (两项皆必填) |
| **禁止参数** | `--reference` (图文评测禁止传入参考图) |
| **标度范围** | 连续浮点数 `[0.0, 100.0]` |
| **取值方向** | **数值越高越优** |
| **骨干网络** | OpenAI CLIP `clip-vit-base-patch32` |
| **权威源** | [openai/CLIP](https://github.com/openai/CLIP) |

---

## 理论公式推导

给定图像 $I$ 与文本提示词 $T$，图像编码器 $\\mathbf{E}_I$ 与文本编码器 $\\mathbf{E}_T$ 提取单位超球面上的 $L_2$ 归一化向量：

```math
\\text{CLIP}(I, T) = 100 \\cdot \\max\\left( \\frac{\\mathbf{E}_I(I) \\cdot \\mathbf{E}_T(T)}{\\|\\mathbf{E}_I(I)\\|_2 \\|\\mathbf{E}_T(T)\\|_2}, 0 \\right)
```

分值范围在 $[0.0, 100.0]$ 之间，分值越高表明生成图像越贴合提示词的语义描述。

---

## 评测阈值与解读建议

- **常见基准分布**：主流扩散模型（如 SD 1.5、SDXL、Midjourney）在 MS-COCO 提示词上的平均分通常在 $25.0$ 至 $33.0$ 之间，超过 $30.0$ 分代表高度对齐。
- **语义盲区提醒**：CLIP 对高维概念匹配灵敏，但在否定语法（如 *“没有戴帽子的猫”*）与微观空间相对拓扑（如 *“在...左边”*）上存在已知固有弱点。
- **组合评测建议**：建议与 **PickScore** 协同使用，分别评估“客观语义遵从”与“主观人类审美喜好”。

---

## 调用示例

<Steps>
  <Step>
    ### 单张图像图文语义评估

    计算单张图片对提示词的遵从得分：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics clip \\
            --image path/to/sample.png \\
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
        image-evaluator --metrics clip \\
            --image path/to/folder/ \\
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

---

## 参考文献与项目源

- **指标论文**: Hessel et al., 2021, *CLIPScore: A Reference-free Evaluation Metric for Image Captioning* (EMNLP 2021, [arXiv:2104.08718](https://arxiv.org/abs/2104.08718))
- **官方代码库**: [openai/CLIP](https://github.com/openai/CLIP)
- **多模态基石论文**: Radford et al., 2021, *Learning Transferable Visual Models From Natural Language Supervision* (ICML 2021, [arXiv:2103.00020](https://arxiv.org/abs/2103.00020))
""")

# ==============================================================================
# PICKSCORE
# ==============================================================================
save("text-image/pickscore.mdx", """---
title: PickScore
description: Fine-tuned CLIP ViT-H-14 human preference reward scoring trained on the Pick-a-Pic benchmark
---

# PickScore

PickScore by Kirstain et al. (NeurIPS 2023) evaluates text-to-image synthesis quality against human subjective preferences. While standard CLIP evaluates objective semantic similarity, PickScore is fine-tuned on over 500,000 empirical human choices from the Pick-a-Pic dataset (`yuvalkirstain/PickScore_v1`), predicting which synthetic generation humans prefer.

---

## Technical Specifications

| Property | Specification |
| :--- | :--- |
| **Category** | Text-to-Image Alignment & Human Preference |
| **CLI Metric** | `pickscore` |
| **Input Options** | `--image <file_or_dir>`, `--prompt "<text_or_file>"` (both required) |
| **Prohibited Options** | `--reference` (not applicable for human preference scoring) |
| **Output Scale** | Calibrated likelihood logits, typically `[15.0, 25.0]` |
| **Direction** | **Higher is better** |
| **Model Backbone** | Fine-tuned CLIP `ViT-H-14` |
| **Upstream Source** | [yuvalkirstain/PickScore_v1](https://huggingface.co/yuvalkirstain/PickScore_v1) |

---

## Mathematical Formulation

PickScore projects image $I$ and prompt $T$ through fine-tuned CLIP ViT-H-14 encoders into normalized 1024-dimensional space, computing a temperature-calibrated softmax preference logit:

```math
s_{\\text{pick}} = 100 \\cdot \\frac{\\Phi_{\\text{image}}(I) \\cdot \\Phi_{\\text{text}}(T)}{\\|\\Phi_{\\text{image}}(I)\\|_2 \\|\\Phi_{\\text{text}}(T)\\|_2}
```

On empirical test sets, real outputs typically score in $[15.0, 25.0]$. Higher values indicate stronger alignment with human aesthetic choices.

---

## Interpretation & Guidance

- **Score Range**: Real outputs typically fall in $[15.0, 25.0]$. Scores above $21.0$ indicate strong visual appeal and high probability of being chosen by human judges. Scores below $18.0$ indicate artifact-laden or poorly aligned outputs.
- **Preference vs. Fidelity**: A technically distorted image may receive a low score even if it contains prompt keywords, because the model captures human aesthetic displeasure.
- **Prompt Sensitivity**: PickScore requires clear descriptive text. Empty or whitespace-only prompts raise an explicit error.

---

## Usage Examples

<Steps>
  <Step>
    ### Single Image Evaluation

    Score human aesthetic preference against a target prompt:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics pickscore \\
            --image path/to/sample.png \\
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
        image-evaluator --metrics pickscore \\
            --image path/to/candidate_folder/ \\
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

---

## References

- **Paper**: Kirstain et al., 2023, *Pick-a-Pic: An Open Dataset of User Preferences for Text-to-Image Generation* (NeurIPS 2023, [arXiv:2305.01569](https://arxiv.org/abs/2305.01569))
- **Model Card & Weights**: [yuvalkirstain/PickScore_v1](https://huggingface.co/yuvalkirstain/PickScore_v1)
- **Project Repository**: [tgxs-by/PickScore](https://github.com/yuvalkirstain/PickScore)
""")

save("text-image/pickscore.zh.mdx", """---
title: PickScore (人类审美偏好对齐)
description: 基于 Pick-a-Pic 真实人类成对反馈数据集微调的 CLIP ViT-H-14 偏好奖励打分模型
---

# PickScore (人类审美偏好对齐)

PickScore (Kirstain et al., NeurIPS 2023) 专门用于评测文本生成图像在人类主观审美维度下的偏好程度。常规 CLIP 衡量的是客观图文特征几何距离，而 PickScore 在包含超 50 万条真实人类二选一打分数据的 Pick-a-Pic 数据集 (`yuvalkirstain/PickScore_v1`) 上进行了深度微调，能够直接预测人类评委更倾向选择哪张生成结果。

---

## 核心规格

| 属性 | 规范定义 |
| :--- | :--- |
| **评测体系** | 跨模态图文对齐与偏好 (Text-to-Image Alignment) |
| **命令行参数** | `--metrics pickscore` |
| **输入要求** | `--image <图片或目录>`, `--prompt "<文本提示词>"` (两项皆必填) |
| **禁止参数** | `--reference` (偏好模型直接基于图文打分，禁止参考图) |
| **标度范围** | 校准后的 Logit 分值，主流测试集集中在 `[15.0, 25.0]` |
| **取值方向** | **数值越高越优** |
| **骨干网络** | 微调版 CLIP `ViT-H-14` |
| **权威源** | [yuvalkirstain/PickScore_v1](https://huggingface.co/yuvalkirstain/PickScore_v1) |

---

## 理论公式推导

PickScore 使用经过人类反馈微调的 ViT-H-14 编码器，分别提取图像特征 $\\Phi_{\\text{image}}(I)$ 与文本特征 $\\Phi_{\\text{text}}(T)$，计算带温度缩放的对数几率评分：

```math
s_{\\text{pick}} = 100 \\cdot \\frac{\\Phi_{\\text{image}}(I) \\cdot \\Phi_{\\text{text}}(T)}{\\|\\Phi_{\\text{image}}(I)\\|_2 \\|\\Phi_{\\text{text}}(T)\\|_2}
```

在主流生成测试集上，分值主要集中在 $[15.0, 25.0]$ 范围。数值越大，代表人类评测者偏好该生成图像的概率越高。

---

## 评测阈值与解读建议

- **基准分位区间**：分值大于 $21.0$ 通常意味着图像构图出众、人体结构完整且符合人类审美；分值低于 $18.0$ 则往往存在肢体瑕疵、过度变形或明显的图文失配。
- **真实审美约束**：即使生成图像完全包含提示词中提到的名词，若画面呈现重度噪点或解剖学畸变，PickScore 依然会给出低分，反映出人类对整体质感的严苛评判。
- **提示词必填**：禁止传入空字符串或纯空格提示词，否则将抛出异常终止评测。

---

## 调用示例

<Steps>
  <Step>
    ### 单张图像人类偏好评分

    评估单张生成样本与提示词的人类偏好对齐度：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics pickscore \\
            --image path/to/sample.png \\
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
        image-evaluator --metrics pickscore \\
            --image path/to/candidate_folder/ \\
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

---

## 参考文献与项目源

- **核心论文**: Kirstain et al., 2023, *Pick-a-Pic: An Open Dataset of User Preferences for Text-to-Image Generation* (NeurIPS 2023, [arXiv:2305.01569](https://arxiv.org/abs/2305.01569))
- **官方权重与模型卡**: [yuvalkirstain/PickScore_v1](https://huggingface.co/yuvalkirstain/PickScore_v1)
- **项目仓库**: [yuvalkirstain/PickScore](https://github.com/yuvalkirstain/PickScore)
""")

# ==============================================================================
# LPIPS
# ==============================================================================
save("pairwise/lpips.mdx", """---
title: LPIPS (Perceptual Distance)
description: Learned Perceptual Image Patch Similarity using AlexNet multi-scale deep features
---

# LPIPS (Perceptual Distance)

Learned Perceptual Image Patch Similarity (LPIPS) by Zhang et al. (CVPR 2018) evaluates perceptual fidelity across generated and reference images. By extracting multi-scale activations from a deep neural network and applying learned channel weights, it correlates strongly with human subjective judgments of image similarity.

---

## Technical Specifications

| Property | Specification |
| :--- | :--- |
| **Category** | Pairwise Perceptual Fidelity |
| **CLI Metric** | `lpips` |
| **Input Options** | `--image <path>`, `--reference <path>` (both required) |
| **Prohibited Options** | `--prompt` (not applicable for pairwise comparison) |
| **Spatial Constraint** | Strictly identical dimensions required ($H_{\\text{ref}} = H_{\\text{gen}}$, $W_{\\text{ref}} = W_{\\text{gen}}$) |
| **Output Scale** | Continuous scalar float in `[0.0, +inf)` |
| **Direction** | **Lower is better** (0.0 denotes exact perceptual match) |
| **Model Backbone** | Official AlexNet trunk (v0.1 learned weights) |
| **Upstream Source** | [richzhang/PerceptualSimilarity](https://github.com/richzhang/PerceptualSimilarity) |

---

## Mathematical Formulation

LPIPS extracts feature activations across $L$ layers from reference $x$ and generated $x_0$. Within each layer $l$, feature channels are normalized by $L_2$ norm, scaled by learned vector $w_l$, and spatially averaged:

```math
d(x, x_0) = \\sum_l \\frac{1}{H_l W_l} \\sum_{h, w} \\left\\| w_l \\odot \\left( \\hat{y}^l_{hw} - \\hat{y}_{0, hw}^l \\right) \\right\\|_2^2
```

---

## Interpretation & Guidance

- **Diagnostic Thresholds**: Values below $0.15$ indicate near-lossless perceptual fidelity. Ranges between $0.15$ and $0.35$ represent moderate stylistic or texture drift. Values above $0.35$ signal heavy perceptual distortion or structural breakdown.
- **Fail-Fast Policy**: Pairwise dimensions must match exactly. The evaluator terminates with a `ValueError` rather than applying silent interpolation, ensuring no resampling blur corrupts measurement.
- **Folder Pairing**: In directory mode, files are paired strictly by matching case-sensitive filename stems across formats.

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

---

## References

- **Paper**: Zhang et al., 2018, *The Unreasonable Effectiveness of Deep Features as a Perceptual Metric* (CVPR 2018, [arXiv:1801.03924](https://arxiv.org/abs/1801.03924))
- **Official Repository**: [richzhang/PerceptualSimilarity](https://github.com/richzhang/PerceptualSimilarity)
""")

save("pairwise/lpips.zh.mdx", """---
title: LPIPS (深度感知距离)
description: 基于 AlexNet 多尺度深层激活特征的感知相似度度量
---

# LPIPS (深度感知距离)

LPIPS (Zhang et al., CVPR 2018) 是一种利用深度神经网络隐藏层激活值评估图像感知保真度的经典指标。传统的像素级比较（如 MSE、PSNR）极易受到轻微空间位移和全局色温偏移的干扰，而 LPIPS 能够准确捕捉高层纹理与结构语义，与人类主观感知具有极强的一致性。

---

## 核心规格

| 属性 | 规范定义 |
| :--- | :--- |
| **评测体系** | 成对保真度 (Pairwise Comparison) |
| **命令行参数** | `--metrics lpips` |
| **输入要求** | `--image <路径>`, `--reference <路径>` (两项皆必填) |
| **禁止参数** | `--prompt` (成对保真度评测禁止传入提示词) |
| **尺寸硬约束** | 两图长宽必须完全一致 ($H_{\\text{ref}} = H_{\\text{gen}}$, $W_{\\text{ref}} = W_{\\text{gen}}$) |
| **标度范围** | 连续非负标量 `[0.0, +inf)` |
| **取值方向** | **数值越低越优** (0.0 代表感知特征完全一致) |
| **骨干网络** | 官方 AlexNet trunk (v0.1 权重) |
| **权威源** | [richzhang/PerceptualSimilarity](https://github.com/richzhang/PerceptualSimilarity) |

---

## 理论公式推导

LPIPS 从参考图 $x$ 与生成图 $x_0$ 的 $L$ 个深度网络层中提取特征，在每一层 $l$ 内对通道向量执行 $L_2$ 归一化，乘以经过人类打分标定的可学习通道权重 $w_l$，并计算空间均方误差均值：

```math
d(x, x_0) = \\sum_l \\frac{1}{H_l W_l} \\sum_{h, w} \\left\\| w_l \\odot \\left( \\hat{y}^l_{hw} - \\hat{y}_{0, hw}^l \\right) \\right\\|_2^2
```

取值越接近 $0.0$，代表两张图像的深层感知特征越趋于一致。

---

## 评测阈值与解读建议

- **基准分位参考**：数值低于 $0.15$ 代表人眼极难察觉的高保真还原；$0.15$ 至 $0.35$ 之间代表存在风格化、局部纹理重构漂移；超过 $0.35$ 则说明生成图与原图在结构或语义上发生较大撕裂。
- **拒绝隐式缩放**：底层杜绝任何隐式双线性重采样。遇到尺寸不匹配时直接抛出 `ValueError`，防止缩放产生的虚假模糊或高频伪影污染特征。
- **目录配对机制**：在文件夹批量模式下，系统严格按照大小写敏感的主文件名（Stem）进行跨格式一一配对。

---

## 调用示例

<Steps>
  <Step>
    ### 单对图像感知距离评估

    比较单张生成图像相对原图的感知距离：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics lpips \\
            --reference path/to/reference.png \\
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
        image-evaluator --metrics lpips \\
            --reference path/to/reference_folder/ \\
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

---

## 参考文献与项目源

- **指标论文**: Zhang et al., 2018, *The Unreasonable Effectiveness of Deep Features as a Perceptual Metric* (CVPR 2018, [arXiv:1801.03924](https://arxiv.org/abs/1801.03924))
- **官方开源仓库**: [richzhang/PerceptualSimilarity](https://github.com/richzhang/PerceptualSimilarity)
""")

# ==============================================================================
# ARCFACE
# ==============================================================================
save("pairwise/arcface.mdx", """---
title: ArcFace Distance
description: Facial identity preservation using InsightFace buffalo_l 512-dimensional cosine feature distance
---

# ArcFace Distance

ArcFace Distance (Deng et al., CVPR 2019) measures facial identity consistency between a generated portrait and a reference photo. By extracting 512-dimensional deep facial embeddings using InsightFace (`buffalo_l`), it computes normalized cosine feature distance. This is the gold-standard metric for evaluating identity retention in LoRA, InstantID, PhotoMaker, and DreamBooth personalized generation.

---

## Technical Specifications

| Property | Specification |
| :--- | :--- |
| **Category** | Facial Identity Preservation (Pairwise) |
| **CLI Metric** | `arcface` |
| **Input Options** | `--image <path>`, `--reference <path>` (both required) |
| **Prohibited Options** | `--prompt` (facial identity compares biometric features) |
| **Face Prerequisite** | Both reference and generated images must contain a detectable face |
| **Output Scale** | Cosine distance in `[0.0, 2.0]` |
| **Direction** | **Lower is better** (0.0 denotes exact identity match) |
| **Model Backbone** | InsightFace `buffalo_l` (RetinaFace + 512-dim ArcFace) |
| **Upstream Source** | [deepinsight/insightface](https://github.com/deepinsight/insightface) |

---

## Mathematical Formulation

The cosine distance between $L_2$-normalized 512-dimensional face embeddings $\\mathbf{f}_1$ and $\\mathbf{f}_2$ is defined as:

```math
\\text{Distance}(\\mathbf{f}_1, \\mathbf{f}_2) = 1 - \\frac{\\mathbf{f}_1 \\cdot \\mathbf{f}_2}{\\|\\mathbf{f}_1\\|_2 \\|\\mathbf{f}_2\\|_2}
```

Scale ranges in $[0.0, 2.0]$, where lower values indicate stronger facial resemblance ($0.0$ denotes exact mathematical identity).

---

## Interpretation & Guidance

- **Benchmark Calibration**: Cosine distance below $0.40$ indicates high facial identity retention (sufficient for InstantID/PhotoMaker verification). Values between $0.40$ and $0.60$ represent borderline drift due to extreme lighting or novel angles. Values above $0.60$ indicate identity loss.
- **Biometric Only**: ArcFace evaluates exclusively facial biometric geometry; it ignores background composition, garments, and lighting.
- **Detection Prerequisite**: If the detector fails to locate a face in either image, the metric returns `None`.

---

## Usage Examples

<Steps>
  <Step>
    ### Single Pair Face Identity Evaluation

    Compare facial identity retention between generated output and real photo:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics arcface \\
            --reference path/to/reference_face.png \\
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
        image-evaluator --metrics arcface \\
            --reference path/to/reference_faces/ \\
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

---

## References

- **Paper**: Deng et al., 2019, *ArcFace: Additive Angular Margin Loss for Deep Face Recognition* (CVPR 2019, [arXiv:1801.07698](https://arxiv.org/abs/1801.07698))
- **Official Repository**: [deepinsight/insightface](https://github.com/deepinsight/insightface)
""")

save("pairwise/arcface.zh.mdx", """---
title: ArcFace (主体人脸一致性)
description: 基于 InsightFace buffalo_l 512 维特征余弦距离的人脸主体身份保持度评测
---

# ArcFace (主体人脸一致性)

ArcFace 人脸距离 (Deng et al., CVPR 2019) 用于度量生成人像与真实人物参考照之间的人脸生物特征一致性。通过 InsightFace (`buffalo_l`) 骨干网络提取主面部 512 维深度人脸嵌入特征，计算其余弦特征距离。该指标是评估 InstantID、PhotoMaker、LoRA 与 DreamBooth 等个性化人脸保持算法的核心度量工具。

---

## 核心规格

| 属性 | 规范定义 |
| :--- | :--- |
| **评测体系** | 成对保真与主体一致 (Pairwise Comparison) |
| **命令行参数** | `--metrics arcface` |
| **输入要求** | `--image <路径>`, `--reference <路径>` (两项皆必填) |
| **禁止参数** | `--prompt` (人脸特征比对基于两图生物特征，禁止提示词) |
| **人脸前置门禁** | 两张输入图像中均必须成功检测到有效人脸 |
| **标度范围** | 余弦距离 `[0.0, 2.0]` |
| **取值方向** | **数值越低越优** (0.0 代表特征完全一致) |
| **骨干网络** | InsightFace `buffalo_l` (RetinaFace + 512 维 ArcFace) |
| **权威源** | [deepinsight/insightface](https://github.com/deepinsight/insightface) |

---

## 理论公式推导

两个 $L_2$ 归一化的 512 维人脸特征向量 $\\mathbf{f}_1$ 与 $\\mathbf{f}_2$ 之间的余弦距离定义为：

```math
\\text{Distance}(\\mathbf{f}_1, \\mathbf{f}_2) = 1 - \\frac{\\mathbf{f}_1 \\cdot \\mathbf{f}_2}{\\|\\mathbf{f}_1\\|_2 \\|\\mathbf{f}_2\\|_2}
```

取值范围为 $[0.0, 2.0]$，分值越低代表面部五官生物特征越相似。

---

## 评测阈值与解读建议

- **判定基准阈值**：人脸距离低于 $0.40$ 时，通常可判定为同一人物且主体特征保持优异（主流 InstantID、LoRA 的验证通过线）；$0.40$ 至 $0.60$ 处于判定临界区（可能受大角度侧脸、遮挡或强烈夸张光影干扰）；高于 $0.60$ 通常说明身份已经丢失。
- **聚焦面部生物几何**：ArcFace 仅分析五官核心特征，完全不受发型、衣着与背景更替的影响。
- **无脸返回规约**：若待测图或参考图中任意一张未检测到合格人脸，该测试对将直接返回 `None`。

---

## 调用示例

<Steps>
  <Step>
    ### 单对人脸身份保真度评估

    评估单张生成人像与人物原照的面部特征距离：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics arcface \\
            --reference path/to/reference_face.png \\
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
        image-evaluator --metrics arcface \\
            --reference path/to/reference_faces/ \\
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

---

## 参考文献与项目源

- **核心论文**: Deng et al., 2019, *ArcFace: Additive Angular Margin Loss for Deep Face Recognition* (CVPR 2019, [arXiv:1801.07698](https://arxiv.org/abs/1801.07698))
- **官方开源项目**: [deepinsight/insightface](https://github.com/deepinsight/insightface)
""")

# ==============================================================================
# SSIM
# ==============================================================================
save("pairwise/ssim.mdx", """---
title: SSIM (Structural Similarity)
description: Structural Similarity Index Measure computed across luminance, contrast, and structure
---

# SSIM (Structural Similarity)

The Structural Similarity Index Measure (SSIM) by Wang et al. (IEEE TIP 2004) evaluates image degradation as perceived changes in structural information. While pixel MSE treats all deviations uniformly, SSIM separates visual differences into luminance, contrast, and structural correlation using local Gaussian window statistics.

---

## Technical Specifications

| Property | Specification |
| :--- | :--- |
| **Category** | Pairwise Structural Fidelity |
| **CLI Metric** | `ssim` |
| **Input Options** | `--image <path>`, `--reference <path>` (both required) |
| **Prohibited Options** | `--prompt` (not applicable for pairwise comparison) |
| **Dimension Floor** | Both dimensions must be $\\ge 11$ pixels ($11 \\times 11$ Gaussian window) |
| **Output Scale** | Continuous scalar in `[-1.0, 1.0]` (1.0 denotes identity) |
| **Direction** | **Higher is better** |
| **Window Parameters** | $11 \\times 11$ Gaussian, $\\sigma=1.5, K_1=0.01, K_2=0.03, L=255$ |
| **Upstream Source** | [scikit-image](https://scikit-image.org/) / [Wang et al., 2004](https://ieeexplore.ieee.org/document/1284395) |

---

## Mathematical Formulation

SSIM evaluates three components across local image patches $x$ and $y$:

```math
\\text{SSIM}(x, y) = [l(x, y)]^\\alpha \\cdot [c(x, y)]^\\beta \\cdot [s(x, y)]^\\gamma
```

Under standard unitary weighting ($\\alpha = \\beta = \\gamma = 1$), this resolves to:

```math
\\text{SSIM}(x, y) = \\frac{(2\\mu_x \\mu_y + C_1)(2\\sigma_{xy} + C_2)}{(\\mu_x^2 + \\mu_y^2 + C_1)(\\sigma_x^2 + \\sigma_y^2 + C_2)}
```

where $C_1 = (K_1 L)^2$ and $C_2 = (K_2 L)^2$ prevent numerical instability ($K_1 = 0.01, K_2 = 0.03, L = 255$).

---

## Interpretation & Guidance

- **Benchmark Interpretation**: Scores above $0.85$ indicate strong structural preservation. Values in $0.65 - 0.85$ represent lossy compression artifacts or slight edge blurring. Values below $0.65$ denote severe structural tear or deformation.
- **Fail-Fast Policy**: SSIM requires image dimensions to be at least $11 \\times 11$ pixels. Inputs smaller than 11 pixels terminate with an explicit `ValueError`.
- **Structural Focus**: Excellent for detecting geometric displacement and blur; complementary to LPIPS deep perceptual evaluation.

---

## Usage Examples

<Steps>
  <Step>
    ### Single Pair Evaluation

    Evaluate structural similarity between a generated image and original reference:

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
        score = predictor.evaluate_ssim(
            reference_path="path/to/reference.png",
            generated_path="path/to/generated.png"
        )
        print(f"SSIM Score: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Directory Batch Evaluation

    Compute mean SSIM across paired folders of images:

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
        mean_score = predictor.evaluate_folder_ssim(
            reference_folder="path/to/reference_folder/",
            generated_folder="path/to/generated_folder/"
        )
        print(f"Mean SSIM: {mean_score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>

---

## References

- **Paper**: Wang et al., 2004, *Image Quality Assessment: From Error Visibility to Structural Similarity* (IEEE Transactions on Image Processing, [DOI:10.1109/TIP.2003.819861](https://doi.org/10.1109/TIP.2003.819861))
- **Standard Reference**: [Zhou Wang Academic Portal](https://ece.uwaterloo.ca/~z70wang/research/ssim/)
""")

save("pairwise/ssim.zh.mdx", """---
title: SSIM (结构相似度)
description: 基于亮度、对比度与结构三要素局部高斯加权协方差的结构相似性度量
---

# SSIM (结构相似度)

结构相似度指标 (Wang et al., IEEE TIP 2004) 旨在模拟人类视觉系统对图像结构特征的提取能力。相比于单纯度量像素点绝对差值的 MSE，SSIM 将图像失真拆解为亮度 (Luminance)、对比度 (Contrast) 与结构 (Structure) 三个相互独立的物理量，能够有效衡量压缩伪影与细节模糊。

---

## 核心规格

| 属性 | 规范定义 |
| :--- | :--- |
| **评测体系** | 成对结构保真度 (Pairwise Comparison) |
| **命令行参数** | `--metrics ssim` |
| **输入要求** | `--image <路径>`, `--reference <路径>` (两项皆必填) |
| **禁止参数** | `--prompt` (成对评测禁止传入提示词) |
| **最小尺寸限制** | 图像宽与高均必须 $\\ge 11$ 像素 ($11 \\times 11$ 高斯平滑窗) |
| **标度范围** | 标量连续浮点数 `[-1.0, 1.0]` (1.0 代表结构完全一致) |
| **取值方向** | **数值越高越优** |
| **标准参数** | $11 \\times 11$ 高斯窗, $\\sigma=1.5, K_1=0.01, K_2=0.03, L=255$ |
| **权威源** | [scikit-image](https://scikit-image.org/) / [Wang et al., 2004](https://ieeexplore.ieee.org/document/1284395) |

---

## 理论公式推导

标准 SSIM 综合局部均值 $\\mu$、方差 $\\sigma^2$ 以及互协方差 $\\sigma_{xy}$：

```math
\\text{SSIM}(x, y) = \\frac{(2\\mu_x \\mu_y + C_1)(2\\sigma_{xy} + C_2)}{(\\mu_x^2 + \\mu_y^2 + C_1)(\\sigma_x^2 + \\sigma_y^2 + C_2)}
```

其中常数 $C_1 = (K_1 L)^2, C_2 = (K_2 L)^2$（默认 $K_1=0.01, K_2=0.03, L=255$）用于避免分母为零。分值越接近 $1.0$ 说明结构越完整。

---

## 评测阈值与解读建议

- **基准分位参考**：分值达到 $0.85$ 以上代表边缘结构、几何轮廓完好保持；$0.65$ 至 $0.85$ 之间代表存在明显的去噪平滑或有损压缩；低于 $0.65$ 代表线条错位、伪影撕裂严重。
- **11 像素硬约束**：受测图像的宽和高必须均不小于 11 像素。任意维度小于 11 像素的图片将直接抛出 `ValueError`。
- **空间互补性**：SSIM 善于发现轮廓线条层面的破损，推荐与具备深层语义感知能力的 **LPIPS** 联合分析。

---

## 调用示例

<Steps>
  <Step>
    ### 单对图像结构相似度评估

    计算单张生成图片与原图的结构相似度：

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
        score = predictor.evaluate_ssim(
            reference_path="path/to/reference.png",
            generated_path="path/to/generated.png"
        )
        print(f"SSIM 得分: {score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### 目录批量配对评测

    批量评估配对图集的平均结构保真度：

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
        mean_score = predictor.evaluate_folder_ssim(
            reference_folder="path/to/reference_folder/",
            generated_folder="path/to/generated_folder/"
        )
        print(f"平均 SSIM: {mean_score:.4f}")
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>

---

## 参考文献与项目源

- **奠基论文**: Wang et al., 2004, *Image Quality Assessment: From Error Visibility to Structural Similarity* (IEEE Transactions on Image Processing, [DOI:10.1109/TIP.2003.819861](https://doi.org/10.1109/TIP.2003.819861))
- **作者权威主页**: [Zhou Wang Image Quality Research](https://ece.uwaterloo.ca/~z70wang/research/ssim/)
""")

# ==============================================================================
# PSNR
# ==============================================================================
save("pairwise/psnr.mdx", """---
title: PSNR (Peak Signal-to-Noise Ratio)
description: Peak Signal-to-Noise Ratio (dB) computed from pixel-wise Mean Squared Error
---

# PSNR (Peak Signal-to-Noise Ratio)

Peak Signal-to-Noise Ratio (PSNR) evaluates the objective reconstruction fidelity of an image by measuring the ratio between the maximum possible pixel power and corrupting mean squared error (MSE). Expressed in decibels (dB), it serves as a foundational engineering baseline for image restoration, super-resolution, and codec compression.

---

## Technical Specifications

| Property | Specification |
| :--- | :--- |
| **Category** | Pairwise Pixel Reconstruction |
| **CLI Metric** | `psnr` |
| **Input Options** | `--image <path>`, `--reference <path>` (both required) |
| **Prohibited Options** | `--prompt` (not applicable for pixel reconstruction) |
| **Spatial Constraint** | Strictly identical dimensions required ($H_{\\text{ref}} = H_{\\text{gen}}$, $W_{\\text{ref}} = W_{\\text{gen}}$) |
| **Output Scale** | Decibels (dB) in `[0.0, +inf)` |
| **Direction** | **Higher is better** |
| **Peak Power** | $\\text{MAX}_I = 255.0$ (8-bit sRGB color space) |
| **Upstream Source** | Classical Signal Processing / ITU-R BT.601 |

---

## Mathematical Formulation

Given reference image $I$ and generated image $K$ of size $m \\times n$:

```math
\\text{MSE} = \\frac{1}{mn} \\sum_{i=0}^{m-1} \\sum_{j=0}^{n-1} [I(i, j) - K(i, j)]^2
```

The logarithmic ratio over peak dynamic range $\\text{MAX}_I = 255.0$ is:

```math
\\text{PSNR} = 10 \\cdot \\log_{10}\\left( \\frac{\\text{MAX}_I^2}{\\text{MSE}} \\right) = 20 \\cdot \\log_{10}(\\text{MAX}_I) - 10 \\cdot \\log_{10}(\\text{MSE})
```

---

## Interpretation & Guidance

- **Decibel Benchmarks**: PSNR above $35\\text{ dB}$ represents excellent reconstruction with imperceptible pixel noise. Ranges between $25 - 35\\text{ dB}$ reflect typical lossy codec compression (JPEG, WebP). Values below $20\\text{ dB}$ indicate heavy noise or severe distortion.
- **Sensitivity Trade-off**: PSNR computes pixel-wise absolute difference. A uniform color tint or a 1-pixel shift drastically penalizes PSNR despite high human visual acceptability. Pair with **LPIPS** for balanced perceptual assessment.

---

## Usage Examples

<Steps>
  <Step>
    ### Single Pair Evaluation

    Evaluate pixel-level reconstruction signal-to-noise ratio:

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

    Calculate mean PSNR across paired image directories:

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

---

## References

- **Standard**: ITU-R Recommendation BT.601, *Studio encoding parameters of digital television for standard 4:3 and wide-screen 16:9 aspect ratios* ([ITU Recommendation](https://www.itu.int/rec/R-REC-BT.601))
- **Foundational Text**: Gonzalez & Woods, *Digital Image Processing*, 4th Edition, Pearson.
""")

save("pairwise/psnr.zh.mdx", """---
title: PSNR (峰值信噪比)
description: 基于逐像素均方误差 (MSE) 的对数信噪比重构精度度量 (dB)
---

# PSNR (峰值信噪比)

峰值信噪比 (Peak Signal-to-Noise Ratio) 是经典图像处理与计算机视觉领域中最基础的客观质量评价指标。它通过计算生成图片相对基准真值图的逐像素均方误差（MSE），得出信号最大可能功率与噪声功率的对数比值（以分贝 dB 为单位），广泛应用于图像重建、超分辨率及编码压缩质量基准。

---

## 核心规格

| 属性 | 规范定义 |
| :--- | :--- |
| **评测体系** | 成对像素重构精度 (Pairwise Comparison) |
| **命令行参数** | `--metrics psnr` |
| **输入要求** | `--image <路径>`, `--reference <路径>` (两项皆必填) |
| **禁止参数** | `--prompt` (成对像素评测禁止传入提示词) |
| **尺寸硬约束** | 两图长宽必须完全一致 ($H_{\\text{ref}} = H_{\\text{gen}}$, $W_{\\text{ref}} = W_{\\text{gen}}$) |
| **标度范围** | 分贝 (dB) 标量非负数 `[0.0, +inf)` |
| **取值方向** | **数值越高越优** |
| **峰值动态范围** | $\\text{MAX}_I = 255.0$ (8位 sRGB 色彩空间) |
| **权威源** | 经典信号处理标准 / ITU-R BT.601 |

---

## 理论公式推导

给定尺寸为 $m \\times n$ 的参考图 $I$ 与生成图 $K$：

```math
\\text{MSE} = \\frac{1}{mn} \\sum_{i=0}^{m-1} \\sum_{j=0}^{n-1} [I(i, j) - K(i, j)]^2
```

当像素动态范围峰值 $\\text{MAX}_I = 255.0$ 时，PSNR 计算公式为：

```math
\\text{PSNR} = 10 \\cdot \\log_{10}\\left( \\frac{\\text{MAX}_I^2}{\\text{MSE}} \\right)
```

单位为分贝（dB），分值越高代表像素重构质量越精准。

---

## 评测阈值与解读建议

- **基准分贝参考**：PSNR 高于 $35\\text{ dB}$ 代表接近无损的高精度重构；$25$ 至 $35\\text{ dB}$ 属于常见有损编码（JPEG、WebP）范围；低于 $20\\text{ dB}$ 则代表图像存在肉眼可见的明显噪点与破坏性失真。
- **像素级敏感性陷阱**：PSNR 对空间微位移与全局色温偏移（如微小暖色偏）极其敏感，往往因局部微调导致数值剧降，但人眼主观依然清晰。因此必须与关注高层纹理的 **LPIPS** 结合分析。

---

## 调用示例

<Steps>
  <Step>
    ### 单对图像峰值信噪比计算

    评估单张生成图片相对原图的像素级重构精度：

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
        print(f"PSNR: {psnr_val:.2f} dB")
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### 目录批量配对计算

    批量评估两组目录的平均峰值信噪比：

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

---

## 参考文献与项目源

- **国际标准规范**: ITU-R Recommendation BT.601, *Studio encoding parameters of digital television for standard 4:3 and wide-screen 16:9 aspect ratios* ([国际电信联盟标准](https://www.itu.int/rec/R-REC-BT.601))
- **经典教材出处**: Gonzalez & Woods, *Digital Image Processing*, 4th Edition.
""")

# ==============================================================================
# FID
# ==============================================================================
save("distribution/fid.mdx", """---
title: FID (Fréchet Inception Distance)
description: Generative distribution distance evaluated in Inception-v3 pool3 feature space
---

# FID (Fréchet Inception Distance)

Fréchet Inception Distance (Heusel et al., NeurIPS 2017) measures the statistical distance between a generated image distribution and a real-world dataset. By fitting multivariate Gaussians to the 2048-dimensional `pool3` features of an Inception-v3 network, it assesses both visual realism and sample diversity.

---

## Technical Specifications

| Property | Specification |
| :--- | :--- |
| **Category** | Dataset Distribution Fidelity |
| **CLI Metric** | `fid` |
| **Input Options** | `--image <dir>`, `--reference <dir>` (both must be directories) |
| **Prohibited Options** | Single image file paths, `--prompt` |
| **Sample Guidance** | $N \\ge 2048$ samples recommended (biased estimator on small $N$) |
| **Output Scale** | Continuous scalar in `[0.0, +inf)` |
| **Direction** | **Lower is better** (0.0 denotes identical feature distributions) |
| **Feature Extractor** | Inception-v3 `pool3` (2048 dimensions, CleanFID protocol) |
| **Upstream Source** | [GaParmar/clean-fid](https://github.com/GaParmar/clean-fid) |

---

## Mathematical Formulation

The Wasserstein-2 distance between two multivariate Gaussians $(\\mu_r, \\Sigma_r)$ and $(\\mu_g, \\Sigma_g)$ is computed as:

```math
\\text{FID} = \\|\\mu_r - \\mu_g\\|_2^2 + \\text{Tr}\\left( \\Sigma_r + \\Sigma_g - 2\\left(\\Sigma_r \\Sigma_g\\right)^{1/2} \\right)
```

Lower values indicate closer fidelity and diversity to the ground-truth distribution.

---

## Directory Layout Contract

FID requires directory inputs on both generated and reference sides. Filenames do not need to match and sample counts may differ ($N_{\\text{ref}} \\neq N_{\\text{gen}}$):

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

## Usage Examples

<Steps>
  <Step>
    ### Dataset Distribution Evaluation

    Compute CleanFID between generated and ground-truth directories:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics fid \\
            --reference path/to/real_images/ \\
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

---

## References

- **Paper**: Heusel et al., 2017, *GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium* (NeurIPS 2017, [arXiv:1706.08500](https://arxiv.org/abs/1706.08500))
- **CleanFID Protocol**: Parmar et al., 2022, *On Bug-Free and Clean Inception Metrics* (CVPR 2022, [arXiv:2104.11222](https://arxiv.org/abs/2104.11222))
- **Official Implementation**: [GaParmar/clean-fid](https://github.com/GaParmar/clean-fid)
""")

save("distribution/fid.zh.mdx", """---
title: FID (弗雷歇距离)
description: 基于 Inception-v3 pool3 特征空间高斯二阶统计量的生成分布距离评测
---

# FID (弗雷歇距离)

弗雷歇 Inception 距离 (Heusel et al., NeurIPS 2017) 用于评估生成图片群体与真实图片数据集之间的整体统计分布差异。该指标将真实图集与生成图集分别输入 Inception-v3 网络提取 2048 维 `pool3` 深层特征，拟合多元高斯分布并计算 Wasserstein-2 统计距离，能够同时反映生成样本的保真度与多样性（防模式崩塌）。

---

## 核心规格

| 属性 | 规范定义 |
| :--- | :--- |
| **评测体系** | 群体生成分布差异 (Dataset Distribution) |
| **命令行参数** | `--metrics fid` |
| **输入要求** | `--image <目录>`, `--reference <目录>` (两项皆必须为文件夹路径) |
| **禁止参数** | 单张图片路径, `--prompt` |
| **样本量推荐** | 建议样本量 $N \\ge 2048$（小样本下存在系统性虚高偏误） |
| **标度范围** | 连续非负浮点数 `[0.0, +inf)` |
| **取值方向** | **数值越低越优** (0.0 代表特征分布完全一致) |
| **特征空间** | Inception-v3 `pool3` (2048 维，CleanFID 无重采样失真规范) |
| **权威源** | [GaParmar/clean-fid](https://github.com/GaParmar/clean-fid) |

---

## 理论公式推导

两个多元高斯分布 $(\\mu_r, \\Sigma_r)$ 与 $(\\mu_g, \\Sigma_g)$ 之间的弗雷歇距离公式为：

```math
\\text{FID} = \\|\\mu_r - \\mu_g\\|_2^2 + \\text{Tr}\\left( \\Sigma_r + \\Sigma_g - 2\\left(\\Sigma_r \\Sigma_g\\right)^{1/2} \\right)
```

分值越低，代表生成样本集的特征分布与真实样本集越接近。

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

## 调用示例

<Steps>
  <Step>
    ### 数据集群体分布距离计算

    计算生成图库与真实图库的 CleanFID 分值：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics fid \\
            --reference path/to/real_images/ \\
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

---

## 参考文献与项目源

- **奠基论文**: Heusel et al., 2017, *GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium* (NeurIPS 2017, [arXiv:1706.08500](https://arxiv.org/abs/1706.08500))
- **CleanFID 规范论文**: Parmar et al., 2022, *On Bug-Free and Clean Inception Metrics* (CVPR 2022, [arXiv:2104.11222](https://arxiv.org/abs/2104.11222))
- **官方开源仓库**: [GaParmar/clean-fid](https://github.com/GaParmar/clean-fid)
""")

# ==============================================================================
# KID
# ==============================================================================
save("distribution/kid.mdx", """---
title: KID (Kernel Inception Distance)
description: Unbiased polynomial kernel maximum mean discrepancy (MMD) in Inception feature space
---

# KID (Kernel Inception Distance)

Kernel Inception Distance (Bińkowski et al., ICLR 2018) is an unbiased metric for evaluating generative image distributions. Unlike FID, which fits a parametric Gaussian distribution and suffers from heavy small-sample bias, KID computes the squared Maximum Mean Discrepancy (MMD) with a cubic polynomial kernel via a U-statistic, providing reliable evaluation on subsets of 1,000 images or fewer.

---

## Technical Specifications

| Property | Specification |
| :--- | :--- |
| **Category** | Unbiased Dataset Distribution Distance |
| **CLI Metric** | `kid` |
| **Input Options** | `--image <dir>`, `--reference <dir>` (both must be directories) |
| **Prohibited Options** | Single image file paths, `--prompt` |
| **Small Sample Robust** | Unbiased on subsets of $100 - 1000$ samples |
| **Output Scale** | U-statistic scalar, typically $[-0.01, 0.10]$ (reported as $\\text{Mean} \\pm \\text{Std}$) |
| **Direction** | **Lower is better** |
| **Kernel Type** | Cubic polynomial $k(x, y) = (x^T y / d + 1)^3$ on Inception features |
| **Upstream Source** | [GaParmar/clean-fid](https://github.com/GaParmar/clean-fid) |

---

## Mathematical Formulation

KID computes MMD with a cubic polynomial kernel $k(x, y) = \\left(\\frac{1}{d} x^T y + 1\\right)^3$ across Inception feature representations:

```math
\\text{KID} = \\text{MMD}^2(P_r, P_g) = \\mathbb{E}[k(x, x')] + \\mathbb{E}[k(y, y')] - 2\\mathbb{E}[k(x, y)]
```

The evaluator returns the mean and standard deviation: $\\text{Mean} \\pm \\text{Std}$. Lower values reflect superior fidelity.

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

## Usage Examples

<Steps>
  <Step>
    ### Dataset Distribution Evaluation

    Compute unbiased KID between generated and reference folders:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics kid \\
            --reference path/to/reference_dir/ \\
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

---

## References

- **Paper**: Bińkowski et al., 2018, *Demystifying MMD GANs* (ICLR 2018, [arXiv:1801.01401](https://arxiv.org/abs/1801.01401))
- **Implementation**: [GaParmar/clean-fid](https://github.com/GaParmar/clean-fid)
""")

save("distribution/kid.zh.mdx", """---
title: KID (核最大均值差异)
description: 基于 Inception 特征空间多项式核最大均值差异 (MMD) 的无偏生成分布距离
---

# KID (核最大均值差异)

核最大均值差异 (Bińkowski et al., ICLR 2018) 是一种面向生成式图像群体分布的无偏评测指标。相较于必须拟合多元高斯分布且严重依赖大样本量（易出现小样本虚高）的 FID，KID 基于三次多项式核并通过无偏 U 统计量计算分布的最大均值差异（MMD），在千张以内的小样本场景下依然保持客观稳定。

---

## 核心规格

| 属性 | 规范定义 |
| :--- | :--- |
| **评测体系** | 群体生成分布无偏度量 (Dataset Distribution) |
| **命令行参数** | `--metrics kid` |
| **输入要求** | `--image <目录>`, `--reference <目录>` (两项皆必须为文件夹路径) |
| **禁止参数** | 单张图片路径, `--prompt` |
| **小样本鲁棒性** | 在 $100 - 1000$ 张小样本子集下具备严格数学无偏性 |
| **标度范围** | U 统计量标量，主流区间 $[-0.01, 0.10]$ (输出 $\\text{均值} \\pm \\text{标准差}$) |
| **取值方向** | **数值越低越优** |
| **核函数** | 三次多项式核 $k(x, y) = (x^T y / d + 1)^3$ |
| **权威源** | [GaParmar/clean-fid](https://github.com/GaParmar/clean-fid) |

---

## 理论公式推导

KID 采用三次多项式核函数 $k(x, y) = \\left(\\frac{1}{d} x^T y + 1\\right)^3$ 衡量 Inception 特征空间距离：

```math
\\text{KID} = \\text{MMD}^2(P_r, P_g) = \\mathbb{E}[k(x, x')] + \\mathbb{E}[k(y, y')] - 2\\mathbb{E}[k(x, y)]
```

评测器输出均值与标准差 $\\text{Mean} \\pm \\text{Std}$。数值越低越优。

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

## 调用示例

<Steps>
  <Step>
    ### 小样本数据集分布评测

    计算生成图库与真实图库之间的无偏 KID 统计量：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics kid \\
            --reference path/to/reference_dir/ \\
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

---

## 参考文献与项目源

- **奠基论文**: Bińkowski et al., 2018, *Demystifying MMD GANs* (ICLR 2018, [arXiv:1801.01401](https://arxiv.org/abs/1801.01401))
- **官方开源实现**: [GaParmar/clean-fid](https://github.com/GaParmar/clean-fid)
""")

