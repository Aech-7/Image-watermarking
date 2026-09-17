# SVD-Based Image Watermarking and Robustness Analysis

An image watermarking project based on **Singular Value Decomposition (SVD)**. The project embeds a QR code into an image by modifying its singular values and studies how the watermark behaves under different levels of **Gaussian noise** and **JPEG compression**.

The main focus is not only on embedding the watermark, but also on understanding the trade-off between **image quality, watermark recoverability, and robustness**.

---

## Overview

Digital watermarking can be used to hide information inside an image without placing an obvious visible mark on it.

In this project, a QR code containing a roll number is used as the watermark. The watermark is embedded into three different cover images using SVD. The watermark strength is controlled using a parameter `α`.

The project investigates:

* SVD implementation using eigendecomposition.
* Watermark embedding and recovery.
* The effect of watermark strength on image quality.
* Watermark recovery using PSNR.
* QR-code decoding as a practical recovery check.
* Robustness to Gaussian noise.
* Robustness to JPEG compression.

The experiments help answer a practical question:

> **How strong should the watermark be so that it remains recoverable without unnecessarily degrading the original image?**

---

## Method

For a cover image \(C\), the image is decomposed using SVD:

$$
C = U_C \Sigma_C V_C^T
$$

Similarly, the QR-code watermark \(Q\) is decomposed as:

$$
Q = U_Q \Sigma_Q V_Q^T
$$

The watermark is embedded by modifying the singular values of the cover image:

$$
\tilde{\Sigma}_i = \Sigma_i + \alpha \Sigma_i^Q
$$

or, in matrix form,

$$
\tilde{\Sigma} = \Sigma_C + \alpha\Sigma_Q
$$

where `α > 0` controls the watermark strength.

The watermarked image is reconstructed using the original structure of the cover image:

$$
C_\alpha = U_C\tilde{\Sigma}V_C^T
$$

The reconstructed pixel values are clipped to the valid image range `[0, 1]`.

### Recovery

The original singular values of the cover image are kept as part of the key. During recovery, the singular values of the watermarked image are used to estimate the watermark singular values:

