"""
Threaded class-based clicker config file
"""

from dataclasses import dataclass

# ~~~ Constants ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Directional Keys
U = "w"
L = "a"
D = "s"
R = "d"


# ~~~ Utilities ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def swap_last_element_in_last_tuple(lst, new_value):
    # Access the last tuple using my_list[-1]
    *initial, last_tuple = lst

    # Create a new tuple:
    # last_tuple[:-1] takes all elements except the last (0, 1)
    # (new_value,) creates a single-element tuple with the new value (9,)
    # The + operator concatenates them into the new tuple (0, 1, 9)
    new_last_tuple = last_tuple[:-1] + (new_value,)

    # Concatenate the initial list with the new last tuple
    return initial + [new_last_tuple]


def spiral(v, h, reduce, wait, cycle_delay=None):
    """Generate a swirrel pattern of WASD movement delays"""
    w = wait

    # Start by getting to the upper-right corner [ (direction, duration, wait), ... ]
    ddw_sequence = [(U, v / 2, w), (R, h / 2, w)]

    # Follow the perimeter for the first 3 sides and end at the upper-left corner
    ddw_sequence += [
        (D, v, w),
        (L, h, w),
        (U, v, w),
    ]

    # top-left coords, center at (0, 0)
    x = -h / 2
    y = v / 2

    # Continuing in a clock-wise manner, from the upper-left corner, construct the swirrel:
    # - reduce each side by the specified amount
    # - until one side is reduced to zero or less, at which point the swirrel is complete
    while v > 0 and h > 0:
        # Move right
        h -= reduce
        if h <= 0:
            break
        ddw_sequence.append((R, h, w))
        x += h

        # Move down
        v -= reduce
        if v <= 0:
            break
        ddw_sequence.append((D, v, w))
        y -= v

        # Move left
        h -= reduce
        if h <= 0:
            break
        ddw_sequence.append((L, h, w))
        x -= h

        # Move up
        v -= reduce
        if v <= 0:
            break
        ddw_sequence.append((U, v, w))
        y += v

    # use the relative coords, to return to the center, if not already there
    if x > 0:
        ddw_sequence.append((L, x, w))
    elif x < 0:
        ddw_sequence.append((R, -x, w))
    if y > 0:
        ddw_sequence.append((D, y, w))
    elif y < 0:
        ddw_sequence.append((U, -y, w))

    if cycle_delay is not None:
        ddw_sequence = swap_last_element_in_last_tuple(ddw_sequence, cycle_delay)

    return ddw_sequence


# ~~~ Shapes Tool-Classes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __iter__(self):
        yield self.x
        yield self.y


# ~~~ Shapes (CLICKS) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
click_after_move = True
point_delay = 0.2
TL = Point(825, 450)
TR = Point(1710, 450)
BL = Point(825, 990)
BR = Point(1710, 990)
park_it = [(2510, 80, 1)]
reconnect = [(1330, 775, 30)]  # 1375, 795;1329, 776

even_diagonal_points = [(*p, point_delay) for p in [TL, BR]]
odd_diagonal_points = [(*p, point_delay) for p in [TR, BL]]
corner_points = [(*p, point_delay) for p in [TL, TR, BL, BR]]
zig_zag_points = (
    [(*TL, point_delay)]
    + list(
        zip(
            [TR.x, BL.x] * 5,
            range(TR.y, BL.y + 1, int((BL.y - TR.y) / 9)),
            [point_delay] * 10,
        )
    )
    + [(*BR, point_delay)]
)
delete_Yahoo_mail = [
    (485, 219, point_delay),  # click the Offers tab
    (340, 310, point_delay),  # click the mail checkbox
    (340, 220, point_delay),  # click the ALL checkbox
    (715, 220, 4),  # click the spam button
]
open_tombs = [
    # (820, 530, 0.2),  # UL tomb in inventory
    # (1695, 530, 0.2),  #  UR tomb in inventory
    (820, 680, 0.2),  # LL tomb in inventory
    (1340, 860, 2),  #   `Open 10 tombs` button
]


# ~~~ Shapes (WASD) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
edge_delay = 12
edge_delay_long = edge_delay * 2
corner_delay = 9.25
cycle_delay = 15

# --- Diagonal -------------------------------------------
abilities_q_e = [("q", 0.1, 3), ("e", 0.1, 3)]

# --- Diagnostic -----------------------------------------
diagnostic_CLCRCUCD = [
    # center-left-center
    ("a", edge_delay_long, corner_delay),
    ("d", edge_delay_long, corner_delay),
    # center-right-center
    ("d", edge_delay_long, corner_delay),
    ("a", edge_delay_long, corner_delay),
    # center-up-center
    ("w", edge_delay, corner_delay),
    ("s", edge_delay, corner_delay),
    # center-down-center
    ("s", edge_delay, corner_delay),
    ("w", edge_delay, corner_delay),
]

# --- Spiral ---------------------------------------------
spiral_RULD = spiral(edge_delay, edge_delay_long, 0.12, corner_delay, cycle_delay)

# --- Linear ---------------------------------------------
L2R = [("a", edge_delay, corner_delay), ("d", edge_delay, corner_delay)]
R2L = L2R[::-1]
F2B = [("w", edge_delay, corner_delay), ("s", edge_delay, corner_delay)]
B2F = F2B[::-1]

