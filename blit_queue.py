import pygame


class GraphicsQueue:
    def __init__(self):
        pass

    def blit_queue(self, surface, array):
        # sort by id in queues
        array = sorted(array, key=lambda item: item.get("layer"))
        # re-arrange image layer index based on y value
        array = sorted(array, key=lambda item: item.get("pos")[1])
        # first layers

        # circles without width, width == 0
        # [pygame.draw.circle(surface, obj['color'], obj['pos'], obj['radius']) for obj in array if obj['type'] == 'circle' and obj['layer'] < 0]
        # images
        [surface.blit(obj['image'], obj['pos']) for obj in array if obj['type'] == 'image' and obj['layer'] < 0]

        # loop through the obj queue
        for obj in array:
            # circle, rect, image, layer 100 is reserved for the bottom walls on the level
            if obj['layer'] >= 0:
                if obj['type'] == 'image' and obj['layer'] != 100:
                    surface.blit(obj['image'], obj['pos'])
                elif obj['type'] == 'circle':
                    if obj['width'] != 0:
                        pygame.draw.circle(surface, obj['color'], obj['pos'], obj['radius'], obj['width'])
                    else:
                        pygame.draw.circle(surface, obj['color'], obj['pos'], obj['radius'])
                elif obj['type'] == 'rect' and not obj['layer'] >= 100:
                    if obj['radius'] != 0:
                        # radius acts as width here. mentioned in the CrossHairs class
                        pygame.draw.rect(surface, obj['color'], obj['rect'], obj['radius'])
                    else:
                        pygame.draw.rect(surface, obj['color'], obj['rect'])

        # bottom wall reserved for highest layer
        [surface.blit(obj['image'], obj['pos']) for obj in array if obj['type'] == 'image' and obj['layer'] >= 100]
        [pygame.draw.rect(surface, obj['color'], obj['rect'], obj['radius']) for obj in array if
         obj['type'] == 'rect' and obj['layer'] >= 100]
        # rect is points for polygon
        [pygame.draw.polygon(surface, obj['color'], obj['rect']) for obj in array if obj['type'] == 'polygon']

