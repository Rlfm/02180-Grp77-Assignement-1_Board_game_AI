from asciimatics.screen import Screen
import time

def animate(screen):
    x = 0
    y = 0
    while True:
        screen.print_at('X', x, y)
        screen.refresh()
        time.sleep(0.1)
        screen.print_at(' ', x, y)
        x += 1
        y += 1
        if x >= screen.width or y >= screen.height:
            x = 0
            y = 0

Screen.wrapper(animate)