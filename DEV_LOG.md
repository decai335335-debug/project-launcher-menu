# Project Launcher Menu DEV_LOG

## 1. 项目起源

这个项目的原始需求很简单：本机有越来越多的 AI、字幕、下载、语音、自动化脚本项目，每个项目都在不同路径里。每次启动都要找目录、开终端、敲命令，重复且容易忘。

因此先用最轻的方式做一个本地启动菜单：一个 `启动菜单.bat` 汇总多个项目，输入编号后调用对应的独立 BAT。后来又加入 `Project Launcher Menu.exe`，让这个入口可以固定到任务栏，像普通桌面应用一样随手打开。

核心目标不是做复杂桌面应用，而是把“每天都要启动的本地工具”放进一个稳定入口。

## 2. 迭代时间线

### v0.2.6 - 本地目录重命名

- 将本地项目目录从 `E:\Projects\launchers` 重命名为 `E:\Projects\project-launcher-menu`，与仓库名称保持一致。
- 重新运行 `generate_bats.py`，让 `runtime/启动菜单.bat` 中的项目 BAT 调用路径指向新目录。
- 更新 README 中所有旧路径，避免后续按文档操作时回到旧目录。
- 经验记录：启动器自身目录改名后，需要重新生成菜单；但不需要重新编译 EXE，因为 EXE 查找 `runtime/启动菜单.bat` 使用的是相对自身路径。
### v0.2.5 - 修复 EXE 调用旧菜单路径

- 发现重新整理目录后，旧版 `Project Launcher Menu.exe` 仍然调用 `bat/启动菜单.bat`，但菜单已经移动到 `bat/runtime/启动菜单.bat`。
- 修复 `Project Launcher Menu.spec`：spec 移入 `packaging/` 后不能继续使用旧的 `runtime/launcher_ps.py` 相对路径，改为用 `SPECPATH` 定位项目目录。
- 重新打包 `Project Launcher Menu.exe`，把新的 `runtime/launcher_ps.py` 逻辑编入 EXE。
- 明确规则：以后只是新增或移动菜单项目，通常只改 `bat/launchers/NN-name.bat` 并运行 `generate_bats.py`；只有启动器自身目录结构或 EXE 入口逻辑变化时才需要重新打包。
### v0.2.4 - 根目录瘦身与分类结构

- 调整 `bat/` 目录：第一层只保留 `Project Launcher Menu.exe` 和 `generate_bats.py` 两个常用文件。
- 新增 `bat/launchers/`，集中存放 `01-*.bat` 到 `07-*.bat` 等项目启动脚本。
- 新增 `bat/runtime/`，集中存放 EXE 运行时需要调用的 `启动菜单.bat`、`launcher_ps.py`、`app.ico`。
- 新增 `bat/packaging/`，集中存放 `Project Launcher Menu.spec`。
- 更新 `generate_bats.py`，自动扫描 `launchers/NN-name.bat`，生成 `runtime/启动菜单.bat`。
- 更新 `launcher_ps.py`，让 EXE 从同级 `runtime/启动菜单.bat` 启动菜单。
- README 更新为新版写作指南要求，更新日志改成版本内有序换行。

### v0.2.3 - 入口重命名与历史文件清理

- 将当前推荐入口命名为 `Project Launcher Menu.exe`。
- 将当前打包配置命名为 `Project Launcher Menu.spec`。
- 清理旧的 `启动菜单ps.exe`、`启动菜单ps2.exe`、旧 spec、build/dist、缓存等历史产物。
- 移除早期废弃入口和旧图标，减少仓库噪音。

### v0.2.2 - 自动发现 BAT 启动项

- `generate_bats.py` 从手写项目列表改为扫描 `NN-name.bat`。
- 未来新增 `08-my-tool.bat` 后，运行生成脚本即可自动加入菜单。
- 降低新增项目时改错主菜单的风险。

### v0.2.1 - 固定入口 EXE 与图标资源

- 明确 `Project Launcher Menu.exe` 是当前实际使用入口，可以固定到任务栏或开始菜单。
- 保留 `Project Launcher Menu.spec`，方便之后按同一配置重新打包。
- 保留图标资源，保证 EXE 可以作为桌面入口使用。
- 调整 `.gitignore`：忽略 build/dist 和旧实验 EXE，但保留正式入口 EXE、spec、图标。

### v0.2.0 - SenseVoice IME 接入与文档整理

- 新增第 7 项 `sensevoice-ime`，调用 `E:\Projects\ai\sensevoice_ime\run.bat`。
- 新增 `07-sensevoice-ime.bat`，让每个项目继续保持独立启动入口。
- 将主菜单改成 ASCII 英文，解决 CMD 中文编码导致菜单文字被当成命令执行的问题。
- 更新 `generate_bats.py`，把 7 个项目统一纳入生成清单。
- 新增 README 和 DEV_LOG，按产品、技术、受众三个维度整理项目。

### v0.1.0 - 初始 BAT 启动菜单

- 创建 `bat/启动菜单.bat`。
- 接入 6 个本地项目：video-sub-md、tabbit-ai-shortcut、win-layout-manager、doubao-podcast、github-repo-downloader、auto-unzip-interactive。
- 为每个项目准备独立 BAT 入口。
- 尝试 Tkinter GUI 和 PyInstaller 打包版本。

