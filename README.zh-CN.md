# AgentSafe

[English 原文](README.md) · 中文译本。

### Don't accidentally publish what your AI agent saw or generated.

**分享截图和调试日志前，先在本地检查。**

这个私有实验本地应用检查截图和日志中你指定的敏感名称／短语、内部域名及带值的认证字段。浏览器 GUI 可选择文件、可选填写上下文、扫描，并查看图片位置或可点击定位的脱敏日志片段。技术用户与 agent 可使用同一核心的 CLI。

**在本机已准备好的工作区中，用 Finder 双击 `AgentSafe.app`。** 日常检查无需输入终端命令。开发启动器使用从本仓库环境准备的私有运行副本，以及已有 Python 解释器与 Tesseract，还不是独立安装包。

选择文件 → 可选填写敏感名称或域名 → 检查 → 审阅 → 用熟悉的工具修改 → 重新选择更新后的文件 → 再检查。没有文件时，可试用应用中的「客户／项目名」「修改前」「修改后」「已知 OCR 漏检」样本。

![实际本地 GUI，检查虚构的客户名和项目名](docs/images/gui-preview.png)

附带虚构 demo 的真实运行结果节选：

```text
HIGH     examples/synthetic/dashboard.png
  WARN  Configured sensitive domain; value hidden
        region x=122 y=308 w=456 h=24 (source pixels); uncertain OCR extraction
  HIGH  Email uses a configured sensitive domain; value hidden
        region x=171 y=376 w=229 h=24 (source pixels)

HIGH     examples/synthetic/session.log
  HIGH  Populated Authorization field; value hidden (validity not checked)
        line 8

Coverage: 2 inspected, 0 uninspected, 0 failed
Findings: 4 HIGH, 2 WARN | Exit: 1
```

**私有技术 demo，尚未公开发布。** 名称和公开分发仍待决定。不需要真实业务产物：所有示例都是虚构的，已审阅副本另行准备，并非自动打码产物。需求和真实准确率仍未验证。

从已准备好的仓库启动新交互界面：

```sh
.venv/bin/agentsafe gui --lang zh
```

它会打开默认浏览器；Mac 开发启动器默认打开中文界面。独立安装包和干净机器上的安装体验仍是后续发布工作。

源码/依赖变化后，从已准备环境运行一次以重建 Mac 开发启动器（需要已有 Apple Command Line Tools/clang）：

```sh
.venv/bin/python scripts/build_macos_launcher.py
```

原生启动二进制是本地忽略的构建产物；应用元数据与构建源码纳入版本管理。构建将已有依赖和当前包代码复制到私有系统临时目录的运行副本，不复制用户扫描输入、不下载依赖，启动时无需读取 Desktop 中的项目目录。系统清理运行副本或基础 Python 路径变化后需重建。这个开发方案还不是干净机器分发。

原来的静态可视化 demo 仍可使用：

```sh
.venv/bin/agentsafe demo --lang zh
```

它会扫描附带虚构样本，并打开包含图片标记、修改后对照和已知漏检的本地页面。

## 交互式本地 GUI

支持文件选择框或拖放、可移除的文件列表、可选敏感词／短语、内部域名及会话 Cookie 名称、异步进度、隐藏敏感值的结果和图片高亮。提供虚构样本、「清除结果」和「结束使用」。格式为 PNG/JPEG 与 UTF-8 `.log`/`.txt`；最多 20 个文件，总计 24 MiB，仍适用单张图片 10 MiB、单个文本 5 MiB 及解码/OCR 限制。不支持文件和错误会明确显示，不扫描目录。

体验新增能力时，直接点击「客户／项目名」，无需选择文件或填写配置。样本只配置虚构名称、不配置域名；参考 Mac 上定位到 2 个图片区域与 3 条日志行（5 HIGH / 0 WARN）。原有修改前/修改后/OCR 漏检样本继续使用各自预设策略。

自己的文件中，两个主要输入框都可留空，普通邮箱/认证字段/Cookie 仍会自动检查。「敏感词／短语」填写客户名、项目名或准确短语，每行一项，例如 `Project Cedar`、`Acme Training`；「内部域名」只填域名，例如原始样本的 `northstar.test`，同时匹配子域名及该域名邮箱。样本按钮使用已说明的预设配置；「开始检查所选文件」使用你填写的设置。设置不会跨会话保存。

