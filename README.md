# SVD-Based Image Watermarking

An image watermarking project using **Singular Value Decomposition (SVD)** to embed and recover a QR-code watermark from RGB images. The project also evaluates how watermark strength affects image quality and how well the watermark survives **Gaussian noise** and **JPEG compression**.

## Overview

The project focuses on:

- Implementing SVD using eigendecomposition instead of directly calling `numpy.linalg.svd`
- Embedding and recovering a QR-code watermark in RGB images
- Studying the effect of watermark strength `α`
- Evaluating image quality and watermark recovery using PSNR
- Testing robustness against Gaussian noise and JPEG compression
- Using QR decoding as a practical check of watermark recovery

Three different cover images are used for the experiments.

---
## Method

For a cover image $C$, SVD decomposes the image as:

$$
C = U_C \Sigma_C V_C^T
$$

The watermark $Q$ is similarly decomposed as:

$$
Q = U_Q \Sigma_Q V_Q^T
$$

The watermark is embedded by modifying the singular values:

$$
\Sigma_W = \Sigma_C + \alpha\Sigma_Q
$$

where $\alpha$ controls the watermark strength.

The watermarked image is reconstructed as:

$$
C_W = U_C\Sigma_WV_C^T
$$

During recovery, the watermark singular values are estimated as:

$$
\hat{\Sigma}_Q =
\frac{\Sigma_W-\Sigma_C}{\alpha}
$$

The recovered watermark is then reconstructed using the watermark's singular vectors.

The same process is applied independently to the three RGB channels.

---

## SVD Implementation

Instead of using `numpy.linalg.svd`, the SVD is implemented using eigendecomposition of the Gram matrix:

$$
G = MM^T
$$

The eigenvalues of $G$ are used to obtain the singular values:

$$
\sigma_i = \sqrt{\lambda_i}
$$

The corresponding eigenvectors are used to construct the singular-vector matrices required for reconstruction.

Small singular values are handled separately to avoid numerical instability.
---

## Watermarking Pipeline

```text
             Cover Image
                  |
          +-------+-------+
          |       |       |
          R       G       B
          |       |       |
         SVD     SVD     SVD
          |       |       |
          +-------+-------+
                  |
         Watermark Embedding
                  |
                  v
          Watermarked Image
                  |
          +-------+-------+
          |               |
       Gaussian          JPEG
        Noise          Compression
          |               |
          +-------+-------+
                  |
                  v
          Watermark Recovery
                  |
                  v
             QR Decoding
````

---

# Experiments

## 1. Effect of Watermark Strength

The watermark strength `α` is varied from `0.01` to `0.50`.

Two PSNR measurements are used:

* **Original vs. Watermarked Image** — measures distortion introduced into the cover image.
* **Original vs. Recovered Watermark** — measures watermark recovery quality.

![Effect of watermark strength](results/plots/psnr_vs_alpha.png)

Increasing `α` makes the watermark stronger but also introduces more distortion into the cover image. The recovery quality also varies with `α`, showing that the strongest watermark is not necessarily the best one.

---

## 2. Robustness to Gaussian Noise

Gaussian noise is added to the watermarked images before attempting watermark recovery.

Tested noise levels:

```text
σ = 0.01, 0.05, 0.10, 0.15
```

![Gaussian noise robustness](results/plots/noise_robustness.png)

At the lower noise levels, the watermark remains recoverable for the tested images. At higher noise levels, recovery quality drops significantly and QR decoding fails for the tested watermark strengths.

This shows that increasing watermark strength alone cannot compensate for sufficiently strong noise.

---

## 3. Robustness to JPEG Compression

The watermarked images are compressed using different JPEG quality factors:

```text
Quality = 90, 70, 50, 30
```

![JPEG robustness](results/plots/jpeg_robustness.png)

JPEG compression reduces the quality of the recovered watermark as the compression becomes stronger.

For the tested images, watermark recovery was strongest around an intermediate watermark strength of approximately:

```text
α ≈ 0.1 – 0.15
```

Increasing `α` beyond this range does not continuously improve recovery because additional distortion and clipping can affect the result.

---

## Evaluation

PSNR is used for numerical evaluation:

$$
PSNR(X,Y) =
10\log_{10}\left(\frac{MAX^2}{MSE(X,Y)}\right)
$$

| Comparison                       | Purpose                                |
| -------------------------------- | -------------------------------------- |
| Original vs. Watermarked         | Measures distortion of the cover image |
| Original Watermark vs. Recovered | Measures watermark recovery quality    |

PSNR is complemented by **QR decoding** to check whether the recovered watermark is actually usable.

---

## Key Observations

* `α` controls the trade-off between watermark strength and cover-image distortion.
* Very small `α` values preserve the cover image better but can be more sensitive to degradation.
* Very large `α` values introduce more distortion and can cause clipping.
* Gaussian noise has a strong effect on watermark recovery at higher noise levels.
* JPEG compression degrades recovery as compression becomes stronger.
* An intermediate `α` gives a better balance between image quality and watermark recovery than simply maximizing watermark strength.

---

## Project Structure

```text
svd-watermarking/
│
├── README.md
├── requirements.txt
│
├── src/
│   ├── svd_watermarking.py
│   ├── watermark_quality.py
│   ├── noise_robustness.py
│   └── jpeg_robustness.py
│
├── data/
│   ├── covers/
│   └── watermark/
│
└── results/
    ├── plots/
    ├── gaussian_noise/
    └── jpeg/
```

### Main Files

* `svd_watermarking.py` — SVD implementation, watermark embedding and recovery
* `watermark_quality.py` — effect of `α` on image and watermark PSNR
* `noise_robustness.py` — robustness against Gaussian noise
* `jpeg_robustness.py` — robustness against JPEG compression

---

## Requirements

* Python 3
* NumPy
* OpenCV
* Matplotlib
* python-dotenv

Install the dependencies with:

```bash
pip install -r requirements.txt
```

---

## Running the Project

```bash
python src/svd_watermarking.py
python src/watermark_quality.py
python src/noise_robustness.py
python src/jpeg_robustness.py
```

The scripts generate the recovered watermarks and plots used for the analysis.

---

## Future Improvements

* Compare SVD watermarking with DCT- and DWT-based methods
* Test robustness against resizing, filtering and cropping
* Automate QR-decoding success rates across all experiments
* Add perceptual image-quality metrics alongside PSNR
* Study the optimal `α` for different types and levels of image degradation
