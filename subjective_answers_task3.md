# Task 3 — Subjective Questions

## Q1. For each image and each stddev, write the minimum value of α for which a QR scanner is able to extract your roll number. In which case did the QR scanner fail to extract the roll no.?

| Image | stddev = 0.01 | stddev = 0.05 | stddev = 0.10 | stddev = 0.15 |
|---|---:|---:|---:|---:|
| Image 1 | 0.01 | 0.01 | NA | NA |
| Image 2 | 0.01 | 0.01 | NA | NA |
| Image 3 | 0.01 | 0.01 | NA | NA |

The QR scanner successfully extracted the roll number at the lowest tested α (0.01) for stddev = 0.01 and 0.05, for all three images. For stddev ≥ 0.10, the scanner failed to extract the roll number **at every tested α value (0.01–0.5)**, for all three images — increasing α did not help recovery here, since at low α the watermark signal is too weak to survive the noise, while at high α the watermarked image itself clips, adding further distortion that recovery cannot undo. As a result, no working α exists in the tested range once stddev reaches 0.10.

## Q2. Write key observations from the plots in `task3_psnr_vs_alpha.png`.

- **Invisibility (top row)** decreases monotonically with α for all stddev values, as expected — a stronger watermark always distorts the image more, independent of noise.
- **Recoverability (bottom row)** behavior depends on noise level: at low stddev (0.01), PSNR rises sharply then **peaks early (α ≈ 0.05–0.15)** and declines afterward, since excess α causes clipping that hurts recovery once the noise floor is already low. At higher stddev (0.05), the peak is broader and shifts right (α ≈ 0.2–0.35). At stddev = 0.1 and 0.15, PSNR **rises only gradually and keeps increasing** across the full α range without a clear peak — the noise dominates, so more watermark strength keeps helping rather than causing clipping to be the limiting factor.
- Higher stddev consistently caps the maximum achievable recovery PSNR much lower (e.g. Image 1: ~22 dB at stddev=0.01 vs ~8 dB at stddev=0.15), consistent with the QR scanner failing outright at stddev ≥ 0.10 in Q1.
- Overall, the optimal α is noise-dependent: low-noise cases favor a small-to-moderate α (avoiding clipping), while high-noise cases would need much larger α than tested to compensate — but even then, quality (top row) degrades severely, and in practice recovery still fails.