"""
Geometry configurations for voter slip extraction.

All values are in pixels at 300 DPI.
These are pure data objects – no logic.
"""

# -------------------------
# Page 3 geometry
# -------------------------

PAGE3 = {
    "NAME": "PAGE3",
    "START_X": 280,
    "START_Y": 474,
    "BOX_W": 977,
    "BOX_H": 328,
    "GAP_X": 9,
    "GAP_Y": 9,
    "ROWS": 6,
    "COLS": 3,
}

# -------------------------
# All other pages geometry
# -------------------------

OTHER = {
    "NAME": "OTHER",
    "START_X": 281,
    "START_Y": 133,
    "BOX_W": 975,
    "BOX_H": 326,
    "GAP_X": 11,
    "GAP_Y": 11,
    "ROWS": 6,
    "COLS": 3,
}

# -------------------------
# Registry (for future use)
# -------------------------

GEOMETRIES = {
    "page3": PAGE3,
    "other": OTHER,
}
