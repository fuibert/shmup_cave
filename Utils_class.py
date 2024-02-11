import pygame
import numpy as np

def make_hitted_image(image):
    # making a red shade with transparency
    surf = image.convert_alpha()
    redshade = pygame.Surface(surf.get_rect().size).convert_alpha()
    redshade.fill((255, 0, 0, 100))  # red with alpha

    # merging the alpha chanel of base image on the redshade, keeping minimum values (most transparent) in each pixel
    alpha_basemask = pygame.surfarray.array_alpha(surf)
    alpha_redmask = pygame.surfarray.pixels_alpha(redshade)
    np.minimum(alpha_basemask, alpha_redmask, out=alpha_redmask)

    # deleting the alpha_redmask reference to unlock redshade (or it cannot be blit)
    del alpha_redmask

    # reddening a copy of the original image
    redsurf = surf.copy()
    redsurf.blit(redshade, (0, 0))
    return redsurf

def load_explosions_sprites():
    images = []
    for i in range(1, 7 + 1) :
        images.append(pygame.image.load("textures/explosions/Explosion_" + str(i) + '.png'))
    return images