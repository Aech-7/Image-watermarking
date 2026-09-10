# Task 1 — Subjective Questions

## Q1. Why using top $k$ singular values and vector works for our tasks? Can we use less than top $k$ singular values and vectors? If yes, what is the minimum value? If not, why?

For an $H \times W$ matrix, there can be at most $k = \min(H,W)$ singular values. In our watermarking method, the singular values of the watermark are added to the corresponding singular values of the cover image. Using all $k$ singular values therefore allows us to embed the complete available singular-value information of the watermark.

We can use fewer than $k$ singular values by embedding only the first $l$ singular values. However, this means that some information from the watermark is not embedded, resulting in less complete recovery. The minimum possible number is 1 singular value, although using all $k$ singular values provides more complete watermark recovery.

## Q2. Which singular values of the cover image will you add the singular values of the watermark and why?

**Answer: (a) Top $l$ singular values.**

The singular values are arranged in decreasing order:

$$
\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_k.
$$

This matches how the embedding formula is constructed: both the cover's and watermark's singular values are sorted in descending order and added index-wise, so the watermark's largest singular values combine with the cover's largest singular values.

The top singular values represent the dominant, structurally significant components of the image, while the smallest singular values correspond to low-energy, fine-detail components. Embedding into the smallest singular values would keep visible distortion low, but these components are fragile, small perturbations, noise, or compression can easily overwhelm or destroy them, making the watermark unreliable to recover. Embedding into the top singular values ties the watermark to the image's dominant structure, making it more robust and reliably recoverable, at the cost of some additional, though still controllable via $\alpha$, visible change to the cover image.