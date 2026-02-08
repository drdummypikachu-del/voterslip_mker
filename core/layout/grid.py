from PIL import Image
import math

def grid_layout(
    images,
    cols,
    rows,
    pad_x=70,
    pad_y=70,
    bg=255,
):
    """
    Arrange images into paged grid layout.
    """
    per_page = cols * rows
    pages = []

    max_w = max(img.width for img in images)
    max_h = max(img.height for img in images)

    cell_w = max_w + pad_x * 2
    cell_h = max_h + pad_y * 2

    page_w = cols * cell_w
    page_h = rows * cell_h

    total_pages = math.ceil(len(images) / per_page)

    for p in range(total_pages):
        page = Image.new("L", (page_w, page_h), bg)

        for i in range(per_page):
            idx = p * per_page + i
            if idx >= len(images):
                break

            img = images[idx]
            col = i % cols
            row = i // cols

            x = col * cell_w + (cell_w - img.width) // 2
            y = row * cell_h + (cell_h - img.height) // 2

            page.paste(img, (x, y))

        pages.append(page)

    return pages
