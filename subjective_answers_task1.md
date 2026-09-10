# Task 1 — Subjective Questions

## Q1. Why using top $k$ singular values and vector works for our tasks? Can we use less than top $k$ singular values and vectors? If yes, what is the minimum value? If not, why?

For an $H \times W$ matrix, there can be at most $k = \min(H,W)$ singular values. In our watermarking method, the singular values of the watermark are added to the corresponding singular values of the cover image. Using all $k$ singular values therefore allows us to embed the complete available singular-value information of the watermark.

We can use fewer than $k$ singular values by embedding only the first $l$ singular values. However, this means that some information from the watermark is not embedded, resulting in less complete recovery. The minimum possible number is 1 singular value, although using all $k$ singular values provides more complete watermark recovery.

## Q2. Which singular values of the cover image will you add the singular values of the water mark and why?

**Answer: (b) Least $l$ singular values.**

The singular values are arranged in decreasing order:

$$
\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_k.
$$

The larger singular values represent the dominant components of the image. Modifying them can cause a more noticeable change to the original image. The smaller singular values have a smaller contribution to the overall appearance of the image, so modifying them can help keep the watermark less visible.

Therefore, the least $l$ singular values are preferable when the goal is to minimize visible distortion.
