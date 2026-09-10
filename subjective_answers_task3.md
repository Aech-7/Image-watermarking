# Task 3 — Subjective Questions

## Q1. For each image and each stddev, write the minimum value of $\alpha$ for which a QR scanner is able to extract your roll number. In which case did the QR scanner fail to extract the roll no.?

| Image | stddev = 0.01 | stddev = 0.05 | stddev = 0.10 | stddev = 0.15 |
|---|---:|---:|---:|---:|
| Image 1 | [fill] | [fill] | [fill] | [fill] |
| Image 2 | [fill] | [fill] | [fill] | [fill] |
| Image 3 | [fill] | [fill] | [fill] | [fill] |

The minimum value of $\alpha$ is the smallest tested value for which the QR scanner successfully extracts the roll number. The cases where the scanner fails should also be mentioned based on the experimental results.

## Q2. Write key observations from the plots in `task3_psnr_vs_alpha.png`.

Increasing $\alpha$ makes the watermark stronger, which generally improves its recovery in the presence of Gaussian noise. However, increasing $\alpha$ also introduces more changes to the original image, causing the PSNR between the original and watermarked image to decrease.

A higher noise standard deviation makes watermark recovery more difficult because the watermarked image contains more noise. Therefore, a larger $\alpha$ may be required for successful QR recovery. At very large values of $\alpha$, clipping can also affect the recovered watermark.

Thus, there is a trade-off between watermark invisibility and recoverability, and an appropriate value of $\alpha$ should be chosen.

