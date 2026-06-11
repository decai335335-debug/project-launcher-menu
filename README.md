# Project Launcher Menu

Windows 本地项目启动菜单，把分散在不同目录里的 BAT/Python 工具整合成一个编号入口，并提供可以固定到任务栏的 `Project Launcher Menu.exe`。

## 1. 一句话定位

Project Launcher Menu 是一个轻量级 Windows 本地启动器：把常用项目的启动脚本放进统一菜单，输入编号即可打开对应工具，适合管理一批本机 AI、字幕、下载、语音和自动化项目。

## 2. 解决什么痛点

以前是这样的：

- 每个项目都在不同目录里，想启动时要先找路径。
- 有些入口是 BAT，有些是 Python，有些还要切工作目录。
- 常用工具越多，桌面快捷方式、终端历史和临时命令越乱。
- 新增项目后容易忘记启动命令，过几天又要重新翻文档。

现在是这样的：

- 打开一个入口，输入编号即可启动对应项目。
- `Project Launcher Menu.exe` 可以固定到任务栏，当成本机工具总入口。
- 每个项目的启动命令都放在独立 `NN-name.bat` 文件里，互不影响。
- 根目录保持干净：第一层只保留推荐入口 EXE 和生成脚本，其余文件按用途分类。
- 新增项目只要放入 `bat/launchers/08-my-tool.bat`，运行生成脚本即可自动加入菜单。

适合谁用：

- 本地自动化工具很多的人 —— 把常用脚本集中到一个入口。
- 经常在 AI、字幕、下载、语音项目之间切换的人 —— 不再手动找目录。
- 想维护一个轻量启动面板的人 —— 不引入复杂桌面框架，BAT 即可运行。

## 3. 核心功能

| 功能 | 解决什么问题 |
| --- | --- |
| 可固定 EXE 入口 | `Project Launcher Menu.exe` 可以固定到任务栏，减少每次找 BAT 的麻烦。 |
| 编号启动菜单 | 把多个项目统一放进命令行菜单，输入数字即可启动。 |
| 独立项目 BAT | 每个项目一个启动脚本，避免主菜单里堆复杂命令。 |
| 自动扫描生成菜单 | `generate_bats.py` 自动扫描 `bat/launchers/NN-name.bat`，不用手改主菜单。 |
| 分类目录结构 | 启动脚本、运行时文件、打包配置分开放，第一层目录更清爽。 |
| ASCII 菜单文本 | 避免 Windows CMD 中文编码导致菜单乱码或命令误执行。 |
| SenseVoice IME 接入 | 第 7 项可直接启动本地语音输入法项目。 |

## 4. 安装方法

1. 确认你在 Windows 环境中。
2. 确认仓库位于：

```text
E:\Projects\launchers
```

3. 确认各项目自己的依赖已经安装好。本启动器只负责调用入口，不负责安装每个项目的 Python 依赖。
4. 推荐把这个入口固定到任务栏：

```text
E:\Projects\launchers\bat\Project Launcher Menu.exe
```

5. 如果只想运行 BAT 菜单，可以打开：

```text
E:\Projects\launchers\bat\runtime\启动菜单.bat
```

6. 如果需要重新生成菜单，运行：

```powershell
cd "E:\Projects\launchers\bat"
python generate_bats.py
```

## 5. 使用方法

### 场景一：启动常用项目

什么时候用：你想快速打开某个本地工具，不想手动找目录和命令。

1. 双击或固定打开 `E:\Projects\launchers\bat\Project Launcher Menu.exe`。
2. 在打开的菜单中查看编号。
3. 输入对应数字，例如 `7`。
4. 按回车，启动 `sensevoice-ime`。

### 场景二：添加第 8 个新项目

什么时候用：你又做了一个新工具，希望它出现在统一启动菜单里。

1. 在 `E:\Projects\launchers\bat\launchers` 下新增一个启动文件，例如：

```text
08-my-tool.bat
```

