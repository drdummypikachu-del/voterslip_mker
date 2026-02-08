from pdf2image import convert_from_path
from PIL import Image

def pdf_to_images(pdf_path, dpi=300):
    """
    Convert PDF to list of PIL Images.
    """
    return convert_from_path(pdf_path, dpi=dpi)


def images_to_pdf(images, dpi=(300, 300)):
    """
    Convert list of PIL Images to a multipage PDF (in memory).
    """
    if not images:
        raise ValueError("No images provided")

    first, rest = images[0], images[1:]
    return first.save(
        None,
        format="PDF",
        save_all=True,
        append_images=rest,
        dpi=dpi
    )
