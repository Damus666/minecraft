from pygame_helper.pygame_helper import *
from perlin_noise import PerlinNoise

s = init_setup(1000,1000,"hi")

noise = PerlinNoise(0.12)

rects = []

for x in range(100):
    for y in range(100):
        n = noise.noise((x*1,y*1))
        if n < 0.08:
            rects.append(pygame.Rect(x*10,y*10,10,10))

while True:
    for e in get_events():
        exit_event(e)

    fill_window("black")

    for r in rects:
        pygame.draw.rect(s,"white",r)

    update_window(60)

