from PIL import Image, ImageDraw, ImageFont

def generate_footer(
    text,
    width,
    height,
    font_path,
    font_size,
    bg=255,
):
    """
    Render centered footer text.
    """
    img = Image.new("L", (width, height), bg)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)

    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (width - w) // 2
    y = (height - h) // 2

    draw.text((x, y), text, fill=0, font=font)
    return img
