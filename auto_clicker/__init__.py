"""
Threaded class-based clicker
"""

import keyboard
import threading
from time import sleep
from math import sqrt, ceil
from ait import mouse, move, click as ait_click
from pynput.keyboard import Listener, KeyCode, Key

# Suppress reload output
from importlib import reload
import logging

# Configurations module
from . import _configurations as _config_module

cfg = _config_module.Configurations()
logging.getLogger().setLevel(logging.ERROR)


# ~~~ Clicker Tool-Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def smooth_mouse_move(x, y, step_px=25, step_s=0.005):
    # Get the starting position of the mouse
    x0, y0 = mouse()

    # Determine the distance to travel
    x_dist = abs(x - x0)
    y_dist = abs(y - y0)
    d = round(sqrt(x_dist**2 + y_dist**2))

    # Determine number of 100px steps
    steps = ceil(d / step_px)

    # No steps, skip...
    if steps == 0:
        return

    # If no duration, move step_px/step_s
    duration = round(steps * step_s, 2)

    # Determine the x & y steppings
    xs = round(x_dist / steps) * (-1 if x < x0 else 1)
    ys = round(y_dist / steps) * (-1 if y < y0 else 1)

    if cfg.debug:
        print(
            f"smooth_mouse_move: ({x0=}, {y0=}) --> ({xs=}, {ys=}) --> ({x=}, {y=}) "
            f"[{d=}/{steps=} | {duration=}s]"
        )

    # for each step, increment (x0, y0) by (xs, ys)
    for step in range(1, steps + 1):
        # Final step, exit, the final coords will be set by click()
        if step == steps:
            x0, y0 = tuple((x, y))

        # All other steps, increment by step_px and use move()
        else:
            x0 += xs
            y0 += ys

        if cfg.debug:
            print(f"                   ({x0=}, {y0=})")

        move(x0, y0)
        sleep(step_s)


def click(x=None, y=None, wait=None, click_after_move=True, **kwargs):
    if None not in [x, y]:
        smooth_mouse_move(x, y, **kwargs)

    if click_after_move:
        ait_click()

    if wait is not None:
        sleep(wait)


def _start_message():
    _print_message("0", bCap=True, sEnd="\r")
    _print_message("Welcome to Ryan's autoclicker!", bCap=False, sEnd="\n")
    _print_message(
        "If something goes wrong, it's definitely his fault.", bCap=True, sEnd="\n"
    )


def _print_message(sMsg, bCap=True, sEnd="\n"):
    """
    Worst case...82
    "   | Key: space | Pos: (nnnn, nnnn) | Move: Active | Click: Active | Mouse Move: Active |"
          ^                                                                                ^
          |                                                                                |
          +--------------------------------------------------------------------------------+
    from..here....................................to....................................here
    """
    width = 82

    lMsg = [f"   | {sMsg[i:i+width]:<{width}} |" for i in range(0, len(sMsg), width)]
    lMsg = [lMsg[0]] if sEnd == "\r" else lMsg

    for msg in lMsg:
        print(msg, end=sEnd)

    if bCap:
        print(f'   +-{"-" * width}-+')


def _countdown(nSeconds):
    nLoop = int(nSeconds)
    nRemainder = nSeconds - nLoop
    for second in range(nLoop, 0, -1):
        print(f"{second:03}", end="\r")
        sleep(1)
    sleep(nRemainder)


def _press_keys(keys):
    for key in keys:
        keyboard.press_and_release(key)


# ~~~ Clicker Sub-Classes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ClickThread(threading.Thread):
    """Base Inheritable class

    From Thread():
        self.name
        self.ident
        self.daemon
        self.getName()
        self.isAlive()
        self.isDaemon()
        self.is_alive()
        self.join()
        self.run()
        self.setDaemon()
        self.setName()
        self.start()
    """

    def __init__(self):
        super().__init__()
        self.running = False
        self.program_running = True

    @property
    def status(self):
        return "Active" if self.running else "Idle"

    @property
    def go(self):
        self.running = True

    @property
    def pause(self):
        self.running = False

    @property
    def toggle(self):
        self.pause if self.running else self.go

    @property
    def exit(self):
        self.pause
        self.program_running = False

    def loop(self, func):
        while self.program_running:
            while self.running:
                func()
            sleep(0.001)


class ClickMouse(ClickThread):
    def _click(self):
        _press_keys(cfg.press_keys)

        click(wait=cfg.click_delay_s)

    def run(self):
        self.loop(self._click)


class MoveClickMouse(ClickThread):
    def _click_loop(self):
        if cfg.debug:
            print(
                f"Clicks={list(cfg.mouse_moves_xys)}, click_after_move={cfg.click_after_move}"
            )

        for click_xys in cfg.mouse_moves_xys:
            x, y, pause_after_click_s = click_xys

            if not self.running:
                break

            if cfg.debug:
                print(f"requested_pos=({x=}, {y=})")

            # Click
            click(x, y, wait=None, click_after_move=cfg.click_after_move)

            if not self.running:
                break

            # Wait
            if cfg.debug:
                print(f"{pause_after_click_s=}")
                _countdown(pause_after_click_s)
            else:
                sleep(pause_after_click_s)

    def run(self):
        self.loop(self._click_loop)


