from dataclasses import dataclass

@dataclass(frozen=True)
class Box:
    x1: int
    y1: int
    x2: int
    y2: int


def generate_boxes(geom: dict) -> list[Box]:
    """
    Generate crop boxes from grid geometry.
    """
    boxes = []
    for r in range(geom["ROWS"]):
        for c in range(geom["COLS"]):
            x1 = geom["START_X"] + c * (geom["BOX_W"] + geom["GAP_X"])
            y1 = geom["START_Y"] + r * (geom["BOX_H"] + geom["GAP_Y"])
            boxes.append(Box(
                x1,
                y1,
                x1 + geom["BOX_W"],
                y1 + geom["BOX_H"],
            ))
    return boxes
