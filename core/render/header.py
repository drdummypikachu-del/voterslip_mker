from PIL import Image, ImageDraw, ImageFont

def generate_header(
    lines,
    width,
    height,
    font_path,
    font_size,
    margin_x=40,
    bg=255,
):
    """
    Render multi-line header image.
    """
    img = Image.new("L", (width, height), bg)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)

    draw.text((margin_x, 30), lines[0], fill=0, font=font)
    draw.text((margin_x, 100), lines[1], fill=0, font=font)

    bbox = draw.textbbox((0, 0), lines[2], font=font)
    text_w = bbox[2] - bbox[0]

    draw.text(
        (width - text_w - margin_x, 100),
        lines[2],
        fill=0,
        font=font
    )

    return img