浏览器选中的是快照。**修改原件后，请重新选择更新后的文件，再检查。** 改动选择或设置，会提示下方是上一次扫描结果。零发现不代表安全，没有识别出文字的图片需要人工检查。

日志现在有**脱敏预览**。试用「修改前」，滚动到 `session.log`，点击认证或 Cookie 问题，即可高亮对应行。`Authorization`、`demo_session` 等名称保留，值及命中的敏感词、域名、邮箱替换为 `[隐藏]`（英文页面为 `[HIDDEN]`）。只保留命中行与少量上下文，省略号表示未展示内容；没有发现就不展示片段。完整内容仍在原文件中。这不会生成可安全分享的日志副本，未支持的秘密或私密上下文仍可能保留。[虚构日志审阅的实际截图](docs/images/gui-log-preview.png)。

`gui` 只在随机端口绑定 `127.0.0.1`。文件字节从浏览器传给这台电脑上的进程，不传给外部服务。所有 API 操作要求随机会话凭证，检查确切的 Host/Origin，不授予 CORS；只提供固定应用资源，不提供任意文件路径。无遥测、外部资源或运行期下载。

原始快照与 OCR 仅在内存中临时处理。最新的隐藏敏感值结果（包含脱敏日志片段与规范化可见图片像素）保留至清除、被替代、会话结束、进程退出或 30 分钟无请求。AgentSafe 不写出报告文件或数据库。浏览器可能保有自身内存/缓存，不保证浏览器或操作系统绝无持久化。标签页 session storage 仅存支持刷新的随机连接凭证，不存产物或策略。关闭标签页不会立即停止进程，需明确清理时点击「结束使用」。

原有 `demo` / `scan --preview` 仍按下方说明生成静态临时 HTML，生命周期独立；GUI 不生成这些文件。图片未打码，不修改原件、不拦截上传或 Git push。

## 运行本地 demo

需要 Python 3.11+、Tesseract 及英语（`eng`）数据。本次在 macOS 26.5.1 arm64、Python 3.12.12、Tesseract 5.5.2 上验证。Linux/Windows 安装尚未验证。

