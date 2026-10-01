> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 有效管理成本

> 跟踪令牌使用情况，设置团队支出限制，并通过上下文管理、模型选择、扩展思考设置和预处理 hooks 来降低 Claude Code 成本。

Claude Code 按 API 令牌消耗收费。有关订阅计划定价（Pro、Max、Team、Enterprise），请参阅 [claude.com/pricing](https://claude.com/pricing)。每个开发者的成本差异很大，取决于模型选择、代码库大小和使用模式，例如运行多个实例或自动化。

在企业部署中，平均成本约为每个开发者每个活跃日 $13，每个开发者每月 $150-250，90% 的用户每个活跃日成本保持在 \$30 以下。要估计您自己团队的支出，请从一个小的试点团体开始，并使用下面的跟踪工具建立基线，然后再进行更广泛的推出。

本页面介绍如何[跟踪成本](#track-your-costs)、[管理团队成本](#manage-costs-for-your-organization)和[减少令牌使用](#reduce-token-usage)。

<h2 id="track-your-costs">
  跟踪成本
</h2>

<h3 id="using-the-/usage-command">
  使用 `/usage` 命令
</h3>

<Note>
  `/usage` 中的 Session 块显示 API 令牌使用情况，适用于 API 用户。Claude Max 和 Pro 订阅者的使用情况包含在订阅中，因此会话成本数据与计费无关。订阅者在同一屏幕上看到计划使用条、活动统计以及使用情况明细。
</Note>

`/usage` 顶部的 Session 块显示当前会话的详细令牌使用统计。Claude Code 从令牌计数本地计算美元数字，按列表价格计算，除非 [`modelPricing`](/docs/zh-CN/settings-reference#modelpricing) 表生效。管理员在您组织的托管设置中设置一个表，以便该数字使用您的合同费率，当表生效时，`Total cost` 行会带有注释 `at your organization's configured rates`。该数字是估计值，有关权威计费，请参阅 [Claude Console](https://platform.claude.com/usage) 中的使用情况页面。

```text theme={null}
Total cost:            $0.55
Total duration (API):  6m 20s
Total duration (wall): 6h 33m 10s
Total code changes:    0 lines added, 0 lines removed
Usage by model:
   claude-sonnet-4-6:  1.2k input, 5.3k output, 940.0k cache read, 50.0k cache write ($0.55)
```

这些总计在 `/clear` 启动新会话时重置，因此下一个会话的总成本从 \$0 开始。在 v2.1.211 之前，它们在 `/clear` 后继续累积，直到 Claude Code 进程的生命周期结束。

对于以 1.1× [数据驻留费率](https://platform.claude.com/docs/en/about-claude/pricing#data-residency-pricing) 计费的 Claude API 响应，Claude Code 在会话成本数字中将该响应令牌的列表价格乘以 1.1。Claude Code 在[状态行的成本字段](/docs/zh-CN/statusline#cost-and-duration-tracking)中报告相同的总计，并将其与 [`--max-budget-usd`](/docs/zh-CN/cli-reference#cli-flags) 进行比较。在 v2.1.239 之前，Claude Code 没有对这些响应应用 1.1×，因此会话成本数字低于账单。

<h4 id="prompt-cache-statistics">
  Prompt cache 统计
</h4>

在主对话的第一个 API 响应之后，Claude Code 还会向 Session 块添加一个 `Prompt cache (main)` 行，总结会话的 [prompt cache](/docs/zh-CN/prompt-caching) 使用情况：请求计数、从缓存提供的输入令牌份额、缓存未命中，以及缓存现在是否处于热状态。需要 Claude Code v2.1.251 或更高版本。

```text theme={null}
Prompt cache (main):   14 requests · 91% of input tokens from cache · 2 misses (last 6m 10s ago, 310.2k tokens re-cached) · 1 expected rebuild (compaction or tool-result clearing) · warm (1h TTL, last activity 40s ago)
```

该行中的未命中、预期重建以及热或冷部分的含义如下：

* **Misses（未命中）**：重新处理缓存已保存内容的请求，包括最后一次未命中的时间以及这些请求写回缓存的令牌数。当请求重新处理了超过 5% 且至少 2,000 个令牌的内容时，Claude Code 会将请求计为未命中，这些内容本可以从缓存中读取。[使缓存失效的操作](/docs/zh-CN/prompt-caching#actions-that-invalidate-the-cache)列出了常见原因。当 Claude Code 能够识别最后一次未命中的可能原因时，该行也会命名它，例如 `likely cause: tool definitions changed`。可能原因文本需要 Claude Code v2.1.260 或更高版本。
* **Expected rebuilds（预期重建）**：当 Claude Code 本身刚刚重写对话时，通过[压缩](/docs/zh-CN/prompt-caching#compacting-the-conversation)或从上下文中清除旧工具结果，它会将相同类型的未命中计为预期重建。此部分仅在至少发生过一次预期重建后出现。
* **Warm or cold（热或冷）**：缓存的前缀是否仍在其[缓存生命周期](/docs/zh-CN/prompt-caching#cache-lifetime)内，以及生效的 TTL。当缓存冷时，该行显示会话已空闲多长时间。当没有响应报告缓存令牌时，该行以 `no prompt caching reported by the API` 结尾。

计数来自 API 响应中的缓存令牌字段，因此该行适用于每个提供商和网关。它仅覆盖主对话，不包括子代理。`/clear` 与 Session 块的其余部分一起重置它。

状态行脚本可以从 [`prompt_cache` 对象](/docs/zh-CN/statusline#prompt-cache-fields)读取相同的数字。

<h4 id="plan-usage-breakdown">
  计划使用情况明细
</h4>

在 Pro、Max、Team 或 Enterprise 计划上，`/usage` 还显示计入您的计划限制的内容明细：

* **Attribution（归属）**：最近使用情况归属于 skills、subagents、plugins 和各个 MCP 服务器，每个都显示为总数的百分比。MCP 服务器的份额仅计算消耗其工具结果之一的请求。在 v2.1.222 之前，在调用 MCP 服务器一次后，Claude Code 将每个后续请求归属于该服务器，高估了其份额。
* **Behavior flags（行为标志）**：行为，例如长上下文或缓存未命中，当其占最近使用情况的 10% 或更多时标记。
* **Loops（循环）**：最近运行的每个最重的 [`/loop` 或其他计划任务](/docs/zh-CN/scheduled-tasks) 的行，按总令牌排序，其余的计数。Claude Code 报告每个任务触发的频率、运行次数、其总令牌和每次运行令牌，以及最后一次运行的时间。Claude Code 通过任务的提示键入行，因此您停止并重新创建的循环保持为一行。需要 Claude Code v2.1.242 或更高版本。

按 `d` 或 `w` 在过去 24 小时和过去 7 天之间切换。这些数据是近似值，从此机器上的本地会话历史记录计算，因此不包括来自其他设备或 claude.ai 的使用情况。

在 [VS Code 扩展](/docs/zh-CN/vs-code#check-account-and-usage)中，归属份额和行为标志显示在"账户和使用情况"对话框中，带有"日"和"周"切换，不包括"循环"行。

<h4 id="check-your-usage-credits-spend">
  检查您的使用额度支出
</h4>

`/usage` 还在[使用额度](#add-usage-credits-to-your-subscription)开启时显示使用额度行。该行显示的内容取决于您的计划：

* **Pro 和 Max**：当前月份的支出，与您设置的每月支出限制进行比较（如果您设置了一个）。当您未设置限制时，该行显示 `Unlimited`，没有支出数字。
* **Team 和 Enterprise**：当前月份的您自己的支出，与您的组织设置的任何[限制](#claude-for-teams-and-enterprise)进行比较，该限制适用于您。覆盖整个组织的限制不会出现在该行中。当您没有自己的限制时，该行显示您的支出，旁边没有限制。当使用额度对您关闭时，`/usage` 不显示使用额度行。

当您有支出限制时，该行在使用额度开启后立即出现，并显示 0%，直到您首次支出使用额度。在 v2.1.236 之前，`/usage` 仅在 Pro 和 Max 计划上显示该行，带有支出限制的行在您支出某些内容之前保持隐藏。

<h4 id="when-the-usage-request-fails">
  当使用情况请求失败时
</h4>

当您的计划限制请求失败时（通常是因为使用情况端点受到速率限制），`/usage` 会显示它在过去 60 分钟内在此机器上加载的最后一个使用情况条，以及一个 `Showing last-known usage` 注释，说明该数据是多久前获取的。按 `r` 重试；成功重试会用新数据替换最后已知的条。如果没有过去 60 分钟内的快照，`/usage` 会报告使用情况端点受到速率限制，并提供相同的重试快捷方式。在 v2.1.208 之前，在尚未加载使用情况的会话中受速率限制的请求始终显示错误，没有条。

<h3 id="analyze-your-usage-patterns">
  分析您的使用情况模式
</h3>

运行 [`/insights`](/docs/zh-CN/commands#all-commands) 以获取关于您如何工作而不是您使用了多少令牌的报告。它分析此机器上的最近会话，并编写一份 HTML 报告，涵盖您处理的内容、摩擦点（例如误解的请求或有缺陷的代码）以及有关更有效地使用 Claude Code 的建议。单次运行分析最多 200 个它之前未见过的会话，并跳过非常短的会话。当会话被遗漏时，报告标题显示分析的计数，括号中显示总数，例如 `200 sessions (412 total)`。

当[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)对会话可用且您最近的会话大多在没有它的情况下运行时，报告还可以包括自动模式在这些会话中可以处理多少权限提示的估计。

Claude Code 将最新报告写入 `~/.claude/usage-data/report.html`，并在同一目录中保存每次运行的时间戳副本，因此早期报告不会被覆盖。Claude Code 按与其余会话数据相同的计划删除报告：在启动时，它删除早于 [`cleanupPeriodDays`](/docs/zh-CN/claude-directory#cleaned-up-automatically) 的文件，默认为 30 天。

您可以在任何计划和任何提供商上运行 `/insights`。分析通过与您的常规会话相同的提供商和账户运行，令牌计入您的计划或 API 使用情况。不包括来自其他设备和 claude.ai 的会话。

<h3 id="add-usage-credits-to-your-subscription">
  向您的订阅添加使用额度
</h3>

[使用额度](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)让您可以在计划的使用限制之外继续工作。要管理它们，请在通过 `/login` 使用您的 claude.ai 订阅登录后运行 `/usage-credits`；该命令不适用于 API 密钥身份验证。在自助服务 Enterprise 组织、Enterprise 试用版和通过 AWS Marketplace 计费的 Enterprise 组织中，该命令需要 Claude Code v2.1.248 或更高版本；早期版本会以 [`Unknown command: /usage-credits`](/docs/zh-CN/errors#unknown-command) 拒绝它。它打开的内容取决于您的角色：

| 您的角色 | `/usage-credits` 的作用 |
| :- | :- |
| Pro 或 Max 订阅者 | 在浏览器中打开 claude.ai 上的 [**Settings > Usage**](https://claude.ai/settings/usage)。在其 **Usage credits** 部分中，您可以打开或关闭使用额度，并检查您的额度余额、本月支出和每月支出限制 |
| 具有计费访问权限的 Team 或 Enterprise 成员 | 在浏览器中打开您的组织的使用情况设置 [**Admin settings > Usage**](https://claude.ai/admin-settings/usage) |
| 没有计费访问权限的 Team 或 Enterprise 成员 | 要求您确认，然后向您的组织管理员发送请求。在 v2.1.211 之前，Claude Code 在没有确认步骤的情况下发送请求 |

对于没有计费访问权限的 Team 和 Enterprise 成员，确认仅在交互式会话中出现：在使用 `-p` 标志的非交互式模式和从[远程控制](/docs/zh-CN/remote-control)中，该命令不发送请求，并告诉您在交互式会话中运行它。

如果您在早期请求等待管理员时再次运行 `/usage-credits`，Claude Code 会告诉您已经发送了请求，而不是发送重复请求。在管理员驳回您的请求后，再次运行该命令会发送新请求。在 v2.1.222 之前，被驳回的请求也会阻止新请求。

在 Pro 和 Max 计划上，当您达到支出限制且仍有使用额度可用时，Claude Code 会提示您提高或移除限制，而无需离开 CLI。如果服务器拒绝更改，请参阅[无法更新您的支出限制](/docs/zh-CN/errors#could-not-update-your-spend-limit)。

<h2 id="manage-costs-for-your-organization">
  管理组织的成本
</h2>

您对 Claude Code 的控制方式取决于您的组织如何访问 Claude Code：通过 Claude for Teams 或 Enterprise 计划、Claude Console 或云提供商。在 Teams 和 Enterprise 计划中，使用情况从每个成员的座位额度中扣除。在 Console 和云提供商上，使用情况按令牌计费到您的组织。如果您的组织混合使用登录方法，每个开发者将根据他们进行身份验证的方法进行计量。

该表将每种设置映射到您查看支出的位置、您限制支出的位置以及如何提取每用户数字。在个人 Pro 或 Max 计划中，您没有组织可管理，因此请跟踪您自己的使用额度支出，包括[快速模式](/docs/zh-CN/fast-mode#see-where-fast-mode-spend-appears)，在[向您的订阅添加使用额度](#add-usage-credits-to-your-subscription)下。

| 您的设置 | 查看支出 | 限制支出 | 每用户报告 |
| :- | :- | :- | :- |
| [Claude for Teams 或 Enterprise](#claude-for-teams-and-enterprise) | [组织分析中的支出报告](https://support.claude.com/en/articles/12883420-view-usage-analytics-for-team-and-enterprise-plans) | 管理员设置中的支出限制 | [支出报告 CSV](https://support.claude.com/en/articles/12883420-view-usage-analytics-for-team-and-enterprise-plans)；Enterprise 上的 [Enterprise Analytics API](https://platform.claude.com/docs/en/api/admin/analytics) |
| [Claude Console (API)](#claude-console) | [Console 使用情况页面](https://platform.claude.com/usage) | 工作区支出限制 | [Console 仪表板](https://platform.claude.com/claude-code)、[Claude Code Analytics API](https://platform.claude.com/docs/en/build-with-claude/claude-code-analytics-api) |
| [Amazon Bedrock、Google Cloud 的 Agent Platform 或 Microsoft Foundry](#cloud-providers) | 您的云计费控制台 | 您的云预算控制 | [OpenTelemetry](/docs/zh-CN/monitoring-usage) 或 [LLM gateway](/docs/zh-CN/llm-gateway) |

[OpenTelemetry 导出](/docs/zh-CN/monitoring-usage)适用于每种设置，是唯一能够以近实时方式将每用户令牌和成本指标流式传输到您自己的可观测性堆栈的选项。

<h3 id="report-spend-at-your-contracted-rates">
  按您的合同费率报告支出
</h3>

默认情况下，Claude Code 按列表价格计算它向开发者显示的每个成本数字，因此如果您的组织支付合同费率，`/usage`、状态行和 OpenTelemetry 中的数字与您的账单不匹配。为了使它们匹配，请将 [`modelPricing`](/docs/zh-CN/settings-reference#modelpricing) 托管设置设置为您的费率。该设置改变 Claude Code 报告的内容，而不是 Anthropic 收费的内容。需要 Claude Code v2.1.242 或更高版本。

<Steps>
  <Step title="从您的合同中获取费率">
    输入您的合同中的每百万令牌费率。Claude Code 不会从 Claude Console 获取它们，因此在合同更改时更新设置。
  </Step>

  <Step title="编写设置">
    为列表价格设置 `multiplier` 以获得固定折扣或高于 1 以获得加价，在 `overrides` 下列出每个模型的四个每令牌费率，或两者都做。加价需要 Claude Code v2.1.271 或更高版本。[`modelPricing` 条目](/docs/zh-CN/settings-reference#modelpricing)具有形状和粘贴就用的示例。
  </Step>

  <Step title="通过托管设置部署它">
    将其作为[托管设置](/docs/zh-CN/managed-settings)交付：服务器管理的设置、MDM 策略、`managed-settings.json` 或[策略助手](/docs/zh-CN/managed-settings#compute-the-policy-with-a-helper-program)。Claude Code 忽略用户、项目和本地设置以及 `--settings` 中的密钥。
  </Step>
</Steps>

要确认费率生效，请在已[接收托管设置](/docs/zh-CN/managed-settings#read-the-source-in-%2Fstatus)的会话中运行 `/usage`：Session 块的 `Total cost` 行带有注释 `at your organization's configured rates`。这些数字仍然是估计值，而不是发票。`/model` 选择器中的每百万令牌价格保持在列表价格。

<h3 id="claude-for-teams-and-enterprise">
  Claude for Teams 和 Enterprise
</h3>

在 Claude for Teams 和 Enterprise 计划中，每个成员的 Claude Code 使用情况从按座位额度中扣除，该额度在滚动五小时窗口和每周窗口上重置。该额度与 Claude chat 和 Cowork 共享，其大小取决于成员的[座位等级](https://support.claude.com/en/articles/11845131-use-claude-code-with-your-team-or-enterprise-plan)（Standard 或 Premium）。您的控制位于 claude.ai 管理控制台中，而不是 Claude Console。

* **查看支出**：[组织分析中的支出报告](https://support.claude.com/en/articles/12883420-view-usage-analytics-for-team-and-enterprise-plans)显示每个用户和每个模型的估计支出，带有 CSV 导出，每日更新。该报告涵盖使用额度支出，并在启用使用额度后出现。座位额度内的使用情况不以美元计量。
* **查看采用情况**：[分析仪表板](https://claude.ai/analytics/claude-code)显示每日活跃用户、会话和贡献指标，带有贡献数据的 CSV 导出。请参阅[使用分析跟踪团队使用情况](/docs/zh-CN/analytics)。
* **限制支出**：座位额度是默认上限。要让成员继续超过它，请启用[使用额度](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)并在组织、组或个人成员级别设置支出限制。
* **提取每用户数字**：在 Enterprise 计划中，[Enterprise Analytics API](https://platform.claude.com/docs/en/api/admin/analytics) 返回跨 Claude 表面（包括 Claude Code）的每用户使用情况和成本报告。主所有者在 [claude.ai/analytics/api-keys](https://claude.ai/analytics/api-keys) 处使用 `read:analytics` 范围创建密钥。在 Teams 计划中，导出[支出报告 CSV](https://support.claude.com/en/articles/12883420-view-usage-analytics-for-team-and-enterprise-plans)，其中列出了每个用户和每个模型的令牌使用情况和估计支出。

[Claude Enterprise 消费指南](https://support.claude.com/en/articles/14782391-claude-enterprise-consumption-guide)是管理员的规划参考。它解释了消费如何在 Claude chat、Claude Code 和 Cowork 中有所不同，并为预算提供了每用户美元起点。为编码座位预算比聊天座位更多：每个 Claude Code 轮次都包含文件内容、工具调用和多步推理，因此一个调试会话可能会消耗超过一天的聊天。

<h3 id="claude-console">
  Claude Console
</h3>

API 组织通过[工作区](https://platform.claude.com/docs/en/build-with-claude/workspaces)管理 Claude Code 支出。您可以[设置工作区支出限制](https://platform.claude.com/docs/en/build-with-claude/workspaces#workspace-limits)以限制 Claude Code 总支出，并在 Console 中[查看成本和使用情况报告](https://platform.claude.com/docs/en/build-with-claude/workspaces#usage-and-cost-tracking)。

<Note>
  当您首次使用 Claude Console 账户对 Claude Code 进行身份验证时，会自动为您创建一个名为"Claude Code"的工作区。此工作区为您的组织中的所有 Claude Code 使用情况提供集中式成本跟踪和管理。您无法为此工作区创建 API 密钥；它专门用于 Claude Code 身份验证和使用。

  对于具有自定义速率限制的组织，此工作区中的 Claude Code 流量计入您的组织整体 API 速率限制。您可以在 Claude Console 的此工作区的 Limits 页面上设置[工作区速率限制](https://platform.claude.com/docs/en/api/rate-limits#setting-lower-limits-for-workspaces)，以限制 Claude Code 的份额并保护其他生产工作负载。
</Note>

对于每用户报告，[Console 仪表板](https://platform.claude.com/claude-code)显示每个成员的支出和接受的行数，[Claude Code Analytics API](https://platform.claude.com/docs/en/build-with-claude/claude-code-analytics-api)使用[管理员 API 密钥](https://platform.claude.com/settings/admin-keys)以编程方式返回相同的每日每用户指标。请参阅[API 客户的分析](/docs/zh-CN/analytics#access-analytics-for-api-customers)。

<h4 id="rate-limit-recommendations">
  速率限制建议
</h4>

为团队设置 Claude Code 时，请根据您的组织规模考虑这些每用户的令牌/分钟 (TPM) 和请求/分钟 (RPM) 建议：

| 团队规模 | 每用户 TPM | 每用户 RPM |
| - | - | - |
| 1-5 用户 | 200k-300k | 5-7 |
| 5-20 用户 | 100k-150k | 2.5-3.5 |
| 20-50 用户 | 50k-75k | 1.25-1.75 |
| 50-100 用户 | 25k-35k | 0.62-0.87 |
| 100-500 用户 | 15k-20k | 0.37-0.47 |
| 500+ 用户 | 10k-15k | 0.25-0.35 |

例如，如果您有 200 个用户，您可能会为每个用户请求 20k TPM，或总共 400 万 TPM (200\*20,000 = 400 万)。

随着团队规模的增长，每用户的 TPM 会减少，因为在较大的组织中，往往较少的用户同时使用 Claude Code。这些速率限制在组织级别应用，而不是按个人用户应用，这意味着当其他人未积极使用该服务时，个人用户可以暂时消耗超过其计算份额的资源。

<Note>
  如果您预期会出现异常高的并发使用情况（例如与大型团体进行的实时培训会话），您可能需要更高的每用户 TPM 分配。
</Note>

<h3 id="cloud-providers">
  云提供商
</h3>

在 Amazon Bedrock、Google Cloud 的 Agent Platform 和 Microsoft Foundry 上，Claude Code 按令牌计费到您的云账户，支出控制位于您的云提供商的计费控制台中。Claude Code 不会从您的云向 Anthropic 发送指标，因此[分析仪表板](/docs/zh-CN/analytics)和 Claude Code Analytics API 不涵盖此使用情况。

对于每用户成本归因，您有三个选项：

* **OpenTelemetry**：[导出指标](/docs/zh-CN/monitoring-usage)从每个开发者的机器到您自己的可观测性堆栈。这为您提供每用户令牌计数、成本和工具活动，无论提供商如何。
* **Claude apps gateway**：自托管的 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway)提供每用户使用情况归因、带有令牌计数的 OTLP 指标，以及这些提供商上的[每用户支出限制](/docs/zh-CN/claude-apps-gateway-spend-limits)。
* **LLM gateway**：通过代理路由所有 Claude Code 流量，该代理按密钥跟踪支出。几个大型企业报告使用[LiteLLM](/docs/zh-CN/llm-gateway)，一个开源工具，可以[按密钥跟踪支出](https://docs.litellm.ai/docs/proxy/virtual_keys#tracking-spend)。此项目与 Anthropic 无关，尚未进行安全审计。

<h3 id="when-a-developer-asks-about-a-limit">
  当开发者询问限制时
</h3>

开发者通常会向他们的管理员提出限制问题，因此了解他们遇到的上限会很有帮助。这些情况意味着不同的事情：

* **"您已达到会话限制"或"您已达到每周限制"**：订阅计划上基于座位的使用窗口，在所有模型中共享，因此开发者无法通过使用 `/model` 切换模型来恢复访问权限。该消息显示窗口何时重置。在模型特定的"您已达到 Opus 限制"或"您已达到 Sonnet 限制"消息之后，使用 `/model` 切换到该系列之外的模型确实会让开发者继续工作。请参阅[使用限制错误](/docs/zh-CN/errors#youve-hit-your-session-limit)。开发者在此期间可以做什么：
  * 运行 `/usage-credits` 以请求超过额度的使用情况，如果您已启用[使用额度](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)。
  * 在 Claude Code v2.1.234 或更高版本上，[在重置后自动等待并继续中断的任务](/docs/zh-CN/interactive-mode#wait-for-a-usage-limit-to-reset)；该部分列出了 Claude Code 何时自动启动等待以及开发者何时从 `/rate-limit-options` 中选择它。要控制您的车队 Claude Code 是否自动启动该等待，请在[托管设置](/docs/zh-CN/settings#settings-precedence)中设置 [`autoContinueAtUsageLimit`](/docs/zh-CN/settings-reference#autocontinueatusagelimit)。
* **"您已达到个人支出限制"、"组织的月度支出限制"或"团队的共享预算"**：开发者的请求将被计费到使用额度，这些额度已达到您设置的支出限制。要让开发者继续，请转到[**管理员设置 > 使用**](https://claude.ai/admin-settings/usage)并增加消息命名的限制。当消息还命名计划重置时间时，开发者可以改为等待直到那时。请参阅[错误参考](/docs/zh-CN/errors#youve-hit-your-monthly-spend-limit)了解每个变体。
* **来自 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 的支出限制消息**：开发者超过了您在自托管网关上设置的支出上限，网关会阻止他们的请求，直到该期间重置或您提高上限。请参阅[网关支出限制](/docs/zh-CN/claude-apps-gateway-spend-limits)以了解上限、重置计划和开发者看到的消息。
* **上下文或自动压缩警告**：不是使用限制。对话已接近会话的[自动压缩窗口](/docs/zh-CN/model-config#set-the-auto-compact-window)，这是 Claude Code 总结较早历史以释放空间的阈值。将开发者指向[减少令牌使用](#reduce-token-usage)。
* **API 或云提供商计划上的意外高支出**：通常可以追溯到从未清除的长会话或将 Opus 作为默认模型。要分享的最高影响习惯是在不相关的任务之间清除和将模型与工作相匹配，两者都在[减少令牌使用](#reduce-token-usage)中涵盖。

<h3 id="agent-team-token-costs">
  Agent 团队令牌成本
</h3>

[Agent 团队](/docs/zh-CN/agent-teams)生成多个 Claude Code 实例，每个实例都有自己的上下文窗口。令牌使用情况随活跃队友的数量和每个队友运行的时间长度而扩展。

为了保持 agent 团队成本可控：

* 为队友使用 Sonnet。它为协调任务平衡了能力和成本。
* 保持团队规模小。每个队友运行自己的上下文窗口，因此令牌使用大致与团队规模成正比。
* 保持生成提示的重点。队友会自动加载 CLAUDE.md、MCP servers 和 skills，但生成提示中的所有内容都会从一开始就添加到其上下文中。
* 工作完成后关闭队友。每个活跃的队友会继续消耗令牌，直到它退出或会话结束。
* Agent 团队默认被禁用。在您的[settings.json](/docs/zh-CN/settings)或环境中设置 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 以启用它们。请参阅[启用 agent 团队](/docs/zh-CN/agent-teams#enable-agent-teams)。

<h2 id="reduce-token-usage">
  减少令牌使用
</h2>

令牌成本随上下文大小而扩展：Claude 处理的上下文越多，您使用的令牌就越多。Claude Code 通过 [prompt caching](/docs/zh-CN/prompt-caching)（减少重复内容（如系统提示）的成本）和 auto-compact（在接近上下文限制时总结对话历史）自动优化成本。

以下策略可帮助您保持上下文较小并降低每条消息的成本。

<h3 id="manage-context-proactively">
  主动管理上下文
</h3>

使用 `/usage` 检查您当前的令牌使用情况，或[配置您的状态行](/docs/zh-CN/statusline#context-window-usage)以连续显示它。

* **在任务之间清除**：使用 `/clear` 在切换到不相关的工作时重新开始。陈旧的上下文会在随后的每条消息上浪费令牌。在清除之前使用 `/rename` 以便您稍后可以轻松找到会话，然后使用 `/resume` 返回到它。
* **添加自定义 compaction 指令**：`/compact Focus on code samples and API usage` 告诉 Claude 在总结期间保留什么。在新会话中，`/compact` 打印 `Not enough messages to compact.`，因为还没有对话历史可以总结。

您还可以在项目根目录的 CLAUDE.md 文件中自定义 compaction 行为：

```markdown theme={null}
# Compact instructions

When you are using compact, please focus on test output and code changes
```

<h3 id="choose-the-right-model">
  选择正确的模型
</h3>

Sonnet 处理大多数编码任务效果很好，成本低于 Opus。为复杂的架构决策或多步推理保留 Opus。使用 `/model` 在会话中途切换模型，或在 `/config` 中设置默认值。对 Opus 的切换也适用于[继承您会话模型的 subagents](/docs/zh-CN/model-config#setting-your-model)。对于简单的 subagent 任务，在您的 [subagent 配置](/docs/zh-CN/sub-agents#choose-a-model)中指定 `model: haiku`。

<h3 id="reduce-mcp-server-overhead">
  减少 MCP server 开销
</h3>

MCP 工具定义[默认被延迟](/docs/zh-CN/mcp#scale-with-mcp-tool-search)，因此只有工具名称和服务器指令进入上下文，直到 Claude 使用特定工具。运行 `/context` 查看占用空间的内容。

* **在可用时优先使用 CLI 工具**：`gh`、`aws`、`gcloud` 和 `sentry-cli` 等工具比 MCP servers 更节省上下文，因为它们不添加任何每工具列表。Claude 可以直接运行 CLI 命令。
* **禁用未使用的 servers**：运行 `/mcp` 查看配置的 servers 并禁用您未积极使用的任何 servers。

<h3 id="install-code-intelligence-plugins-for-typed-languages">
  为类型化语言安装代码智能插件
</h3>

[代码智能插件](/docs/zh-CN/plugins/code-intelligence)为 Claude 提供精确的符号导航，而不是基于文本的搜索，减少在探索不熟悉的代码时不必要的文件读取。单个"转到定义"调用替代了可能需要的 grep 后跟读取多个候选文件。已安装的语言服务器还会在编辑后自动报告类型错误，因此 Claude 无需运行编译器即可捕获错误。

<h3 id="offload-processing-to-hooks-and-skills">
  将处理卸载到 hooks 和 skills
</h3>

自定义 [hooks](/docs/zh-CN/hooks)可以在 Claude 看到数据之前对其进行预处理。Claude 不是读取 10,000 行日志文件来查找错误，hook 可以 grep `ERROR` 并仅返回匹配的行，将上下文从数万个令牌减少到数百个。

[skill](/docs/zh-CN/skills)可以为 Claude 提供领域知识，这样它就不必进行探索。例如，"codebase-overview" skill 可以描述您的项目架构、关键目录和命名约定。当 Claude 调用该 skill 时，它会立即获得此上下文，而不是花费令牌读取多个文件来理解结构。

例如，此 PreToolUse hook 过滤测试输出以仅显示失败：

<Tabs>
  <Tab title="settings.json">
    将此添加到您的 [settings.json](/docs/zh-CN/settings#where-settings-live)以在每个 Bash 命令之前运行 hook：

    ```json theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "~/.claude/hooks/filter-test-output.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="filter-test-output.sh">
    hook 调用此脚本。使用 `mkdir -p ~/.claude/hooks` 创建文件夹，将下面的脚本保存为 `~/.claude/hooks/filter-test-output.sh`，并使用 `chmod +x ~/.claude/hooks/filter-test-output.sh` 使其可执行。它检查命令是否为测试运行器并修改它以仅显示失败：

    ```bash theme={null}
    #!/bin/bash
    input=$(cat)
    cmd=$(echo "$input" | jq -r '.tool_input.command')

    # If running tests, filter to show only failures
    if [[ "$cmd" =~ ^(npm test|pytest|go test) ]]; then
      filtered_cmd="$cmd 2>&1 | grep -A 5 -E '(FAIL|ERROR|error:)' | head -100"
      echo "$input" | jq --arg filtered "$filtered_cmd" \
        '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "allow", updatedInput: (.tool_input + {command: $filtered})}}'
    else
      echo "{}"
    fi
    ```
  </Tab>
</Tabs>

要验证设置，运行 `/hooks` 并检查 hook 是否出现在 PreToolUse 下。您也可以使用 `claude --debug-file ./claude-debug.txt` 启动 Claude Code 并要求 Claude 运行 `npm test`。当 hook 重写命令时，该日志文件包含一个 `modified tool input keys` 行，列出 `command` 和其他 Bash 输入字段。

<h3 id="move-instructions-from-claude-md-to-skills">
  将指令从 CLAUDE.md 移动到 skills
</h3>

您的 [CLAUDE.md](/docs/zh-CN/memory)文件在会话开始时加载到上下文中。如果它包含特定工作流的详细指令（如 PR 审查或数据库迁移），即使您在做不相关的工作时，这些令牌也会存在。[Skills](/docs/zh-CN/skills)仅在调用时按需加载，因此将专门指令移动到 skills 中可以保持您的基础上下文较小。目标是通过仅包含必要内容来将 CLAUDE.md 保持在 200 行以下。

<h3 id="adjust-extended-thinking">
  调整扩展思考
</h3>

扩展思考默认启用，因为它显著改进了复杂规划和推理任务的性能。思考令牌作为输出令牌计费，默认预算可能是每个请求数万个令牌，具体取决于模型。

对于不需要深度推理的更简单任务，您可以通过在 `/effort` 中或在 `/model` 中降低 [effort level](/docs/zh-CN/model-config#adjust-effort-level)、或在 `/config` 中禁用思考来降低成本。您无法在 Opus 5.5、Sonnet 5.5 或 Fable 模型上关闭思考，它们始终使用扩展思考。

在具有[固定思考预算](/docs/zh-CN/model-config#adaptive-reasoning-and-fixed-thinking-budgets)的模型上，您也可以通过设置 `MAX_THINKING_TOKENS` [环境变量](/docs/zh-CN/env-vars)（例如 `MAX_THINKING_TOKENS=8000`）来降低预算。自适应推理模型忽略非零预算，因此请改用 effort levels。

<h3 id="delegate-verbose-operations-to-subagents">
  将冗长的操作委托给 subagents
</h3>

运行测试、获取文档或处理日志文件可能会消耗大量上下文。将这些委托给 [subagents](/docs/zh-CN/sub-agents#isolate-high-volume-operations)，以便冗长的输出保留在 subagent 的上下文中，而只有摘要返回到您的主对话。

subagent 自己的请求仍然会消耗您的使用量。为了在这些请求上花费更少，[为 subagent 选择更小的模型](/docs/zh-CN/sub-agents#choose-a-model)或[在一个模型上运行每个 subagent](/docs/zh-CN/sub-agents#run-every-subagent-on-one-model)。

<h3 id="manage-agent-team-costs">
  管理 agent 团队成本
</h3>

当队友在 plan mode 中运行时，Agent 团队使用的令牌大约是标准会话的 7 倍，因为每个队友维护自己的上下文窗口并作为单独的 Claude 实例运行。保持团队任务小且独立，以限制每个队友的令牌使用。有关详细信息，请参阅 [agent 团队](/docs/zh-CN/agent-teams)。

<h3 id="write-specific-prompts">
  编写具体的提示
</h3>

模糊的请求（如"改进此代码库"）会触发广泛扫描。具体的请求（如"向 auth.ts 中的登录函数添加输入验证"）让 Claude 能够以最少的文件读取高效地工作。

<h3 id="work-efficiently-on-complex-tasks">
  高效处理复杂任务
</h3>

对于较长或更复杂的工作，这些习惯有助于避免因走错路而浪费的令牌：

* **对复杂任务使用 plan mode**：按 Shift+Tab 进入 [plan mode](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode)，然后再进行实现。Claude 探索代码库并提出一个方法供您批准，防止当初始方向错误时的昂贵返工。
* **尽早纠正方向**：如果 Claude 开始朝错误的方向发展，按 Escape 立即停止。使用 `/rewind` 或双击 Escape 将对话和代码恢复到之前的 checkpoint。
* **给出验证目标**：在您的提示中包含测试用例、粘贴屏幕截图或定义预期输出。当 Claude 可以验证自己的工作时，它会在您需要请求修复之前捕获问题。
* **增量测试**：编写一个文件，测试它，然后继续。这会在问题便宜时尽早捕获问题。

<h2 id="background-token-usage">
  后台令牌使用
</h2>

Claude Code 即使在空闲时也会为某些后台功能使用令牌：

* **对话总结**：为 `claude --resume` 功能总结以前对话的后台作业
* **命令处理**：某些命令（如 `/usage`）可能会生成请求以检查状态

这些后台进程即使没有活跃交互也会消耗少量令牌（通常每个会话不到 \$0.04）。

启用提示建议时，Claude Code 在 Claude 响应后还会向您的会话使用的模型发送一个简短请求，以[建议您的下一个提示](/docs/zh-CN/interactive-mode#prompt-suggestions)。该请求重用对话的提示缓存，因此主要是缓存读取加上少量输出令牌。当您的账户接近或达到使用限制时，Claude Code [会跳过这些请求](/docs/zh-CN/interactive-mode#when-claude-code-skips-suggestions)。要停止这些请求，[关闭提示建议](/docs/zh-CN/interactive-mode#turn-prompt-suggestions-off)。

<h2 id="why-usage-climbs-in-a-long-session">
  为什么长时间会话中使用量会增加
</h2>

一个已经打开数小时的会话可能会使用远超你的活动量所暗示的计划限额，通常是由于以下原因之一：

* **长上下文**：Claude Code 在每个请求中发送你与它的完整对话，每当 Claude 使用工具时，它会发送另一个请求，其中包含该批工具结果。使用 [prompt caching](/docs/zh-CN/prompt-caching)，Claude Code 以 [缓存令牌速率](https://platform.claude.com/docs/en/about-claude/pricing) 重新读取该历史记录，因此即使在已打开一整天的会话中提出一行问题，仍然会为整个对话消耗使用量。请参阅 [主动管理上下文](#manage-context-proactively) 了解保持上下文较小的方法
* **缓存未命中**：在超过 [缓存生命周期](/docs/zh-CN/prompt-caching#cache-lifetime) 的中断后的第一条消息会错过缓存并重新处理你的完整上下文。在订阅上生命周期为一小时，一旦你开始使用 [使用额度](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)，生命周期会降至五分钟；在 API 密钥或云提供商上，默认为五分钟。要在使用使用额度时保持一小时的生命周期，[自己选择 TTL](/docs/zh-CN/prompt-caching#choose-the-ttl-yourself)。在 Pro 和 Max 计划上，当你在长时间中断后恢复大型会话时，Claude Code [提供从摘要恢复](/docs/zh-CN/sessions#resume-from-a-summary) 的选项，以便后续请求不会携带完整历史记录
* **计划任务**：[计划任务](/docs/zh-CN/scheduled-tasks) 按其间隔触发，即使会话处于空闲状态，每次都发送你的完整上下文
* **跨会话消息**：当此会话处于空闲状态时，Claude Code 将 [来自你另一个会话的消息](/docs/zh-CN/cross-session-messaging) 作为新轮次传递，每次都发送你的完整上下文。要保留入站消息而不是传递它们，请将 [`crossSessionInbound`](/docs/zh-CN/settings-reference#crosssessioninbound) 设置为 `hold`
* **目标检查**：当后台工作使活跃的 [目标](/docs/zh-CN/goal) 保持等待时，Claude Code [要求 Claude 检查该工作](/docs/zh-CN/goal#background-work-defers-evaluation)，即使会话处于空闲状态，启动发送你完整上下文的新轮次。Claude Code 在你的提示之间每个目标最多启动三个空闲检查。在 v2.1.246 之前，空闲检查是无限制的。要关闭检查，请将 [`CLAUDE_CODE_GOAL_CHECKIN_MINUTES`](/docs/zh-CN/env-vars) 设置为 `0`。空闲检查需要 Claude Code v2.1.236 或更高版本
* **子代理和工作流**：每个子代理，以及每个 [动态工作流](/docs/zh-CN/workflows#cost) 生成的代理，都会在主对话的基础上发送自己的请求。[属性分解](#plan-usage-breakdown) 显示子代理份额
* **代理队友**：每个活跃的 [队友](#agent-team-token-costs) 会继续消耗令牌，直到它退出
* **压缩**：`/compact` 读取它总结的对话，因此 [压缩大型上下文](/docs/zh-CN/prompt-caching#compacting-the-conversation) 本身就是一个大型请求。当你想要全新开始而不是连续性时，`/clear` 不消耗任何成本

在 Pro、Max、Team 或 Enterprise 计划上，`/usage` 分解会标记占你最近使用量 10% 或更多的行为，例如长上下文或缓存未命中，每个都附带减少它的提示。

<h2 id="understanding-changes-in-claude-code-behavior">
  了解 Claude Code 行为的变化
</h2>

Claude Code 定期接收更新，这些更新可能会改变功能的工作方式，包括成本报告。运行 `claude --version` 来检查您当前的版本。

有关您特定账户的计费问题，请通过产品内信使联系 Anthropic 支持：

* **订阅计划**（Pro、Max、Team、Enterprise）：在 [claude.ai](https://claude.ai) 登录，点击左下角的您的首字母缩写，然后选择**获取帮助**
* **Console（API）计费**：在 [platform.claude.com](https://platform.claude.com) 登录，点击您的首字母缩写，然后选择**获取帮助**

请参阅[如何获取支持](https://support.claude.com/en/articles/9015913-how-to-get-support)了解完整流程，包括每个计划中谁可以联系人工代理。
