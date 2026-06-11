# Project Launcher Menu

一个 Windows 本地项目启动菜单，把分散在不同目录里的 BAT/Python 工具整合成一个编号入口，并提供可固定到任务栏的 `启动菜单ps3.exe` 图形入口。

## 1. 一句话定位

Project Launcher Menu 是一个轻量级 Windows 启动器：用 `启动菜单ps3.exe` / `启动菜单.bat` 汇总多个本地项目，输入编号即可启动对应工具。

## 2. 解决什么痛点

以前是这样的：

- 每个项目都放在不同目录，想启动时要先找路径。
- 有些项目入口是 Python 脚本，有些是 BAT，有些还需要切工作目录。
- 常用工具越多，桌面快捷方式和终端历史越乱。
- 新增项目时容易忘记启动命令，过几天又要重新翻文档。

现在是这样的：

- 打开一个菜单，输入编号即可启动对应项目。
- 可以把 `启动菜单ps3.exe` 固定到任务栏或开始菜单，当作本机工具入口。
- 每个项目的启动命令被封装在独立 `.bat` 文件里。
- 主菜单只负责展示和跳转，结构简单，容易维护。
- 新项目只要新增一个编号 BAT，再挂到菜单里。

适合谁用：

- 本地自动化工具很多的人 —— 把常用脚本集中到一个入口。
- 经常在多个 AI/字幕/下载/语音项目之间切换的人 —— 不再手动找目录。
- 想维护一个轻量启动面板的人 —— 不引入复杂桌面框架，BAT 即可运行。

## 3. 核心功能

| 功能 | 解决什么问题 |
| --- | --- |
| 可固定 EXE 入口 | `启动菜单ps3.exe` 可以固定到底部任务栏，减少每次找 BAT 的麻烦。 |
| 编号启动菜单 | 把多个项目统一放进一个命令行菜单，输入数字即可启动。 |
| 独立项目 BAT | 每个项目一个启动脚本，避免主菜单里堆复杂命令。 |
| ASCII 菜单文本 | 避免 Windows CMD 中文编码导致菜单乱码或命令被误执行。 |
| 一键重新生成脚本 | `generate_bats.py` 维护项目清单，必要时可重新生成菜单和启动 BAT。 |
| SenseVoice IME 接入 | 第 7 项直接启动本地语音输入法项目。 |
| 可扩展结构 | 新增项目只需要添加一项 BAT 和菜单跳转，不影响其他项目。 |

## 4. 安装方法

1. 确认你在 Windows 环境中。
2. 确认本仓库位于：

```text
E:\Projects\launchers
```

3. 确认各项目自己的依赖已经安装好。本启动器只负责调用入口，不负责安装每个项目的 Python 依赖。
4. 推荐把这个入口固定到任务栏：

```text
E:\Projects\launchers\bat\启动菜单ps3.exe
```

5. 如果只想运行 BAT，也可以打开：

```bat
E:\Projects\launchers\bat\启动菜单.bat
```

6. 如果需要重新生成所有 BAT，运行：

```powershell
cd "E:\Projects\launchers\bat"
python generate_bats.py
```

## 5. 使用方法

### 场景一：启动常用项目

什么时候用：你想快速打开某个本地工具，不想手动找目录和命令。

1. 双击或固定打开 `bat/启动菜单ps3.exe`。
2. 在打开的菜单中查看编号。
3. 输入对应数字，例如 `7`。
4. 按回车，启动 `sensevoice-ime`。

### 场景二：添加一个新项目

什么时候用：你又做了一个新工具，希望它出现在统一启动菜单里。

1. 在 `bat/` 下新增一个启动文件，例如 `08-my-tool.bat`。
2. 在 `启动菜单.bat` 里新增一行菜单显示：`echo 8. my-tool`。
3. 新增判断：`if "%choice%"=="8" goto p8`。
4. 在文件底部新增 `:p8` 段，`call` 你的启动 BAT。
5. 保存后重新打开启动菜单测试。

### 场景三：用生成脚本维护菜单

什么时候用：项目数量越来越多，想用一个 Python 清单统一管理。

1. 打开 `bat/generate_bats.py`。
2. 在 `PROJECTS` 列表里新增一项：编号、名称、项目目录、启动命令。
3. 运行 `python generate_bats.py`。
4. 检查生成后的 `启动菜单.bat`。

## 6. 技术栈 / 工具链 / 依赖库

| 层级 | 技术 |
| --- | --- |
| 主入口 | Windows Batch (`.bat`) |
| 固定入口 | PyInstaller 打包的 `启动菜单ps3.exe` |
| 生成脚本 | Python 3 |
| 可选 GUI | Tkinter (`launcher_ps.py`) |