$$
\tilde{\Sigma}_Q =
\frac{\Sigma' - \Sigma_C}{\alpha}
$$

The estimated singular values are then combined with the watermark's singular vectors to reconstruct the QR code.

This follows the formulation used in the project assignment, where the cover's singular values and the watermark's singular vectors act as part of the private recovery information.

---

## SVD Implementation

Instead of directly using `numpy.linalg.svd`, the SVD implementation is built using eigendecomposition.

For an image matrix \(M\), the Gram matrix is formed as:

$$
G = MM^T
$$

The eigenvalues and eigenvectors of this matrix are then used to obtain the singular values and the left singular vectors:

$$
\sigma_i = \sqrt{\lambda_i}
$$

The right singular vectors are obtained from the relationship between \(M\), \(U\), and the singular values.

The implementation also handles numerical issues around very small singular values and maintains consistent signs between the singular-vector matrices.

This makes the SVD implementation useful for understanding what happens internally rather than treating SVD as a black-box operation.

---

## RGB Watermarking

The watermarking process is applied independently to the three RGB channels.

```text
                    Cover Image
                         |
             +-----------+-----------+
             |           |           |
             v           v           v
             R           G           B
             |           |           |
            SVD         SVD         SVD
             |           |           |
             +-----------+-----------+
                         |
                  Watermark Embedding
                         |
                         v
                  Reconstruction
                         |
                         v
                 Watermarked Image
```

The same channel-wise process is used during watermark recovery.

---

## Watermark Strength

The parameter `α` determines how strongly the watermark is embedded.

A small value of `α` produces less modification to the cover image, but the watermark can become more difficult to recover after image degradation.

A large value of `α` produces a stronger watermark, but also increases the distortion introduced into the original image.

The experiments use:

```text
α = 0.01, 0.05, 0.10, 0.15, 0.20, ..., 0.50
```

This makes it possible to study the effect of watermark strength rather than evaluating only one manually selected value.

---

# Image Quality Evaluation

Two PSNR measurements are used in the experiments.

## 1. Watermarked Image PSNR

$$
PSNR(C,C_\alpha)
$$

This compares the original cover image with the watermarked image.

It measures **invisibility**: how much the watermarking process changes the original image.

A higher value means that the watermarked image is numerically closer to the original.

---

## 2. Recovered Watermark PSNR

$$
PSNR(Q,\hat{Q})
$$

This compares the original QR watermark with the recovered watermark.

It measures **recoverability**: how accurately the embedded watermark can be reconstructed.

These two measurements capture different objectives.

```text
Higher α
   |
   +----> Stronger watermark
   |
   +----> More distortion in cover image
   |
   +----> Potentially better recovery
   |
   +----> Excessive α can cause clipping
```

Therefore, the best value of `α` is not necessarily the largest one.

---

# Experiments

## Experiment 1 — SVD Watermarking

The first experiment implements the complete watermarking and recovery pipeline.

For each cover image:

1. Decompose the cover image using SVD.
2. Decompose the QR watermark using SVD.
3. Modify the cover singular values.
4. Reconstruct the watermarked image.
5. Recover the watermark.
6. Compare the original and recovered images.

The experiment verifies the basic embedding and recovery process before introducing additional image degradation.

---

## Experiment 2 — Effect of Watermark Strength

The watermark strength `α` is swept over multiple values.

For every value of `α`, the following are measured:

* PSNR between the original and watermarked image.
* PSNR between the original and recovered watermark.

The experiment shows the expected trade-off:

* Increasing `α` generally reduces the PSNR of the watermarked image.
* A stronger watermark can improve recovery when the watermark is otherwise too weak.
* At sufficiently large `α`, clipping and distortion can start reducing recovery quality.

This means that watermark strength needs to be selected based on the required balance between image quality and watermark recovery.

---

# Experiment 3 — Gaussian Noise Robustness

A watermarked image may be modified or degraded after it has been generated. To test this, Gaussian noise is added before attempting watermark recovery.

The experiments use the following standard deviations:

```text
σ = 0.01
σ = 0.05
σ = 0.10
σ = 0.15
```

For each noise level, multiple watermark strengths are tested.

### Observations

At low noise levels (`σ = 0.01` and `σ = 0.05`), the QR code could be recovered at the lowest tested watermark strength.

For `σ >= 0.10`, the QR scanner failed to recover the roll number for all tested values of `α`.

This shows that simply increasing the watermark strength is not enough to overcome sufficiently strong noise.

The noise experiment also shows that the best `α` depends on the amount of degradation present in the image.

---

# Experiment 4 — JPEG Compression Robustness

JPEG compression is a common source of information loss in images.

To test its effect on watermark recovery, the watermarked images are compressed using different JPEG quality factors:

```text
qf = 90
qf = 70
qf = 50
qf = 30
```

The compressed image is then used for watermark recovery.

### Observations

Lower JPEG quality means stronger compression and greater information loss.

Increasing `α` can make the watermark more resistant to compression, but increasing it indefinitely is not beneficial. At high values, the additional distortion and pixel clipping can negatively affect recovery.

The experiments showed a useful recovery region around:

```text
α ≈ 0.1 – 0.15
```

for the tested JPEG conditions.

The lowest JPEG quality was also the least reliable case for QR decoding, even though the minimum tested `α` was sufficient for a successful decode.

---

# QR-Code Recovery

PSNR provides a numerical measure of image similarity, but it does not directly answer whether the watermark is actually usable.

For this reason, QR decoding is also used as a functional test.

The evaluation therefore has two levels:

```text
                 Watermark Recovery
                        |
             +----------+----------+
             |                     |
             v                     v
            PSNR               QR Scanner
             |                     |
             v                     v
     Numerical similarity     Actual decoding
```

A high recovery PSNR does not necessarily guarantee successful QR decoding, so using both measurements gives a better picture of the system's performance.

---

# Results and Observations

The experiments show several important trends.

### 1. Watermark strength affects both quality and robustness

Increasing `α` makes the watermark stronger but also changes the cover image more significantly.

### 2. There is a trade-off between invisibility and recoverability

A very weak watermark may be difficult to recover after noise or compression.

A very strong watermark introduces more distortion and can eventually suffer from clipping during reconstruction.

### 3. Noise has a strong effect on recovery

The QR code was recoverable at low noise levels but failed consistently at the higher tested noise levels.

### 4. JPEG compression reduces watermark information

Stronger JPEG compression makes watermark recovery more difficult.

### 5. The largest `α` is not always the best choice

The experiments showed that recovery quality can peak at an intermediate watermark strength rather than continuously improving with `α`.

This makes the selection of `α` a parameter-selection problem rather than simply choosing the strongest possible watermark.

---

# Project Structure

```text
svd-watermarking-robustness/
│
├── README.md
├── requirements.txt
├── .env.example
│
├── src/
│   ├── svd_watermarking.py
│   ├── watermark_quality.py
│   ├── noise_robustness.py
│   └── jpeg_robustness.py
│
├── data/
│   ├── covers/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── image3.jpg
│   │
│   └── watermark/
│       └── qr_watermark.png
│
└── results/
    ├── baseline/
    ├── noise_robustness/
    └── jpeg_robustness/
```

## Main files

### `src/svd_watermarking.py`

Contains the core SVD implementation and the watermark embedding and recovery functions.

### `src/watermark_quality.py`

Sweeps over different values of `α` and evaluates the effect of watermark strength using PSNR.

### `src/noise_robustness.py`

Adds Gaussian noise with different standard deviations and evaluates the recovered watermark.

### `src/jpeg_robustness.py`

Compresses watermarked images at different JPEG quality factors and evaluates watermark recovery.

---

# Technologies

* Python
* NumPy
* OpenCV
* Matplotlib
* python-dotenv
* Singular Value Decomposition
* Eigenvalue decomposition
* PSNR-based image quality evaluation
* QR-code decoding
* JPEG compression analysis

---

# Running the Project

Clone the repository:

```bash
git clone <repository-url>
cd svd-watermarking-robustness
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Set the watermark path if required by the implementation:

```bash
cp .env.example .env
```

Then run the experiments from the `src/` directory.

For example:

```bash
python src/svd_watermarking.py
python src/watermark_quality.py
python src/noise_robustness.py
python src/jpeg_robustness.py
```

The generated plots and recovered watermark images can be stored in the `results/` directory.

---

# Takeaway

The main part of this project was not just embedding a QR code into an image. The experiments were used to understand how the watermark behaves as the image is modified.

By varying the watermark strength and introducing Gaussian noise and JPEG compression, the project studies the balance between:

```text
Image Quality
      ↕
Watermark Strength
      ↕
Watermark Recoverability
      ↕
Robustness to Degradation
```

The results show that watermark strength needs to be chosen carefully. A stronger watermark is not always better, and the suitable operating point depends on the type and amount of image degradation.

---

## Future Improvements

Some possible extensions to the current implementation are:

* Compare SVD watermarking with other transform-domain methods such as DCT or DWT.
* Evaluate robustness against additional image operations such as resizing, filtering, and cropping.
* Measure QR decoding success rate automatically instead of checking it manually.
* Build a combined robustness map over `α` and degradation strength.
* Use perceptual image-quality metrics in addition to PSNR, since pixel-wise PSNR does not always correspond to human visual similarity.
