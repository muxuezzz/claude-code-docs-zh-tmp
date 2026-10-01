> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用快速模式加快响应速度

> 通过切换快速模式在 Claude Code 中获得更快的 Opus 响应。

<Note>
  快速模式处于[研究预览](#research-preview)阶段。该功能、定价和可用性可能会根据反馈而改变。
</Note>

快速模式是 Claude Opus 的高速配置，使模型速度提高最多 2.5 倍，但每个令牌的成本更高。当您需要速度进行交互式工作（如快速迭代或实时调试）时，使用 `/fast` 将其打开，当成本比延迟更重要时，将其关闭。

快速模式不是一个不同的模型。它使用 Claude Opus，但采用不同的 API 配置，优先考虑速度而不是成本效率。您获得相同的质量和功能，只是响应速度更快。快速模式在 Opus 5.5、Opus 5 和 Opus 4.8 上受支持。它在 Sonnet、Haiku 或其他模型上不可用。

Opus 4.7 不支持快速模式，因此切换到它会关闭快速模式。Opus 4.7 的快速模式已于 2026 年 6 月 25 日弃用，并于 2026 年 7 月 24 日移除。

需要了解的内容：

* 使用 `/fast` 在 Claude Code CLI 中切换快速模式。[VS Code 扩展](/docs/zh-CN/vs-code)在选定的模型支持快速模式时提供**切换快速模式**命令。Claude Code 将该切换保存到您的 [`fastMode` 设置](#toggle-fast-mode)。
* 快速模式定价在 Opus 5.5 上为 $8/$40 MTok 输入/输出，在 Opus 5 和 Opus 4.8 上为 $10/$50 MTok 输入/输出。
* 可供订阅计划（Pro/Max/Team/Enterprise）上的 Claude Code 用户和 Claude 控制台使用。Team 和 Enterprise 组织需要所有者先启用它，Console 组织需要先配置访问权限，两者都在[要求](#requirements)下描述。
* 对于订阅计划（Pro/Max/Team/Enterprise）上的 Claude Code 用户，快速模式仅通过使用额度提供，不包含在订阅速率限制中。

<h2 id="toggle-fast-mode">
  切换快速模式
</h2>

在 CLI 中，通过以下任一方式切换快速模式：

* 运行 `/fast`，按空格键打开或关闭，然后按 Enter 键确认
* 在您的[用户设置文件](/docs/zh-CN/settings)中设置 `"fastMode": true`

默认情况下，在交互式会话中打开的快速模式在会话之间保持。您可以配置快速模式在每个会话时重置。有关详细信息，请参阅[要求每个会话选择加入](#require-per-session-opt-in)。

在[云会话](#use-fast-mode-in-cloud-sessions)之外，在[非交互式模式](/docs/zh-CN/headless)中使用 `-p` 标志，`/fast` 仅在使用快速模式在其 [`--settings`](/docs/zh-CN/cli-reference#cli-flags) 值中启动的会话中工作，例如 `claude -p --settings '{"fastMode": true}'`；切换然后仅适用于该会话，不会保存为您的默认值。`-p` 形式需要 Claude Code v2.1.205 或更高版本。在非交互式模式的其他地方，该命令报告快速模式不可用。

您可以在 Claude 工作时运行 `/fast`，Claude Code 会在不等待当前轮次结束的情况下切换快速模式。Claude Code 以其原始速度完成正在运行的轮次，因此速度变化从您的下一轮开始生效。如果您当前的模型不支持快速模式，打开它也会切换您的模型，Claude Code 会在该轮次的下一个请求中使用新模型。

为了获得最佳成本效率，在会话开始时启用快速模式，而不是在对话中途切换。有关详细信息，请参阅[了解成本权衡](#understand-the-cost-tradeoff)。

启用快速模式时：

* 如果您当前的模型不支持快速模式，Claude Code 会切换到 Opus
* 您将看到确认消息："Fast mode ON"
* 快速模式处于活动状态时，提示旁边会出现一个小的 `↯` 图标
* 随时再次运行 `/fast` 以检查快速模式是否打开或关闭

Opus 5.5 是 Claude Code v2.1.280 及更高版本中的快速模式默认值。在 v2.1.280 之前，快速模式在 v2.1.219 版本中默认为 Opus 5，在 v2.1.154 到 v2.1.218 版本中默认为 Opus 4.8，在 v2.1.142 到 v2.1.153 版本中默认为 Opus 4.7。

当您再次使用 `/fast` 禁用快速模式时，您仍然保持在 Opus 上。要切换到不同的模型，请使用 `/model`。

<h3 id="switch-models-while-fast-mode-is-on">
  在快速模式打开时切换模型
</h3>

快速模式在两个方向上都遵循您的模型切换：

* **切换离开**：当您切换到不支持快速模式的模型时，Claude Code 会关闭快速模式。这包括 Opus 4.7；在 v2.1.221 之前，快速模式在切换到 Opus 4.7 后保持打开，API 拒绝了请求。
* **切换回来**：当您保存的快速模式偏好设置为打开时，切换回支持的 Opus 模型会再次打开快速模式，这与新会话默认启动的偏好设置相同。模型切换永远不会为保存的偏好设置为关闭的会话打开快速模式，配置了[每个会话选择加入](#require-per-session-opt-in)后，切换回也不会打开它；运行 `/fast` 以重新启用它。

每当模型切换打开或关闭快速模式时，Claude Code 都会显示 `Fast mode ON` 或 `Fast mode OFF` 确认，`↯` 图标在快速模式打开时出现。无论您使用 `/model`、[`/config model=<model>`](/docs/zh-CN/settings) 切换，还是从通过[远程控制](/docs/zh-CN/remote-control)连接的设备切换，这都适用。

Claude Code 在模型切换、重新连接或失败的[可用性检查](#use-fast-mode-behind-proxies-and-llm-gateways)后，会将会话的快速模式状态重新发送到通过远程控制连接的设备。

<h3 id="use-fast-mode-in-cloud-sessions">
  在云会话中使用快速模式
</h3>

当快速模式在您的账户上可用时，快速模式在[云会话](/docs/zh-CN/claude-code-on-the-web)中工作，无论会话是在 Anthropic 管理的基础设施还是[自托管运行器](/docs/zh-CN/self-hosted-environments)上运行。需要会话环境中的 Claude Code v2.1.271 或更高版本。

在会话中输入 `/fast on` 以打开快速模式。它仅对该会话保持打开，不会保存为您的默认值。[要求](#requirements)也适用于云会话。

在浏览器中访问 [claude.ai/code](https://claude.ai/code)，您也可以从消息框上的模型菜单打开和关闭快速模式。当您的计划包含快速模式且所选模型支持它时，菜单会显示该开关。

<h2 id="understand-the-cost-tradeoff">
  了解成本权衡
</h2>

快速模式的每个令牌定价高于标准 Opus：

| 模型 | 输入 (MTok) | 输出 (MTok) |
| - | - | - |
| Opus 5.5 | \$8 | \$40 |
| Opus 5 | \$10 | \$50 |
| Opus 4.8 | \$10 | \$50 |

快速模式定价在整个 1M 令牌上下文窗口中是固定的。有关要比较的标准 Opus 费率，请参阅 [Claude 定价参考](https://platform.claude.com/docs/zh-CN/about-claude/pricing)。

在对话中首次启用快速模式时，您需要为整个对话上下文支付完整的快速模式未缓存输入令牌价格。对话进行得越深入，成本就越高，因此从一开始就启用快速模式更便宜。该成本每个对话只应用一次，因此稍后关闭快速模式再打开不会重复收费。有关机制，请参阅 [快速模式如何与提示缓存交互](/docs/zh-CN/prompt-caching#turning-on-fast-mode)。

<h3 id="see-where-fast-mode-spend-appears">
  查看快速模式支出出现的位置
</h3>

您看到快速模式支出的位置取决于您如何登录，因此首先运行 [`/status`](/docs/zh-CN/commands) 来检查。如果它显示 `Login method` 行（例如 `Claude Max account`），则您使用 Claude 订阅登录。如果它显示 `API key` 行，则您的请求计费到 Claude Console 组织。

* **Pro 和 Max**：您从使用额度中支付快速模式费用。转到 claude.ai 上的 [**Settings > Usage**](https://claude.ai/settings/usage)，其中 **Usage credits** 部分显示您本月在使用额度中花费了多少。该数字包括快速模式，但不单独列出。
* **Team 和 Enterprise**：您的组织从其使用额度中支付您的快速模式使用费用。要查看您自己的使用额度支出，运行 [`/usage`](/docs/zh-CN/costs#check-your-usage-credits-spend)。有关您的组织在哪里看到该支出，请参阅 [Claude for Teams and Enterprise](/docs/zh-CN/costs#claude-for-teams-and-enterprise)。
* **Claude Console**：您的组织使用其 API 使用的其余部分支付快速模式费用。在 Console [Usage](https://platform.claude.com/usage) 和 [Cost](https://platform.claude.com/cost) 页面上，在 **Group by** 菜单中选择 **Speed (Research Preview)** 以将快速模式与标准速度使用分开。只有当选定的日期范围包括快速模式使用时，您才会看到该选项。

<h2 id="decide-when-to-use-fast-mode">
  决定何时使用快速模式
</h2>

快速模式最适合响应延迟比成本更重要的交互式工作：

* 快速迭代代码更改
* 实时调试会话
* 时间敏感的工作，有紧迫的截止日期

标准模式更适合：

* 速度不那么重要的长期自主任务
* 批处理或 CI/CD 管道
* 成本敏感的工作负载

<h3 id="fast-mode-vs-effort-level">
  快速模式与努力级别
</h3>

快速模式和努力级别都会影响响应速度，但方式不同：

| 设置 | 效果 |
| - | - |
| **快速模式** | 相同的模型质量，更低的延迟，更高的成本 |
| **较低的努力级别** | 更少的思考时间，更快的响应，在复杂任务上可能质量较低 |

您可以结合两者：在直接任务上使用快速模式和较低的[努力级别](/docs/zh-CN/model-config#adjust-effort-level)以获得最大速度。

<h2 id="requirements">
  要求
</h2>

快速模式需要以下所有条件：

* **仅限 Anthropic API 或订阅**：快速模式可通过 Anthropic 控制台 API 和使用使用额度的 Claude 订阅计划获得。它在 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry 或 AWS 上的 Claude Platform 上不可用。控制台组织还必须[为您的组织配置快速模式访问权限](#enable-fast-mode-for-your-organization)。
* **为订阅计划启用使用额度**：在 Pro、Max、Team 或 Enterprise 计划上，您的账户必须[启用使用额度](/docs/zh-CN/costs#add-usage-credits-to-your-subscription)，这允许在您的计划包含的使用量之外进行计费。在启用之前，`/fast` 显示"Fast mode requires usage credits"。您启用它们的方式取决于您的计划：
  * 在 Pro 和 Max 上，在 claude.ai 上的[**Settings > Usage**](https://claude.ai/settings/usage)的**Usage credits**部分中启用它们，或运行 `/usage-credits` 来打开该页面。
  * 在 Team 和 Enterprise 上，具有计费访问权限的成员在[**Admin settings > Usage**](https://claude.ai/admin-settings/usage)处为组织启用它们，没有访问权限的成员运行 `/usage-credits` 向组织的管理员发送请求。

<Note>
  快速模式使用直接计入使用额度，即使您的计划上还有剩余使用量。
</Note>

* **付费控制台组织**：Claude 控制台账户不使用使用额度，您的组织按令牌为快速模式付费，与其余 API 使用量一起。在控制台的免费 Evaluation 计划上，`/fast` 显示"Fast mode unavailable during evaluation. Please purchase credits."。要清除它，在您的[控制台计费设置](https://platform.claude.com/settings/billing)中购买额度。
* **团队和企业的所有者启用**：快速模式默认对团队和企业组织禁用。所有者必须明确[启用快速模式](#enable-fast-mode-for-your-organization)，用户才能访问它。

<Note>
  四个组织设置可以阻止使用 `/fast` 启用快速模式：

  * **快速模式未启用**：如果您的组织尚未启用快速模式，使用 `/fast` 启用快速模式会显示"Fast mode has been disabled by your organization."。
  * **快速模式被托管设置关闭**：如果您的组织部署[托管设置](/docs/zh-CN/managed-settings)，设置 [`fastMode: false`](/docs/zh-CN/settings-reference#fastmode)，使用 `/fast` 启用快速模式会显示相同的"Fast mode has been disabled by your organization"消息。
  * **需要每个会话选择加入**：托管设置设置 [`fastModePerSessionOptIn: true`](#require-per-session-opt-in) 在除交互式终端会话外的任何地方都拒绝 `/fast on`，显示相同的消息。
  * **快速模式模型不允许**：如果您的组织的 [`availableModels`](/docs/zh-CN/model-config#restrict-model-selection) 允许列表排除了快速模式 Opus 模型，启用它会被拒绝，显示"is not in your organization's allowed models"。在已在支持快速模式的允许 Opus 模型上运行的会话中，`/fast` 改为在您当前的模型上启用快速模式，而不是切换模型。
</Note>

<h3 id="enable-fast-mode-for-your-organization">
  为您的组织启用快速模式
</h3>

您启用快速模式的位置取决于您的组织使用的产品：

* **控制台**（API 客户）：管理员在 [Claude Code 偏好设置](https://platform.claude.com/claude-code/preferences)中启用它。快速模式处于[研究预览](#research-preview)中，因此您的组织还必须在快速模式请求成功之前配置快速模式访问权限。要获得访问权限，请联系您的账户经理或加入等待列表，如[Claude API 上的快速模式](https://platform.claude.com/docs/en/build-with-claude/fast-mode)中所述。

  没有配置的访问权限，API 会以 429 拒绝每个快速模式请求，Claude Code 会将每个拒绝视为[快速模式速率限制](#handle-rate-limits)。与速率限制的冷却时间不同，拒绝会继续，直到配置了访问权限。
* **Claude AI**（团队和企业）：所有者在[管理员设置 > Claude Code](https://claude.ai/admin-settings/claude-code)中启用它

另一个完全禁用快速模式的选项是设置 `CLAUDE_CODE_DISABLE_FAST_MODE=1`。请参阅[环境变量](/docs/zh-CN/env-vars)。

<h3 id="use-fast-mode-behind-proxies-and-llm-gateways">
  在代理和 LLM 网关后面使用快速模式
</h3>

在提供快速模式之前，Claude Code 会通过直接请求 `api.anthropic.com` 来检查您的组织的快速模式可用性。该检查不遵循 [`ANTHROPIC_BASE_URL`](/docs/zh-CN/llm-gateway-connect#set-the-base-url-and-credential)，因此在通过 [LLM 网关](/docs/zh-CN/llm-gateway)路由 Claude 流量并阻止直接出站到 `api.anthropic.com` 的网络上，即使推理请求有效，检查也会失败。该检查确实使用配置的 [HTTP 代理](/docs/zh-CN/network-config#proxy-configuration)，因此网络块仅在 `api.anthropic.com` 即使通过代理也无法到达的地方才会导致检查失败。

当检查失败时，`/fast` 报告"Fast mode unavailable due to network connectivity issues"，请求以标准速度运行，即使您的组织已启用快速模式。过去成功的检查会从其缓存结果继续工作，因此被阻止的检查主要影响新安装。

当检查到达 `api.anthropic.com` 但呈现 Anthropic 拒绝的凭证时，同样的连接消息也会出现在开放网络上。其解析的密钥是网关颁发的凭证的会话，保存在 [`ANTHROPIC_API_KEY`](/docs/zh-CN/llm-gateway-connect#set-the-base-url-and-credential) 中或由 [`apiKeyHelper`](/docs/zh-CN/settings-reference#apikeyhelper) 生成，会使用该密钥发送检查，被拒绝的请求会被报告为连接失败。

要恢复快速模式，在网络块是原因的地方允许直接出站到 `api.anthropic.com`，或设置与检查失败方式相匹配的任何变量：

* `CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS=1` 将失败的检查视为可用，并仍然遵守"disabled by your organization"响应。当您的网络拒绝连接或 Anthropic 拒绝网关凭证时使用它；允许列表对凭证情况没有帮助，因为没有任何东西被阻止。
* `CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK=1` 完全跳过检查。当您的网络拦截请求而不是拒绝它时使用它。

两个网关配置报告"Fast mode has been disabled by your organization"而不是连接消息，即使您的组织已启用快速模式：

* 仅使用 [`ANTHROPIC_AUTH_TOKEN`](/docs/zh-CN/llm-gateway-connect#set-the-base-url-and-credential) 进行身份验证的会话会跳过检查：没有 claude.ai 登录或 Anthropic API 密钥，也没有缓存的成功检查，Claude Code 会将快速模式视为由您的组织禁用，而不发送请求。
* 拦截检查并用自己的页面回答的代理，例如返回 HTTP 200 阻止页面的 TLS 检查代理，被读取为响应说您的组织已禁用快速模式。

在这两种情况下，设置 `CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK=1` 来恢复快速模式。`CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS` 不适用于任何一种情况，因为它仅绕过失败的检查，而这两种情况都会产生禁用响应。允许列表对承载者令牌情况没有帮助，它从不发送请求。

这些变量仅影响客户端检查。当您的组织禁用了快速模式时，API 会拒绝快速模式请求，无论是否设置了这些变量。来自 API 的拒绝即使设置了跳过变量也会成立。Claude Code 会以标准速度重试被拒绝的请求，关闭快速模式，并且 `/fast` 报告您的组织已禁用快速模式。

设置 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 也会抑制可用性检查。没有之前缓存的成功检查，`/fast` 报告"Fast mode is currently unavailable"；两个跳过变量在该配置中也会恢复快速模式。

<h3 id="require-per-session-opt-in">
  要求每个会话选择加入
</h3>

默认情况下，用户在交互式会话中启用的快速模式会在会话之间保持。要更改此行为，在任何[设置文件](/docs/zh-CN/settings#where-settings-live)中将 `fastModePerSessionOptIn` 设置为 `true`，这会导致每个会话以快速模式关闭开始，并要求用户使用 `/fast` 明确启用它。[Team](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_teams#team-&-enterprise) 或 [Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_enterprise) 计划上的所有者可以通过[服务器托管设置](/docs/zh-CN/server-managed-settings)在组织范围内部署它。

```json theme={null}
{
  "fastModePerSessionOptIn": true
}
```

这对于在用户运行多个并发会话的组织中控制成本很有用。用户的快速模式偏好仍然被保存，因此删除此设置会恢复默认的持久行为。

当托管设置设置该密钥时，`/fast on` 仅在交互式终端会话中有效。在其他任何地方，包括[非交互式模式](/docs/zh-CN/headless)、[VS Code 扩展](/docs/zh-CN/vs-code)和[云会话](#use-fast-mode-in-cloud-sessions)，它会被拒绝，显示您的组织已禁用快速模式的消息。

<h2 id="handle-rate-limits">
  处理速率限制
</h2>

快速模式与标准 Opus 有单独的速率限制。所有支持的 Opus 模型共享一个快速模式速率限制池：任何模型上的使用都会从相同的限制中扣除。当您达到快速模式速率限制时：

1. 快速模式自动回退到标准速度
2. `↯` 图标变灰以指示冷却
3. 您继续以标准速度和定价工作
4. 冷却过期时，快速模式自动重新启用

要手动禁用快速模式而不是等待冷却，请再次运行 `/fast`。

如果您在会话中途用完使用额度，Claude Code 会在标准速度和定价下重试每个被拒绝的快速模式请求，因此您可以继续工作，没有冷却。您看到拒绝的方式取决于会话类型：

* 在交互式会话中，Claude Code 显示"快速模式已禁用 · 使用额度已耗尽"通知，并在会话的其余部分关闭快速模式。您保存的快速模式偏好设置不会改变；运行 `/fast` 以重新打开快速模式。
* 在[非交互式模式](/docs/zh-CN/headless)中使用 `--output-format stream-json`，以及通过 Agent SDK，Claude Code 在消息流上作为 `system` 消息发出相同的文本，子类型为 `notification`，在您用完使用额度时每轮一次。快速模式保持打开。需要 Claude Code v2.1.221 或更高版本。

<h2 id="research-preview">
  研究预览
</h2>

快速模式是一个研究预览功能。这意味着：

* 该功能可能会根据反馈而改变
* 可用性和定价可能会改变
* 底层 API 配置可能会演变

通过您通常的 Anthropic 支持渠道报告问题或反馈。

<h2 id="see-also">
  另请参阅
</h2>

* [模型配置](/docs/zh-CN/model-config)：切换模型并调整努力级别
* [有效管理成本](/docs/zh-CN/costs)：跟踪令牌使用情况并降低成本
* [状态行配置](/docs/zh-CN/statusline)：显示模型和上下文信息