## 3. 踩坑记录

| 问题 | 根因 | 解决方案 | 涉及版本 |
| --- | --- | --- | --- |
| CMD 把“项目启动菜单”等中文当成命令执行 | BAT 文件编码和 CMD 当前代码页不一致，中文行被错误解析 | 主菜单改为 ASCII 英文文本，避免编码依赖 | v0.2.0 |
| 新增项目后还要修改生成脚本清单 | 固定 `PROJECTS` 列表需要手动维护 | 改为扫描 `launchers/NN-name.bat` 文件自动生成菜单 | v0.2.2 |
| 根目录文件越来越多 | EXE、BAT、图标、spec、启动项都堆在第一层 | 按 `launchers/`、`runtime/`、`packaging/` 分类，第一层只留入口和生成器 | v0.2.4 |
| EXE 移动后找不到菜单 | 原逻辑默认 `启动菜单.bat` 和 EXE 在同一目录 | `launcher_ps.py` 改为从 EXE 同级的 `runtime/启动菜单.bat` 启动 | v0.2.4 |
| 仓库可能上传大量打包产物 | build/dist/spec 是本机生成文件，旧实验 EXE 也会造成混乱 | `.gitignore` 忽略中间产物和旧实验 EXE，但保留正式入口 | v0.2.1 |
| 主菜单里直接写复杂启动命令后维护困难 | 所有逻辑集中在一个 BAT 内会越来越乱 | 每个项目一个独立 BAT，主菜单只做跳转 | v0.1.0 |

## 4. 设计决策

### 为什么用 BAT 菜单而不是完整 GUI?

| 方案 | 优点 | 缺点 | 决策 |
| --- | --- | --- | --- |
| BAT 菜单 | 无依赖、可直接运行、容易调试 | 视觉简单 | 当前主方案 |
| `Project Launcher Menu.exe` | 可固定到任务栏，打开更顺手 | 需要保留打包产物和图标 | 当前推荐入口 |
| Tkinter GUI | 有按钮界面，适合桌面使用 | 打包和路径处理更复杂 | 作为 EXE 入口外壳保留 |
| PowerShell 脚本 | 语法更强，适合复杂逻辑 | 执行策略和用户习惯可能带来阻碍 | 暂不作为主入口 |
| 桌面启动器应用 | 体验最好 | 对当前需求过重 | 长期再考虑 |

### 为什么根目录只留两个文件?

用户每天最常碰的是 `Project Launcher Menu.exe`，新增项目时最常碰的是 `generate_bats.py`。其它文件虽然必要，但不应该和常用入口混在一起。分类后第一层更像“操作台”，子目录才是“工具箱”。

### 为什么新增项目放到 `launchers/`?

`launchers/` 只存放可被菜单调用的项目入口，命名规则统一为 `NN-name.bat`。这样 `generate_bats.py` 可以稳定扫描，也方便肉眼判断编号和项目名。

### 为什么菜单文本改成英文?

BAT 文件在 Windows CMD 中容易受到编码影响。中文菜单虽然好看，但一旦文件编码和代码页不一致，CMD 可能把乱码片段当作命令执行。英文 ASCII 菜单牺牲一点可读性，换来稳定性。

### 为什么每个项目一个独立 BAT?

主菜单应该只做“选择和跳转”。具体项目怎么启动，放在独立 BAT 里。这样新增、删除、调试某个项目时不会影响其它项目。

## 5. 实际测试数据

| 测试项 | 结果 |
| --- | --- |
| `generate_bats.py` 自动扫描 `launchers/` 下 7 个 `NN-name.bat` 项目 | 成功 |
| 生成 `runtime/启动菜单.bat` | 成功 |
| `runtime/launcher_ps.py` 指向 `runtime/启动菜单.bat` | 已确认 |
| `Project Launcher Menu.spec` 指向 `runtime/launcher_ps.py` 和 `runtime/app.ico` | 已确认 |
| `bat/` 第一层只保留 `Project Launcher Menu.exe` 和 `generate_bats.py` 两个文件 | 已确认 |
| 重新打包后的 `Project Launcher Menu.exe` 调用 `runtime/启动菜单.bat` | 已完成 |
| 第 7 项 `sensevoice-ime` 路径存在 | 成功配置 |

## 6. 文件位置

```text
project-launcher-menu/
├── README.md
├── DEV_LOG.md
├── .gitignore
└── bat/
    ├── Project Launcher Menu.exe
    ├── generate_bats.py
    ├── launchers/
    │   ├── 01-video-sub-md.bat
    │   ├── 02-tabbit-ai-shortcut.bat
    │   ├── 03-win-layout-manager.bat
    │   ├── 04-doubao-podcast.bat
    │   ├── 05-github-repo-downloader.bat
    │   ├── 06-auto-unzip-interactive.bat
    │   └── 07-sensevoice-ime.bat
    ├── runtime/
    │   ├── 启动菜单.bat
    │   ├── launcher_ps.py
    │   └── app.ico
    └── packaging/
        └── Project Launcher Menu.spec
```


