# based from https://github.com/kovidgoyal/kitty/discussions/4447#discussioncomment-3240635
# for colors: https://github.com/kovidgoyal/kitty/blob/3c4f2aa1b85683dfe5c07f3c04d8be51e9b83053/kitty/options/definition.py#L1621

# pyright: reportMjjjg;gImports=false
import sys
import subprocess

# import platform
import os
import re
from datetime import datetime
from kitty.boss import get_boss
from kitty.fast_data_types import Screen, add_timer, get_options
from kitty.utils import color_as_int
from kitty.tab_bar import (
    DrawData,
    ExtraData,
    Formatter,
    TabBarData,
    as_rgb,
    draw_attributed_string,
    draw_title,
)

opts = get_options()
icon_fg = as_rgb(color_as_int(opts.color15))
icon_bg = as_rgb(color_as_int(opts.color16))
color_white = as_rgb(color_as_int(opts.color15))
color_grey = as_rgb(color_as_int(opts.color8))
color_red = as_rgb(color_as_int(opts.color160))
SEPARATOR_SYMBOL, SOFT_SEPARATOR_SYMBOL = ("", "")
RIGHT_MARGIN = 1
REFRESH_TIME = 1
ICON = "  "
UNPLUGGED_ICONS = {
    10: "",
    20: "",
    40: "",
    60: "",
    100: "",
}

PLUGGED_ICONS = {
    10: "",
    20: "",
    40: "",
    60: "",
    100: "",
}
UNPLUGGED_COLORS = {
    15: as_rgb(color_as_int(opts.color1)),
    16: as_rgb(color_as_int(opts.color15)),
}
PLUGGED_COLORS = {
    15: as_rgb(color_as_int(opts.color1)),
    16: as_rgb(color_as_int(opts.color6)),
    99: as_rgb(color_as_int(opts.color6)),
    100: as_rgb(color_as_int(opts.color2)),
}


def _draw_icon(screen: Screen, index: int) -> int:
    if index != 1:
        return 0
    fg, bg = screen.cursor.fg, screen.cursor.bg
    screen.cursor.fg = icon_fg
    screen.cursor.bg = icon_bg
    screen.draw(ICON)
    screen.cursor.fg, screen.cursor.bg = fg, bg
    screen.cursor.x = len(ICON)
    return screen.cursor.x


def _draw_left_status(
    draw_data: DrawData,
    screen: Screen,
    tab: TabBarData,
    before: int,
    max_title_length: int,
    index: int,
    is_last: bool,
    extra_data: ExtraData,
) -> int:
    if screen.cursor.x >= screen.columns - right_status_length:
        return screen.cursor.x
    tab_bg = screen.cursor.bg
    tab_fg = screen.cursor.fg
    default_bg = as_rgb(int(draw_data.default_bg))
    if extra_data.next_tab:
        next_tab_bg = as_rgb(draw_data.tab_bg(extra_data.next_tab))
        needs_soft_separator = next_tab_bg == tab_bg
    else:
        next_tab_bg = default_bg
        needs_soft_separator = False
    if screen.cursor.x <= len(ICON):
        screen.cursor.x = len(ICON)
    screen.draw(" ")
    screen.cursor.bg = tab_bg
    draw_title(draw_data, screen, tab, index)
    if not needs_soft_separator:
        screen.draw(" ")
        screen.cursor.fg = tab_bg
        screen.cursor.bg = next_tab_bg
        screen.draw(SEPARATOR_SYMBOL)
    else:
        prev_fg = screen.cursor.fg
        if tab_bg == tab_fg:
            screen.cursor.fg = default_bg
        elif tab_bg != default_bg:
            c1 = draw_data.inactive_bg.contrast(draw_data.default_bg)
            c2 = draw_data.inactive_bg.contrast(draw_data.inactive_fg)
            if c1 < c2:
                screen.cursor.fg = default_bg
        screen.draw(" " + SOFT_SEPARATOR_SYMBOL)
        screen.cursor.fg = prev_fg
    end = screen.cursor.x
    return end


def _draw_right_status(screen: Screen, is_last: bool, cells: list) -> int:
    if not is_last:
        return 0
    draw_attributed_string(Formatter.reset, screen)
    screen.cursor.x = screen.columns - right_status_length
    screen.cursor.fg = 0
    for color, status in cells:
        screen.cursor.fg = color
        screen.draw(status)
    screen.cursor.bg = 0
    return screen.cursor.x


