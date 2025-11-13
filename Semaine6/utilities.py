from typing import Union
import numpy as np
from PIL import Image  # type: ignore


def foreground_filter(
    img: Union[Image.Image, np.ndarray], theta: int = 150
) -> np.ndarray:
    """Create a black and white image outlining the foreground."""
    M = np.array(img)  # In case this is not yet a Numpy array
    G = np.min(M[:, :, 0:3], axis=2)
    F = G < theta
    return F


def transparent_background_filter(
    img: Union[Image.Image, np.ndarray], foreground: np.ndarray
) -> Image.Image:
    """Make all pixels not in the foreground transparent."""
    M = np.array(img)
    N = np.zeros([M.shape[0], M.shape[1], 4], dtype=M.dtype)
    N[:, :, :3] = M[:, :, :3]
    N[:, :, 3] = foreground * 255
    return Image.fromarray(N)


def yellowness_filter(img: Union[Image.Image, np.ndarray]) -> np.ndarray:
    """Return a grey-level image measuring the yellowness of each pixel."""
    # Remplacer la ligne suivante par le code adéquat
    M = np.array(img)
    return M[:, :, 0]*1.0+M[:, :, 1]*1.0-M[:, :, 2]*1.0


def color_correlation_filter(
    img: Union[Image.Image, np.ndarray], color: np.ndarray
) -> np.ndarray:
    """Return a grey-level image measuring the correlation of the pixels
    with the given color."""
    img_array = np.array(img)

    correlation_image = np.zeros_like(img_array[:, :, 0], dtype=float)

    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            pixel_color = img_array[i, j, :]
            correlation = np.corrcoef(pixel_color, color)[0, 1]
            correlation_image[i, j] = correlation

    return correlation_image
