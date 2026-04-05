import json

WIDTH  = 500
HEIGHT = 200
TILE   = 32

FLOOR     = 388  # warm wood tile from WA_Room_Builder
COLLISION = 3    # WA_Special_Zones collision tile
WALL      = 13   # dark charcoal tile from WA_Room_Builder

# 2-tile border
BORDER = 2

def make_grid(default=0):
    return [[default] * WIDTH for _ in range(HEIGHT)]

def is_interior(r, c):
    return BORDER <= r < HEIGHT - BORDER and BORDER <= c < WIDTH - BORDER

# Floor layer — fill inside the border
floor = make_grid(0)
for r in range(HEIGHT):
    for c in range(WIDTH):
        if is_interior(r, c):
            floor[r][c] = FLOOR

# Wall layer — dark charcoal border tiles
walls = make_grid(0)
for r in range(HEIGHT):
    for c in range(WIDTH):
        if not is_interior(r, c):
            walls[r][c] = WALL

# Collision layer — block the border
collisions = make_grid(0)
for r in range(HEIGHT):
    for c in range(WIDTH):
        if not is_interior(r, c):
            collisions[r][c] = COLLISION

def flatten(grid):
    result = []
    for row in grid:
        result.extend(row)
    return result

# Spawn point — dead centre
SPAWN_X = (WIDTH  // 2) * TILE   # 1600
SPAWN_Y = (HEIGHT // 2) * TILE   # 1600

map_data = {
    "compressionlevel": -1,
    "height": HEIGHT,
    "infinite": False,
    "layers": [
        {
            "data": flatten(floor),
            "height": HEIGHT,
            "id": 1,
            "name": "floor",
            "opacity": 1,
            "type": "tilelayer",
            "visible": True,
            "width": WIDTH,
            "x": 0,
            "y": 0
        },
        {
            "data": flatten(walls),
            "height": HEIGHT,
            "id": 2,
            "name": "walls",
            "opacity": 1,
            "type": "tilelayer",
            "visible": True,
            "width": WIDTH,
            "x": 0,
            "y": 0
        },
        {
            "data": flatten(collisions),
            "height": HEIGHT,
            "id": 3,
            "name": "collisions",
            "opacity": 1,
            "type": "tilelayer",
            "visible": False,
            "width": WIDTH,
            "x": 0,
            "y": 0
        },
        {
            "draworder": "topdown",
            "id": 4,
            "name": "floorLayer",
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
                    "x": SPAWN_X,
                    "y": SPAWN_Y
                }
            ],
            "opacity": 1,
            "type": "objectgroup",
            "visible": True,
            "x": 0,
            "y": 0
        }
    ],
    "nextlayerid": 5,
    "nextobjectid": 2,
    "orientation": "orthogonal",
    "renderorder": "right-down",
    "tiledversion": "1.10.2",
    "tileheight": TILE,
    "tilesets": [
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
            "tileheight": TILE,
            "tiles": [
                {
                    "id": 2,
                    "properties": [
                        {
                            "name": "collides",
                            "type": "bool",
                            "value": True
                        }
                    ]
                }
            ],
            "tilewidth": TILE
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
            "tileheight": TILE,
            "tilewidth": TILE
        }
    ],
    "tilewidth": TILE,
    "type": "map",
    "version": "1.10",
    "width": WIDTH
}

output_path = "library.tmj"
with open(output_path, "w") as f:
    json.dump(map_data, f, indent=2)

print(f"Done. {WIDTH}x{HEIGHT} map written to {output_path}")
print(f"Spawn point: ({SPAWN_X}, {SPAWN_Y}) — tile ({WIDTH//2}, {HEIGHT//2})")