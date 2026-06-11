# -*- coding: utf-8 -*-
"""Regenerate project launcher .bat files.

The generated batch files intentionally use ASCII menu text. This avoids
Chinese encoding issues in cmd.exe while still keeping project names readable.
"""
from pathlib import Path

BAT_DIR = Path(__file__).resolve().parent

# number, name, project_dir, command
PROJECTS = [
    ("01", "video-sub-md", "E:/Projects/Codex/video-sub-md", "python main.py"),
    ("02", "tabbit-ai-shortcut", "E:/Projects/ai/tabbit-ai-shortcut", "python ai_button_hotkey_v4.py"),
    ("03", "win-layout-manager", "E:/Projects/tools/win-layout-manager", "python snap_all.py"),
    ("04", "doubao-podcast", "E:/Projects/ai/doubao-podcast-obsidian-bridge", "python doubao_pipeline.py"),
    ("05", "github-repo-downloader", "E:/Projects/tools/github-repo-downloader", "python github_batch_downloader.py"),
    ("06", "auto-unzip-interactive", "E:/Projects/tools/auto-unzip", "python scripts/extract_interactive.py"),
    ("07", "sensevoice-ime", "E:/Projects/ai/sensevoice_ime", "call run.bat"),
]


def write_ascii(path: Path, content: str) -> None:
    path.write_text(content, encoding="ascii")
    print(f"Generated: {path}")


for num, name, project_dir, command in PROJECTS:
    bat_path = BAT_DIR / f"{num}-{name}.bat"
    content = "\n".join([
        "@echo off",
        "chcp 65001 > nul",
        f"cd /d \"{project_dir}\"",
        command,
        "pause" if not command.lower().startswith("call ") else "",
        "",
    ])
    write_ascii(bat_path, content)

menu_lines = [
    "@echo off",
    "chcp 65001 > nul",
    ":menu",
    "cls",
    "echo ================================",
    "echo        Project Launcher Menu",
    "echo ================================",
]

for num, name, _, _ in PROJECTS:
    menu_lines.append(f"echo {int(num)}. {name}")

menu_lines.extend([
    "echo 0. Exit",
    "echo ================================",
    "set /p choice=Input number: ",
])

for num, _, _, _ in PROJECTS:
    idx = str(int(num))
    menu_lines.append(f'if "%choice%"=="{idx}" goto p{idx}')

menu_lines.extend([
    'if "%choice%"=="0" goto end',
    "goto menu",
    "",
])

for num, name, _, _ in PROJECTS:
    idx = str(int(num))
    menu_lines.extend([
        f":p{idx}",
        f"call \"{(BAT_DIR / f'{num}-{name}.bat').as_posix()}\"",
        "goto menu",
        "",
    ])

menu_lines.extend([
    ":end",
    "echo Exit.",
    "pause",
    "",
])

write_ascii(BAT_DIR / "启动菜单.bat", "\n".join(menu_lines))
print("All launcher bat files regenerated.")
