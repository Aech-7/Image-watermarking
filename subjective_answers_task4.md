# Task 4 — Subjective Questions

## Q1. For each image and each quality factor $q_f$, write the minimum value of $\alpha$ for which a QR scanner is able to extract your roll number.

| Image | $q_f = 30$ | $q_f = 50$ | $q_f = 70$ | $q_f = 90$ |
|---|---:|---:|---:|---:|
| Image 1 | 0.01 | 0.01 | 0.01 | 0.01 |
| Image 2 | 0.01 | 0.01 | 0.01 | 0.01 |
| Image 3 | 0.01 | 0.01 | 0.01 | 0.01 |

 At qf=30, α=0.01 is the smallest value at which the roll number was extracted at all, though decoding was inconsistent and required multiple scan attempts. From qf=50 onward, α=0.01 decoded reliably on the first attempt. We report the 'first successful decode' α in the table; qf=30 is the least robust case despite sharing the same minimum α value.

## Q2. Write key observations from the plots in `task4_psnr_vs_alpha.png`.

JPEG compression introduces information loss into the watermarked image. A lower JPEG quality factor means stronger compression and therefore more information loss, making watermark recovery more difficult.

Increasing $\alpha$ makes the watermark stronger and can improve its robustness against JPEG compression. However, a larger $\alpha$ also causes greater distortion to the original image, resulting in lower PSNR.

Therefore, there is a trade-off between robustness and invisibility. Lower JPEG quality generally requires a stronger watermark for successful recovery, while higher quality preserves more of the watermark information.


- **Invisibility (top row)** decreases monotonically with α for all quality factors, as expected. Curves separate at low α (higher qf → higher PSNR) but converge around α ≥ 0.3, since large watermark distortion dominates over compression loss.
- **Recoverability (bottom row)** is *not* monotonic — it rises, peaks around α ≈ 0.1–0.15, then falls. Low α loses the watermark to JPEG quantization; high α causes pixel clipping in the watermarked image, which the linear recovery step can't undo.
- Quality separation is clearer in recovery: qf=90 consistently peaks highest, while qf=30 stays lowest and least reliable, matching the Q1 findings.
- Overall, there's an **optimal α (~0.1–0.15)** balancing invisibility and recoverability — not a monotonic "higher is better" relationship.