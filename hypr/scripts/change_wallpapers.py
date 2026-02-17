import sys
import os
import subprocess
import json
import re
from typing import Dict, List, Any, Union
from pathlib import Path
from psutil import process_iter


class ScreenContext:
    def __init__(self, wallpaper_path: str, monitor: str) -> None:
        self._monitor = monitor
        self._wallpaper_path = Path(wallpaper_path).absolute()

    def to_hyprpaper_conf(self) -> str:
        return (
            f"preload = {self._wallpaper_path}\n"
            f"wallpaper = {self._monitor}, {self._wallpaper_path}"
        )

    def __repr__(self):
        return f"ScreenContext(monitor='{self._monitor}', wallpaper='{self._wallpaper_path}')"


class ScreenContextBuilder:
    @staticmethod
    def build_from_data(wallpaper_path: str, monitor: str) -> ScreenContext:
        return ScreenContext(wallpaper_path, monitor)

    @staticmethod
    def build_from_hypr_config(
        config_path: str | Path = "~/.config/hypr/hyprpaper.conf",
    ) -> List[ScreenContext]:
        config_path = Path(config_path).expanduser()
        text = config_path.read_text()

        wallpaper_entries = []

        for line in text.splitlines():
            line = line.strip()
            if line.startswith("wallpaper") and "=" in line:
                _, rest = line.split("=", 1)
                monitor, path = map(str.strip, rest.split(",", 1))
                wallpaper_entries.append(ScreenContext(path, monitor))

        return wallpaper_entries


def reload_hyprpaper() -> None:
    proc_name = "hyprpaper"

    for proc in process_iter(["name"]):
        if proc.info["name"] == proc_name:
            proc.terminate()
            break
    subprocess.Popen(proc_name)


def hyprpaper_change_wallpapers(path: Path, monitor: str = "") -> None:
    config = Path("~/.config/hypr/hyprpaper.conf").expanduser()

    if not config.exists or not config.is_file():
        raise TypeError(f"Файл {config} не сущетвует.")
    elif not os.access(config, os.W_OK):
        raise PermissionError(f"Файл {config} не доступен для записи")

    with config.open("w") as f:
        f.write(f"""
        preload = {path.absolute()}
        wallpaper = {monitor}, {path.absolute()} 
        """)


def get_hypr_monitors() -> List[str]:
    process_output = subprocess.run(
        ["hyprctl", "monitors", "-j"],
        capture_output=True,
        text=True,
    )

    str_json_monitors = process_output.stdout

    monitors_json: List[Dict[str, Any]] = json.loads(str_json_monitors)

    monitors = []

    for monitor in monitors_json:
        if not monitor["disabled"]:
            monitors.append(monitor["name"])

    return monitors


class ContextsRepo:
    _taken_monitors = set()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Missing argument")
    path = Path(sys.argv[1])

    available_monitors = get_hypr_monitors()

    hyprpaper_change_wallpapers(path)
    reload_hyprpaper()
