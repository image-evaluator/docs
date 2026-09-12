import os

docs_dir = "content/docs"

def update_file(rel_path, content):
    full_path = os.path.join(docs_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n\n")
    print(f"Updated: {full_path}")

# ==============================================================================
# 8. PAIRWISE: SSIM
# ==============================================================================
update_file("pairwise/ssim.mdx", """---
title: SSIM (Structural Similarity)
description: Structural Similarity Index Measure computed across luminance, contrast, and structure
---

# SSIM (Structural Similarity)

The Structural Similarity Index Measure (SSIM) by Wang et al. (IEEE TIP 2004) evaluates image degradation as perceived changes in structural information. While pixel MSE treats all deviations uniformly, SSIM separates visual differences into luminance, contrast, and structural correlation using local Gaussian window statistics.

---

## Benchmark Diagnostic Scale

<MetricScale
  min={0.0}
  max={1.0}
  unit=""
  direction="higher"
  segments={[
    { label: "High Structural Fidelity", range: [0.85, 1.0], color: "emerald", note: "Preserves edges, contours, and surface textures" },
    { label: "Noticeable Compression", range: [0.65, 0.85], color: "amber", note: "Lossy compression artifacts or slight blurring" },
    { label: "Severe Degradation", range: [0.0, 0.65], color: "rose", note: "Heavy distortion, edge rupture, or geometric shifts" }
  ]}
/>

---

## Parameter Contract

<TypeTable
  type={{
    "--metrics": {
      type: "string",
      description: "Must include 'ssim'.",
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
      description: "Not allowed for SSIM evaluation.",
      default: "none"
    }
  }}
/>

<Callout type="warn">
  **Minimum Spatial Size Requirement**: Because SSIM computes statistics over an $11 \\times 11$ Gaussian sliding window, both images must measure at least 11 pixels in height and width. Inputs smaller than 11 pixels raise a `ValueError`.
</Callout>

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

## Usage Examples

<Steps>
  <Step>
    ### Single Pair Evaluation

    Evaluate structural similarity between a generated image and original reference:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics ssim \
            --reference path/to/reference.png \
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
        image-evaluator --metrics ssim \
            --reference path/to/reference_folder/ \
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
""")

update_file("pairwise/ssim.zh.mdx", """---
title: SSIM (结构相似度)
description: 基于亮度、对比度与结构三要素局部高斯加权协方差的结构相似性度量
---

# SSIM (结构相似度)

结构相似度指标 (Wang et al., IEEE TIP 2004) 旨在模拟人类视觉系统对图像结构特征的提取能力。相比于单纯度量像素点绝对差值的 MSE，SSIM 将图像失真拆解为亮度 (Luminance)、对比度 (Contrast) 与结构 (Structure) 三个相互独立的物理量，能够有效衡量压缩伪影与细节模糊。

---

## 指标诊断区间标尺

<MetricScale
  min={0.0}
  max={1.0}
  unit=""
  direction="higher"
  segments={[
    { label: "高保真结构保持", range: [0.85, 1.0], color: "emerald", note: "边缘清晰、几何轮廓完好、微观结构高度一致" },
    { label: "轻微模糊或压缩", range: [0.65, 0.85], color: "amber", note: "常见有损压缩伪影或轻度去噪平滑" },
    { label: "严重结构破损", range: [0.0, 0.65], color: "rose", note: "线条撕裂、错位畸变或局部几何严重变形" }
  ]}
/>

---

## 接口参数契约

<TypeTable
  type={{
    "--metrics": {
      type: "string",
      description: "声明评测指标，必须包含 'ssim'。",
      default: "必填"
    },
    "--image": {
      type: "string (路径)",
      description: "待测生成图像文件或目录路径。",
      default: "必填"
    },
    "--reference": {
      type: "string (路径)",
      description: "基准参考图像文件或目录路径。",
      default: "必填"
    },
    "--prompt": {
      type: "string",
      description: "成对评测禁止传入提示词。",
      default: "禁止"
    }
  }}
/>

<Callout type="warn">
  **最小分辨率限制**：由于 SSIM 底层采用 $11 \\times 11$ 的高斯平滑窗口进行局部统计，受测图像的宽和高必须均不小于 11 像素。任意维度小于 11 像素的图片将直接抛出 `ValueError`。
</Callout>

---

## 理论公式推导

标准 SSIM 综合局部均值 $\\mu$、方差 $\\sigma^2$ 以及互协方差 $\\sigma_{xy}$：

```math
\\text{SSIM}(x, y) = \\frac{(2\\mu_x \\mu_y + C_1)(2\\sigma_{xy} + C_2)}{(\\mu_x^2 + \\mu_y^2 + C_1)(\\sigma_x^2 + \\sigma_y^2 + C_2)}
```

其中常数 $C_1 = (K_1 L)^2, C_2 = (K_2 L)^2$（默认 $K_1=0.01, K_2=0.03, L=255$）用于避免分母为零。分值越接近 $1.0$ 说明结构越完整。

---

## 调用示例

<Steps>
  <Step>
    ### 单对图像结构相似度评估

    计算单张生成图片与原图的结构相似度：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics ssim \
            --reference path/to/reference.png \
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
        image-evaluator --metrics ssim \
            --reference path/to/reference_folder/ \
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
""")

# ==============================================================================
# 9. PAIRWISE: PSNR
# ==============================================================================
update_file("pairwise/psnr.mdx", """---
title: PSNR (Peak Signal-to-Noise Ratio)
description: Peak Signal-to-Noise Ratio (dB) computed from pixel-wise Mean Squared Error
---

# PSNR (Peak Signal-to-Noise Ratio)

Peak Signal-to-Noise Ratio (PSNR) evaluates the objective reconstruction fidelity of an image by measuring the ratio between the maximum possible pixel power and corrupting mean squared error (MSE). Expressed in decibels (dB), it serves as a foundational engineering baseline for image restoration, super-resolution, and codec compression.

---

## Benchmark Diagnostic Scale

<MetricScale
  min={15.0}
  max={50.0}
  unit=" dB"
  direction="higher"
  segments={[
    { label: "High Fidelity", range: [35.0, 50.0], color: "emerald", note: "Imperceptible pixel differences, near-lossless" },
    { label: "Standard Codec Range", range: [25.0, 35.0], color: "amber", note: "Standard lossy compression (JPEG, WebP)" },
    { label: "Severe Pixel Degradation", range: [15.0, 25.0], color: "rose", note: "Heavy noise, severe color tints, or blurring" }
  ]}
/>

---

## Parameter Contract

<TypeTable
  type={{
    "--metrics": {
      type: "string",
      description: "Must include 'psnr'.",
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
      description: "Not allowed for PSNR evaluation.",
      default: "none"
    }
  }}
/>

<Callout type="info">
  **Sensitivity Trade-off**: PSNR computes pixel-wise absolute difference. While it provides mathematically exact noise metrics, a global color shift (e.g. slight warm tint) or a single-pixel spatial shift can drastically reduce PSNR while leaving perceived quality intact. Pair with **LPIPS** for holistic evaluation.
</Callout>

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

## Usage Examples

<Steps>
  <Step>
    ### Single Pair Evaluation

    Evaluate pixel-level reconstruction signal-to-noise ratio:

    <Tabs items={["CLI Command", "Python API"]}>
      <Tab value="CLI Command">
        ```bash
        image-evaluator --metrics psnr \
            --reference path/to/reference.png \
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
        image-evaluator --metrics psnr \
            --reference path/to/reference_folder/ \
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

update_file("pairwise/psnr.zh.mdx", """---
title: PSNR (峰值信噪比)
description: 基于逐像素均方误差 (MSE) 的对数信噪比重构精度度量 (dB)
---

# PSNR (峰值信噪比)

峰值信噪比 (Peak Signal-to-Noise Ratio) 是经典图像处理与计算机视觉领域中最基础的客观质量评价指标。它通过计算生成图片相对基准真值图的逐像素均方误差（MSE），得出信号最大可能功率与噪声功率的对数比值（以分贝 dB 为单位），广泛应用于图像重建、超分辨率及编码压缩质量基准。

---

## 指标诊断区间标尺

<MetricScale
  min={15.0}
  max={50.0}
  unit=" dB"
  direction="higher"
  segments={[
    { label: "极高像素保真", range: [35.0, 50.0], color: "emerald", note: "接近无损，像素级误差肉眼几乎不可见" },
    { label: "标准有损编码", range: [25.0, 35.0], color: "amber", note: "主流 JPEG、WebP 压缩图库常见范围" },
    { label: "严重像素劣化", range: [15.0, 25.0], color: "rose", note: "大范围噪点、剧烈色偏或重度模糊失真" }
  ]}
/>

---

## 接口参数契约

<TypeTable
  type={{
    "--metrics": {
      type: "string",
      description: "声明评测指标，必须包含 'psnr'。",
      default: "必填"
    },
    "--image": {
      type: "string (路径)",
      description: "待测生成图像文件或目录路径。",
      default: "必填"
    },
    "--reference": {
      type: "string (路径)",
      description: "基准参考图像文件或目录路径。",
      default: "必填"
    },
    "--prompt": {
      type: "string",
      description: "成对像素评测禁止传入提示词。",
      default: "禁止"
    }
  }}
/>

<Callout type="info">
  **像素级敏感度陷阱**：PSNR 评估的是纯几何空间上的逐像素误差。全局轻微色温偏移（如整体微暖）或极微小的空间亚像素平移，都会导致 PSNR 显著暴跌，哪怕人眼主观感知依然清晰完好。建议与 **LPIPS**、**SSIM** 联合使用以进行多尺度综合判定。
</Callout>

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

## 调用示例

<Steps>
  <Step>
    ### 单对图像峰值信噪比计算

    评估单张生成图片相对原图的像素级重构精度：

    <Tabs items={["命令行 CLI", "Python API 代码"]}>
      <Tab value="命令行 CLI">
        ```bash
        image-evaluator --metrics psnr \
            --reference path/to/reference.png \
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
        image-evaluator --metrics psnr \
            --reference path/to/reference_folder/ \
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

