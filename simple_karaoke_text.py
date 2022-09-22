#!/usr/bin/env python

# This example shows how to use pygame to build a graphic frontend for
#  a karaoke application. 
# Requires: pygame.

import midi_parser, time, datetime, sys
import pygame


def simple_karaoke_text():
    print('Please enter filename of .mid or .kar file:')
    filename = input()
    pygame.init()
    screenx = 1200
    screeny = 600
    screen = pygame.display.set_mode([screenx, screeny])
    font = pygame.font.Font(None, 60)
    color1 = (100, 100, 250, 0)
    color2 = (250, 250, 250, 0)

    m = midi_parser.MidiParser()
    m.load_file(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(0, 0)  # Start song at 0 and don't loop
    start = datetime.datetime.now()

    if not m.karfile:
        print("This is not a karaoke file. I'll just play it")
        while pygame.mixer.music.get_busy():
            time.sleep(1)
        sys.exit(0)

    rect = pygame.Rect((0, 0), (32, 32))
    # start=start-datetime.timedelta(0,9) # To start lyrics at a later point
    dt = 0.
    while pygame.mixer.music.get_busy():
        dt = (datetime.datetime.now() - start).total_seconds()
        m.update_karaoke(dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    rect.move_ip(0, -2)
                elif event.key == pygame.K_s:
                    rect.move_ip(0, 2)
                elif event.key == pygame.K_a:
                    rect.move_ip(-2, 0)
                elif event.key == pygame.K_d:
                    rect.move_ip(2, 0)
        for iline in range(3):
            l = font.size(m.karlinea[iline] + m.karlineb[iline])[0]
            x0a = screenx / 2 - l / 2.
            linea = font.render(m.karlinea[iline], 0, color1)
            lineb = font.render(m.karlineb[iline], 0, color2)
            recta = screen.blit(linea, [x0a, 80 + iline * 60])
            x0b = x0a + recta.width
            recbt = screen.blit(lineb, [x0b, 80 + iline * 60])

        pygame.display.update()
        screen.fill(0)

        time.sleep(.1)
