# %%
# Imports
# ================================================================
# Don't update these imports. 
import os
import cv2
import glob
import getpass
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
load_dotenv()
# %%
# Helper Functions
# ================================================================
# This are helper functions that you can use in your implementation.
# Don't update these functions

os.makedirs("plots", exist_ok=True)

def load_image_as_grayscale(image_path: str) -> np.ndarray:
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = image.astype(np.float32) / 255.0  # Normalize to [0, 1]
    return image

def load_image_as_rgb(image_path: str) -> np.ndarray:
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    image = image.astype(np.float32) / 255.0  # Normalize to [0, 1]
    return image

# ================================================================
# %%
# Task 1
# ======


def svd_decomposition(M: np.ndarray) -> tuple:
    """Perform SVD decomposition on an image
    
            Equivalent to np.linalg.svd(M, full_matrices=False), computed from the
            eigendecomposition of the smaller Gram matrix.
    
            Parameters
            ----------
            M : np.ndarray
                Input matrix of shape (H, W)
    
            Returns
            -------
            tuple
                U (H, k), sigma (k,), Vt (k, W) with k = min(H, W)
            """

    gram = M@M.T
    eigenvalues, eigenvectors = np.linalg.eigh(gram) 
    idx = np.argsort(eigenvalues)[::-1]                 #Gives the indices of the eigenvalues in descending order
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    sigma = np.sqrt(np.maximum(eigenvalues, 0))
    sigma = np.where(sigma <= 1e-8, 0, sigma)          #Replace almost zero singular values with 0
    # print("sigma shape:", sigma.shape)                  #Just a check to see if the shape of sigma is correct
    # print("minimum sigma:", sigma.min())                # To check if we have almost zero singular values
    U = eigenvectors                             
    A = U.T @ M
    Vt = np.zeros((len(sigma), M.shape[1]), dtype=M.dtype)       # Vt = sigma^-1 * U^T * M
    nonzero = sigma > 0
    Vt[nonzero, :] = A[nonzero, :] / sigma[nonzero, None]        # Only caclulate Vt for non-zero singular values to avoid division by zero

    for i in range(len(sigma)):

        if sigma[i] == 0:  # Skip the zero singular values
            continue

        rhs = sigma[i] * U[:, i]
        lhs = M @ Vt[i, :].T

        if np.dot(lhs, rhs) < 0:  # If the dot product is negative, flip the sign of U and Vt
            U[:, i] *= -1
            Vt[i, :] *= -1

    return U, sigma, Vt                    

def add_watermark_single_channel(cover_image: np.ndarray, watermark: np.ndarray, alpha: float) -> np.ndarray:
    """Add watermark to a given channel of an image
    
        Parameters
        ----------
        cover_image : np.ndarray
            Image where watermark needs to be applied
        watermark : np.ndarray
            Watermark
        alpha : float
            Alpha to control the strength of watermark
    
        Returns
        -------
        np.ndarray
            Watermarked Image
        """

    U, sigma, Vt = svd_decomposition(cover_image)
    _, sigma_q, _ = svd_decomposition(watermark)
    sigma_w = sigma + alpha * sigma_q                           #Gives vector of singular values of the watermarked image
    Sigma_w = np.diag(sigma_w)                                  #Makes a diagonal matrix
    watermarked_image = U @ Sigma_w @ Vt
    # print("watermarked_image shape:", watermarked_image.shape)  # Just a check shape
    watermarked_image = np.clip(watermarked_image, 0, 1)        # Ensure pixel values are in [0, 1]
    
    return watermarked_image


def recover_watermark(original_image: np.ndarray, watermarked_image: np.ndarray, watermark: np.ndarray, alpha: float) -> np.ndarray:
    """Recover watermark from a given channel of an image
    
        Parameters
        ----------
        original_image : np.ndarray
            Original image
        watermarked_image : np.ndarray
            Watermarked image
        watermark : np.ndarray
            Watermark
        alpha : float
            Alpha used during watermarking
    
        Returns
        -------
        np.ndarray
            Recovered watermark
        """

    _, sigma, _ = svd_decomposition(original_image)                 #Get the singular values of the original image
    U_q, _, Vt_q = svd_decomposition(watermark)                     #Get U and Vt of the watermark
    _, sigma_w, _ = svd_decomposition(watermarked_image)            #Get the singular values of the watermarked image
    sigma_q_recovered = (sigma_w - sigma)/alpha
    Sigma_q_recovered = np.diag(sigma_q_recovered)
    recovered_watermark = U_q @ Sigma_q_recovered @ Vt_q
    # print("recovered_watermark shape:", recovered_watermark.shape)  # Just a check shape
    recovered_watermark = np.clip(recovered_watermark, 0, 1)        # Ensure pixel values are in [0, 1]

    return recovered_watermark


