import pygame
import pytmx



class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):

        temp_surface = pygame.Surface((self.width * 2, self.height * 2))

        self.render(temp_surface)
        return temp_surface


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h,group):
        pygame.sprite.Sprite.__init__(self, group)
        self.rect = pygame.Rect(x, y, w, h)



