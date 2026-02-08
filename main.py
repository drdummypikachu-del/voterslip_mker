from pathlib import Path

from core.io.pdf import pdf_to_images
from core.geometry.boxes import generate_boxes
from core.geometry.crop import crop_boxes
from core.ops.watermark import remove_gray_watermark
from core.ops.normalize import normalize_width
from core.render.header import generate_header
from core.render.footer import generate_footer
from core.compose.voter_slip import compose_voter_slip
from core.layout.grid import grid_layout

from PIL import Image

# -------------------------
# GLOBAL CONFIG
# -------------------------

DPI = 300

# Geometry configs
from configs.geometry import PAGE3, OTHER

# Assets
FONT_PATH = Path("assets/fonts/NotoSerifBengali-Regular.ttf")

# Header/footer layout
WIDTH = 1400
HEADER1_PATH = Path("assets/header1.png")   # static header
HEADER2_HEIGHT = 220
FOOTER_HEIGHT = 120
FONT_SIZE = 36

# PDF layout
GRID_COLS = 2
GRID_ROWS = 4
PAD_X = 70
PAD_Y = 70


# -------------------------
# Helpers (IO shell only)
# -------------------------

def save_image(img, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, dpi=(DPI, DPI))


def load_image(path):
    return Image.open(path).convert("L")


# -------------------------
# Stage A: PDF → voter slips
# -------------------------

def extract_voter_slips(pdf_path: Path, out_dir: Path):
    pages = pdf_to_images(pdf_path, dpi=DPI)
    out_dir.mkdir(parents=True, exist_ok=True)

    index = 1

    for page_idx, page in enumerate(pages):
        if page_idx < 2:
            continue

        geom = PAGE3 if page_idx == 2 else OTHER
        boxes = generate_boxes(geom)
        crops = crop_boxes(page, boxes)

        for img in crops:
            clean = remove_gray_watermark(img)
            save_image(clean, out_dir / f"{index:07d}.png")
            index += 1

    return index - 1


# -------------------------
# Stage B: headers & footers
# -------------------------

def build_header_footer(folder: Path):
    cfg = folder / "config.txt"
    if not cfg.exists():
        return None, None

    lines = cfg.read_text(encoding="utf-8").splitlines()
    if len(lines) < 4:
        raise ValueError(f"{cfg} must contain 4 lines")

    header2 = generate_header(
        lines=lines[:3],
        width=WIDTH,
        height=HEADER2_HEIGHT,
        font_path=FONT_PATH,
        font_size=FONT_SIZE,
    )

    footer = generate_footer(
        text=lines[3],
        width=WIDTH,
        height=FOOTER_HEIGHT,
        font_path=FONT_PATH,
        font_size=FONT_SIZE,
    )

    save_image(header2, folder / "header2.png")
    save_image(footer, folder / "footer.png")

    return header2, footer


# -------------------------
# Stage C: compose slips
# -------------------------

def compose_folder_slips(folder: Path):
    header1 = load_image(HEADER1_PATH)
    header2 = load_image(folder / "header2.png")
    footer = load_image(folder / "footer.png")

    for img_path in sorted(folder.glob("*.png")):
        if img_path.name.startswith("header"):
            continue
        if img_path.name.startswith("footer"):
            continue

        main_img = load_image(img_path)

        final = compose_voter_slip(
            main_img,
            header1,
            header2,
            footer,
            normalize_mode="scale",
        )

        save_image(final, img_path)


# -------------------------
# Stage D: images → PDF
# -------------------------

def make_pdf_from_folder(folder: Path):
    images = [load_image(p) for p in sorted(folder.glob("*.png"))]
    if not images:
        return

    pages = grid_layout(
        images,
        cols=GRID_COLS,
        rows=GRID_ROWS,
        pad_x=PAD_X,
        pad_y=PAD_Y,
    )

    output = folder.parent / f"out_{folder.name}.pdf"
    pages[0].save(
        output,
        save_all=True,
        append_images=pages[1:],
        dpi=(DPI, DPI),
    )


# -------------------------
# MAIN PIPELINE
# -------------------------

def main(input_root: Path):
    for pdf in sorted(input_root.glob("*.pdf")):
        out_dir = input_root / pdf.stem
        print(f"Processing PDF: {pdf.name}")

        count = extract_voter_slips(pdf, out_dir)
        print(f"  extracted {count} slips")

        header2, footer = build_header_footer(out_dir)
        if header2 is None:
            print("  skipped (no config.txt)")
            continue

        compose_folder_slips(out_dir)
        make_pdf_from_folder(out_dir)

        print("  done")


# -------------------------
# ENTRY POINT
# -------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python main.py <input_folder>")
        sys.exit(1)

    main(Path(sys.argv[1]))