# --- Squares --------------------------------------------
square_RFLB = [
    ("d", edge_delay, corner_delay),
    ("w", edge_delay, corner_delay),
    ("a", edge_delay, corner_delay),
    ("s", edge_delay, corner_delay),
]
square_RFLB_wait = swap_last_element_in_last_tuple(square_RFLB, cycle_delay)
square_RFLBR = [
    ("d", edge_delay / 2, corner_delay),
    ("w", edge_delay, corner_delay),
    ("a", edge_delay, corner_delay),
    ("s", edge_delay, corner_delay),
    ("d", edge_delay / 2, cycle_delay),
]
square_RFLBR_wait = swap_last_element_in_last_tuple(square_RFLBR, cycle_delay)
square_RFLB_retreat = [
    ("d", edge_delay, 0.25),
    ("a", 2, 0.25),
    ("w", edge_delay, 0.25),
    ("s", 2, 0.25),
    ("a", edge_delay, 0.25),
    ("d", 2, 0.25),
    ("s", edge_delay, 0.25),
    ("w", 2, 0.25),
]

# --- rectangles -----------------------------------------
rectangle_RFLB = [
    ("d", edge_delay_long, corner_delay),
    ("w", edge_delay, corner_delay),
    ("a", edge_delay_long, corner_delay),
    ("s", edge_delay, corner_delay),
]
rectangle_RFLB_wait = swap_last_element_in_last_tuple(rectangle_RFLB, cycle_delay)
rectangle_RFLBR = [
    ("d", edge_delay / 2, corner_delay),
    ("w", edge_delay_long, corner_delay),
    ("a", edge_delay, corner_delay),
    ("s", edge_delay_long, corner_delay),
    ("d", edge_delay / 2, corner_delay),
]
rectangle_RFLBR_wait = swap_last_element_in_last_tuple(rectangle_RFLBR, cycle_delay)

# --- Figure-8 -------------------------------------------
fig8_BF = [
    ("d", edge_delay / 2, corner_delay),
    ("w", edge_delay, corner_delay),
    ("a", edge_delay, corner_delay),
    ("w", edge_delay, corner_delay),
    ("d", edge_delay, corner_delay),
    ("s", edge_delay, corner_delay),
    ("a", edge_delay, corner_delay),
    ("s", edge_delay, corner_delay),
    ("d", edge_delay / 2, corner_delay),
]
fig8_BF_wait = swap_last_element_in_last_tuple(fig8_BF, cycle_delay)
fig8_BF_squat = [
    ("d", edge_delay_long / 2, corner_delay),
    ("w", edge_delay * 0.7, corner_delay),
    ("a", edge_delay_long, corner_delay),
    ("w", edge_delay * 1.3, corner_delay),
    ("d", edge_delay_long, corner_delay),
    ("s", edge_delay * 0.7, corner_delay),
    ("a", edge_delay_long * 1.3, corner_delay),
    ("s", edge_delay, corner_delay),
    ("d", edge_delay_long / 2, corner_delay),
]
fig8_BF_squat_wait = swap_last_element_in_last_tuple(fig8_BF_squat, cycle_delay)
fig8_BF_narrow = [
    ("d", edge_delay / 2, corner_delay),
    ("w", edge_delay / 2.1, corner_delay),
    ("a", edge_delay, corner_delay),
    ("w", edge_delay / 1.9, corner_delay),
    ("d", edge_delay, corner_delay),
    ("s", edge_delay / 2.1, corner_delay),
    ("a", edge_delay, corner_delay),
    ("s", edge_delay / 1.9, corner_delay),
    ("d", edge_delay / 2, corner_delay),
]
fig8_BF_narrow_wait = swap_last_element_in_last_tuple(fig8_BF_narrow, cycle_delay)
fig8_LR = [
    ("w", edge_delay / 2, corner_delay),
    ("a", edge_delay, corner_delay),
    ("s", edge_delay, corner_delay),
    ("d", edge_delay, corner_delay),
    ("w", edge_delay, corner_delay),
    ("d", edge_delay, corner_delay),
    ("s", edge_delay, corner_delay),
    ("a", edge_delay, corner_delay),
    ("w", edge_delay, corner_delay),
]
fig8_LR_wait = swap_last_element_in_last_tuple(fig8_LR, cycle_delay)

# --- key-presses ----------------------------------------
press_key_every = [("f", 0.1, 0.1)]
hold_key_every = [("e", 3, 60 * 5)]

# ~~~ Global Configs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
debug = False
click_delay_s = 0.15
press_keys = []  # ["q"]
mouse_moves_xys = open_tombs
kb_moves_khw = abilities_q_e  # square_RFLB_retreat


# ~~~ Config Class ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Configurations:
    """
    Allow standard named items to be updated on the fly
    """

    @property
    def debug(self):
        return debug

    @property
    def click_delay_s(self):
        return click_delay_s

    @property
    def press_keys(self):
        return press_keys

    @property
    def mouse_moves_xys(self):
        return mouse_moves_xys

    @property
    def click_after_move(self):
        return click_after_move

    @property
    def kb_moves_khw(self):
        return kb_moves_khw