2. 文件名必须是 `两位数字-英文或拼音名称.bat`，例如 `08-obsidian-helper.bat`。
3. 在这个 BAT 里写好你的项目启动命令。
4. 运行：

```powershell
cd "E:\Projects\launchers\bat"
python generate_bats.py
```

5. 重新打开 `Project Launcher Menu.exe`，第 8 项会自动出现。

### 场景三：整理或删除项目入口

什么时候用：某个项目不常用了，或者编号想重新排序。

1. 打开 `E:\Projects\launchers\bat\launchers`。
2. 删除、移动或重命名对应的 `NN-name.bat`。
3. 运行 `python generate_bats.py`。
4. 检查 `E:\Projects\launchers\bat\runtime\启动菜单.bat` 是否已经更新。

## 6. 技术栈 / 工具链 / 依赖库

| 层级 | 技术 |
| --- | --- |
| 主菜单 | Windows Batch (`.bat`) |
| 固定入口 | PyInstaller 打包的 `Project Launcher Menu.exe` |
| 生成脚本 | Python 3 |
| GUI 入口 | Tkinter (`runtime/launcher_ps.py`) |
| 打包配置 | PyInstaller spec (`packaging/Project Launcher Menu.spec`) |

| 工具 | 用途 |
| --- | --- |
| `Project Launcher Menu.exe` | 当前推荐固定到任务栏的入口。 |
| `generate_bats.py` | 扫描 `launchers/` 并生成 `runtime/启动菜单.bat`。 |
| `runtime/启动菜单.bat` | 实际展示编号菜单并跳转到对应 BAT。 |
| `launchers/NN-name.bat` | 每个本地项目的独立启动入口。 |
| `runtime/app.ico` | EXE 使用的图标资源。 |
| `packaging/Project Launcher Menu.spec` | 重新打包 EXE 时使用的配置。 |

| 依赖库 | 用途说明 |
| --- | --- |
| 无必需第三方依赖 | BAT 菜单本身只依赖 Windows CMD。 |
| Tkinter | Python 标准库，用于 GUI 启动器入口。 |
| PyInstaller | 需要重新打包 EXE 时使用。 |

## 7. 文件结构

```text
project-launcher-menu/
├── README.md
├── DEV_LOG.md
├── .gitignore
└── bat/
    ├── Project Launcher Menu.exe      # 当前推荐固定到任务栏的入口
    ├── generate_bats.py               # 自动扫描 launchers 并生成菜单
    ├── launchers/                     # 每个项目一个独立 BAT
    │   ├── 01-video-sub-md.bat
    │   ├── 02-tabbit-ai-shortcut.bat
    │   ├── 03-win-layout-manager.bat
    │   ├── 04-doubao-podcast.bat
    │   ├── 05-github-repo-downloader.bat
    │   ├── 06-auto-unzip-interactive.bat
    │   └── 07-sensevoice-ime.bat
    ├── runtime/                       # EXE 运行时需要调用的文件
    │   ├── 启动菜单.bat
    │   ├── launcher_ps.py
    │   └── app.ico
    └── packaging/                     # 打包配置
        └── Project Launcher Menu.spec
```

## 8. 常见问题

Q: 下次添加新功能，只要添加到启动菜单里就可以了吗?
A: 如果新功能已经是一个可独立运行的项目，是的。推荐把它写成 `bat/launchers/08-my-tool.bat`，然后运行 `python generate_bats.py`，菜单会自动更新。

Q: 第一层文件夹为什么只留两个文件?
A: 你平时最需要看到的是 `Project Launcher Menu.exe` 和 `generate_bats.py`。其它文件按用途放进 `launchers/`、`runtime/`、`packaging/`，减少误删和混乱。

Q: 为什么菜单文本主要用英文?
A: Windows CMD 对中文 BAT 编码比较挑剔。之前出现过中文菜单被拆成乱码命令执行的问题，所以主菜单采用更稳的 ASCII 文本。

Q: 为什么上传 EXE?
A: 这个 EXE 是实际入口，可以固定到任务栏。它会调用 `runtime/启动菜单.bat`，所以 EXE、runtime 菜单和图标都需要一起保留。

