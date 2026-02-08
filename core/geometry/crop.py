def crop_boxes(img, boxes):
    """
    Crop image into sub-images using boxes.
    """
    return [img.crop((b.x1, b.y1, b.x2, b.y2)) for b in boxes]
