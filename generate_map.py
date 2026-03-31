#!/usr/bin/env python3
"""Generate library.tmj (WorkAdventure / Tiled JSON) from 2D layer grids."""

import json
from pathlib import Path

W = H = 40

# Global tile IDs: WA_Room_Builder firstgid=13 (after 12 Special_Zones tiles).
# Former floor gid 376 (local 375) → 13 + 375 = 388
FLOOR_TILE = 388
# Former wall global 106 (local 105) → 13 + 105 = 118
WALL_TILE = 118
# WA_Special_Zones: firstgid 1, local id 2 with collides → global 3
COLLISION_TILE = 3
EMPTY = 0


def empty_grid() -> list[list[int]]:
    return [[EMPTY for _ in range(W)] for _ in range(H)]


def fill_rect(
    grid: list[list[int]], r0: int, r1: int, c0: int, c1: int, value: int
) -> None:
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            if 0 <= r < H and 0 <= c < W:
                grid[r][c] = value


def is_border(r: int, c: int) -> bool:
    return r == 0 or r == H - 1 or c == 0 or c == W - 1


def build_layers() -> tuple[
    list[list[int]],
    list[list[int]],
    list[list[int]],
    list[list[int]],
    list[list[int]],
]:
    floor_mask = empty_grid()
    rooms = [
        (28, 39, 14, 26),  # Entrance Hall
        (14, 27, 10, 30),  # Fireside
        (4, 14, 1, 10),  # Reading Room
        (4, 14, 29, 38),  # The Stacks
        (1, 4, 10, 30),  # Notice Board Corridor
        (1, 7, 1, 9),  # Employer Gallery
    ]
    for r0, r1, c0, c1 in rooms:
        fill_rect(floor_mask, r0, r1, c0, c1, 1)

    def cell_is_walkable(r: int, c: int) -> bool:
        return bool(floor_mask[r][c]) and not is_border(r, c)

    floor = empty_grid()
    walls = empty_grid()
    collisions = empty_grid()
    for r in range(H):
        for c in range(W):
            if cell_is_walkable(r, c):
                floor[r][c] = FLOOR_TILE
                walls[r][c] = EMPTY
                collisions[r][c] = EMPTY
            else:
                floor[r][c] = EMPTY
                walls[r][c] = WALL_TILE
                collisions[r][c] = COLLISION_TILE

    furniture = empty_grid()
    floor_layer = empty_grid()

    return floor, floor_layer, walls, furniture, collisions


def flatten_row_major(grid: list[list[int]]) -> list[int]:
    out: list[int] = []
    for r in range(H):
        out.extend(grid[r])
    return out


def main() -> None:
    floor, floor_layer, walls, furniture, collisions = build_layers()

    root = Path(__file__).resolve().parent
    out_path = root / "library.tmj"

    tilesets = [
        {
            "columns": 6,
            "firstgid": 1,
            "image": "tilesets/WA_Special_Zones.png",
            "imageheight": 64,
            "imagewidth": 192,
            "margin": 0,
            "name": "WA_Special_Zones",
            "spacing": 0,
            "tilecount": 12,
            "tileheight": 32,
            "tiles": [
                {
                    "id": 2,
                    "properties": [
                        {
                            "name": "collides",
                            "type": "bool",
                            "value": True,
                        }
                    ],
                }
            ],
            "tilewidth": 32,
        },
        {
            "columns": 25,
            "firstgid": 13,
            "image": "tilesets/WA_Room_Builder.png",
            "imageheight": 1280,
            "imagewidth": 800,
            "margin": 0,
            "name": "WA_Room_Builder",
            "spacing": 0,
            "tilecount": 1000,
            "tileheight": 32,
            "tilewidth": 32,
        },
        {
            "columns": 12,
            "firstgid": 1013,
            "image": "tilesets/WA_Other_Furniture.png",
            "imageheight": 416,
            "imagewidth": 384,
            "margin": 0,
            "name": "WA_Other_Furniture",
            "spacing": 0,
            "tilecount": 156,
            "tileheight": 32,
            "tilewidth": 32,
        },
        {
            "columns": 13,
            "firstgid": 1169,
            "image": "tilesets/WA_Seats.png",
            "imageheight": 448,
            "imagewidth": 416,
            "margin": 0,
            "name": "WA_Seats",
            "spacing": 0,
            "tilecount": 182,
            "tileheight": 32,
            "tilewidth": 32,
        },
        {
            "columns": 10,
            "firstgid": 1351,
            "image": "tilesets/WA_Tables.png",
            "imageheight": 864,
            "imagewidth": 320,
            "margin": 0,
            "name": "WA_Tables",
            "spacing": 0,
            "tilecount": 270,
            "tileheight": 32,
            "tilewidth": 32,
        },
        {
            "columns": 12,
            "firstgid": 1621,
            "image": "tilesets/WA_Decoration.png",
            "imageheight": 256,
            "imagewidth": 384,
            "margin": 0,
            "name": "WA_Decoration",
            "spacing": 0,
            "tilecount": 96,
            "tileheight": 32,
            "tilewidth": 32,
        },
    ]

    m = {
        "compressionlevel": -1,
        "height": H,
        "infinite": False,
        "layers": [
            {
                "data": flatten_row_major(floor),
                "height": H,
                "id": 1,
                "name": "floor",
                "opacity": 1,
                "type": "tilelayer",
                "visible": True,
                "width": W,
                "x": 0,
                "y": 0,
            },
            {
                "data": flatten_row_major(floor_layer),
                "height": H,
                "id": 2,
                "name": "floorLayer",
                "opacity": 1,
                "type": "tilelayer",
                "visible": True,
                "width": W,
                "x": 0,
                "y": 0,
            },
            {
                "data": flatten_row_major(walls),
                "height": H,
                "id": 3,
                "name": "walls",
                "opacity": 1,
                "type": "tilelayer",
                "visible": True,
                "width": W,
                "x": 0,
                "y": 0,
            },
            {
                "data": flatten_row_major(furniture),
                "height": H,
                "id": 4,
                "name": "furniture",
                "opacity": 1,
                "type": "tilelayer",
                "visible": True,
                "width": W,
                "x": 0,
                "y": 0,
            },
            {
                "data": flatten_row_major(collisions),
                "height": H,
                "id": 5,
                "name": "collisions",
                "opacity": 1,
                "type": "tilelayer",
                "visible": True,
                "width": W,
                "x": 0,
                "y": 0,
            },
            {
                "draworder": "topdown",
                "id": 6,
                "name": "start",
                "objects": [
                    {
                        "height": 0,
                        "id": 1,
                        "name": "start",
                        "point": True,
                        "rotation": 0,
                        "type": "",
                        "visible": True,
                        "width": 0,
                        "x": 640,
                        "y": 640,
                    }
                ],
                "opacity": 1,
                "type": "objectgroup",
                "visible": True,
                "x": 0,
                "y": 0,
            },
        ],
        "nextlayerid": 7,
        "nextobjectid": 2,
        "orientation": "orthogonal",
        "renderorder": "right-down",
        "tiledversion": "1.10.2",
        "tileheight": 32,
        "tilesets": tilesets,
        "tilewidth": 32,
        "type": "map",
        "version": "1.10",
        "width": W,
    }

    out_path.write_text(json.dumps(m, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
