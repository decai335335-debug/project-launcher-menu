# -*- coding: utf-8 -*-
"""Regenerate the launcher menu from existing NN-name.bat files.

Usage:
    1. Put a file like 08-my-tool.bat in this folder.
    2. Run: python generate_bats.py
    3. The main 启动菜单.bat menu will include it automatically.

Only files matching NN-name.bat are added to the menu. The main menu itself
and any non-numbered helper bat files are ignored.
"""
from pathlib import Path
import re

BAT_DIR = Path(__file__).resolve().parent
MENU_NAME = "启动菜单.bat"
ENTRY_RE = re.compile(r"^(\d{2})-(.+)\.bat$", re.IGNORECASE)


def write_ascii(path: Path, content: str) -> None:
    path.write_text(content, encoding="ascii")
    print(f"Generated: {path}")


def discover_entries():
    entries = []
    for path in BAT_DIR.glob("*.bat"):
        if path.name == MENU_NAME:
            continue
        match = ENTRY_RE.match(path.name)
        if not match:
            continue
        num, name = match.groups()
        entries.append((int(num), num, name, path))
    entries.sort(key=lambda item: item[0])
    return entries


def build_menu(entries):
    menu_lines = [
        "@echo off",
        "chcp 65001 > nul",
        ":menu",
        "cls",
        "echo ================================",
        "echo        Project Launcher Menu",
        "echo ================================",
    ]

    for idx, _, name, _ in entries:
        menu_lines.append(f"echo {idx}. {name}")

    menu_lines.extend([
        "echo 0. Exit",
        "echo ================================",
        "set /p choice=Input number: ",
    ])

    for idx, _, _, _ in entries:
        menu_lines.append(f'if "%choice%"=="{idx}" goto p{idx}')

    menu_lines.extend([
        'if "%choice%"=="0" goto end',
        "goto menu",
        "",
    ])

    for idx, _, _, path in entries:
        menu_lines.extend([
            f":p{idx}",
            f"call \"{path.as_posix()}\"",
            "goto menu",
            "",
        ])

    menu_lines.extend([
        ":end",
        "echo Exit.",
        "pause",
        "",
    ])
    return "\n".join(menu_lines)


def main():
    entries = discover_entries()
    if not entries:
        raise SystemExit("No launcher entries found. Expected files like 01-example.bat")
    write_ascii(BAT_DIR / MENU_NAME, build_menu(entries))
    print("Launcher entries:")
    for idx, _, name, path in entries:
        print(f"  {idx}. {name} -> {path.name}")


if __name__ == "__main__":
    main()