| 工具 | 用途 |
| --- | --- |
| `启动菜单ps3.exe` | 当前实际使用的固定入口，可以放到底部任务栏。 |
| `启动菜单ps3.spec` | 当前 EXE 的 PyInstaller 打包配置。 |
| `启动菜单.bat` | 主启动菜单。 |
| `app.ico` / `project-launcher-icon.ico` | EXE 和快捷方式使用的图标资源。 |
| `01-*.bat` 到 `07-*.bat` | 各项目独立启动入口。 |
| `generate_bats.py` | 根据项目清单重新生成 BAT。 |
| `.gitignore` | 忽略 build/dist 和旧实验入口。 |

| 依赖库 | 用途说明 |
| --- | --- |
| 无必需第三方依赖 | BAT 菜单本身只依赖 Windows CMD。 |
| Tkinter | 可选 GUI 启动器实验，随 Python 标准库提供。 |
| PyInstaller | 用于重新打包 `启动菜单ps3.exe`。 |

## 7. 文件结构

```text
project-launcher-menu/
├── README.md
├── DEV_LOG.md
├── .gitignore
├── launcher_ps.py
└── bat/
    ├── 启动菜单ps3.exe          # 当前推荐固定到任务栏的入口
    ├── 启动菜单ps3.spec         # 当前 EXE 打包配置
    ├── 启动菜单.exe             # 早期可用入口
    ├── 启动菜单.spec            # 早期入口打包配置
    ├── 启动菜单.bat             # 主菜单入口
    ├── 01-video-sub-md.bat
    ├── 02-tabbit-ai-shortcut.bat
    ├── 03-win-layout-manager.bat
    ├── 04-doubao-podcast.bat
    ├── 05-github-repo-downloader.bat
    ├── 06-auto-unzip-interactive.bat
    ├── 07-sensevoice-ime.bat
    ├── generate_bats.py
    ├── app.ico
    └── project-launcher-icon.ico
```

## 8. 常见问题

Q: 下次添加新功能，只要添加到启动菜单里就可以了吗?
A: 如果新功能已经是一个可独立运行的项目，是的。推荐先给它写一个独立 `NN-project-name.bat`，再在 `启动菜单.bat` 里新增编号和 `goto` 段。

Q: 为什么菜单改成英文了?
A: Windows CMD 对中文 BAT 编码很挑剔，之前出现过中文被拆成命令执行的问题。主菜单使用 ASCII 英文可以最大限度避免编码故障。

Q: 为什么上传 `启动菜单ps3.exe`?
A: 这是当前实际使用入口，可以固定到任务栏或开始菜单。旧的 `启动菜单ps.exe`、`启动菜单ps2.exe` 和 build/dist 中间产物仍然忽略。

Q: 双击某个项目没有启动怎么办?
A: 先单独运行对应的 `NN-project-name.bat`，确认项目路径和依赖是否正确。启动器只负责调用，不会自动修复被调用项目的环境。

Q: 重新运行 `generate_bats.py` 会覆盖手改菜单吗?
A: 会。以后推荐把新增项目写进 `PROJECTS` 列表，再用生成脚本统一生成，减少手动编辑出错。

## 9. 未来开发路线图 (Roadmap)

当前状态：稳定版，小型本地启动器。

近期：

- 增加项目清单 JSON —— 让项目路径、编号和启动命令从数据文件读取，减少改 Python 的频率。
- 给每个启动项增加说明字段 —— 菜单里只显示名称，README 中可自动生成详细说明。

中期：

- 改进 Tkinter GUI 启动器 —— 给不想看命令行菜单的场景一个按钮界面。
- 增加路径存在性检查 —— 启动前提示项目目录不存在，减少静默失败。

长期：

- 成为本机自动化工具的轻量入口层，而不是复杂桌面平台。
- 保持核心简单：BAT 可直接运行，Python 只负责生成和可选 GUI。

如何参与：

- 有新项目要接入，提交 Issue 或直接新增 `NN-project-name.bat`。
- 有编码、路径、环境问题，附上运行截图和对应 BAT 内容。

## 10. 更新日志

v0.2.1 (2026-06-11) ✅ 上传当前实际使用入口 `启动菜单ps3.exe` ✅ 上传 `启动菜单ps3.spec`、`app.ico`、`project-launcher-icon.ico` 图标资源 📋 调整 `.gitignore`，只忽略 build/dist 和旧实验 EXE，保留正式入口 EXE 与 SPEC
v0.2.0 (2026-06-11) ✅ 新增第 7 项 `sensevoice-ime` 启动入口 ✅ 新增独立 `07-sensevoice-ime.bat` 🔧 修复中文 BAT 编码导致 CMD 把菜单文字当命令执行的问题 ⚡ 优化主菜单为 ASCII 稳定文本 📋 新增 `.gitignore`，忽略 build/dist 等本地打包中间产物 🔄 重写 README/DEV_LOG 为产品、技术、受众三维结构
v0.1.0 (2026-06-09) 🚀 初始功能：整合 video-sub-md、tabbit-ai-shortcut、win-layout-manager、doubao-podcast、github-repo-downloader、auto-unzip-interactive 等本地项目入口 ✅ 新增编号菜单和独立 BAT 启动脚本 ✅ 新增 `generate_bats.py` 用于批量生成启动脚本
