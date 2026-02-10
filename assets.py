import pygame

_image_cache = {}
_sound_cache = {}
_font_cache = {}
_sysfont_cache = {}


def load_image(path, convert_alpha=True, scale=None, smooth=False, flip_x=False, flip_y=False):
    key = (path, convert_alpha, scale, smooth, flip_x, flip_y)
    cached = _image_cache.get(key)
    if cached is not None:
        return cached
    image = pygame.image.load(path)
    if convert_alpha is True:
        image = image.convert_alpha()
    elif convert_alpha is False:
        image = image.convert()
    if scale is not None:
        if smooth:
            image = pygame.transform.smoothscale(image, scale)
        else:
            image = pygame.transform.scale(image, scale)
    if flip_x or flip_y:
        image = pygame.transform.flip(image, flip_x, flip_y)
    _image_cache[key] = image
    return image


def load_sound(path):
    cached = _sound_cache.get(path)
    if cached is not None:
        return cached
    sound = pygame.mixer.Sound(path)
    _sound_cache[path] = sound
    return sound


def load_font(path, size):
    key = (path, size)
    cached = _font_cache.get(key)
    if cached is not None:
        return cached
    font = pygame.font.Font(path, size)
    _font_cache[key] = font
    return font


def load_sysfont(name, size):
    key = (name, size)
    cached = _sysfont_cache.get(key)
    if cached is not None:
        return cached
    font = pygame.font.SysFont(name, size)
    _sysfont_cache[key] = font
    return font


def clear_caches():
    _image_cache.clear()
    _sound_cache.clear()
    _font_cache.clear()
    _sysfont_cache.clear()
