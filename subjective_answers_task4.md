# Task 4 — Subjective Questions

## Q1. For each image and each quality factor $q_f$, write the minimum value of $\alpha$ for which a QR scanner is able to extract your roll number.

| Image | $q_f = 30$ | $q_f = 50$ | $q_f = 70$ | $q_f = 90$ |
|---|---:|---:|---:|---:|
| Image 1 | [fill] | [fill] | [fill] | [fill] |
| Image 2 | [fill] | [fill] | [fill] | [fill] |
| Image 3 | [fill] | [fill] | [fill] | [fill] |

The minimum value of $\alpha$ is the smallest tested value for which the QR scanner successfully extracts the roll number. These values should be obtained from the actual experimental results of `task4.py`.

## Q2. Write key observations from the plots in `task4_psnr_vs_alpha.png`.

JPEG compression introduces information loss into the watermarked image. A lower JPEG quality factor means stronger compression and therefore more information loss, making watermark recovery more difficult.

Increasing $\alpha$ makes the watermark stronger and can improve its robustness against JPEG compression. However, a larger $\alpha$ also causes greater distortion to the original image, resulting in lower PSNR.

Therefore, there is a trade-off between robustness and invisibility. Lower JPEG quality generally requires a stronger watermark for successful recovery, while higher quality preserves more of the watermark information.