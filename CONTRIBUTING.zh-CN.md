# 参与 AgentSafe

[English](CONTRIBUTING.md)

从 [README](README.zh-CN.md) 和内置虚构样本开始。Alpha 阶段欢迎可复现的安装反馈、审阅体验改进、误报减少及受支持信号漏检的具体描述。通过小型 issue 或聚焦的 PR 说明问题与可观察的结果。

## 开发

安装 Python 3.11+、Tesseract 与 `eng`，在仓库中执行：

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install '.[dev]'
.venv/bin/agentsafe doctor
.venv/bin/python -m pytest -q
```

若 `python3` 至少为 3.11，也可替换解释器命令。测试读取 `src/`，已安装命令是另一份副本；修改后用 `.venv/bin/python -m pip install .` 更新，再执行 `.venv/bin/agentsafe gui --lang zh`。不要求可编辑安装。

缺少 OCR 会跳过部分测试，请同时报告通过与跳过数量。CI 先运行 `doctor` 并拒绝跳过项；非 OCR 测试通过不证明图片检查正常。

单独验证打包：

```sh
.venv/bin/python -m pip install build
.venv/bin/python -m build
```

把生成的 wheel 安装到新的虚拟环境，切换到仓库外的目录，用新环境运行 `agentsafe doctor`、`agentsafe demo --no-open` 和 `python /仓库绝对路径/scripts/smoke_installed.py`。检查脚本通过短时有认证的本机服务验证打包的 UI 资源、虚构 GUI 扫描和 PNG 副本重检，不向外发送文件。静态 demo 会生成私密临时 HTML，审阅后可删除。

## 保持改动聚焦并提供证据

- 保留 GUI/CLI 共用核心及本地处理。新增格式、依赖、云服务、自动打码或发布集成前，先讨论具体用途。
- 仅使用虚构截图、日志和无效的凭证样式测试值。不要向 issue、PR 或 CI 附件提交真实客户素材、有效 token 或完整私密报告。
- 测试可观察行为：发现与位置、原件不变、输出隐藏敏感值、限制、覆盖失败和不可信输入。跳过或失败不能描述为检查通过。
- 提供平台、Python/OCR 版本、命令和虚构复现。不把精选样本表现当作普遍准确率。
- 行为和安装变化时，同步英文文档与已有中文版本，保持界面中英文解释一致。
- 阅读 [AGENTS.md](AGENTS.md)、[PRODUCT.md](PRODUCT.md) 和 [ARCHITECTURE.md](ARCHITECTURE.md)。历史实验记录不授权扩大功能范围。

漏洞请按 [SECURITY.zh-CN.md](SECURITY.zh-CN.md) 反馈，不要公开详细漏洞。贡献采用项目 [MIT 许可证](LICENSE)，保留适用的第三方声明。
