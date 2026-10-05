# AgentSafe

[English 原文](README.md) · 中文译本。

### Don't accidentally publish what your AI agent saw or generated.

**分享截图和调试日志前，先在本地检查。**

这个私有实验 CLI 查找配置为敏感的域名和带值的认证字段，显示图片区域或文本行号，并隐藏匹配值。

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

如果 Tesseract 已在 PATH，无需额外配置。当前 Apple Silicon 开发机器的 Homebrew 不在默认 PATH，使用：

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

## 检查内容

- 明确指定的 PNG/JPEG 路径和 UTF-8 `.log`/`.txt` 文件。
- 使用本地 OCR 识别可读英文图片文字，提供原始像素坐标。
- 已配置敏感域名、带值 Authorization/Proxy-Authorization 字段和已配置会话 cookie 名称。
- 普通邮箱和其他带值 cookie 给出警告；低置信度 OCR 匹配也只警告。

仅在指定 `--config` 时读取配置：

```toml
sensitive_domains = ["northstar.test"]
session_cookie_names = ["demo_session"]
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

只覆盖已声明的文字模式。任意 API key/密码、内部后台识别、名称/人脸、QR、PDF/视频/HAR 解析和自动打码不属于 demo。源码 secret scanner 不会自动扫描图片 OCR 输出。

运行期扫描不联网，不创建原图/OCR 临时文件；Tesseract 通过 stdin/stdout 运行，安装下载另行进行。报告仍包含可能敏感的文件名，分享输出前请审阅。

这是人工触发的本地检查，不检查 Git 历史、不安装 hook、不拦截任何上传或推送。扫描后修改需要重扫。通过不等于隐私认证。

## 开发与证据

```sh
.venv/bin/python -m pytest -q
.venv/bin/python examples/synthetic/generate.py
```

测试覆盖决策、隐藏敏感值、覆盖失败和真实 OCR。缺少 Tesseract/eng 时，OCR 测试会明确跳过，不能把跳过的运行当作 OCR 验证。源码测试使用 `src/`；修改后运行 `.venv/bin/python -m pip install .` 刷新已安装命令。样本生成器用 Pillow 绘制虚构布局，不截取屏幕。

项目目前处于私有 demo review 阶段。先判断检测结果和定位是否易懂，再增加集成。公开发布、许可证和 Git 路线均为后续决策；MIT 仍是建议，尚未确立许可证授权。

## 设计文档

- [产品定义与竞品评估](PRODUCT.zh-CN.md)
- [路线图](ROADMAP.zh-CN.md)
- [架构与覆盖](ARCHITECTURE.zh-CN.md)
- [贡献者与 agent 工作约束](AGENTS.zh-CN.md)