class PressKeys(ClickThread):
    def _move_loop(self):
        if cfg.debug:
            print(f"keys={list(cfg.kb_moves_khw)=}")

        for key_sw in cfg.kb_moves_khw:
            key_to_press, sec_to_hold, pause_after_press_s = key_sw

            if not self.running:
                break

            if cfg.debug:
                print(f"{key_to_press=}")
                print(f"{sec_to_hold=}")

            # Press
            keyboard.press(key_to_press)
            sleep(sec_to_hold)
            keyboard.release(key_to_press)

            if cfg.debug:
                print(f"{pause_after_press_s=}")

            # Wait
            sleep(pause_after_press_s)

    def run(self):
        self.loop(self._move_loop)


# ~~~ Clicker Class ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Clicker_Main:
    def __init__(self):
        self.display_coords = Key.f2  # key to display the mouses current coordinates
        self.go_pause_wasd = Key.f3  # key to start movement loop
        self.go_pause_move = Key.f4  # key to start mouse movement loop
        self.go_pause_click = Key.f5  # key to start clicking
        self.reload_key = Key.f6  # key to reload the config module
        self.exit_key = Key.f7  # key to stop the clicker

        if cfg.debug:
            print(f"{cfg.click_delay=}")
            print(f"{cfg.mouse_moves=}")
            print(f"{cfg.kb_moves=}")

    def _on_press(self, key):
        # Create uniform key & string
        if isinstance(key, KeyCode):
            key_name = key.char
            k = key.vk
        elif isinstance(key, Key):
            key_name = key.name
            k = key
        else:
            raise ValueError(f"Unknown key: {key=} ({type(key)})")

        # Apparently sometimes the keys have no name, ignore those
        if key_name is None:
            _print_message(
                f"Unknown key [{key_name=}, {k=}]: {key=} ({type(key)})",
                bCap=False,
                sEnd="\r",
            )
            return

        # Show detected key-press
        if cfg.debug:
            _print_message(f"Key: {key_name}", bCap=False, sEnd="\r")

        # Determine new status
        mouse_pos = "" * 17
        if k == self.go_pause_click:
            self.click_thread.toggle

        elif k == self.go_pause_move:
            self.move_click_thread.toggle

        elif k == self.go_pause_wasd:
            self.key_press_thread.toggle

        elif k == self.display_coords:
            mouse_pos = f"Pos: {str(tuple(mouse())):^12}"

        elif k == self.reload_key:
            reload(_config_module)

        elif k == self.exit_key:
            self.listener.stop()
            self.click_thread.exit
            self.move_click_thread.exit
            self.key_press_thread.exit
            _print_message(
                f'Closing the Clicker in 3s...{" " * 15}', bCap=False, sEnd="\r"
            )
            _countdown(3)
            _print_message(f'Closing the Clicker...{" " * 25}')

        # Print Status
        self._print_status(key_name, mouse_pos)

    def _print_status(self, key_name, mouse_pos):
        """
        Worst case...
        "   | Key: space | Move: Active | Click: Active | Mouse Move: Active | Pos: (nnnn, nnnn) |"
        "   | Key: space | Move: Active | Click: Active | Mouse Move: Active |                   |"
        """
        _print_message(
            f"Key: {key_name:^5} | "
            f"Move: {self.key_press_thread.status:^6} | "
            f"Mouse Move: {self.move_click_thread.status:^6} | "
            f"Click: {self.click_thread.status:^6} | "
            f"{mouse_pos}",
            bCap=False,
            sEnd="\r",
        )

    def _show_menu(self):
        _print_message("Waiting for key-press:", bCap=False)
        _print_message(f"    * Show Coords: {self.display_coords.name}", bCap=False)
        _print_message(f"    * WASD Move:   {self.go_pause_wasd.name}", bCap=False)
        _print_message(f"    * Mouse Move:  {self.go_pause_move.name}", bCap=False)
        _print_message(f"    * Mouse Click: {self.go_pause_click.name}", bCap=False)
        _print_message(f"    * Reload CFG:  {self.reload_key.name}", bCap=False)
        _print_message(f"    * Exit:        {self.exit_key.name}")

    def run(self):
        self.click_thread = ClickMouse()
        self.move_click_thread = MoveClickMouse()
        self.key_press_thread = PressKeys()

        self.click_thread.start()
        self.move_click_thread.start()
        self.key_press_thread.start()

        _start_message()

        self._show_menu()

        with Listener(on_press=self._on_press) as self.listener:
            self.listener.join()


# Package exports
__all__ = ["Clicker_Main", "click", "smooth_mouse_move"]
