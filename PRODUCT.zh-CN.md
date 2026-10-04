# AgentSafe — 产品定义

[English 原文](PRODUCT.md) · 中文译本。

**状态：** 等待 review 的草案，尚未授权实现产品。  
**调研日期：** 2026 年 10 月 5 日。  
**暂定名称：** AgentSafe；名称是否适合正式使用尚未确认。

<a id="second-pass-review"></a>

## 二次评审 — 2026 年 10 月 5 日

**评审状态：** 下方初稿的默认策略和发布范围正在重新讨论，不是已经批准的需求。下面的建议需要在实现之前统一修订到各份文档中；它们并未悄悄替换后面的详细约定。

1. **首先验证拦截位置。** 截图泄漏证明有问题存在，却不能证明 Git push 是主要发布路径。请潜在用户回顾最近三次产物发布：是受 Git 跟踪的 blob、release/API 上传、附件，还是 CI 产物？pre-push 产品应面向其真实路径能被覆盖的用户。否则应评估与某一个上传工具结合的、明确的本地发布前检查，不要扩成通用的数据外发控制平台。
2. **默认策略优先考虑选择性阻止。** 阻止强凭证线索或已配置的敏感内容；对普通邮箱、普通 cookie 和没有检查的格式发出提醒。成功检查且没有发现问题的图片，不应仅因是图片就强制批准。用户可主动选择严格策略，要求审阅每张选定图片。这会接受残余的视觉上下文风险，必须明确说明。受支持内容扫描失败，仍然应报告可见错误；更改默认策略是产品取舍，不代表检测能力增强。
3. **缩小首次实现实验。** 从 PNG/JPEG、指定文件扫描、staged 扫描、少量证据规则、隐藏敏感值且能有效定位问题的输出，以及范围有限的例外机制开始。先验证检测结果有用、安装可用，再做完整 hook/批准生命周期。如果 v0.1 面向 Git，在实验之后加入正确的 pre-push 适配器；除非试用证明有必要，否则后置 HAR 专门解析、导出/报告覆盖、对未检查内容的强制批准，以及复杂的批准管理。
4. **不要在截图承诺中留下凭证检测空缺。** 安装现有源码扫描器，并不会自动把 OCR 文本送入它。要么为一个成熟的本地 secret 引擎增加小适配器，要么明确说明图片里独立出现的 API key/密码不属于初版规则。复用检测，不自己实现各服务商 token 规则目录。
5. **按暴露上下文收窄用户。** 优先考虑处理真实登录态/内部数据，又向外发布 demo 或问题复现的开发者。“每周向公开 Git 发布”的筛选条件，只有验证发布渠道之后才适用。一般开源前端开发者可能没有多少敏感内容需要保护。
6. **衡量不必要的打断，而不只是规则准确率。** 正确识别公开邮箱，仍可能做出错误的发布决策。样本应同时标注实体是否存在，以及是否应该阻止发布。记录正常推送被打断的次数、解决耗时、反复覆盖决定和关闭工具的情况。现有的 95%/90% 目标，以及 5 名试用者中留存 3 名的门槛，属于规划假设，不是产品与市场契合的统计证据。
7. **实现选择保持暂定。** 确定 Tesseract 之前，先测试浏览器小字号截图的 OCR 质量和干净机器的安装体验。如果实际目标的可信远程 ref 能证明历史已经发布，就不要让每个新分支都触发全历史重扫。全量遍历仍可作为保守回退，不应是预期的正常使用体验。
8. **不要把例外记录等同于人工授权。** 一个努力完成正常任务的 agent，也可能执行文档中的 `allow --yes`，无需具有恶意。默认指导应要求它报告被阻止的结果，等待用户决定，而不是建议自行批准。这是针对愿意配合的 agent 的行为指导，不是防篡改强制控制。

当前需要先决定：验证一个 **Git 产物发布检查工具**，还是在另一种上传位置做**产物发布前检查**。本地扫描核心以后可以支持两者；首发承诺应选择一个实际覆盖的流程。

