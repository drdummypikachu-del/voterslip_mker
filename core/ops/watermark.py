import numpy as np
from PIL import Image

def remove_gray_watermark(img, lower=175, upper=225):
    """
    Remove gray watermark via luminance thresholding.
    """
    gray = img.convert("L")
    arr = np.array(gray)

    mask = (arr >= lower) & (arr <= upper)
    arr[mask] = 255

    return Image.fromarray(arr)
