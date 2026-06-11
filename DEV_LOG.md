# Project Launcher Menu DEV_LOG

## 1. 项目起源

这个项目的原始需求很简单：本机有越来越多的 AI、字幕、下载、语音、自动化脚本项目，每个项目都在不同路径里。每次启动都要找目录、开终端、敲命令，重复且容易忘。

因此先用最轻的方式做一个本地启动菜单：一个 `启动菜单.bat` 汇总多个项目，输入编号后调用对应的独立 BAT。后来又加入 `启动菜单ps3.exe`，让这个入口可以固定到任务栏，像普通桌面应用一样随手打开。

核心目标不是做复杂桌面应用，而是把“每天都要启动的本地工具”放进一个稳定入口。

## 2. 迭代时间线

### v0.2.1 - 固定入口 EXE 与图标资源

- 明确 `启动菜单ps3.exe` 是当前实际使用入口，可以固定到任务栏或开始菜单。
- 保留 `启动菜单ps3.spec`，方便之后按同一配置重新打包。
- 保留 `app.ico` 和 `project-launcher-icon.ico` 作为图标资源。
- 调整 `.gitignore`：继续忽略 build/dist 和旧实验 EXE，但不忽略正式入口 `启动菜单ps3.exe`、`启动菜单ps3.spec`、图标文件。

### v0.2.0 - SenseVoice IME 接入与文档整理

- 新增第 7 项 `sensevoice-ime`，调用 `E:\Projects\ai\sensevoice_ime\run.bat`。
- 新增 `07-sensevoice-ime.bat`，让每个项目继续保持独立启动入口。
- 将主菜单改成 ASCII 英文，解决 CMD 中文编码导致菜单文字被当成命令执行的问题。
- 更新 `generate_bats.py`，把 7 个项目统一纳入生成清单。
- 新增 `.gitignore`，忽略 PyInstaller build/dist/exe、图片、图标等本地产物；随后在 v0.2.1 调整为保留正式 EXE 和图标。
- 新增 README 和 DEV_LOG，按产品、技术、受众三个维度整理项目。

### v0.1.0 - 初始 BAT 启动菜单

- 创建 `bat/启动菜单.bat`。
- 接入 6 个本地项目：
  - video-sub-md
  - tabbit-ai-shortcut
  - win-layout-manager
  - doubao-podcast
  - github-repo-downloader
  - auto-unzip-interactive
- 为每个项目准备独立 BAT 入口。
- 尝试 Tkinter GUI 和 PyInstaller 打包版本。

## 3. 踩坑记录

| 问题 | 根因 | 解决方案 | 涉及版本 |
| --- | --- | --- | --- |
| CMD 把“项目启动菜单”等中文当成命令执行 | BAT 文件编码和 CMD 当前代码页不一致，中文行被错误解析 | 主菜单改为 ASCII 英文文本，避免编码依赖 | v0.2.0 |
| 新增项目后还要修改生成脚本清单 | 固定 `PROJECTS` 列表需要手动维护 | 改为扫描 `NN-name.bat` 文件自动生成菜单 | v0.2.2 |
| 仓库可能上传大量打包产物 | build/dist/spec 是本机生成文件，旧实验 EXE 也会造成混乱 | `.gitignore` 忽略中间产物和旧实验 EXE，但保留正式入口 `启动菜单ps3.exe` | v0.2.1 |
| 主菜单里直接写复杂启动命令后维护困难 | 所有逻辑集中在一个 BAT 内会越来越乱 | 每个项目一个独立 BAT，主菜单只做跳转 | v0.1.0 |
| GUI 打包版本容易和本机路径绑定 | PyInstaller 产物包含本机环境假设 | 保留当前实际使用的 ps3 入口和 spec，忽略旧实验入口 | v0.2.1 |

## 4. 设计决策

### 为什么用 BAT 菜单而不是完整 GUI?

| 方案 | 优点 | 缺点 | 决策 |
| --- | --- | --- | --- |
| BAT 菜单 | 无依赖、可直接运行、容易调试 | 视觉简单 | 当前主方案 |
| `启动菜单ps3.exe` | 可固定到任务栏，打开更顺手 | 需要保留打包产物和图标 | 当前推荐入口 |
| Tkinter GUI | 有按钮界面，适合桌面使用 | 打包和路径处理更复杂 | 保留为实验基础 |
| PowerShell 脚本 | 语法更强，适合复杂逻辑 | 执行策略和用户习惯可能带来阻碍 | 暂不作为主入口 |
| 桌面启动器应用 | 体验最好 | 对当前需求过重 | 长期再考虑 |

### 为什么菜单文本改成英文?

BAT 文件在 Windows CMD 中容易受到编码影响。中文菜单虽然好看，但一旦文件编码和代码页不一致，CMD 可能把乱码片段当作命令执行。英文 ASCII 菜单牺牲一点可读性，换来稳定性。

### 为什么每个项目一个独立 BAT?

主菜单应该只做“选择和跳转”。具体项目怎么启动，放在独立 BAT 里。这样新增、删除、调试某个项目时不会影响其它项目。

### 为什么保留 `启动菜单ps3.exe`，但忽略其它打包产物?

`启动菜单ps3.exe` 是实际使用入口，方便固定到任务栏；`build/`、`dist/`、旧的 `启动菜单ps*.exe` 和中间文件则是实验或可再生成产物，不应该让仓库膨胀。

## 5. 实际测试数据

| 测试项 | 结果 |
| --- | --- |
| `启动菜单.bat` 使用 ASCII 后由 CMD 读取 | 成功 |
| 第 7 项 `sensevoice-ime` 路径存在 | 成功 |
| `07-sensevoice-ime.bat` 调用 `run.bat` | 成功配置 |
| `generate_bats.py` 自动扫描 7 个 `NN-name.bat` 项目 | 成功 |
| Git 忽略 build/dist 和旧实验 EXE，同时保留正式 `启动菜单ps3.exe` | 成功配置 |
| `启动菜单ps3.spec` 使用 `launcher_ps.py` 和 `app.ico` | 已确认 |

## 6. 文件位置

```text
project-launcher-menu/
├── README.md
├── DEV_LOG.md
├── .gitignore
├── launcher_ps.py
└── bat/
    ├── 启动菜单ps3.exe
    ├── 启动菜单ps3.spec
    ├── 启动菜单.exe
    ├── 启动菜单.spec
    ├── 启动菜单.bat
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