def add_watermark_rgb(cover_image: np.ndarray, watermark: np.ndarray, alpha: float) -> np.ndarray:
    """Add watermark to a given RGB image
        Parameters
        ----------
        cover_image : np.ndarray
            Image where watermark needs to be applied
        watermark : np.ndarray
            Watermark
        alpha : float
            Alpha to control the strength of watermark
    
        Returns
        -------
        np.ndarray
            Watermarked Image
        """

    red_watermarked = add_watermark_single_channel(cover_image[:, :, 0], watermark[:, :, 0], alpha)
    green_watermarked = add_watermark_single_channel(cover_image[:, :, 1], watermark[:, :, 1], alpha)
    blue_watermarked = add_watermark_single_channel(cover_image[:, :, 2], watermark[:, :, 2], alpha)
    watermarked_image = np.stack((red_watermarked, green_watermarked, blue_watermarked), axis=2)

    return watermarked_image

def recover_watermark_rgb(original_image: np.ndarray, watermarked_image: np.ndarray, watermark: np.ndarray, alpha: float) -> np.ndarray:
    """Recover watermark from a given RGB image
        Parameters
        ----------
        original_image : np.ndarray
            Original image
        watermarked_image : np.ndarray
            Watermarked image
        watermark : np.ndarray
            Watermark
        alpha : float
            Alpha used during watermarking
    
        Returns
        -------
        np.ndarray
            Recovered watermark
        """

    recovered_red = recover_watermark(original_image[:, :, 0], watermarked_image[:, :, 0], watermark[:, :, 0], alpha)
    recovered_green = recover_watermark(original_image[:, :, 1], watermarked_image[:, :, 1], watermark[:, :, 1], alpha)
    recovered_blue = recover_watermark(original_image[:, :, 2], watermarked_image[:, :, 2], watermark[:, :, 2], alpha)

    recovered_watermark = np.stack((recovered_red, recovered_green, recovered_blue), axis=2)
    return recovered_watermark


if __name__ == "__main__":

    image_paths = sorted(glob.glob("imgs/*.jpg"))
    images_rgb = [load_image_as_rgb(path) for path in image_paths]
    watermark_rgb = load_image_as_rgb(os.getenv("watermark_path"))
    # NOTE: All 3 provided cover images in imgs/ are (321, 481) i.e. same size,
    # so k = min(H, W) = 321 for every image. As described in questions.md, the
    # watermark is resized to (k, k) once here in a hard-coded manner rather than
    # dynamically per image.     
    watermark_rgb = cv2.resize(watermark_rgb, (321, 321))

    watermarked_images_rgb = []
    recovered_watermarks_rgb = []

    for image in images_rgb:
        # Apply watermarking to the image and recover the watermark from the watermarked image
        # ###############################################
        # Comment these lines and write your code here
        watermarked_image_rgb = add_watermark_rgb(image, watermark_rgb, alpha=0.1)
        recovered_rgb = recover_watermark_rgb(image, watermarked_image_rgb, watermark_rgb, alpha=0.1)
        # ###############################################

        watermarked_images_rgb.append(watermarked_image_rgb)
        recovered_watermarks_rgb.append(recovered_rgb)

    # 3x3 plots; first row: original images, second row: watermarked images, third row: recovered watermarks
    fig, axes = plt.subplots(3, 3, figsize=(12, 12))
    for i in range(3):
        axes[0, i].imshow(images_rgb[i])
        axes[0, i].set_title("Original Image")
        axes[0, i].axis("off")

        axes[1, i].imshow(watermarked_images_rgb[i])
        axes[1, i].set_title("Watermarked Image")
        axes[1, i].axis("off")

        axes[2, i].imshow(recovered_watermarks_rgb[i])
        axes[2, i].set_title("Recovered Watermark")
        axes[2, i].axis("off")
    plt.tight_layout()
    plt.savefig("plots/task1_results.png", metadata={"Author": getpass.getuser()})
