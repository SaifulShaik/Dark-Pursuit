import json
import pygame

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, -1)])): 0, # left top
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1, # top
    tuple(sorted([(-1, 0), (0, -1)])): 2, #corner right top
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 3, # right
    tuple(sorted([(-1, 0), (0, 1)])): 4, # corner right bottom
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 5, # bottom
    tuple(sorted([(1, 0), (0, 1)])): 6, # corner left bottom
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7, # left
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8, # filler
    tuple(sorted([(0, 1)])): 9, # one side covered top
    tuple(sorted([(0, -1)])): 10, # one side covered bottom
    tuple(sorted([(0, 1), (0, -1)])): 11, # two side covered (up and bottom)
    tuple(sorted([(-1, 0)])): 12, # one side covered left
    tuple(sorted([(1, 0)])): 13, # one side covered right
    tuple(sorted([(1, 0), (-1, 0)])): 14, # two side covered (left and right)
    tuple(sorted([])): 15, # empty
}

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}
AUTOTILE_TYPES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        
    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)
                    
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]
        
        return matches
    
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()
        
    def load(self, path):
        with open(path, 'r') as f:
            content = f.read().strip()
            if not content:
                print(f"Warning: File {path} is empty or invalid")
                return
            map_data = json.loads(content)
        
        self.tilemap = map_data.get('tilemap', {})
        self.tile_size = map_data.get('tile_size', self.tile_size)
        self.offgrid_tiles = map_data.get('offgrid', [])
        
    def solid_check(self, pos):
        tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc]
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
            
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
