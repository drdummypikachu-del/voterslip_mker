from PIL import Image

def stack_vertical(images, bg=255):
    """
    Stack images vertically.
    """
    if not images:
        raise ValueError("No images to stack")

    width = max(img.width for img in images)
    height = sum(img.height for img in images)

    canvas = Image.new("L", (width, height), bg)

    y = 0
    for img in images:
        canvas.paste(img, (0, y))
        y += img.height

    return canvas