在本仓库内，使用已有 Python 3.12 解释器创建环境并安装本地项目：

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install '.[dev]'
```

原生 OCR 依赖单独安装。macOS 使用 Homebrew：

```sh
brew install tesseract
```

Tesseract 会从 PATH 及 macOS 标准 Homebrew 路径自动查找；本工作区无需环境变量。需要显式覆盖时使用：

```sh
export AGENTSAFE_TESSERACT=/opt/homebrew/bin/tesseract
```

本工作区已准备好环境和 OCR 依赖，可直接运行：

```sh
.venv/bin/agentsafe doctor --config examples/synthetic/policy.toml
.venv/bin/agentsafe scan examples/synthetic/dashboard.png examples/synthetic/session.log --config examples/synthetic/policy.toml
```

扫描会按预期返回 **1**，因为虚构原件包含受支持的风险线索。再对比人工准备的已审阅版本：

```sh
.venv/bin/agentsafe scan examples/synthetic/dashboard-reviewed.png examples/synthetic/session-reviewed.log --config examples/synthetic/policy.toml
```

这次返回 **0**，保留一条偏好 cookie 警告。用已有本地查看器/编辑器打开原文件，检查提示区域或行，自行修改并重扫。AgentSafe 不修改原文件。

以短横线开头的文件名放在 `--` 后。不遍历目录。不要安装其他同名公开 `agentsafe` 软件包；这里仅说明从本地仓库安装。本机跳过隐藏的 editable 安装 `.pth` 文件，因此采用普通安装；修改源码后，验证已安装 CLI 前需要重新安装本地包。

## 可视化审阅

```sh
.venv/bin/agentsafe demo --lang zh
.venv/bin/agentsafe scan examples/synthetic/dashboard.png --config examples/synthetic/policy.toml --preview --lang zh
```

`demo` 所需虚构图片、日志和配置已随本地包安装，离开仓库目录也能运行。它扫描三个分组：修改前、预先准备的修改后对照，以及已知的小字模糊 OCR 漏检。切换分组，点击图片检测条目高亮对应区域，或关闭标记框查看原来的图片。日志展示有发现的行的脱敏片段，点击问题说明即可高亮原始行号对应的位置，不嵌入原始日志。只有存在定位框时才显示标记开关。OCR 未提取出文字的图片使用黄色人工检查状态，分组摘要单独提示；不增加 WARN/HIGH 数量，也不改变扫描退出码。中文页面翻译 OCR 提示，并合并重复的无文字说明。修改后对照不是自动打码生成的。

`--lang zh` 显示中文页面（普通 `scan` 终端输出仍为英文）。`--no-open` 只生成页面，不打开浏览器；默认会尝试用系统默认浏览器打开本地 HTML，打开失败可手动打开打印的路径。OCR 缺失仍明确报错。全部样本检查和页面生成完成时，`demo` 返回 0，即使修改前分组含 HIGH；检查或页面生成不完整返回 2。`scan --preview` 保留普通扫描退出码，预览生成失败返回 2。

**预览包含图片可见内容，并非打码后的导出文件。** 页面使用实际扫描时的归一化图片快照与 SVG 标记框，不重新读取或修改原件，只嵌入命中行的有限脱敏片段，不保存日志原文或 OCR 全文。不需要服务器、外部脚本、字体或网络请求。图片和日志中未命中的上下文仍可能透露私密信息，自己的预览应保持私密。

页面存放在 Git 仓库外、操作系统临时目录中的 `agentsafe-previews-<user>/`。POSIX 上目录权限为 700、文件为 600；Windows 权限行为尚未验证。保持原有文件布局的会话超过 24 小时后，在下次生成预览时清理；没有后台自动删除。用完也可自行删除页面或会话目录。每个页面的归一化图片总量限制为 24 MiB。不带 `--preview` 的普通 `scan` 不生成预览，也不打开查看器。

## 检查内容

- 明确指定的 PNG/JPEG 路径和 UTF-8 `.log`/`.txt` 文件。
- 使用本地 OCR 识别可读英文图片文字，提供原始像素坐标。
- 已配置的字面敏感词／短语与敏感域名、带值 Authorization/Proxy-Authorization 字段和已配置会话 cookie 名称。
- 普通邮箱和其他带值 cookie 给出警告；低置信度 OCR 匹配也只警告。

仅在指定 `--config` 时读取配置：

```toml
sensitive_domains = ["northstar.test"]
session_cookie_names = ["demo_session"]
sensitive_terms = ["Project Cedar", "Acme Training", "华星演示客户"]
```

敏感词在同一行内做字面匹配，英文不区分大小写，短语间空白可变化，英文采用 ASCII 单词边界。空格/逗号属于短语；不支持正则、拼写变体或跨行匹配。去首尾空白/合并空格、按大小写无关去重，最多 100 项，每项 2–128 字符，不含控制字符。可靠配置命中为 HIGH、不确定 OCR 为 WARN；说明隐藏具体内容，图片框定位可见像素，日志给出行号。中文适用于 UTF-8 文本，图片 OCR 仍为英文。这不代表自动发现保密名称或理解业务数据。

也可通过共用 CLI 对比业务上下文：

```sh
.venv/bin/agentsafe scan examples/synthetic/business-context.png examples/synthetic/business-context.log --config examples/synthetic/terms-policy.toml
```

示例域名和全部认证值均为虚构。保留示例邮箱和明显占位符会被抑制，除非域名被明确配置为敏感。HIGH 是结构/配置证据，不代表凭证实际有效。无命中的图片不需要批准。

## 结果与限制

| 退出码 | 含义 |
| --- | --- |
| 0 | 全部输入已检查，没有 HIGH，仍可能有警告。 |
| 1 | 检查完成，存在需要审阅的 HIGH。 |
| 2 | 设置/输入/检查失败，优先于检测结果。 |

不支持输入、图片损坏、编码错误、OCR 缺失和超出限制，不会被悄悄判通过。`doctor` 就绪返回 0，前置条件/配置问题返回 2。文本扫描不要求 Tesseract，图片扫描需要。

**已知漏检：** 附带的小字模糊截图包含已配置域名，但 OCR 未提取出文字，扫描返回 0 并显示限制。这真实展示了覆盖空缺，不是图片安全的判断。参见[样本标签与实测结果](examples/synthetic/README.zh-CN.md)。

初始限制：单图 10 MiB/2000 万像素，单文本 5 MiB/100,000 行，单行 32,768 字符，单文件 200 条发现，单次 20 文件，每个 OCR 子进程 10 秒。60 秒总预算在阶段之间协作检查，不是对解码器/文件读取的硬沙箱。不悄悄截断输入。动画和 EXIF 旋转 JPEG 会被拒绝；透明像素渲染在白底上。隐藏像素和元数据不检查。

只覆盖已声明的文字模式。任意 API key/密码、内部后台识别、自动名称/敏感性分类、人脸、QR、PDF/视频/HAR 解析和自动打码不属于 demo。源码 secret scanner 不会自动扫描图片 OCR 输出。

普通 CLI 扫描不联网、不创建原图/OCR 临时文件；GUI 仅增加前文所述本机连接。显式 `--preview` 和 `demo` 会按上文说明生成私密本地 HTML。Tesseract 通过 stdin/stdout 运行，安装下载另行进行。报告仍包含可能敏感的文件名，分享输出前请审阅。

这是人工触发的本地检查，不检查 Git 历史、不安装 hook、不拦截任何上传或推送。扫描后修改需要重扫。通过不等于隐私认证。

## 开发与证据

```sh
.venv/bin/python -m pytest -q
.venv/bin/python examples/synthetic/generate.py
```

测试覆盖决策、隐藏敏感值、覆盖失败和真实 OCR。缺少 Tesseract/eng 时，OCR 测试会明确跳过，不能把跳过的运行当作 OCR 验证。源码测试使用 `src/`；修改后运行 `.venv/bin/python -m pip install .` 刷新已安装命令。样本生成器用 Pillow 绘制虚构布局，不截取屏幕。

2026 年 10 月 6 日：参考 Mac 上 **93 项测试通过、无跳过**，包含认证本机请求、格式错误/超限选择、覆盖失败、缺失 OCR、隐藏敏感值、真实 OCR、清除/重扫和结束。真实浏览器验证文件选择框、无效域名设置、原始文件（4 HIGH / 2 WARN）、已审阅文件（0 HIGH / 1 WARN）、图片高亮和刷新恢复。上方实际截图仅含虚构数据。已验证原生 LaunchServices 启动及只监听本机的进程。部分后续浏览器工具点击发生调度超时；拖放与小屏布局尚未全面验证。不据此宣称干净机器/跨平台支持或独立用户易用性。

2026 年 10 月 7 日：参考 Mac 上 **122 项测试通过、无跳过**。新增验证不配置域名的敏感短语、中文日志、标点/正则符号的字面词、英文单词边界、隐藏敏感值、配置/资源失败，以及 OCR 短语框/置信度。虚构业务图片/日志分别得到 2、3 条 HIGH。真实浏览器验证新样本、图片点击高亮、自行选择文件并填写三项敏感短语、无效敏感词/旧结果提示，以及相同文件留空配置重扫（0 发现）和恢复敏感词重扫（5 HIGH）。本地安装和开发启动器已按本轮源码重建，并验证原生启动后的本机监听服务提供新版界面。这仍是虚构证据，干净机器分发与更全面 UI 验证待完成。

2026 年 10 月 7 日，脱敏日志后续改进：**137 项测试通过、无跳过**。新增验证认证/Cookie/敏感词/域名/邮箱遮蔽、重叠范围、格式异常的 Cookie 上下文、占位符、HTML/控制字符转义、长行窗口、普通扫描默认不保留片段、原件与快照一致，以及失败不保留部分片段。真实浏览器检查修改前（4 HIGH / 2 WARN）、修改后（0 HIGH / 1 WARN）和业务样本（5 HIGH / 0 WARN），验证点击切换行高亮/聚焦及中文遮蔽；该轮未观察到浏览器警告/错误。上方截图仅含虚构数据，更广泛的小屏、干净机器和独立用户验证仍待完成。

项目目前处于私有 demo review 阶段。先判断检测结果和定位是否易懂，再增加集成。公开发布、许可证和 Git 路线均为后续决策；MIT 仍是建议，尚未确立许可证授权。

## 设计文档

- [产品定义与竞品评估](PRODUCT.zh-CN.md)
- [路线图](ROADMAP.zh-CN.md)
- [架构与覆盖](ARCHITECTURE.zh-CN.md)
- [贡献者与 agent 工作约束](AGENTS.zh-CN.md)
