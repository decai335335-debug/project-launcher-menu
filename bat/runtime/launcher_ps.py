import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys
import threading
import ctypes

# DPI 感知（高分屏不模糊）
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

# 全局进程管理
processes = {}
last_launcher = None


def kill_process(key):
    """关闭指定 key 的进程"""
    global processes
    proc = processes.get(key)
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
    processes[key] = None


def launch_wt():
    """用 Windows Terminal 打开启动菜单"""
    global last_launcher
    kill_process('menu')
    bat_path = os.path.join(os.path.dirname(sys.executable), "runtime", "启动菜单.bat")
    processes['menu'] = subprocess.Popen(
        ["wt.exe", "powershell.exe", "-NoExit", "-Command", f"cmd /k '{bat_path}'"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    last_launcher = 'wt'
    status_label.config(text="状态: 已用 Windows Terminal 打开")


def launch_ps():
    """用 PowerShell 打开启动菜单"""
    global last_launcher
    kill_process('menu')
    bat_path = os.path.join(os.path.dirname(sys.executable), "runtime", "启动菜单.bat")
    processes['menu'] = subprocess.Popen(
        ["powershell.exe", "-NoExit", "-Command", f"cmd /k '{bat_path}'"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    last_launcher = 'ps'
    status_label.config(text="状态: 已用 PowerShell 打开")


def launch_vscode():
    """用 VS Code 打开 video-sub-md 项目，并启动工作目录在项目下的 PowerShell 终端"""
    global last_launcher
    kill_process('vscode')
    kill_process('vscode_term')
    project_path = r"E:\git项目\Codex\video-sub-md"
    # 打开 VS Code 项目
    processes['vscode'] = subprocess.Popen(
        ["code.cmd", project_path],
        shell=True
    )
    # 同时启动一个外部 PowerShell，工作目录直接设在项目下
    processes['vscode_term'] = subprocess.Popen(
        ["powershell.exe", "-NoExit", "-Command", f"cd '{project_path}'"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    last_launcher = 'vscode'
    status_label.config(text="状态: 已用 VS Code 打开 + 项目终端")


def relaunch():
    """重新打开：关闭旧的，再开新的"""
    if last_launcher == 'wt':
        launch_wt()
    elif last_launcher == 'vscode':
        launch_vscode()
    else:
        launch_ps()


# GUI
root = tk.Tk()
root.title("项目启动菜单")
root.geometry("380x340")
root.resizable(False, False)

# 标题
ttk.Label(root, text="项目启动菜单", font=("微软雅黑", 14, "bold")).pack(pady=10)
ttk.Label(root, text="video-sub-md · B站 + YouTube 字幕下载", font=("微软雅黑", 9)).pack()

# 按钮区域
btn_frame = ttk.Frame(root)
btn_frame.pack(pady=15, fill=tk.X, padx=30)

ttk.Button(btn_frame, text="用 Windows Terminal 打开", command=launch_wt).pack(pady=4, fill=tk.X)
ttk.Button(btn_frame, text="用 PowerShell 打开", command=launch_ps).pack(pady=4, fill=tk.X)
ttk.Button(btn_frame, text="用 VS Code 打开项目", command=launch_vscode).pack(pady=4, fill=tk.X)
ttk.Button(btn_frame, text="重新打开（关闭旧的再打开）", command=relaunch).pack(pady=4, fill=tk.X)

# 状态栏
status_label = ttk.Label(root, text="状态: 就绪", foreground="gray")
status_label.pack(pady=5)

# 分隔线 + 退出
ttk.Separator(root, orient='horizontal').pack(fill=tk.X, pady=10, padx=20)
ttk.Button(root, text="退出", command=root.destroy).pack(pady=5)

# 默认延迟启动 PowerShell
threading.Timer(0.3, launch_ps).start()

root.mainloop()

