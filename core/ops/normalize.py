from PIL import Image

def resize_to_width(img, target_width):
    """
    Proportionally scale image to target width.
    """
    scale = target_width / img.width
    new_height = int(img.height * scale)
    return img.resize((target_width, new_height), Image.LANCZOS)


def pad_to_width(img, target_width, bg=255):
    """
    Center image inside target width without scaling.
    """
    if img.width >= target_width:
        return img

    canvas = Image.new("L", (target_width, img.height), bg)
    x = (target_width - img.width) // 2
    canvas.paste(img, (x, 0))
    return canvas


def normalize_width(img, target_width, mode="scale"):
    """
    Normalize image width using selected strategy.
    """
    if mode == "scale":
        return resize_to_width(img, target_width)
    elif mode == "pad":
        return pad_to_width(img, target_width)
    else:
        raise ValueError(f"Unknown normalize mode: {mode}")
