# 虚构 demo 样本与首次实测

[English 原文](README.md) · 中文译本。

全部示例均为虚构。生成器用 Pillow 内置字体在本地绘制截图，不截取真实应用。保留域名 `northstar.test` 被明确配置为敏感。认证字符串是虚构的无效值，不是打码占位符，因此可以检验结构规则。测试另在临时目录创建损坏/不支持输入。

`dashboard-reviewed.png` 和 `session-reviewed.log` 是另外准备的用户修改示例，不是自动打码工具的输出。它们演示审阅/重扫流程，不修改原件。不使用真实客户、员工或会话数据。

## 标签与实测结果

2026 年 10 月 5 日；macOS 26.5.1 arm64、Python 3.12.12、Tesseract 5.5.2（eng）、Pillow 12.3.0、Rich 14.3.4、Typer 0.27.2、pytest 9.1.1。未记录 CPU 型号。时间来自此前测试之后，每文件一次顺序的进程内扫描，不含 CLI 启动与安装；没有提取缓存。这是观察值，不是 p95 或冷启动基准。

| 文件 | 预期标签 / 用途 | 退出码 | HIGH / WARN | 秒 |
| --- | --- | --- | --- | --- |
| dashboard.png | URL 和账户邮箱包含配置域名 | 1 | 1 / 1 | 0.191 |
| dashboard-reviewed.png | 人工准备的正常副本 | 0 | 0 / 0 | 0.161 |
| public-page.png | 正常公开文档 | 0 | 0 / 0 | 0.167 |
| public-page.jpg | 正常 JPEG 编码 | 0 | 0 / 0 | 0.180 |
| heldout-summary.jpg | 不同布局/字体，包含配置域名 | 1 | 1 / 0 | 0.104 |
| small-blurred.png | 已知敏感性，困难 OCR 探针 | 0 | 0 / 0 | 0.057 |
| blank.png | 空白图片，显示无文字限制 | 0 | 0 / 0 | 0.049 |
| session.log | 认证字段、配置会话 cookie 和主机名 | 1 | 3 / 1 | 0.001 |
| session-reviewed.log | 打码占位字段，普通偏好 cookie | 0 | 0 / 1 | <0.001 |
| benign.log | header 提及/占位符、示例和普通 cookie | 0 | 0 / 3 | <0.001 |

十个输入均按受支持格式完成处理。`dashboard.png` 中 URL 被识别到，但 OCR 置信度较低，因此给出 WARN；配置邮箱域名得到 HIGH。不要只为了让演示更有冲击力就调整阈值。

**已知漏检：** `small-blurred.png` 包含已配置域名，但没有提取出可读文字。返回 0，同时显示无可读文字的限制。保留这个探针：OCR 进程完成不证明图片没有敏感数据。保留的另一布局在首轮规则完成后评估，只是一个虚构变体，不是独立准确率基准。

初版源码测试在本机得到 **59 项通过，0 项跳过**，包含六个真实 OCR 样本案例。本次可用性改进后得到 **74 项通过，0 项跳过**，新增在仓库目录之外运行完整附带样本 demo 的真实 OCR 检查。依赖一致性检查（`pip check`）也通过。这些仅是本地 demo 的证据。

## 复现

按[主 README](../../README.zh-CN.md)在仓库根目录安装；Tesseract 不在 PATH 时先配置路径：

```sh
.venv/bin/agentsafe scan examples/synthetic/dashboard.png examples/synthetic/session.log --config examples/synthetic/policy.toml
.venv/bin/agentsafe scan examples/synthetic/dashboard-reviewed.png examples/synthetic/session-reviewed.log --config examples/synthetic/policy.toml
.venv/bin/agentsafe scan examples/synthetic/small-blurred.png --config examples/synthetic/policy.toml
.venv/bin/python -m pytest -q
```

仅在需要时用 `.venv/bin/python examples/synthetic/generate.py` 重新绘图。Pillow/字体版本可能改变字节和 OCR 结果，应重新验证标签，不假设输出相同。

自动化测试检查结构决策、原文件不变、隐藏敏感值的诊断、无效配置、符号链接/管道拒绝、不支持/损坏/旋转/动画输入、字节/像素/行数/发现数/时间限制，以及真实 OCR。测试禁用了 Python socket 连接，但这不是对可信原生 OCR 程序的操作系统级网络审计，也没有数据包层面的声明。

这些证据支持 review 一个小型私有技术 demo，不证明通用准确率、市场需求、阻止真实事件、其他平台干净机器安装或公开发布就绪。

## 一条命令的可视化 demo

```sh
.venv/bin/agentsafe demo --lang zh --no-open
```

去掉 `--no-open` 会请求打开默认浏览器。 已安装命令在 `/private/tmp`、不设置 Tesseract 环境变量时验证成功：修改前 4 HIGH/2 WARN（扫描退出 1），修改后 0 HIGH/1 WARN（扫描退出 0），已知漏检 0 HIGH/0 WARN（扫描退出 0），demo 退出 0。 已检查 HTML 生成、文本隐藏敏感值、快照保留、私密权限、保守清理和 JavaScript 语法。 没有通过其他服务方式绕过限制。

样本生成器会同步六个随包安装的 demo 资源，测试检查它们与源样本一致；重新生成后需重新安装本地包。预览文件生命周期见主 README。

此次审阅发现日志留白大、条目看起来可点击、OCR 说明残留英文、无框时仍有开关，以及已知漏检旁的状态容易让人安心。 这些问题已通过紧凑静态日志行、翻译并去重 OCR 说明、仅在有框时显示开关、黄色无文字/人工检查状态及独立摘要处理。 扫描发现、覆盖和退出决策保持原有含义。

更新后的源码测试在参考机器得到 **79 项通过，0 项跳过**。 回归检查人工检查状态不虚构风险发现、按实际区域显示控件、文本隐藏敏感值及失败优先级。 审阅确认日志列表紧凑、OCR 说明为中文、无定位框时没有开关、无文字状态为黄色并独立计数，修改前后发现数量保持一致。 响应式表现和自动化浏览器交互仍未验证。
