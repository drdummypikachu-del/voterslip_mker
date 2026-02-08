from core.ops.normalize import normalize_width
from core.ops.stack import stack_vertical

def compose_voter_slip(
    main_img,
    header1,
    header2,
    footer,
    normalize_mode="scale",
):
    """
    Compose final voter slip image.
    """
    target_width = header1.width

    main_img = normalize_width(main_img, target_width, normalize_mode)
    header2 = normalize_width(header2, target_width, normalize_mode)
    footer = normalize_width(footer, target_width, normalize_mode)

    return stack_vertical([
        header1,
        header2,
        main_img,
        footer
    ])