## 1. 建议方向

为即将发布到公开 GitHub 仓库的截图和调试产物，做一个小型本地发布检查工具。先面向使用具备浏览器能力的 Coding Agent、为改动生成视觉证据的开发者。

更大的愿景是**为 AI 生成的开发产物提供隐私保护**。第一个产品承诺应更窄：

> 在截图和调试产物进入公开 Git 仓库之前，对它们进行检查与审阅。

品牌文案：

> Don't accidentally publish what your AI agent saw or generated.  
> 别把你的 AI agent 看到或生成的内容意外发布出去。

这是一个有可能成立的开源工具方向，但需求、留存和差异化尚未得到证实。给 secret scanner 包一层 OCR 很容易被复制。最值得验证的假设，是一个有用的发布流程：正确的 Git 检查范围、绑定到确切产物的证据、根据目标作出的决策，以及内容变化后失效的批准。

不要把 v0.1 定位为全面 DLP、隐私保证，或能识别所有保密画面的系统。

## 2. 现有证据支持什么

Glow 的 PixelLeak 调研描述了 Coding Agent 把内部审阅截图发布到相邻公开仓库的情况。这支持该失败模式确实存在，包括私有代码仓库旁边的公开产物仓库。这是供应商报告的调查，不是对市场规模、用户安装意愿或本产品效果的独立证明。[一手调研](https://www.glow.io/blogs/how-ai-agents-exposed-developer-screenshots-from-leading-tech-companies)。

我们的推断是：首批用户应当是发布视觉调试证据的人，而不是所有 AI 编辑器用户。仓库本地 hook 只能在已安装它的公开目标仓库中发挥作用；它不会自动保护 agent 新创建的相邻仓库。

**二次评审更正：** [gitshot 文档中的默认后端](https://github.com/vipulgupta2048/gitshot#how-it-works)将图片作为 GitHub Release Assets，上传到专门的公开仓库。这条路径不会调用开发者本地的 Git pre-push hook。因此，引用的事件证明了产物暴露问题，但不能证明拟议 hook 可以阻止所有或大部分报告中的事件。通过被覆盖 Git push 发生的事件占比尚未确立。

## 3. 批判性评估

| 假设或风险 | 评估 | 对产品的影响 |
| --- | --- | --- |
| 传统扫描器无法检查图片 | 表述过于宽泛；带 OCR 的扫描器和本地截图打码工具已经存在 | 通过发布流程形成差异化，而不仅是 OCR |
| 可以可靠识别 AI 生成文件 | Git 通常不记录文件由谁或什么工具生成的可靠来源 | 对选定产物进行扫描，不区分人工或 agent 生成 |
| 邮箱、私有 IP、cookie 或 QR code 能证明泄漏 | 不成立；公开联系方式、偏好 cookie、示例、localhost 和公开 QR 链接都很常见 | 区分证据、敏感性和审阅要求 |
| OCR 能识别内部后台 | OCR 提取可读文字；判断保密性需要它可能并不掌握的上下文 | v0.1 不做后台分类器，也不宣称能判断内容是否保密 |
| local-first 是护城河 | 现有工具也可本地处理 | 将本地处理视为信任要求 |
| pre-push 只需检查最终 diff | 不安全；已经删除的产物仍可能存在于待推送提交中 | 检查待推送历史中的相关产物版本 |
| hook 能对 agent 实施强制控制 | 有本地 shell 权限的 agent 可以关闭或绕过 hook | 面向愿意配合的用户防止意外发布，不宣称能强制约束对抗行为 |
| 私有目标永远安全 | 仓库可见性可以在没有后续本地推送时改变 | 说明边界；后续可见性改变需要另行审计 |
| 可见性未知意味着私有 | 错误；认证、网络错误、别名和不支持的服务商都会产生未知状态 | UNKNOWN 使用公开策略，明确显示不确定性 |
| 生成产物是所有用户普遍、频繁的大问题 | 未证实；很多产物根本不进入 Git | 招募确实有产物发布流程的用户 |
| 有冲击力的 demo 能证明准确率 | 少量预设示例无法证明正常资源上的表现和 OCR 漏检情况 | 评估正常样本、漏检、延迟和重复使用 |
| 跨平台安装能在两分钟内完成 | 原生 OCR 依赖可能占据主要安装成本，尤其 Windows | 在干净机器验证安装，不宣称单文件可执行程序安装 |
| 阻止每一张变化的图片可以接受 | 未证实；对图片资源较多的项目可能过重 | 将其明确作为审阅策略，通过留存验证 |

新扫描器的主要替代方案是良好的产物管理：原始截图放在工作区之外、使用虚构数据、只发布审阅后的副本，以及文件被跟踪前通过 `.gitignore` 排除。AgentSafe 必须证明增加的帮助值得付出使用摩擦。

## 4. 竞争格局

下表能力描述依据调研日期所查阅的公开文档。它们不是实际使用评测，也不声称完整覆盖所有能力。README 没提某项功能，不代表竞品无法增加它。

| 项目或类别 | 文档中描述的重叠能力 | 对本项目的启示 |
| --- | --- | --- |
| [Prowl](https://github.com/Lercas/prowl) | 文档描述图片/纯图片 PDF 的本地 OCR，以及 Git/CLI 流程；README 标注 PolyForm Noncommercial 1.0.0 | 文档层面的能力接近，不是经实测确认的等价产品，也不是不受限制的可复用依赖 |
| [Screenshot Redactor](https://github.com/cleanroom-ai/screenshot-redactor) | 设备端截图隐私审阅与打码，包含 PII 和 QR code | 分享前准备图片的直接替代品；可作为组件或互操作参考 |
| [RedactShot](https://github.com/SpookySandwich/RedactShot) | Windows 截图流程，含本地 OCR 与 PII 审阅 | 在捕获到分享的更早环节竞争 |
| [Talisman](https://github.com/thoughtworks/talisman) | Git hook、可疑文件/内容/大小检查，以及基于 checksum 的例外 | 产物管理和绑定内容的例外不是新概念 |
| [Gitleaks](https://github.com/gitleaks/gitleaks) | Git、文件、stdin 凭证检测，以及 hook 集成 | 成熟 secret 规则的补充来源；不要复制它的规则目录 |
| [GitGuardian / ggshield](https://docs.gitguardian.com/ggshield-docs/integrations/overview) | Git 和 Coding Agent 集成中的 secret 扫描 | agent 集成本身不构成差异化；应公平比较覆盖范围和数据流 |
| [TruffleHog](https://github.com/trufflesecurity/trufflehog) | 凭证检测、可选服务商验证、多种数据源和文件格式 | secret 工作流程的补充或替代；避免无依据地评价其二进制覆盖 |
| [GitHub push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection) | 服务端阻止受支持的凭证模式 | 已存在的强保护；AgentSafe 需要增加凭证之外的产物上下文 |
| [Presidio Image Redactor](https://github.com/microsoft/presidio/tree/main/presidio-image-redactor) | 图片中 PII 的检测与打码 | 属于工具包，不是 Git 发布产品；应复用或参考，不应宣称图片 PII 检测是原创 |
| 企业 DLP 与 agent 运行时控制 | 相邻的预防预算和策略流程 | 范围与部署成本不同，不是 v0.1 客户 |
| 人工审阅、外部打码工具和 `.gitignore` | 往往无需新 hook，就能解决相同任务 | 最强的采用竞争者可能是继续现有管理方式 |

这不意味着穷尽市场，也不意味着本项目是唯一类别。调研尚未确认存在一个成熟工具，恰好组合本提案中的所有能力；这不是市场为空的证据。

功能列表只能证明已有实现，不能证明成熟度、采用规模、检测可靠性或市场饱和。把接近的产品视为等价替代品之前，应在相同流程上评估。源代码公开，也不等于许可证宽松。

### 名称冲突

暂定名已被用于一个[已归档的 agent 工具安全项目](https://github.com/brian93512/agentsafe)、一个[本地 agent 沙箱](https://github.com/Debashish-Mukherjee/agent-safe)，以及一个[带 scope 的 npm 包](https://www.npmjs.com/package/@decionis/agentsafe)。这属于品牌、搜索和分发上的冲突，不是对商标权的判定。

review 期间保留暂定名。发布前选择有辨识度的名称，核查仓库、软件包、命令名和域名是否可用。不要让用户安装未经核实的 `agentsafe` 软件包。“ArtifactGate”“CaptureGate”只是命名方向建议，尚未核查是否可用。

## 5. 首批目标用户

**主要画像：** 个人开源 Web 开发者或小项目维护者，使用具备浏览器能力的 Coding Agent 或浏览器测试工具，每周至少一次向公开 GitHub 发布截图/调试产物，并能安装本地 hook。

典型任务：

> 我需要展示 UI 修改已经生效，同时不把真实账户、内部 URL 或带认证信息的调试会话一起发布出去。

按工作流程招募，而不是按工具品牌招募。Codex、Claude Code 和 Cursor 用户在确实生成并发布这些产物时才符合画像。首版不需要工具专属集成。

**后续次要用户：** 将内部项目的脱敏证据用于公开问题复现的贡献者，以及维护公开测试样本的维护者。

**初期排除：** 只生成源码的开发者、企业安全采购者、要求集中强制策略的团队、期待视频检查的媒体密集项目，以及寻求 prompt 过滤、恶意软件防护或自主 agent 沙箱的用户。

## 6. 威胁模型（threat model）

### 受保护的数据与事件

受保护的数据包括：调试证据中的凭证、员工/客户邮箱、已配置的内部域名、带认证信息的 HTTP header，以及尚未审阅的视觉上下文。威胁事件是通过一次本地 Git push，将选定开发产物意外公开到外部。

过程：

1. 开发者或 agent 捕获或生成敏感证据。
2. 产物被提交，常见起因是范围过大的 `git add .`。
3. 本地 Git push 指向公开或未经验证的仓库。
4. 已安装的检查工具在 Git 发送推送之前，检查待推送产物版本。
5. 发现强风险线索、仍需审阅的产物或检查不完整时，停止推送。

正常流程在 `git add` 和 `git push` 之间还有 `git commit`。pre-push 发布的不是尚未提交的工作区/index 文件。

### 信任边界与假设

- 用户愿意配合工具，并在正在推送的仓库中安装了它。
- 目标依据实际 push 调用确定，不一定是 `origin` 或当前检出的分支。
- 检查读取已提交 blob，而不是信任当前工作区内容。
- 在防止意外泄漏的模型中，信任本地配置、批准记录和已安装依赖。
- 产物内容是不可信的解析输入，不能成为可执行指令。
- Git 和可见性服务提供路由元数据；不确定性必须保持可见。

### 明确不覆盖

- 恶意 agent/用户关闭 hook、使用 `--no-verify`、修改批准状态，或通过其他渠道外传数据。
- 通过 GitHub API、issue/PR 附件、release assets、Git LFS、CI 上传、云存储，或没有 hook 的其他 worktree 进行发布。LFS pointer 只会被识别为未检查内容，不意味着实际载荷已被扫描。
- 发给模型服务商的 agent prompt、浏览器/网络外传，以及 Git 之外的文件。
- 保证识别客户姓名、人脸、图表、商业机密、微小文字、非英文文字、隐藏元数据或隐写信息。
- 远程已有历史、无关 ref，或之后通过托管平台界面变为公开的私有仓库。
- 通用源码 secret 扫描、仓库级事故响应、合规认证或凭证轮换。

该工具能减少覆盖路径内的意外发布，不能证明产物安全，也不能收回已经公开的信息。

## 7. 小范围 v0.1

### 包含的能力

1. **GitHub.com 目标可见性：** 可行时匿名查询元数据；可选复用已认证的 GitHub CLI。分别显示 PUBLIC、PRIVATE、INTERNAL 和 UNKNOWN。UNKNOWN 使用公开策略。用户可以为离线操作声明按公开仓库处理；任何设置都不能静默把未知/公开改称为已验证私有。
2. **待推送 Git 范围：** 处理所有 hook ref 更新、待推送提交历史，以及发生变化的产物版本，包括后来被删除的版本；按 blob 去重扫描。首次/新 ref 推送可能需要遍历完整可达历史。历史缺失必须报错，不能给出没有问题的结果。
3. **PNG/JPEG 审阅：** 本地 OCR 提取可读文字及坐标；检测邮箱与内部域名。初稿要求每个选定的新增/修改图片版本都经过一次绑定内容的发布批准，即使没有命中规则。这个保守策略用于补偿语义盲区；其摩擦必须验证。
4. **调试文本：** 对大小受限的 UTF-8 `.log`/`.txt` 和 HAR HTTP header/cookie 进行扫描。明确产物目录中的文本型 JSON/CSV 和生成的 Markdown 也可被选中，但仅使用基础文本规则。不理解任意报告，也不做完整 HAR 载荷分析。
5. **少量确定性规则：** 邮箱、已配置内部域名、非空 Authorization/proxy-authorization 值，以及非空 Cookie/Set-Cookie 值。只有明确配置的会话 cookie 名称，才足以支持 HIGH cookie 结果；其他非空 cookie 需要审阅。排除明显空值/占位符；通用标识符检测排除保留示例域名，但明确配置的敏感域名匹配优先。不要实现各服务商凭证规则目录。
6. **未检查内容的产物清单：** 已识别的 PDF、视频、压缩包、不支持的图片和 LFS pointer 候选项，需要作为内容未检查的项目审阅。识别属于低成本清单能力，不是内容扫描。不能通过改扩展名，把受支持格式扫描失败转成可直接批准的未检查项目。
7. **仓库本地 pre-push hook：** 明确安装/移除、可重复执行、不覆盖已有 hook、push 中不出现交互式确认。
8. **CLI：** `init`、`scan`、`inspect`、`allow`、`doctor`、`uninstall`；普通终端和 JSON 输出，退出码稳定。
9. **例外：** 范围有限的 ignore pattern，以及绑定确切内容、路径、目标和策略的本地批准。不自动添加宽泛 allowlist，也不自动信任 baseline。

QR 解码后置。图片仍需视觉审阅，包括 QR 内容。如果以后加入 QR 检测，不能仅因存在 QR code 就判为 HIGH。

### 产物选择边界

结合文件签名和名称，选择所有 PNG/JPEG、已知截图/媒体/文档格式、`.log`、`.txt`、`.har` 及 LFS pointer blob。在配置的产物目录中选择 JSON、CSV、Markdown 和其他文本，例如 `screenshots/`、`captures/`、`artifacts/`、`debug/` 和 `reports/`。目录名只决定候选范围，不证明来源或敏感性。

普通源码，以及这些目录之外的一般 JSON/CSV/Markdown，不属于核心检查范围。报告范围外和忽略项数量。无法保证识别没有扩展名的未知二进制 blob。仅靠 `.gitignore` 不能豁免已经被跟踪的产物。

### 策略、置信度与覆盖情况

| 观察到的情况 | 严重性/状态 | PUBLIC 或 UNKNOWN | 已验证 PRIVATE 或 INTERNAL |
| --- | --- | --- | --- |
| 文本/HAR 中非占位符 Authorization 值，或非空且已配置的会话 cookie | HIGH，直接/配置定义的内容证据 | 阻止，直到修复或明确批准 | 警告 |
| URL/邮箱中命中已配置内部域名，提取证据较强 | HIGH，由配置确定敏感性 | 阻止，直到修复或明确批准 | 警告 |
| 没有敏感性上下文的普通邮箱 | MEDIUM，可能是个人信息 | 需要审阅 | 警告 |
| 未配置为敏感会话的非空 cookie | MEDIUM，可能包含上下文信息 | 需要审阅 | 警告 |
| 选定图片，包括没有规则命中的图片 | REVIEW，发布决策，不是泄漏检测结果 | 需要确切版本的审阅 | 提示 |
| PDF/视频/压缩包/不支持的图片/LFS pointer 候选项 | REVIEW，未检查内容 | 需要确切版本的审阅，并确认覆盖限制 | 提示 |
| 处理限制内的大型生成产物，没有其他线索 | LOW | 仅警告 | 提示 |
| 必需扫描器缺失、超时、受支持输入损坏、Git 范围未知或超过限制 | ERROR，覆盖不完整 | 退出码 2，停止 | 退出码 2，停止 |
| 选定文本已完整检查，未发现相关线索 | 没有检测结果 | 放行 | 放行 |

OCR 产生的匹配必须说明提取不确定性。低置信度的域名/header 匹配应进入 MEDIUM/审阅，而不是作为确定的 HIGH 结果。初稿已经要求所有图片审阅。任何百分比都不能被表述为经过校准的泄漏概率。

私有/内部目标采用建议性的隐私策略，但不宣称其安全。每种可见性状态下，选定的受支持产物都必须检查；只有检测结果/审阅要求在已验证私有/内部目标上改为建议性质。结构、配置和 Git 错误仍是错误。自动化成功不能隐藏检查失败。不能通过 `allow` 豁免错误；应修复环境/输入/限制，或通过可见的 ignore 规则明确改变范围。

### 不进入 v0.1 的能力

- 自动打码、图片编辑器、`agentsafe redact`，以及自动改写/amend/rebase 提交。
- 视频抽帧/音频转写、PDF OCR/文本提取、压缩包递归、LFS 获取和完整导出数据分析。
- QR 解码、人脸识别、人员/客户姓名识别、任意组织名称识别和内部后台分类。
- 云端 LLM/视觉调用、读取 agent 会话记录、生成来源归因和后台文件监控。
- 各服务商 token 规则目录与在线凭证验证；初期可选的现有扫描器仍独立运行。
- 强制 gitleaks 适配器、MCP server、Codex/Claude/Cursor 插件及 IDE 扩展。
- GitLab/Bitbucket/企业 API 适配器；非 GitHub 目标采用 UNKNOWN/公开策略，不声称已验证可见性。
- 服务端组织级强制控制、dashboard、SaaS 账户、RBAC、合规审计、SARIF 和 CI 产品。
- 在任意仓库中铺设全局 hook，以及自动保护 agent 新建仓库。

## 8. CLI 接口约定

下面是拟议接口，不是已经可用的软件。

| 命令 | 用途 |
| --- | --- |
| `agentsafe init` | 检查依赖/目标、写入最小配置；hook 位置可用时安装仓库 hook |
| `agentsafe init --assume-public` | 无需查询可见性，采用保守公开策略；标明这是一个假设 |
| `agentsafe scan --staged` | 提交前检查 index blob；只作预览，不授权任意未来推送 |
| `agentsafe scan --remote origin --ref HEAD` | 对一个本地 ref 做只读推送预演；解析目标 ref，必要时要求 `--to-ref`；实际 hook 仍是最终依据 |
| `agentsafe scan --remote origin --ref HEAD --to-ref refs/heads/main` | 明确预览指定更新；说明服务端状态可能变化 |
| `agentsafe scan --staged --format json` | 输出结构化结果，明确扫描范围与覆盖情况 |
| `agentsafe inspect F12` | 查看隐藏敏感值后的详情、已提交版本、坐标/行号与修复说明 |
| `agentsafe inspect F12 --open` | 明确地在本地生成/打开确切 Git 产物，供人工视觉审阅；说明正在打开原始内容 |
| `agentsafe allow F12 --reason "Reviewed synthetic demo"` | 批准该确切产物项中列出的检测结果和发布审阅要求；此命令中才进行交互式批准确认 |
| `agentsafe allow F12 --reason "Reviewed synthetic demo" --yes` | 明确的非交互式等效操作；用于愿意配合的自动化，不代表经验证的人工授权 |
| `agentsafe allow --list` / `agentsafe allow --revoke A7` | 查看隐藏敏感值后的批准元数据，或撤销批准 |
| `agentsafe doctor` | 在不上传产物的情况下，解释运行时/OCR/hook/配置/目标问题 |
| `agentsafe uninstall` | 只移除 AgentSafe 管理的 hook 和安装元数据；批准记录保留，直到另行清理 |

初始化必须可以重复执行。hook 目录已存在是正常情况；未被修改的 AgentSafe 自有 hook 允许再次运行。无关 hook 或共享/全局 hook 目标属于冲突，应提供手工组合方法，不覆盖、不自动串联，也不进行全局安装。文档必须说明如何让两个 hook 都收到相同参数和完整 stdin。执行前明确展示配置/hook 改动；`--yes` 是明确的自动化模式。

拟议输出示例，使用虚构数据。保留英文，便于与 CLI 原文对照：

```text
AgentSafe Privacy Gate
Destination: github.com/example/ui-demo
Visibility: PUBLIC (verified for this push)
Scope: 3 outgoing commits -> 4 artifact versions

HIGH    F12  screenshots/dashboard.png @ 8f3a2c1
        Configured internal URL; email address (OCR)
        Exact image version requires review
HIGH    F13  debug/session.har @ 8f3a2c1
        Authorization and session-cookie values present
REVIEW  F14  demo.mov @ 21ab9de
        Video content not inspected; publishing approval required
LOW     F15  artifacts/output.json @ 21ab9de
        Large generated artifact; size alone is not a leak

Coverage: 3 inspected, 1 uninspected, 0 ignored, 0 errors
Push stopped: 2 HIGH artifact items and 1 REVIEW-only item.

Next: agentsafe inspect F12 --open
Fix the outgoing commit history, or explicitly approve reviewed content.
```

示例检查三个待推送提交中的四个产物版本：截图和 HAR 为 HIGH，视频未检查而需审阅，较大的 JSON 仅为 LOW 提醒。三项已检查、一项未检查，没有忽略或错误；两项 HIGH 和一项仅需 REVIEW 的产物导致推送停止。

普通邮箱本身不能让截图被标为 HIGH。示例中的内部 URL 和会话 cookie 名称命中明确的敏感配置；Authorization 本身也足以支持 HAR 项的 HIGH 等级。默认不显示原始 token、完整 OCR 文本、解码载荷或周边保密文字。坐标、行号和检测类别足以支持终端排查。

**退出码：** 0 = 声明范围内没有尚未完成的发布检查要求；1 = 检测结果/审阅要求阻止发布；2 = 检查或安装错误。JSON 报告区分 `pass`、`pass_with_exceptions`、`blocked`、`advisory` 和 `error`，同时提供可见性和覆盖情况。退出码 0 不构成隐私安全认证。

### 例外与恢复

`allow` 使用保存在隐藏敏感值后的扫描清单中的产物项 ID。一个项目汇总同一 blob/路径/目标的全部证据和发布审阅要求；HIGH 图片项包含图片审阅，不需要再完成一个隐藏的批准。记录例外之前，命令列出被接受的所有结果/覆盖限制，并要求明确确认。记录 blob ID、路径、仓库/目标身份、已显示的规则/审阅要求、策略指纹、理由和时间。内容字节、目标、路径或相关策略变化后，批准失效。批准不覆盖其他产物项，也不覆盖新出现的要求。ID 在本地解析，推送被阻止后仍可查看；清单过期或缺失时需要重扫。

可见性 UNKNOWN 仍可能对应确定的目标身份，此时可在公开策略下使用绑定内容的批准。如果路由/别名让身份无法确定，可以提供保守预览，但检查会返回目标解析错误，直到使用可识别目标。不能以通用 UNKNOWN 身份签发可重复使用的批准。

ignore pattern 放在明确配置中，并在每次覆盖摘要中显示。不预置 `screenshots/**`、`*.png` 或 `debug/**` 之类的宽泛忽略。ignore 会移除检查覆盖，并可能在内容变化后仍有效；必须说明它与 `allow` 的区别。理由/路径本身可能敏感，因此批准状态保存在 Git 目录下，并建议填写不敏感理由。

推送停止后，修改工作区文件或在后续提交删除它，不会移除较早的敏感版本。用户必须 amend 或改写包含它的尚未推送提交，再重扫。工具解释该过程，但不自动操作历史。如果已经发生暴露，应转向事故处理，并通过现有工具轮换凭证。

## 9. 验证与决策门槛

以下是拟议验收目标，不是已测得的结果：

- 访谈 8–12 名符合主要流程的用户；至少 5 名有近期真实产物发布例子，而不只是对 AI 安全感兴趣。
- 至少 5 名用户参加一周自愿试用；至少 3 名持续启用工具，并在无人提醒时用于另一次真实推送。
- 在相同虚构样本上与现有 secret hook 和人工审阅比较。展示截图/隐私上下文的额外价值，不是给 token 告警换个名字。
- 至少 100 个虚构样本，记录正负样本划分、图片质量变化，以及正常 logo/截图/公开邮箱/本地 URL。公布每条规则的精确率、召回率和计数；不把小样本结果推广为全部数据的效果。
- 自动 HIGH 检测结果目标精确率至少 95%；清晰可读、属于声明规则的正样本，目标召回率至少 90%。单独测量不可读/不受支持情况。策略要求的 REVIEW 停止不算正确检测到泄漏，应单独报告负担。
- 在指定参考硬件上，检查 10 张新的 1080p 图片和 10 个小文本产物，目标 p95 hook 耗时少于 15 秒；无候选变化时增加耗时小于 1 秒，不计网络/Git 成本。分别报告冷启动和缓存情况。
- 在文档说明先决条件的干净 macOS/Linux 环境中，首次完成受保护虚构推送，目标少于 5 分钟。除非 Windows 通过等效测试，否则保持单独测量的实验支持等级。
- 受支持产物没有静默跳过；默认/JSON 报告不出现原始载荷；明确测试历史中已删除 blob 和 hook 冲突。

如果用户只关心源码 token，应推荐成熟扫描器。如果用户重视截图审阅，却反复关闭 hook，应转向更小的**用于可发布截图的审阅/导出命令**，并与现有打码工具结合。如果用户要求覆盖所有上传渠道和 agent 新建仓库，本地仓库 hook 不足以满足；不能暗示 MVP 能解决。

## 10. 实现前需要 review 的决定

1. 接受收窄的主要用户和 GitHub.com 可见性范围。
2. 接受对每张选定图片进行确切版本审阅，前提是试用证据支持；改变此默认策略，需要更新威胁与覆盖承诺。
3. 接受 v0.1 不包含自动打码、QR 解码、视频/PDF 检查或强制 secret 引擎适配器。
4. 接受 Python 加独立原生 OCR 依赖，并把安装体验作为发布门槛。
5. 分发前选择有辨识度的公开名称和开源许可证。默认提案为 MIT，等待依赖/许可证检查。

以上仍是初稿待讨论项，应与顶部二次评审一起阅读。

[ROADMAP.zh-CN.md](ROADMAP.zh-CN.md)规定验证阶段。[ARCHITECTURE.zh-CN.md](ARCHITECTURE.zh-CN.md)规定批准之后的实现约束。[AGENTS.zh-CN.md](AGENTS.zh-CN.md)保留仅做文档、等待 review 的工作边界。
