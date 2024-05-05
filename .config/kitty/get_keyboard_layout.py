#!/usr/bin/env python3

import subprocess
import platform
import os


def get_keyboard_layout():
    try:
        system = platform.system()

        if system == "Darwin":  # macOS
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
            layout = result.stdout.strip()
            # layout = result.stdout.strip()[0]
            # layout = str(result)[0]
            return layout
        elif system == "Linux":
            result = subprocess.run(
                ["setxkbmap", "-query"], capture_output=True, text=True
            )
            lines = result.stdout.split("\n")
            layout_line = next(line for line in lines if "layout" in line)
            layout = layout_line.split(":")[1].strip()

        else:
            raise Exception(f"Unsupported operating system: {system}")

        print(f"system:{system}, layout: {layout}")
        return layout

    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    layout = get_keyboard_layout()

    if layout:
        print(layout)
