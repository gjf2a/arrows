from pybricks.parameters import Port, Stop, Direction, Button, Color
import lib

def wait_until_clear(ev3):
    while len(ev3.buttons.pressed()) > 0:
        pass


def mod_inc(n: int, m: int) -> int:
    return (n + 1) % m

def mod_dec(n: int, m: int) -> int:
    return (n - 1) % m

def menuShowAll(ev3, items: List[str]) -> int:
    wait_until_clear(ev3)
    current = 0
    down = False
    refresh(ev3, items, current)
    while True:
        pressed = ev3.buttons.pressed()
        if len(pressed) > 0:
            if not down:
                ev3.speaker.beep()
                down = True
                if Button.CENTER in pressed:
                    return current
                elif Button.UP in pressed or Button.LEFT in pressed:
                    current = mod_dec(current, len(items))
                    refresh(ev3, items, current)
                elif Button.DOWN in pressed or Button.RIGHT in pressed:
                    current = mod_inc(current, len(items))
                    refresh(ev3, items, current)
        else:
            down = False

def refresh(ev3, items: List[str], current: int):
    ev3.screen.clear()
    for i, item in enumerate(items):
        fore, back = (Color.BLACK, Color.WHITE) if i != current else (Color.WHITE, Color.BLACK)
        ev3.screen.draw_text(0, i * lib.TEXT_HEIGHT, item, text_color=fore, background_color=back)
         
def menuManyOptions(ev3, list_labels: List[str], multi_option_list: List[List[str]]) -> List[int]:
    wait_until_clear(ev3)
    choices = [0] * len(multi_option_list)
    row = 0
    down = False
    refreshMany(ev3, multi_option_list, row, choices[row])
    while True:
        pressed = ev3.buttons.pressed()
        if len(pressed) > 0:
            if not down:
                ev3.speaker.beep()
                down = True
                if Button.CENTER in pressed:
                    return choices
                elif Button.UP in pressed:
                    row = mod_dec(row, len(multi_option_list))
                    refreshMany(ev3, multi_option_list, row, choices[row])
                elif Button.DOWN in pressed:
                    row =  mod_inc(row, len(multi_option_list))
                    refreshMany(ev3, multi_option_list, row, choices[row])
                elif Button.LEFT in pressed:
                    choices[row] = mod_dec(choices[row], len(multi_option_list[row]))
                    refreshMany(ev3, multi_option_list, row, choices[row])
                elif Button.RIGHT in pressed:
                    choices[row] = mod_inc(choices[row], len(multi_option_list[row]))
                    refreshMany(ev3, multi_option_list, row, choices[row])
        else:
            down = False


def refreshMany(ev3, multi_option_list: List[List[str]], row: int, option: int):
    ev3.screen.clear()
    for i, opt_list in enumerate(multi_option_list):
        fore, back = (Color.BLACK, Color.WHITE) if i != row else (Color.WHITE, Color.BLACK)
        ev3.screen.draw_text(0, i * lib.TEXT_HEIGHT, multi_option_list[row][option], text_color=fore, background_color=back)