def _redraw_tab_bar(_):
    tm = get_boss().active_tab_manager
    if tm is not None:
        tm.mark_tab_bar_dirty()


def get_battery_cells(color) -> list:
    try:
        if sys.platform.startswith("linux"):
            status_path = "/sys/class/power_supply/BAT0/status"
            capacity_path = "/sys/class/power_supply/BAT0/capacity"
            with open(status_path, "r") as f:
                status = f.read()
            with open(capacity_path, "r") as f:
                percent = int(f.read())
        elif sys.platform == "darwin":
            pmset_output = subprocess.check_output(["pmset", "-g", "batt"]).decode(
                "utf-8"
            )
            status = re.search(r"\d+%", pmset_output).group()[:-1]
            percent = int(status)
        else:
            return []

        bat_text_color = color
        icon_color = color
        if percent <= 10:
            icon_color = color_red

        charging_icons = (
            PLUGGED_ICONS if "discharging" not in pmset_output else UNPLUGGED_ICONS
        )
        icon = (
            charging_icons[min(charging_icons.keys(), key=lambda x: abs(x - percent))]
            + "  "
        )

        percent_cell = (bat_text_color, str(percent) + "% ")
        icon_cell = (icon_color, icon)
        return [percent_cell, icon_cell]
    except FileNotFoundError:
        return []


def get_wifi_status() -> str:
    try:
        if sys.platform == "darwin":
            result = subprocess.run(
                ["networksetup", "-getairportnetwork", "en0"],
                capture_output=True,
                text=True,
            )
            # output = result.stdout.lower()
            output = result.stdout
            match = re.search(r"(.*Current Wi-Fi Network: )(.*)", output)

            if match:
                wifi_network = match.group(2)
                return f" {wifi_network}"
            else:
                return "󰤭 " + "\xa0"
        elif sys.platform.startswith("linux"):
            result = subprocess.run(
                ["nmcli", "radio", "wifi"], capture_network=True, text=True
            )
            network = result.stdout.lower()

            if "enabled" in network:
                return f"  "
            else:
                return "󰤭 " + "\xa0"
        else:
            return "󰤫 " + "\xa0"
    except (subprocess.CalledProcessError, AttributeError):
        return "󱚼" + "\xa0"


def get_keyboard_layout():
    try:
        if sys.platform == "darwin":
            plist_path = os.path.expanduser(
                "~/Library/Preferences/com.apple.HIToolbox.plist"
            )

            result = subprocess.run(
                [
                    "defaults",
                    "read",
                    plist_path,
                    "AppleCurrentKeyboardLayoutInputSourceID",
                ],
                capture_output=True,
                text=True,
            )
            layout_identifier = result.stdout.strip()

            result = subprocess.run(
                ["awk", "-F", ".", "{print $4}"],
                input=layout_identifier,
                capture_output=True,
                text=True,
            )
            layout = result.stdout.strip()[0]

            return "[" + layout + "] "

        elif sys.platform.startswith("linux"):
            result = subprocess.run(
                ["setxkbmap", "-query"], capture_output=True, text=True
            )
            lines = result.stdout.split("\n")
            layout_line = next(line for line in lines if "layout" in line)
            layout = layout_line.split(":")[1].strip()

        return layout + "\xa0"

    except Exception as e:
        print(f"Error: {e}")
        return None


timer_id = None
right_status_length = -1


def draw_tab(
    draw_data: DrawData,
    screen: Screen,
    tab: TabBarData,
    before: int,
    max_title_length: int,
    index: int,
    is_last: bool,
    extra_data: ExtraData,
) -> int:
    global timer_id
    global right_status_length
    if timer_id is None:
        timer_id = add_timer(_redraw_tab_bar, REFRESH_TIME, True)
    clock = datetime.now().strftime(" %H:%M")
    date = datetime.now().strftime(" %Y-%m-%d")

    cells = get_battery_cells(color_white)
    cells.append((color_grey, get_keyboard_layout()))
    cells.append((color_white, get_wifi_status()))
    cells.append((color_grey, date))
    cells.append((color_grey, clock))

    right_status_length = RIGHT_MARGIN
    for cell in cells:
        right_status_length += len(str(cell[1]))

    _draw_icon(screen, index)
    _draw_left_status(
        draw_data,
        screen,
        tab,
        before,
        max_title_length,
        index,
        is_last,
        extra_data,
    )
    _draw_right_status(
        screen,
        is_last,
        cells,
    )
    return screen.cursor.x
