import json
import math

WIDTH  = 500
HEIGHT = 200
TILE   = 32

FLOOR     = 388  # warm wood from WA_Room_Builder
COLLISION = 3    # WA_Special_Zones collision tile
WALL      = 13   # dark charcoal from WA_Room_Builder

BORDER = 2

# Colourful bookshelf tiles (WA_Other_Furniture, 2 wide x 3 tall)
SHELF_TOP = [1023, 1024]
SHELF_MID = [1035, 1036]
SHELF_BOT = [1047, 1048]

# 6 pages — name and URL
PAGES = [
    ("Organisations",       "https://www.aprntcshp.co.uk/organisations"),
    ("Find Apprenticeships","https://www.aprntcshp.co.uk/find-apprenticeships"),
    ("Companies",           "https://www.aprntcshp.co.uk/companies"),
    ("Industries",          "https://www.aprntcshp.co.uk/industries"),
    ("Resources",           "https://www.aprntcshp.co.uk/cv-resources"),
    ("Communities",         "https://www.aprntcshp.co.uk/communities"),
]

def make_grid(default=0):
    return [[default] * WIDTH for _ in range(HEIGHT)]

def is_interior(r, c):
    return BORDER <= r < HEIGHT - BORDER and BORDER <= c < WIDTH - BORDER

# Floor
floor = make_grid(0)
for r in range(HEIGHT):
    for c in range(WIDTH):
        if is_interior(r, c):
            floor[r][c] = FLOOR

# Walls
walls = make_grid(0)
for r in range(HEIGHT):
    for c in range(WIDTH):
        if not is_interior(r, c):
            walls[r][c] = WALL

# Collisions
collisions = make_grid(0)
for r in range(HEIGHT):
    for c in range(WIDTH):
        if not is_interior(r, c):
            collisions[r][c] = COLLISION

# Furniture layer — bookshelves
furniture = make_grid(0)

def place_shelf(row, col):
    for i, gid in enumerate(SHELF_TOP): furniture[row][col + i]     = gid
    for i, gid in enumerate(SHELF_MID): furniture[row + 1][col + i] = gid
    for i, gid in enumerate(SHELF_BOT): furniture[row + 2][col + i] = gid

# Arc of 6 shelves above spawn
# Arc centre slightly above spawn (250, 100), radius 35 tiles
CX, CY = 250, 83
RADIUS = 35
angles = [180 + i * (180 / 5) for i in range(6)]  # spread 180°–360°

shelf_positions = []
for angle in angles:
    rad = math.radians(angle)
    col = round(CX + RADIUS * math.cos(rad))
    row = round(CY + RADIUS * math.sin(rad))
    shelf_positions.append((row, col))
    place_shelf(row, col)

def flatten(grid):
    result = []
    for row in grid:
        result.extend(row)
    return result

# Spawn dead centre
SPAWN_X = (WIDTH  // 2) * TILE
SPAWN_Y = (HEIGHT // 2) * TILE

map_data = {
    "compressionlevel": -1,
    "height": HEIGHT,
    "infinite": False,
    "layers": [
        {
            "data": flatten(floor),
            "height": HEIGHT, "id": 1, "name": "floor",
            "opacity": 1, "type": "tilelayer", "visible": True,
            "width": WIDTH, "x": 0, "y": 0
        },
        {
            "data": flatten(walls),
            "height": HEIGHT, "id": 2, "name": "walls",
            "opacity": 1, "type": "tilelayer", "visible": True,
            "width": WIDTH, "x": 0, "y": 0
        },
        {
            "data": flatten(collisions),
            "height": HEIGHT, "id": 3, "name": "collisions",
            "opacity": 1, "type": "tilelayer", "visible": False,
            "width": WIDTH, "x": 0, "y": 0
        },
        {
            "data": flatten(furniture),
            "height": HEIGHT, "id": 4, "name": "furniture",
            "opacity": 1, "type": "tilelayer", "visible": True,
            "width": WIDTH, "x": 0, "y": 0
        },
        {
            "draworder": "topdown",
            "id": 5,
            "name": "floorLayer",
            "objects": [
                {
                    "height": 0, "id": 1, "name": "start",
                    "point": True, "rotation": 0, "type": "",
                    "visible": True, "width": 0,
                    "x": SPAWN_X, "y": SPAWN_Y
                }
            ],
            "opacity": 1, "type": "objectgroup", "visible": True,
            "x": 0, "y": 0
        }
    ],
    "nextlayerid": 6,
    "nextobjectid": 2,
    "orientation": "orthogonal",
    "renderorder": "right-down",
    "tiledversion": "1.10.2",
    "tileheight": TILE,
    "tilesets": [
        {
            "columns": 6, "firstgid": 1,
            "image": "tilesets/WA_Special_Zones.png",
            "imageheight": 64, "imagewidth": 192,
            "margin": 0, "name": "WA_Special_Zones",
            "spacing": 0, "tilecount": 12,
            "tileheight": TILE,
            "tiles": [{"id": 2, "properties": [{"name": "collides", "type": "bool", "value": True}]}],
            "tilewidth": TILE
        },
        {
            "columns": 25, "firstgid": 13,
            "image": "tilesets/WA_Room_Builder.png",
            "imageheight": 1280, "imagewidth": 800,
            "margin": 0, "name": "WA_Room_Builder",
            "spacing": 0, "tilecount": 1000,
            "tileheight": TILE, "tilewidth": TILE
        },
        {
            "columns": 12, "firstgid": 1013,
            "image": "tilesets/WA_Other_Furniture.png",
            "imageheight": 416, "imagewidth": 384,
            "margin": 0, "name": "WA_Other_Furniture",
            "spacing": 0, "tilecount": 156,
            "tileheight": TILE, "tilewidth": TILE
        }
    ],
    "tilewidth": TILE,
    "type": "map",
    "version": "1.10",
    "width": WIDTH
}

output_path = "library.tmj"
with open(output_path, "w") as f:
    json.dump(map_data, f)

print(f"Done. {WIDTH}x{HEIGHT} map written to {output_path}")
print(f"Spawn: tile ({WIDTH//2}, {HEIGHT//2})")
print()
print("Shelf positions (for WorkAdventure interactive zones):")
for (row, col), (name, url) in zip(shelf_positions, PAGES):
    print(f"  {name}")
    print(f"    tile: col={col}, row={row}  |  px: x={col*TILE}, y={row*TILE}")
    print(f"    url: {url}")