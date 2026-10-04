# AgentSafe

[English 原文](README.md) · 中文译本。

### 别把你的 AI agent 看到或生成的内容意外发布出去。

**为即将发布到公开 Git 仓库的截图和调试产物提供本地隐私检查。**

你的 agent 为了证明修复有效，截取了一个浏览器窗口。但截图里仍然有内部 URL 和账户邮箱。一次范围过大的 `git add .`，就可能让它进入下一次提交。

AgentSafe 的设计目标是在产物公开之前阻止这次推送，并告诉你哪些内容需要检查。

以下保留英文 CLI 示例，方便与原文及未来的命令行界面对照：

```text
AgentSafe Privacy Gate
Destination: github.com/example/ui-demo   Visibility: PUBLIC

HIGH    F12  screenshots/dashboard.png
        Configured internal URL + email address (local OCR)
HIGH    F13  debug/session.har
        Authorization + session-cookie values
REVIEW  F14  demo.mov
        Video content not inspected

Push stopped. Inspect the exact versions, fix, or explicitly approve.
```

示例表示：截图命中已配置的内部 URL 和邮箱；HAR 含有 Authorization 和会话 cookie；视频内容没有被检查。推送被停止，需要检查对应版本、修复，或明确批准。

**概念草案，尚未发布。** 上面是使用虚构数据展示的拟议 CLI，不是已经运行的软件录像。项目名称仍是暂定名。本仓库尚未提供可执行程序、安装包或安装命令。

**设计评审：** [二次评审](PRODUCT.zh-CN.md#second-pass-review)正在重新考虑“每张图片都必须审阅”，并验证 Git push 是否确实是目标用户使用的发布路径。下述流程仍是等待这些决定的提案。

示例中的内部域名和会话 cookie 名称，均已被明确配置为敏感项。普通邮箱或偏好设置 cookie 本身，不足以构成 HIGH 风险。

## 为什么需要它

Coding agent 越来越多地生成截图、日志和浏览器调试记录。即使这些文件没有包含可识别的 API key，也可能暴露个人信息或内部上下文。

AgentSafe 关注的是**产物发布决策**：哪些已经提交的证据即将离开你的机器、会被发到哪里，以及对应的确切内容是否已经经过审阅。你仍应保留现有的凭证扫描工具；AgentSafe 的目标是补充它的能力。

最初的目标用户，是向公开 GitHub 发布浏览器或 agent 生成证据的开源 Web 开发者。它不依赖某一种 Coding Agent。

## 拟议的 v0.1

- 检查实际的 GitHub.com 推送目标；可见性未知时采用公开仓库策略。
- 检查待推送提交中的选定产物版本，包括后来被删除或替换的版本。
- 使用本地 OCR，在 PNG/JPEG 截图中定位可读邮箱和已配置的内部域名。
- 使用少量规则检查调试文本，以及 HAR 中的认证和 cookie 字段。
- 对选定图片要求确切版本的审阅，并明确标记没有检查内容的媒体或文档。
- 提供隐藏敏感值的检测结果、仓库本地 pre-push hook、绑定内容的批准记录，以及明确的忽略配置。

```text
捕获 / 调试 -> git add -> git commit -> AgentSafe 检查 -> git push
                                            |
                                      检查 -> 修复或审阅
```

## 预期使用流程

这些命令描述的是拟议接口，目前还不能在这个草案仓库中运行。发布前会核实分发名称与安装说明；不要假定名为 `agentsafe` 的软件包属于本项目。

```text
agentsafe init
agentsafe scan --staged
git commit
git push

# 推送被停止之后：
agentsafe inspect F12 --open
agentsafe allow F12 --reason "Reviewed synthetic demo"
git push
```

批准只适用于界面列出的要求，以及对应的确切文件内容、路径、目标和策略。内容变化后，需要重新审阅。重试前应检查所有尚未处理的项目。

如果内容确实敏感，需要修复包含它的、尚未推送的提交。修改工作区文件或在后续提交里删除它，并不会消除较早的 Git 版本。AgentSafe 会解释这一点，但不会自动改写你的历史。

## 本地处理与明确的限制

产物扫描在你的机器上完成。可见性查询只向 GitHub 发送仓库目标元数据，不发送产物内容。离线模式采用保守的公开仓库策略。当前计划不需要 AgentSafe 账户，也不使用云端视觉分析或遥测。

OCR 可能漏掉很小、模糊或语言不受支持的文字。工具无法可靠判断保密后台或客户名称，因此初稿提出：即使没有命中规则，也要求审阅选定图片。已识别的视频、PDF 和其他无法检查内部内容的候选产物，需要在未扫描内容的情况下审阅。自动打码和 QR 解码不属于 v0.1。

本地 hook 只覆盖已安装该 hook 的仓库中的本地 Git push。它可以被绕过，不能保护 API 上传、PR 附件、release/CI 产物、LFS 实际载荷传输，或尚未安装 hook 的新仓库。它不会审计一个后来变为公开的私有仓库。扫描通过不是隐私安全认证。

## 设计文档

- [产品定义与竞争评估](PRODUCT.zh-CN.md)
- [Demo、发布和发布后路线图](ROADMAP.zh-CN.md)
- [架构、拟议技术栈与仓库结构](ARCHITECTURE.zh-CN.md)
- [贡献者与 Coding Agent 工作约束](AGENTS.zh-CN.md)

下一步是 review 这些草案。明确批准之后才开始实现。MIT 是拟议的开源许可证；目前尚未确立许可证授权，也尚未发布软件包。

## 发布时的视觉方案

用一段已经验证、使用虚构数据的 30–45 秒 demo 替换说明性的终端代码块：捕获 → 推送被停止 → 检查确切版本 → 审阅后重试。在主标题下方加入虚构截图与标出审阅区域的并排对比。所有原始值都必须是虚构的；展示 OCR 在本地运行，并演示一个在后续删除之后仍然存在的历史版本。

README 首屏应让人几秒内理解“截图也会泄漏上下文”。避免虚构徽章、未经验证的准确率，或“第一个截图扫描工具”之类的表述；OCR 扫描和本地打码工具已经存在。