Q: 双击某个项目没有启动怎么办?
A: 先单独运行对应的 `bat/launchers/NN-name.bat`，确认项目路径和依赖是否正确。启动器只负责调用，不会自动修复被调用项目的环境。

Q: 运行 `generate_bats.py` 会覆盖手改菜单吗?
A: 会。以后推荐只维护 `bat/launchers/NN-name.bat`，再统一生成菜单，避免手工编辑主菜单出错。

## 9. 未来开发路线图 (Roadmap)

当前状态：稳定版，小型本地启动器。

近期：

- 增加路径检查 —— 启动前提示目标 BAT 或项目目录不存在，减少静默失败。
- 增加项目说明字段 —— 菜单里可以显示更友好的项目说明，不只是文件名。

中期：

- 引入 JSON 配置 —— 让项目名称、路径、说明、分组从数据文件读取，减少改代码频率。
- 改进 Tkinter GUI —— 给不想看命令行菜单的场景一个按钮式界面。

长期：

- 成为本机自动化工具的轻量入口层，而不是复杂桌面平台。
- 保持核心简单：BAT 可直接运行，Python 只负责生成菜单和可选 GUI。

如何参与：

- 有新项目要接入，新增 `bat/launchers/NN-name.bat`。
- 有路径、编码、打包问题，附上运行截图和对应 BAT 内容。

## 10. 更新日志

v0.2.4 (2026-06-11)
- 🔄 调整目录结构，`bat` 第一层只保留 `Project Launcher Menu.exe` 和 `generate_bats.py`。
- ✅ 新增 `launchers/`、`runtime/`、`packaging/` 分类目录，启动脚本、运行文件、打包配置分开管理。
- ⚡ `generate_bats.py` 改为扫描 `launchers/NN-name.bat` 并生成 `runtime/启动菜单.bat`。
- 📋 README 和 DEV_LOG 按新版文档规范重写，更新日志改为版本内有序换行。

v0.2.3 (2026-06-11)
- 🔄 当前入口重命名为 `Project Launcher Menu.exe` / `Project Launcher Menu.spec`。
- 📋 移除早期入口和旧图标归档，减少仓库里的历史噪音。
- ✅ 保留正式 EXE、SPEC、图标资源，方便固定到任务栏和后续重新打包。

v0.2.2 (2026-06-11)
- ✅ `generate_bats.py` 改为自动扫描 `NN-name.bat` 文件。
- ✅ 新增项目只需放入类似 `08-my-tool.bat` 后重新生成菜单。
- ⚡ 主菜单不再依赖手写 `PROJECTS` 清单，降低维护成本。

v0.2.1 (2026-06-11)
- ✅ 上传当前实际使用入口 `启动菜单ps3.exe`。
- ✅ 上传 `启动菜单ps3.spec`、`app.ico`、`project-launcher-icon.ico` 图标资源。
- 📋 调整 `.gitignore`，只忽略 build/dist 和旧实验 EXE，保留正式入口 EXE 与 SPEC。

v0.2.0 (2026-06-11)
- ✅ 新增第 7 项 `sensevoice-ime` 启动入口。
- ✅ 新增独立 `07-sensevoice-ime.bat`。
- 🔧 修复中文 BAT 编码导致 CMD 把菜单文字当命令执行的问题。
- ⚡ 优化主菜单为 ASCII 稳定文本。
- 📋 新增 `.gitignore`，忽略 build/dist 等本地打包中间产物。
- 🔄 重写 README/DEV_LOG 为产品、技术、受众三维结构。

v0.1.0 (2026-06-09)
- 🚀 初始功能：整合 video-sub-md、tabbit-ai-shortcut、win-layout-manager、doubao-podcast、github-repo-downloader、auto-unzip-interactive 等本地项目入口。
- ✅ 新增编号菜单和独立 BAT 启动脚本。
- ✅ 新增 `generate_bats.py` 用于批量生成启动脚本。
