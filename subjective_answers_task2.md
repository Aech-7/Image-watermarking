# Task 2 — Subjective Questions

## Q1. What do you think PSNR is measuring? What can be a disadvantage of it?

PSNR measures the similarity between a reference image and a modified image based on their pixel-level differences. It is calculated using the mean squared error (MSE), which measures the average squared difference between corresponding pixels.

A higher PSNR means that the pixel differences are smaller and the two images are more similar numerically. In this assignment, PSNR is used to measure both the invisibility of the watermark and the quality of the recovered watermark.

One disadvantage is that PSNR only considers pixel-level differences and does not account for human visual perception. Therefore, two images with similar PSNR values may not necessarily look equally similar to a human observer.

## Q2. Briefly explain, what does the script `task2.py` do?

The script `task2.py` evaluates different values of the watermark strength $\alpha$. For each value of $\alpha$, it creates a watermarked image and then recovers the watermark.

It calculates PSNR between the original and watermarked image to measure invisibility, and PSNR between the original and recovered watermark to measure recoverability. It then plots these values against $\alpha$ to study the trade-off between keeping the watermark invisible and making it recoverable.
