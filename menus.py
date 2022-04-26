from pybricks.parameters import Port, Stop, Direction, Button, Color
import lib

def menuShowAll(ev3, items: List[str]) -> int:
    current = 0
    refresh(ev3, items, current)
    while True:
        pressed = ev3.buttons.pressed()
        if Button.CENTER in pressed:
            ev3.speaker.beep()
            return current
        elif Button.UP in pressed or Button.LEFT in pressed:
            current = (current - 1) % len(items)
            refresh(ev3, items, current)
            ev3.speaker.beep()
        elif Button.DOWN in pressed or Button.RIGHT in pressed:
            current = (current + 1) % len(items)
            refresh(ev3, items, current)
            ev3.speaker.beep()

def refresh(ev3, items: List[str], current: int):
    ev3.screen.clear()
    for i, item in enumerate(items):
        fore, back = (Color.BLACK, Color.WHITE) if i != current else (Color.WHITE, Color.BLACK)
        ev3.screen.draw_text(0, i * lib.TEXT_HEIGHT, item, text_color=fore, background_color=back)
         
