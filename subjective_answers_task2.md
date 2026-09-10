# Task 2 — Subjective Questions

## Q1. What do you think PSNR is measuring? What can be a disadvantage of it?

PSNR measures the similarity between a reference image and a modified image based on their pixel-level differences. It is calculated using the mean squared error (MSE), which measures the average squared difference between corresponding pixels.

A higher PSNR means that the pixel differences are smaller and the two images are more similar numerically. In this assignment, PSNR is used to measure both the invisibility of the watermark and the quality of the recovered watermark.

One disadvantage is that PSNR only considers pixel-level differences and does not account for human visual perception. Therefore, two images with similar PSNR values may not necessarily look equally similar to a human observer.

## Q2. Briefly explain, what does the script `task2.py` do?

The script `task2.py` evaluates the effect of the watermark strength α by sweeping over 11 values (0.01 to 0.5). For each α, it embeds the watermark into all three cover images and recovers it back, then computes two PSNR metrics: PSNR(original, watermarked) for invisibility, and PSNR(watermark, recovered watermark) for recoverability.

The results are plotted as two PSNR-vs-α curves. As shown in the plots, both PSNR values **decrease monotonically as α increases** — invisibility PSNR drops from ~45 dB to ~15 dB, and recovery PSNR drops from ~30–53 dB down to ~10–13 dB across the three images. This confirms the expected trade-off: a stronger watermark (higher α) is embedded more robustly but distorts the cover image more, while a weaker watermark preserves the original image better but is itself less faithfully recovered. The script's purpose is to visualize this trade-off so a suitable α can be chosen.