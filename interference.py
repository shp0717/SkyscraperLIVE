import math, random


def strength(h, max_h, a=0.6, b=3.0):
    return a * (math.exp(b * h / max_h) - 1)


def strength2(h, max_h, a=0.6, b=3.0, w=None):
    h = h % max_h
    if w is None:
        w = max_h / math.pi
    s = strength(h, max_h, a, b)
    return s * math.sin(h / w)


def shake(h, max_h, wave=808.5, wind_force=1, t=0):
    u = lambda x: random.uniform(-x, x)
    return u(strength2(h, max_h, 0.1, 5.0)) + wind(h, max_h, wave, t) * wind_force


def wind(h, max_h, wave=808.5, t=0):
    return math.sin(h / wave + t * 0.02) * strength2(h, max_h, 0.0002, 10.0)
