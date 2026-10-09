> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 选择权限模式

> 控制 Claude 在采取行动前是否需要征求您的同意。在 CLI 中使用 Shift+Tab 切换权限模式，在 VS Code 中使用模式指示器，或在 Desktop 中使用模式选择器。

权限模式设置 Claude 在会话中可以在不先询问您的情况下执行哪些操作。在 Manual 模式下，Claude Code 会在大多数编辑文件、运行 shell 命令或访问网络的操作前停止并询问您。在[自动模式](#eliminate-prompts-with-auto-mode)中，第二个模型（分类器）会审查操作而不是您；[分类器如何评估操作](#how-the-classifier-evaluates-actions)列出了它审查的操作以及哪些跳过它。

在 Claude Code v2.1.283 或更高版本中，自动模式是交互式终端和 VS Code 会话的内置起始权限模式。在早期版本中，它仅在 Pro、Max 和 Team 计划上是内置的起始权限模式。[会话在哪个模式下启动](#which-mode-a-session-starts-in)涵盖了改变起始权限模式的表面和设置。您也可以随时更改正在运行的会话的权限模式。

<h2 id="available-modes">
  可用的模式
</h2>

每种模式在便利性和监督之间做出不同的权衡。下表显示了在每种模式下 Claude 无需权限提示即可执行的操作。手动模式显示在其配置值 `default` 下。

| 模式 | 无需询问即可运行的内容 | 最适合 |
| :- | :- | :- |
| `default` | 仅读取 | 自己审查每项操作，敏感工作 |
| [`acceptEdits`](#auto-approve-file-edits-with-acceptedits-mode) | 读取、文件编辑和常见文件系统命令（`mkdir`、`touch`、`mv`、`cp` 等） | 迭代您正在审查的代码 |
| [`plan`](#analyze-before-you-edit-with-plan-mode) | 读取，加上当 [auto 模式](#eliminate-prompts-with-auto-mode) 可用时分类器批准的命令 | 在更改代码库之前探索它 |
| [`auto`](#eliminate-prompts-with-auto-mode) | 一切，带有后台安全检查 | 长任务，减少提示疲劳 |
| [`dontAsk`](#allow-only-pre-approved-tools-with-dontask-mode) | 读取和预批准的工具；任何会提示的内容都被拒绝 | 锁定的 CI 和脚本 |
| [`bypassPermissions`](#skip-all-checks-with-bypasspermissions-mode) | 一切 | 仅限隔离容器和虚拟机 |

审查每项操作的模式在 CLI 中名为 **Manual**，在 `claude --help` 中、在 VS Code 和 JetBrains 扩展中以及在桌面应用中也是如此。其配置值是 `default`，这是 hook 和 SDK 集成使用的。CLI 在您输入值的任何地方接受 `manual` 作为别名，例如 `claude --permission-mode manual` 或 `"defaultMode": "manual"`。

对 [受保护路径](#protected-paths) 的写入永远不会自动批准，除非在 `bypassPermissions` 模式下以及在 plan 模式会话中，其中绕过权限可用，意味着会话以 [将 `bypassPermissions` 放入模式循环](#switch-permission-modes) 的方式启动。

模式设置基线。在顶部分层 [权限规则](/docs/zh-CN/permissions#manage-permissions) 以预批准或阻止特定工具。拒绝规则在每种模式下都会阻止，包括 `bypassPermissions`。拒绝和询问规则不适用于 [`EndConversation`](/docs/zh-CN/tools-reference#endconversation-tool-behavior)，只要 Claude 仍然至少有一个其他工具可以调用。允许规则在 `bypassPermissions` 中无效。

<h3 id="actions-no-mode-auto-approves">
  任何模式都不会自动批准的操作
</h3>

Claude Code 在任何模式下都不会自动批准以下内容，包括 `bypassPermissions`。每个项目符号链接到说明在每种模式下会发生什么的部分：

* 与显式 [询问规则](/docs/zh-CN/permissions#manage-permissions) 匹配的工具
* 您的组织 [设置为 `ask`](/docs/zh-CN/mcp#organization-controls-on-connector-tools) 的连接器工具，在该设置到达 Claude Code 的会话中
* 需要用户交互的工具：内置 `AskUserQuestion` 工具和标记为 [`requiresUserInteraction`](/docs/zh-CN/mcp#require-approval-for-a-specific-tool) 的 MCP 工具
* `rm` 和 `rmdir` 移除针对 [关键路径](#critical-paths)，没有允许规则或 `PreToolUse` hook `"allow"` 批准
* [跨会话消息传递保护措施](#skip-all-checks-with-bypasspermissions-mode)
* 在 [`permissions.blockReadsOutsideWorkingDirectories`](/docs/zh-CN/settings-reference#permissions-blockreadsoutsideworkingdirectories) 打开时在工作目录外读取：识别的文件读取 Bash 命令和任何需要批准才能在沙箱外运行的 [未沙箱化重试](/docs/zh-CN/sandboxing#the-unsandboxed-retry-escape-hatch)，即使在 auto 模式和 `bypassPermissions` 模式下也会提示。需要 Claude Code v2.1.257 或更高版本。

  shell 解析器无法追踪的命令，例如更改目录多次或运行子 shell 的命令，即使在未命名任何外部路径时也会以相同方式提示。当命令在 [沙箱](/docs/zh-CN/sandboxing) 中运行且沙箱强制执行该块时，此提示不适用。

<h2 id="common-setups">
  常见设置
</h2>

权限模式决定 Claude 是否在操作前询问，[Bash 沙箱](/docs/zh-CN/sandboxing)和外部[隔离边界](/docs/zh-CN/sandbox-environments)决定操作运行后可以到达什么。下表将目标与获得该目标的标志或设置以及所需的隔离配对，作为起点。[可用模式](#available-modes)列出了在每种模式下无需提示即可运行的内容。

| 您想要 | 从以下开始 | 需要的隔离 | 注意 |
| :- | :- | :- | :- |
| 自己审查每个操作 | Manual 模式：`claude --permission-mode default` | 无 | 敏感工作、不熟悉的代码 |
| 在本地迭代，更少提示，无分类器 | Manual 模式加上 Bash 沙箱在[自动允许模式](/docs/zh-CN/sandboxing#sandbox-modes)：`claude --permission-mode default`，然后运行 `/sandbox` 并选择自动允许 | 内置 Bash 沙箱，在 macOS、Linux 和 WSL2 上 | 拒绝规则仍然适用，询问规则命名命令（如 `Bash(git push *)`）仍然会提示。要从设置文件启用沙箱，请改为将 [`sandbox.enabled`](/docs/zh-CN/settings-reference#sandbox-enabled) 设置为 `true` |
| 在更改任何内容前探索 | `claude --permission-mode plan` | 无 | Claude Code 阻止编辑，直到您[批准计划](#review-and-approve-a-plan) |
| 在自动模式下无需干预工作 | `claude --permission-mode auto`，v2.1.283 或更高版本的[内置起始权限模式](#which-mode-a-session-starts-in) | 无；沙箱或容器增加深度防御 | 需要[支持的模型](#eliminate-prompts-with-auto-mode)，您的组织可以[关闭自动模式](#eliminate-prompts-with-auto-mode) |
| 在 CI 中使用精确允许列表运行 | `claude -p "run the test suite" --permission-mode dontAsk --allowedTools "Bash(npm test)" "Read"` | 无，超出您的 CI 运行器提供的 | [云会话](/docs/zh-CN/claude-code-on-the-web)忽略设置文件中的 `dontAsk` |
| 在容器内完全无人值守运行 | `claude -p "<prompt>" --dangerously-skip-permissions` | 必需：容器、虚拟机或[沙箱运行时](/docs/zh-CN/sandbox-environments#sandbox-runtime)；在 Linux 和 macOS 上，以[非 root 用户](#skip-all-checks-with-bypasspermissions-mode)身份运行 | 云会话忽略设置文件中的此模式。在此 `-p` 运行中，[仍会提示的少数调用](#skip-all-checks-with-bypasspermissions-mode)被拒绝 |

Bash 沙箱和自动模式独立工作并结合，除了在[沙箱模式](/docs/zh-CN/sandboxing#sandbox-modes)下列出的例外。有关完整交互，请参阅[沙箱化如何与权限和权限模式相关](/docs/zh-CN/sandboxing#how-sandboxing-relates-to-permissions-and-permission-modes)和[隔离如何与权限模式相关](/docs/zh-CN/sandbox-environments#how-isolation-relates-to-permission-modes)。

<h2 id="which-mode-a-session-starts-in">
  会话在哪个模式下启动
</h2>

当您在终端中启动新会话时，Claude Code 从以下第一个适用的获取权限模式：

1. `--permission-mode` 标志或 `--dangerously-skip-permissions`

2. [设置文件](/docs/zh-CN/settings#where-settings-live)中的 `permissions.defaultMode`

   如果您在 `.claude/settings.json` 或 `.claude/settings.local.json` 中设置 `"auto"`，该值不会生效，Claude Code 然后使用内置默认值而不是来自 `~/.claude/settings.json` 的 `defaultMode`。如果您在这两个文件中设置 `"bypassPermissions"`，它也不会生效，会话以 Manual 模式启动。其他值从任何设置文件应用。

3. 内置默认值

VS Code 扩展启动的对话遵循[切换权限模式](#switch-permission-modes)中的扩展自己的列表。有关 Claude Code 在恢复会话中启动的权限模式，请参阅[恢复时的权限模式](/docs/zh-CN/sessions#permission-mode-on-resume)。

内置 `auto` 默认值在 macOS、Linux 和 WSL 上需要 Claude Code v2.1.228 或更高版本，在本机 Windows 上需要 v2.1.233 或更高版本。在较早的版本上，内置默认值是 Manual。

内置默认值取决于您如何运行 Claude Code。匹配您会话的第一行适用。该表涵盖您在终端或通过 VS Code 扩展启动的会话；对于桌面应用和 claude.ai，请参阅[切换权限模式](#switch-permission-modes)中的 Desktop 和 Web 选项卡。

| 您如何运行 Claude Code | 内置起始权限模式 |
| :- | :- |
| 任何设置文件将 `disableAutoMode` 设置为 `"disable"` | `default` |
| `claude -p` 或 [Agent SDK](/docs/zh-CN/agent-sdk/permissions#permission-modes) | 在[获取功能标志](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)的会话中为 `default`。在不获取功能标志的会话中，例如在第三方提供商上或关闭遥测的情况下，Claude Code v2.1.285 或更高版本中为 `auto`，较早版本中为 `default`。组织策略禁止 `auto` 默认值的会话改为以 `default` 启动 |
| 您的组织已应用 [HIPAA 配置](#hipaa-configuration)，且该会话[符合其适用条件](/docs/zh-CN/hipaa-setup#check-how-developers-sign-in-and-connect) | Claude Code v2.1.285 或更高版本中为 `default`；仍可切换到自动模式 |
| 在终端或通过 [VS Code 扩展](/docs/zh-CN/vs-code) | Claude Code v2.1.283 或更高版本中为 `auto`；在较早的版本上，在 Pro、Max 或 Team 计划中为 `auto`（在[获取功能标志](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)的会话中），否则为 `default` |

在您[安装或升级后的第一个会话](/docs/zh-CN/env-vars#first-session-after-an-install-or-upgrade)中，Claude Code 可以在其功能标志到达之前选择起始权限模式。该会话可能以与表格不同的权限模式启动。

当标志、设置文件或内置默认值选择 `auto` 但自动模式对会话不可用时，Claude Code 以 Manual 启动会话。自动模式在会话不满足[可用性要求](#eliminate-prompts-with-auto-mode)时不可用，例如设置文件关闭它或不支持它的模型，或当 Anthropic 已在服务器端临时关闭它时。

内置默认值第一次在自动模式下启动您的一个会话时，Claude Code 显示链接到此页面的通知：

* 在终端中，一次，在会话顶部
* 在 VS Code 扩展中，作为新对话屏幕上的卡片，保留直到您关闭它

如果您的 `~/.claude/settings.json` 将 `defaultMode` 设置为 `auto` 以外的值，且没有其他设置文件设置它，您的会话继续以该模式启动。在 Pro、Max 和 Team 计划上，以及在[不获取功能标志](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)的会话中，Claude Code 在终端或 VS Code 扩展中询问一次是否将设置更改为自动模式。如果您拒绝，您的设置保持原样。

<h3 id="start-in-a-different-mode">
  以不同的权限模式启动
</h3>

您可以为一个会话设置起始权限模式，或作为机器、项目或组织中每个会话的默认值。当多个设置文件设置 `permissions.defaultMode` 时，[设置优先级](/docs/zh-CN/settings#settings-precedence)决定，因此项目或托管值优先于 `~/.claude/settings.json`。要更改已运行会话的权限模式，请参阅[切换权限模式](#switch-permission-modes)。

| 要为以下设置起始权限模式 | 执行此操作 |
| :- | :- |
| 您即将启动的一个会话 | 将权限模式作为标志传递，例如 `claude --permission-mode default` |
| 您在此机器上启动的每个终端会话 | 在 `~/.claude/settings.json` 中设置 `permissions.defaultMode`。有关 VS Code 扩展读取的内容，请参阅[切换权限模式](#switch-permission-modes) |
| 您在一个项目中启动的每个终端会话 | 在项目的 `.claude/settings.json` 中设置 `permissions.defaultMode`。您在终端中启动的会话遵守除 `auto` 和 `bypassPermissions` 外的每个值；VS Code 扩展启动的会话不读取项目设置以获取起始权限模式 |
| 您的组织中的每个终端会话 | 在[托管设置](/docs/zh-CN/managed-settings)中设置 `permissions.defaultMode`。终端会话以该模式启动，人们仍然可以切换到自动模式；有关 VS Code 扩展读取的内容，请参阅[切换权限模式](#switch-permission-modes)。要移除自动模式以便没有人可以选择它，请改为将 `permissions.disableAutoMode` 设置为 `"disable"` |

此示例使您机器上的每个终端会话以 Manual 模式启动，其配置值为 `default`。将其保存在 `~/.claude/settings.json` 中：

```json theme={null}
{
  "permissions": {
    "defaultMode": "default"
  }
}
```

您启动的下一个会话在状态栏中显示 `⏸ manual mode on`。

<h3 id="hipaa-configuration">
  HIPAA 配置下的权限模式
</h3>

在已应用 [HIPAA 配置](/docs/zh-CN/hipaa-setup)的组织中，内置 `auto` 默认值不适用。当没有其他方式选择起始权限模式时，终端或 VS Code 会话以 Manual 模式启动。终端会话还会显示 `Auto mode isn't the default for your organization · Shift+Tab to switch`，而 VS Code 扩展不显示任何通知。[检查开发人员如何登录和连接](/docs/zh-CN/hipaa-setup#check-how-developers-sign-in-and-connect)列出了适用此规则的会话。

自动模式和 `bypassPermissions` 仍然可用：

* **切换到自动模式**：按 `Shift+Tab`，或使用[您界面中的控件](#switch-permission-modes)
* **以自动模式启动**：传递 `--permission-mode auto`，或在您的用户设置中将 `permissions.defaultMode` 设置为 `auto`，或在托管设置中为整个组织进行此设置。请参阅[以不同的权限模式启动](#start-in-a-different-mode)
* **移除自动模式**：在托管设置中将 [`permissions.disableAutoMode`](/docs/zh-CN/settings-reference#disableautomode) 设置为 `"disable"`
* **阻止 `bypassPermissions`**：在托管设置中将 [`permissions.disableBypassPermissionsMode`](/docs/zh-CN/settings-reference#permissions-disablebypasspermissionsmode) 设置为 `"disable"`

需要 Claude Code v2.1.285 或更高版本，即 [HIPAA 配置的最低版本](/docs/zh-CN/hipaa-setup#update-claude-code-and-claude-desktop)。

<h2 id="switch-permission-modes">
  切换权限模式
</h2>

每个界面都有自己的控件用于在会话期间切换权限模式，以及自己的方式来选择新会话启动的权限模式。选择您的界面以查看其控件。

<Tabs>
  <Tab title="CLI">
    **在会话期间**：按 `Shift+Tab` 循环权限模式。从 `auto` 开始，第一次按下会切换到 `default`，之后循环依次为 `default` → `acceptEdits` → `plan`。可选模式在 `plan` 之后插入。状态栏显示活动模式为灰色 `⏸ manual mode on`（对于 `default`），或为 `⏵⏵ accept edits on`、`⏸ plan mode on`、`⏵⏵ auto mode on`、`⏵⏵ don't ask on` 或 `⏵⏵ bypass permissions on`。

    请观察此片段中状态栏的变化，该会话以自动模式启动。每次按下 `Shift+Tab`，状态栏都会从 `auto mode on` 依次变为 `manual mode on`、`accept edits on`、`plan mode on`，然后回到 `auto mode on`。

    <Frame>
      <video autoPlay muted loop playsInline className="w-full dark:hidden" style={{aspectRatio: "1440 / 264"}} src="https://mintcdn.com/claude-code/oa7CKjMeIChox26S/images/permission-modes-cycle-light.mp4?fit=max&auto=format&n=oa7CKjMeIChox26S&q=85&s=198ca90aeb2e3675b3d01b7d686aab0b" aria-label="每次按下 Shift+Tab，Claude Code 输入框下方的状态栏都会变化：auto mode on、manual mode on、accept edits on、plan mode on，然后再次变为 auto mode on。" data-path="images/permission-modes-cycle-light.mp4" />

      <video autoPlay muted loop playsInline className="w-full hidden dark:block" style={{aspectRatio: "1440 / 264"}} src="https://mintcdn.com/claude-code/oa7CKjMeIChox26S/images/permission-modes-cycle-dark.mp4?fit=max&auto=format&n=oa7CKjMeIChox26S&q=85&s=994cdeec4e99d2f474d236c1087d6e63" aria-label="每次按下 Shift+Tab，Claude Code 输入框下方的状态栏都会变化：auto mode on、manual mode on、accept edits on、plan mode on，然后再次变为 auto mode on。" data-path="images/permission-modes-cycle-dark.mp4" />
    </Frame>

    并非每个模式都在默认循环中：

    * `auto`：当[自动模式可用](#eliminate-prompts-with-auto-mode)时出现；循环到它会在没有确认提示的情况下切换权限模式
    * `bypassPermissions`：在您使用 `--permission-mode bypassPermissions`、`--dangerously-skip-permissions`、`--allow-dangerously-skip-permissions` 或[用户、`--settings` 或托管设置](/docs/zh-CN/settings-reference#permissions-defaultmode)中的 `permissions.defaultMode: "bypassPermissions"` 启动后出现。`--allow-` 变体将权限模式添加到循环中而不激活它
    * `dontAsk`：永远不会在循环中出现；使用 `--permission-mode dontAsk` 设置它

    启用的可选模式在 `plan` 之后插入，`bypassPermissions` 优先，`auto` 最后。如果您同时启用了两者，您将在循环到 `auto` 的途中循环通过 `bypassPermissions`。

    **从 Bash 权限提示**：在 Manual 和 `acceptEdits` 权限模式下，当[自动模式](#eliminate-prompts-with-auto-mode)可用时，Claude Code 将**是的，并切换到自动模式**添加到 Bash 命令的权限提示。选择它以批准命令并将会话切换到自动模式。[PowerShell 工具](/docs/zh-CN/tools-reference#powershell-tool)提示不提供该选项。需要 Claude Code v2.1.247 或更高版本。

    Claude Code 不会将该选项添加到由您的[`ask` 规则](/docs/zh-CN/permissions#manage-permissions)之一或[hook](/docs/zh-CN/hooks#pretooluse-decision-control)强制的提示，因为自动模式仍然向您显示这些提示，所以切换不会移除它们。

    **在启动时**：将权限模式作为标志传递。

    ```bash theme={null}
    claude --permission-mode plan
    ```

    **作为默认值**：在您想要的范围设置 `permissions.defaultMode`，如[以不同的权限模式启动](#start-in-a-different-mode)中所述。

    相同的 `--permission-mode` 标志适用于 `-p` 用于[非交互式运行](/docs/zh-CN/headless)。
  </Tab>

  <Tab title="VS Code">
    **在会话期间**：点击提示框底部的模式指示器。它为此页面上的模式使用这些标签：

    | UI 标签 | 模式 |
    | :- | :- |
    | Manual | `default` |
    | Edit automatically | `acceptEdits` |
    | Plan | `plan` |
    | Auto | `auto` |
    | Bypass permissions | `bypassPermissions` |

    **作为默认值**：要固定对话启动的权限模式，请在您的 VS Code 用户设置中将 `claudeCode.initialPermissionMode` 设置为 `default`、`manual`、`acceptEdits`、`plan` 或 `bypassPermissions`。该设置不接受 `auto`；要以 Auto 启动，请将其保留未设置并从模式指示器中选择**Auto**一次，如下面的第 2 项所述。扩展在以下第一个适用的中启动每个新对话：

    1. `claudeCode.initialPermissionMode`
    2. 您从模式指示器最后选择的模式，如果它是 Manual、Edit automatically 或 Auto。选择 Plan 或 Bypass permissions 仅适用于该对话
    3. 来自[托管设置](/docs/zh-CN/managed-settings)或 `~/.claude/settings.json` 的 `permissions.defaultMode`
    4. 您的计划、提供商和组织设置的[内置默认值](#which-mode-a-session-starts-in)

    扩展永远不会从项目的 `.claude/settings.json` 或 `.claude/settings.local.json` 读取起始权限模式。当 `claudeCode.claudeProcessWrapper` 被设置时，第 3 和 4 项不适用：这些对话以 Manual 启动，除非第 1 或第 2 项设置权限模式。

    在 v2.1.283 之前，第 3 项仅在 Pro、Max 和 Team 计划上应用，在[获取功能标志](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)的会话中。

    当[自动模式可用](#eliminate-prompts-with-auto-mode)时，Auto 出现在模式指示器中。

    Bypass permissions 需要扩展设置中的**Allow dangerously skip permissions**切换。没有它，权限模式不会出现在指示器中，来自第 1 或第 3 项的 `bypassPermissions` 值以 Manual 启动对话。来自任何项的 Auto 同样在自动模式不可用时以 Manual 启动对话。

    有关扩展特定的详细信息，请参阅 [VS Code 指南](/docs/zh-CN/vs-code)。
  </Tab>

  <Tab title="JetBrains">
    JetBrains 插件在 IDE 终端中运行 Claude Code，因此切换权限模式的工作方式与 CLI 中相同：按 `Shift+Tab` 循环，或在启动时传递 `--permission-mode`。
  </Tab>

  <Tab title="Desktop">
    **在会话期间**：在 Code 选项卡中，使用发送按钮旁边的模式选择器。并非每个模式都出现在选择器中：

    * **Auto**：当[自动模式可用](#eliminate-prompts-with-auto-mode)时出现
    * **Bypass permissions**：在 Pro 和 Max 计划上需要 Desktop 设置中的**Allow bypass permissions mode**切换；在 Team 和 Enterprise 计划上，组织策略控制它

    Cowork 选项卡不使用这些模式。Cowork 有自己的权限模式，单独启用，Cowork 选项卡在为您的账户启用超出其默认值的模式之前不显示模式选择器。请参阅 [Cowork 文档](https://claude.com/docs/cowork/overview)。

    有关 desktop 特定的详细信息，请参阅 Desktop 指南中的[选择权限模式](/docs/zh-CN/desktop#choose-a-permission-mode)。

    **作为默认值**：在[设置](/docs/zh-CN/settings#where-settings-live)中设置 `defaultMode`。桌面应用读取与 CLI 相同的设置文件，并将权限模式应用于新的本地会话。

    您在模式选择器中选择的模式会按文件夹记住，并对该文件夹优先于 `defaultMode`。Plan 是例外：选择它仅适用于当前会话。

    有关 `defaultMode` 在设置文件中的位置，请参阅[以不同的权限模式启动](#start-in-a-different-mode)下的示例。
  </Tab>

  <Tab title="Web and mobile">
    在 [claude.ai/code](https://claude.ai/code) 上，使用输入框旁边的模式下拉菜单。在移动应用中，点击输入框中的 **+** 按钮，然后点击 **Permission**。云端会话和 Remote Control 会话提供不同的权限模式：

    * **[Cloud sessions](/docs/zh-CN/claude-code-on-the-web)**：Accept edits、Plan 和 Auto。Accept edits 对应于 `default` 模式：云会话预先批准文件编辑，无论模式如何，因此下拉菜单显示 Accept edits 而不是 Manual。云会话仍然遵守设置中的 `defaultMode: "acceptEdits"`。Auto 模式仅在您的组织允许且所选模型支持时出现。Bypass permissions 不可用。
    * **[Remote Control](/docs/zh-CN/remote-control) sessions** 在您的本地机器上：Manual、Accept edits、Plan 和 Auto（对于您自己启动的会话），您无法从应用中选择 Bypass permissions。要使用 Auto，会话必须满足自动模式的[可用性要求](#eliminate-prompts-with-auto-mode)。对于在您的计算机上运行的项目线程，请参阅[在您自己的计算机上运行线程](/docs/zh-CN/claude-projects#run-a-thread-on-your-own-computer)。
      * 除了 Bypass permissions，下拉菜单显示本地会话所在的权限模式，包括从终端设置的模式。它在应用或终端中权限模式更改时更新。
      * 由[桌面应用](/docs/zh-CN/desktop)或 [VS Code 扩展](/docs/zh-CN/vs-code)托管的会话在权限模式更改时向 claude.ai 报告，与在终端中托管的会话相同。
      * 在 v2.1.202 之前，使用 `/remote-control` 或 `claude --remote-control` 连接的会话根本不报告其权限模式，因此 claude.ai 和移动应用可能显示会话不在的权限模式。不匹配仅影响标签。Claude Code 从会话的实际权限模式生成权限提示，它们仍然出现在应用中以供批准。

    对于 Remote Control，运行会话的本地机器必须使用您的 claude.ai 账户登录；不支持 API 密钥。您也可以在启动该本地会话时设置起始权限模式：

    ```bash theme={null}
    claude remote-control --permission-mode acceptEdits
    ```
  </Tab>
</Tabs>

<h2 id="auto-approve-file-edits-with-acceptedits-mode">
  使用 acceptEdits 模式自动批准文件编辑
</h2>

`acceptEdits` 模式让 Claude 在您的工作目录中创建和编辑文件而无需提示。当此模式处于活动状态时，状态栏显示 `⏵⏵ accept edits on`。

除了文件编辑外，`acceptEdits` 模式还自动批准常见的文件系统 Bash 命令：`mkdir`、`touch`、`rm`、`rmdir`、`mv`、`cp` 和 `sed`。当这些命令带有安全环境变量（如 `LANG=C` 或 `NO_COLOR=1`）或进程包装器（如 `timeout`、`nice` 或 `nohup`）作为前缀时，也会自动批准。与文件编辑一样，自动批准仅适用于工作目录或 `additionalDirectories` 内的路径。

每个路径也会经过[符号链接检查](/docs/zh-CN/permissions#symlinks)，因此解析到该范围之外的写入也不会自动批准。超出该范围的路径、对[受保护路径](#protected-paths)的写入、`rm` 和 `rmdir` 移除针对[关键路径](#critical-paths)的操作以及所有其他 Bash 命令（除了[内置只读集合](/docs/zh-CN/permissions#read-only-commands)）仍然会提示。

当启用 [PowerShell 工具](/docs/zh-CN/tools-reference#powershell-tool)时，`acceptEdits` 模式还会自动批准 `Set-Content`、`Add-Content`、`Clear-Content` 和 `Remove-Item` 在范围内路径上的操作，以及它们的常见别名。相同的范围和受保护路径规则适用，`Remove-Item` 获得[自己的检查](#remove-item-in-powershell)。包含引号字符的位置参数，如 `Set-Content .\notes.txt "It's done"` 中的撇号，即使在范围内路径上也仍然会提示，因为 Claude Code 无法静态验证其引用和未引用读数不同的参数。通过命名参数（如 `-Value`）传递内容以避免提示。

当您想在编辑器中或通过 `git diff` 事后查看更改，而不是逐个批准每个编辑时，使用 `acceptEdits`。

从 Manual 模式按一次 `Shift+Tab` 进入它，或直接启动它：

```bash theme={null}
claude --permission-mode acceptEdits
```

<h2 id="analyze-before-you-edit-with-plan-mode">
  使用 plan mode 在编辑前进行分析
</h2>

Plan mode 告诉 Claude 研究并提议更改而不进行编辑。Claude 读取文件、运行 shell 命令进行探索并编写计划，但不编辑您的源代码。除了在[绕过权限可用](#skip-all-checks-with-bypasspermissions-mode)的交互式终端会话中，编辑保持阻止状态，直到您批准计划。

shell 命令在规划期间发生的情况取决于会话，以下第一个匹配的情况适用：

* **具有可用绕过权限的交互式终端会话**：分类器和提示都不适用于规划命令。[使用 bypassPermissions 模式跳过所有检查](#skip-all-checks-with-bypasspermissions-mode)涵盖仍会在那里提示的少数事项。
* **[Auto mode](/docs/zh-CN/auto-mode-config)可用且 `useAutoModeDuringPlan` 设置打开**，默认情况下是这样：分类器审查 shell 命令（除了[关键路径移除](#critical-paths)）而不是提示您。批准的命令运行，拒绝的命令被阻止。
* **Auto mode 不可用，或 `useAutoModeDuringPlan` 关闭**：[内置只读集合](/docs/zh-CN/permissions#read-only-commands)外的命令会提示批准，包括当沙箱的[自动允许模式](/docs/zh-CN/sandboxing#sandbox-modes)启用时。

通过按 `Shift+Tab` 或在单个提示前加上 `/plan` 进入 plan mode。您也可以从 CLI 启动 plan mode：

```bash theme={null}
claude --permission-mode plan
```

再次按 `Shift+Tab` 以退出 plan mode 而不批准计划。

<h3 id="review-and-approve-a-plan">
  审查并批准计划
</h3>

当计划准备好时，Claude 会呈现它并询问如何继续。从该提示中，您可以选择：

* **是的，并使用自动模式**：批准并以[自动模式](#eliminate-prompts-with-auto-mode)启动。如果自动模式不[可用于您的会话](#eliminate-prompts-with-auto-mode)，例如因为您的组织关闭了它，此选项读取**是的，自动接受编辑**。如果您使用启用的绕过权限启动会话，该选项读取**是的，并为此会话切换到绕过权限（无进一步提示）**。
* **是的，手动批准编辑**：批准并逐个审查每个编辑。
* **否，继续规划**：保持在 plan mode 并告诉 Claude 要更改什么。

批准计划退出 plan mode 并将会话切换到每个批准选项描述的权限模式，因此 Claude 开始编辑。要再次规划，使用 `Shift+Tab` 循环回到 plan mode，或在下一个提示前加上 `/plan`。

按 `Ctrl+G` 在默认文本编辑器中打开建议的计划并在 Claude 继续之前直接编辑它。当启用 [`showClearContextOnPlanAccept`](/docs/zh-CN/settings-reference#showclearcontextonplanaccept) 时，列表获得第一个选项，该选项批准计划并清除规划上下文。

接受计划也会根据计划为会话提供[生成的标题](/docs/zh-CN/sessions#name-your-sessions)，除非您已经命名了会话。

<h3 id="set-plan-mode-as-the-default">
  将 plan mode 设置为默认值
</h3>

要使 plan mode 成为项目的终端会话的默认值，请在 `.claude/settings.json` 中将 `defaultMode` 设置为 `plan`，如[以不同的权限模式启动](#start-in-a-different-mode)下的示例所示。[VS Code 扩展](/docs/zh-CN/vs-code)启动的对话不读取项目设置以获取起始权限模式。在那里，改为在您的 VS Code 用户设置中将 `claudeCode.initialPermissionMode` 设置为 `plan`。

<h2 id="eliminate-prompts-with-auto-mode">
  使用自动模式消除权限提示
</h2>

自动模式让 Claude 无需经过常规权限提示即可执行操作。一个独立的分类器模型会在操作运行前对其进行审查，阻止任何超出您请求范围、针对无法识别的基础设施，或看起来受 Claude 读取的恶意内容驱动的操作。显式的 [ask 规则](/docs/zh-CN/permissions#manage-permissions)仍会强制弹出提示。

在 Claude Code v2.1.283 或更高版本中，对于所有计划和提供商，自动模式都是交互式终端和 VS Code 会话的[内置初始权限模式](#which-mode-a-session-starts-in)。在更早的版本中，它仅在 Pro、Max 和 Team 计划中是内置初始权限模式。

分类器还会在 Claude Code 投递之前审查 Claude 通过 [`SendMessage`](/docs/zh-CN/tools-reference) 发送给另一个 Agent 的每条消息，无论是纯文本还是结构化的 [agent team](/docs/zh-CN/agent-teams) 消息，这在自动模式和[分类器审查命令时的计划模式](#analyze-before-you-edit-with-plan-mode)中均适用；发送审查需要 Claude Code v2.1.222 或更高版本。

默认情况下，分类器不会审查针对关键路径的 `rm` 和 `rmdir` 删除操作，例如 `rm -rf /` 或 `rm -rf ~`。[关键路径](#critical-paths)介绍了它们在各权限模式下的处理方式。

自动模式还会促使 Claude 持续工作，而不停下来提出澄清性问题，不过当您的提示词或某个 skill 明确依赖提问时，Claude 仍会提问。如果希望在仍会向您提示的模式下获得更强的自主行为，请改为设置 [Proactive 输出样式](/docs/zh-CN/output-styles)。

<Warning>
  自动模式可以减少权限提示，但不能保证安全。请将其用于您信任总体方向的任务，而不是作为敏感操作审查的替代品。
</Warning>

只有当您的账户满足以下所有要求时，才能使用自动模式：

* **计划**：所有计划。
* **组织**：在 Team 和 Enterprise 上，自动模式默认可用。管理员可以通过在[托管设置](/docs/zh-CN/managed-settings)中将 `permissions.disableAutoMode` 设置为 `"disable"` 来为组织关闭该功能。
* **模型**：在 Anthropic API 和 [Claude Platform on AWS](/docs/zh-CN/claude-platform-on-aws) 上，需要 Claude Opus 4.6 或更高版本、Sonnet 4.6 或更高版本、Haiku 5.5，或 [Fable 模型](/docs/zh-CN/model-config#work-with-fable)。在 Amazon Bedrock、Google Cloud's Agent Platform、Microsoft Foundry 以及已登录的 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 会话中，仅支持 Claude Sonnet 5 或更高版本、Opus 4.7 或更高版本、Haiku 5.5 以及 Fable 模型。较旧的模型（包括 Sonnet 4.5、Opus 4.5、Haiku 4.5 和 claude-3 模型）在任何提供商上均不受支持。
* **提供商**：在 Anthropic API、Claude Platform on AWS、Amazon Bedrock、Google Cloud's Agent Platform、Microsoft Foundry 以及已登录的 Claude apps gateway 会话中默认可用。

如果 Claude Code 报告自动模式不可用，请首先检查这些要求，以及是否有任何设置文件设置了 [`disableAutoMode`](/docs/zh-CN/settings-reference#disableautomode)。Anthropic 也可能已在服务器端关闭了自动模式，或者服务器可能拒绝了您账户的自动模式。收到上述任一答复的会话会在会话结束前一直保持自动模式关闭，因此请稍后启动新会话。

另一条指明某个模型并表示自动模式"cannot determine the safety"（无法确定安全性）的消息，意味着某次分类器请求失败。这种失败通常是暂时的，但在 Amazon Bedrock 上，它可能会反复出现，直到您的账户能够调用所指明的模型。有关原因和处理方法，请参阅[错误参考](/docs/zh-CN/errors#auto-mode-cannot-determine-the-safety-of-an-action)。

如果您在[设置](/docs/zh-CN/settings-reference#all-settings)中设置了 `defaultMode: "auto"`，而终端会话却以 Manual 模式启动且没有报错，那么该设置很可能位于 `.claude/settings.json` 或 `.claude/settings.local.json` 中。`auto` 在这些文件中不会生效。请将其移至 `~/.claude/settings.json`。对于由 VS Code 扩展启动的对话，请改为查看[切换权限模式](#switch-permission-modes)中该扩展自己的列表。

<h3 id="enable-auto-mode-on-bedrock-agent-platform-or-foundry">
  Bedrock、Agent Platform 或 Foundry 上的自动模式
</h3>

在 [Amazon Bedrock](/docs/zh-CN/amazon-bedrock)、[Google Cloud's Agent Platform](/docs/zh-CN/google-vertex-ai)、[Microsoft Foundry](/docs/zh-CN/microsoft-foundry) 以及已登录的 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 会话中，自动模式默认可用。当没有其他内容设置权限模式时，在该部分表格所列的版本上，它也是[内置初始权限模式](#which-mode-a-session-starts-in)。要自行选择初始权限模式，请按照[以不同的权限模式启动](#start-in-a-different-mode)中的说明设置 `permissions.defaultMode`，或从 VS Code 扩展的模式指示器中选择权限模式。

在这些提供商上，仅支持 Claude Sonnet 5 或更高版本、Opus 4.7 或更高版本、Haiku 5.5 以及 Fable 模型。在任何其他模型上，会话将改为以 Manual 模式启动。在这些提供商上将自动模式与 Haiku 5.5 一起使用需要 Claude Code v2.1.293 或更高版本。

要阻止开发者使用自动模式，请在[托管设置](/docs/zh-CN/managed-settings)中将 `disableAutoMode` 设置为 `"disable"`。这会将 `auto` 从 `Shift+Tab` 循环中移除，并且使用 `--permission-mode auto` 启动的会话将改为以 Manual 模式启动。当该设置从[管理员部署的来源](/docs/zh-CN/managed-settings#which-managed-source-claude-code-uses)到达一个已在自动模式下运行的会话时，该会话会退出自动模式，并显示 `auto mode disabled by settings`。在 v2.1.251 之前，正在运行的会话会保持自动模式直到会话结束。

在 v2.1.158 到 v2.1.206 中，这些提供商上的自动模式默认关闭，直到您设置 `CLAUDE_CODE_ENABLE_AUTO_MODE=1`；并且除非同时设置了该变量，否则 Claude Code 会在这些提供商上忽略 `defaultMode: "auto"`。出于兼容性考虑，该变量仍然可用，但从 v2.1.207 起不再产生任何效果。

<h3 id="server-side-classifier-review">
  服务器端分类器审查
</h3>

在自动模式下，Claude Code 可以在会话的模型请求中请求服务器检查由[决策顺序](#how-the-classifier-evaluates-actions)送交审查的操作，以代替发送其自身的分类器请求。以下会话会请求服务器审查：

* **直接连接到 Anthropic API**：在交互式终端会话以及 `-p`、Agent SDK、[VS Code 扩展](/docs/zh-CN/vs-code)和[桌面应用](/docs/zh-CN/desktop)会话中，无论您的计划或账户类型如何，随 Anthropic 逐步推出而生效。在交互式终端会话中，Pro、Max 和 Team 计划需要 Claude Code v2.1.271 或更高版本，Enterprise 计划和 Claude API 账户需要 v2.1.278 或更高版本。在 `-p`、Agent SDK、VS Code 扩展和桌面应用会话中，需要 Claude Code v2.1.281 或更高版本。从 v2.1.282 起，[不获取功能标志](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)的会话（例如因为您关闭了遥测）在任何类型的会话中都会默认请求服务器审查。
* **云提供商，或 LLM 网关或代理**：在 [Claude Platform on AWS](/docs/zh-CN/claude-platform-on-aws)、Amazon Bedrock、Google Cloud's Agent Platform 和 Microsoft Foundry 上，以及每当您将 `ANTHROPIC_BASE_URL` 指向 [LLM 网关或代理](/docs/zh-CN/llm-gateway)时，无论您的计划如何。默认请求服务器审查需要 Claude Code v2.1.278 或更高版本。
* **已登录的 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 会话**：需要 Claude Code v2.1.280 或更高版本

当服务器审查这些操作时，由服务器的裁决决定结果。此外还有另外两种可能的结果：

* **服务器不审查该会话**：响应完成但没有审查结果，或服务器答复它不审查此会话。最常见的原因是 LLM 网关或代理丢弃了审查请求或结果，以及平台、区域或凭据尚不支持服务器端检查。Claude Code 会回退到其自身的分类器请求。一旦该回退在会话剩余时间内保持生效，在这些请求需要计费的账户上，它会显示[关于分类器请求费用的通知](/docs/zh-CN/auto-mode-classifier-billing)。
* **服务器未对某个操作给出裁决**：Claude Code 会拒绝该操作，而不是在未经审查的情况下运行它。在任何连接上，当响应在审查结果到达前结束，或结果以 Claude Code 无法读取的形式到达时，都会发生这种情况。截断响应或改写结果的 LLM 网关或代理可能导致上述任一情况。在直接连接到 Anthropic API 时，当服务器对该操作的检查失败（例如超时）时也会发生这种情况。[服务器未返回安全裁决](/docs/zh-CN/errors#the-server-returned-no-safety-verdict)介绍了拒绝消息、拒绝反复发生时的情况以及处理方法。

要跳过请求服务器审查并始终使用 Claude Code 自身的分类器请求，请设置 [`CLAUDE_CODE_AUTO_MODE_SERVER=0`](/docs/zh-CN/env-vars)。在直接连接到 Anthropic API 时，该变量需要 Claude Code v2.1.281 或更高版本。在这种连接上将其设置为 `1`，会在尚未启用服务器审查的会话中启用它，除非您同时设置了 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`。如果您设置了 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` 且未设置 `CLAUDE_CODE_AUTO_MODE_SERVER`，Claude Code 也会停止请求服务器审查，[禁用预发布功能](/docs/zh-CN/llm-gateway-protocol#disable-pre-release-capabilities)中描述的情况除外。

<h3 id="what-the-classifier-blocks-by-default">
  分类器默认阻止的内容
</h3>

分类器信任您的工作目录以及会话启动时为其配置的远程仓库。在会话期间通过 `git remote add` 或 `git remote set-url` 添加或重新指向的远程仓库不受信任，其他所有内容都被视为外部内容，直到您[配置受信任的基础设施](/docs/zh-CN/auto-mode-config)。

**默认阻止**：

* 下载并执行代码，例如 `curl | bash`
* 将敏感数据发送到外部端点
* 生产环境部署和迁移
* 在云存储上进行批量删除
* 授予 IAM 或仓库权限
* 修改共享基础设施
* 不可逆地销毁会话开始前已存在的文件
* 强制推送
* 提交或推送一项更改，该更改在运行时会将密钥或敏感数据发送到仓库之外，或扩大部署所暴露的内容。这包括将密钥传递给尚未接收它的目标的 CI 工作流或部署配置、读取密钥存储并将数据发送出去的脚本或设置步骤，以及扩大部署发布内容的配置更改，例如注册表、可见性、制品或 sourcemap 设置。该检查适用于任何分支，即使仓库是公开的也同样适用，并在更改被提交或推送时触发，无论该提交或推送是否会触发流水线；要解除阻止，需要说明其执行效果，而不仅仅是提交或推送本身。在 v2.1.211 之前，该检查改为限定于默认分支：当推送到默认分支的内容包含敏感内容、相对于您的要求隐瞒或错误描述的更改、从仓库外部移植的内容，或绕过了您要求的审查时，该推送会被阻止
* `git reset --hard`、`git checkout -- .`、`git restore .`、`git clean -fd`、`git stash drop` 或 `git stash clear`，分类器会假定这些命令会丢弃未提交的更改
* 当 HEAD 处的提交并非在本会话中创建时执行 `git commit --amend`
* 从 v2.1.198 起，当 HEAD 处的提交已被推送时执行 `git commit --amend`。仅修改提交信息的改写不会被阻止：即在 Claude 于本会话中创建的提交上，不暂存任何新内容的情况下执行 `--amend -m`
* `terraform destroy`、`pulumi destroy`、`cdk destroy` 或 `terragrunt destroy`，以及应用会销毁资源的计划
* 写入密钥管理器，或更改 DNS 记录或 TLS 证书
* 合并没有任何人工批准的 Pull Request、批准 Claude 自己的 Pull Request，或禁用 CI 检查
* 发布本身就是对自动化发出的命令的评论，例如 `atlantis apply` 或机器人的 `/deploy` 或 `/merge`
* 切换、逐步放量或删除生产环境的功能标志
* 将基础设施更改应用到受保护的 IaC 作用域，或排空并移除集群节点
* 对共享计算集群的写入超出了您所指定的资源，例如会波及其他用户作业的标签选择器或 `--all`
* 创建在每个节点上运行或拦截集群流量的 Kubernetes 资源，例如 DaemonSet 和准入 webhook
* 连接到敏感远程目标的交互式 shell 或端口转发
* 打开使本地服务可从公共互联网访问的隧道或反向 shell
* 将有效的凭据或令牌打印到会话记录或文件中
* 访问在您的[环境](/docs/zh-CN/auto-mode-config#define-trusted-infrastructure)中被列为敏感数据位置的位置、从中复制数据，或将数据从此类位置发送给该条目所排除的受众
* 绕过您的内部包注册表、将包安装路由到公共注册表。当您的环境中列出了内部注册表或镜像，或者您在对话中告诉 Claude 存在内部注册表或镜像时，此规则适用
* 使用会解除安全防护的标志运行命令，例如 `--insecure`
* 启动无需人工批准或沙箱即可运行的自主 Agent 循环，例如使用 `--dangerously-skip-permissions` 或 `--no-sandbox` 启动的循环。这包括在禁用隔离和逐操作批准的情况下运行第三方 Agent 或评估工具，例如使用 `--yes-always` 启动的运行器
* 可能将页面内容、cookie 或凭据发送到源站之外的 [Claude in Chrome](/docs/zh-CN/chrome) 浏览器操作
* 通过通配符、glob 或时间过滤器（而非指定的具体路径）删除 `/tmp`、`$TMPDIR` 或其他共享临时目录或缓存目录中的文件
* 在发送、上传、发布或写入给他人或共享系统的内容中包含敏感细节，而您自己的消息并未授权将这些细节提供给该接收方。当仓库位于信任边界之外或为公开仓库（包括您组织自己的公开仓库）时，PR 和 issue 正文、提交信息以及评论都属于此类外发内容；内部文件路径、代号、实时 API 响应数据（例如电子邮件或账户标识符）以及基础设施标识符都属于敏感细节。对于 PR 或 issue 正文中来自 API 响应的实时个人数据，例如电子邮件地址、账户或组织标识符或使用量指标，无论仓库的可见性或信任边界如何，都需要您明确指出这些细节和接收方。该检查需要 Claude Code v2.1.203 或更高版本
* 向 Claude Code 自己的 tmux 窗格发送按键以驱动其自身界面，分类器会将此视为 Claude 更改其自身的权限或监督
* 注释掉、删除或强制通过用于保护安全行为（例如身份验证、访问控制、输入验证或沙箱隔离）的测试或断言
* 删除或拆除 Claude 未在本会话中创建的有状态资源，且没有更具体的删除规则适用、您也未指定该资源
* 将 API 基础 URL、代理端点、webhook 接收器或注册表镜像重新指向与任务不相符的第三方主机，包括在 `.env.example` 等示例文件中
* 使用 `git remote set-url` 或 `git remote add` 更改推送目标，除非您指定了新的远程仓库
* 将密钥或个人数据、受托数据推送到已知为公开的仓库，或将不属于该仓库本身工作的机密材料推送到该仓库。对于个人数据或受托数据，唯一的例外是 dotfiles 仓库本身的主题内容；来自私有仓库的内容进入任何公开渠道也会以同样方式被阻止；这两项细化都需要 Claude Code v2.1.203 或更高版本。在 v2.1.203 之前，个人数据与机密材料归为一类，仅在不属于该仓库本身工作时才被阻止。当仓库的可见性无法确定时，分类器不会仅凭这一点进行阻止，而是依据其他规则来判断内容
* 向其他仓库或组织发起 Pull Request、使用 `gh repo fork` 进行 fork，或推送到第三方仓库，除非您指定了该外部目标

其中一些类别依赖于[环境](/docs/zh-CN/auto-mode-config#define-trusted-infrastructure)条目，例如敏感远程目标和受保护的 IaC 作用域，您可以将它们收窄到具体名称。

Claude Code v2.1.203 及更高版本还会默认阻止以下操作：

* 来自敏感本地存储的内容，或来自名称、路径或类型表明其为敏感文件的内容，进入提交、推送、PR 或 issue 文本、gist 或粘贴、或包发布，除非您同时指定了来源和目标。会话记录和对话日志、凭据和配置类点文件夹（例如 SSH 密钥、云凭据、浏览器配置文件和 shell 历史记录）以及用户数据导出都包括在内，仓库为私有也不能解除此阻止

Claude Code v2.1.205 及更高版本还会默认阻止以下操作：

* 写入 Claude Code 会话记录，即 `~/.claude/projects/` 或您所配置的配置目录下的 `.jsonl` 历史文件，无论是直接写入还是通过 shell 命令写入。该规则还涵盖 Claude Code 为其自身检查而附加到每条会话记录条目中的元数据行。读取会话记录不会被阻止
* 递归强制删除，例如 `rm -rf "$VAR"` 或 `Remove-Item -Recurse -Force $dir`，其目标是在分类器所见对话中任何地方都未赋值的 shell 变量，或以此类变量为根的 glob。该值仅来自先前的命令输出，而分类器从不接收这些输出，因此分类器无法根据其他删除规则验证删除目标。当您指明要删除的确切路径，或 Claude 将解析后的字面路径写入命令并重新运行删除时，该阻止会解除。分类器能够解析目标的删除操作不受影响。

  直接位于变量下的 glob（例如 `rm -rf "$VAR"/*`）则属于[关键路径](#critical-paths)。目标为单独的 `*` 或以 `/*` 或 `\*` 结尾的 `Remove-Item` 永远不会到达分类器：Claude Code 会[直接拒绝它们](#remove-item-in-powershell)。

Claude Code v2.1.257 及更高版本还会默认阻止以下操作：

* 从云实例元数据端点（例如 `169.254.169.254`）请求凭据，或明确使用机器自身的服务账户或节点身份对云、集群或注册表调用进行身份验证
* 通过直接请求以外的路径访问公共主机，例如隧道、反向 shell，或被改写为指向外部的解析器或代理配置
* 读取属于主机而非您的任务的凭据，例如节点证书或节点的容器注册表身份验证信息
* 连接或扫描 Claude 未启动的同级容器、pod 或虚拟机，或容器所在的节点

如果 Claude Code 运行的环境本应允许其中某项操作，请在 `autoMode.environment` 中的 [Host containment 条目](/docs/zh-CN/auto-mode-config#define-trusted-infrastructure)中描述该设置。

Claude Code v2.1.261 及更高版本还会默认阻止以下操作：

* 当 URL 本身携带了正在共享的内容时，在消息、PR 或 issue 文本、文档或任何其他会打开或获取该链接的地方，发布或写入指向公共粘贴、图表或数据共享服务的链接，除非您指定了该服务

**默认允许**：

* 在您的工作目录中进行本地文件操作
* 安装您的锁文件或清单中声明的依赖
* 读取 `.env` 并将凭据发送到与之匹配的 API
* 只读 HTTP 请求
* 推送到您正在处理的仓库的任何分支，包括默认分支。名称表明其为部署或发布目标的非默认分支（例如 `production` 或 `gh-pages`）不在此列：分类器会单独判断推送到这类分支的操作。推送的内容仍会根据其他规则进行检查，[`permissions.deny` 规则](/docs/zh-CN/permissions#manage-permissions)在所有模式下仍可按[命令的书写形式](/docs/zh-CN/permissions#bash-rule-limits)阻止推送命令，并且远程仓库自身的分支保护仍然适用。在 v2.1.211 之前，默认仅允许推送到您开始时所在的分支、Claude 创建的分支，以及对默认分支的常规推送；而在 v2.1.203 之前，任何直接推送到默认分支的操作都会被阻止
* 删除 Claude 在同一会话中先前创建的确切作业
* 作为任务的一部分，读取、审查或编写与安全相关的代码、配置和威胁模型
* 在同一多 Agent 会话中协同工作的 Agent 之间的消息
* 将数据发送到您在 [`environment`](/docs/zh-CN/auto-mode-config#define-trusted-infrastructure) 中列出的受信任域名、存储桶和服务。这仅涵盖数据流动，不包括对同一基础设施的破坏性操作或凭据操作
* [Claude in Chrome](/docs/zh-CN/chrome) 导航到受信任的内部域名、localhost 或您指定的 URL

沙箱化命令默认没有网络访问权限。Claude 会在命令本身上指明该命令所需的主机，分类器会将这些主机与命令一起审查，而获批的列表仅为该条命令开放这些主机。[按命令允许的域名](/docs/zh-CN/sandboxing#per-command-allowed-domains-in-auto-mode)介绍了列表能开放和不能开放的内容，以及命令尝试访问未列出的主机时会发生什么。

运行 `claude auto-mode defaults` 可以以 JSON 格式打印完整的规则列表。如果常规操作被阻止，管理员可以通过 `autoMode.environment` 设置添加受信任的仓库、存储桶和服务：请参阅[配置自动模式](/docs/zh-CN/auto-mode-config)。

推送到您正在处理的仓库的任何分支，以及创建与您的请求相符的 Pull Request，都会在无提示的情况下运行，除非该推送或 Pull Request 属于[阻止列表](#what-the-classifier-blocks-by-default)中的情况，例如密钥或敏感数据离开仓库，或 Pull Request 针对的是其他仓库或组织。如果要在保持自动模式的同时，要求在这些命令执行前进行人工确认，请添加 `permissions.ask` 规则，这些规则按[命令的书写形式](/docs/zh-CN/permissions#bash-rule-limits)进行匹配：请参阅[常见边界](/docs/zh-CN/auto-mode-config#common-boundaries)。

<h3 id="first-read-outside-the-working-directories">
  首次读取工作目录之外的内容
</h3>

当 [`permissions.blockReadsOutsideWorkingDirectories`](/docs/zh-CN/settings-reference#permissions-blockreadsoutsideworkingdirectories) 关闭时，在自动模式下文件读取无需提示即可运行，包括读取[工作目录](/docs/zh-CN/permissions#working-directories)之外的内容。当 Claude 首次对工作目录之外的路径使用 Read、Grep 或 Glob 工具时，Claude Code 会询问是否允许该读取。

在非交互式 `-p` 运行或后台会话中不会出现该提示；这些情况下的读取照常运行。

无论您如何回答，Claude 都会继续工作：

* **是，并继续允许读取工作目录之外的任何内容**：读取会运行，之后对工作目录之外内容的读取照常运行，并且 Claude Code 会记录您的回答，使该提示不再出现
* **否，并从现在起阻止读取工作目录之外的内容**：读取会被拒绝，并且 Claude Code 会在您的用户设置中将 [`permissions.blockReadsOutsideWorkingDirectories`](/docs/zh-CN/settings-reference#permissions-blockreadsoutsideworkingdirectories) 设置为 `true`，这会使文件工具在之后的每个会话和每种权限模式中拒绝此类读取。如果之后要让 Claude 读取此类路径，请使用 `/add-dir` 添加其目录，或移除该设置。
* **否，下次再询问**：读取会被拒绝，下一次读取工作目录之外的内容时会再次提示
* **是，但下次再询问**：读取会运行，不会保存任何内容，下一次读取工作目录之外的内容时会再次提示

<h3 id="boundaries-you-state-in-conversation">
  您在对话中声明的边界
</h3>

分类器会将您在对话中声明的边界视为阻止信号。如果您告诉 Claude "不要推送"或"在部署前等我审查"，即使默认规则允许，分类器也会阻止相应的操作。边界会一直有效，直到您在后续消息中解除它。Claude 自己判断某个条件已满足并不能解除边界。

边界不会作为规则存储。分类器在每次检查时都会从会话记录中重新读取这些边界，因此如果[上下文压缩](/docs/zh-CN/costs#reduce-token-usage)移除了声明边界的消息，该边界可能会丢失。如需硬性保证，请改为添加 [deny 规则](/docs/zh-CN/permissions#permission-rule-syntax)。

<h3 id="approvals-you-state-in-conversation">
  您在对话中声明的批准
</h3>

如果您告诉 Claude 某个被阻止的操作是允许的，分类器会将其视为您的批准，并可以解除阻止。您的措辞决定了该操作是否会运行，以及批准的覆盖范围：

* **指明操作及其具体细节**：您的消息必须指明该操作以及使其具有危险性的具体内容，例如强制推送的分支。仅指明动词不会解除任何阻止，因此"您可以强制推送"不会解除阻止。
* **预期它仅涵盖一个操作**：批准涵盖您所指明的破坏性操作，因此之后的操作会再次被阻止，除非您授予的是持续性批准。如果不想逐个操作地批准某种常规模式，请将其添加到 [`autoMode.allow`](/docs/zh-CN/auto-mode-config#override-the-block-and-allow-rules)。
* **有些阻止会保持不变**：[分类器的优先级顺序](/docs/zh-CN/auto-mode-config#override-the-block-and-allow-rules)规定了您的批准可以解除哪些阻止。要运行它不会解除阻止的步骤，请[退出自动模式](#switch-permission-modes)并回应权限提示。

<h3 id="when-auto-mode-falls-back">
  自动模式回退时
</h3>

当自动模式无法批准您会话中的操作时，具体情况取决于以下场景：

* **操作被阻止**：Claude Code 会显示通知，并在 `/permissions` 的 **Recently denied** 选项卡下列出该操作，您可以在那里按 `r` 以手动批准的方式重试。
* **反复阻止**：如果分类器连续 3 次或累计 20 次阻止操作，自动模式会暂停，Claude Code 会恢复提示。批准被提示的操作后会恢复自动模式。有关阻止次数的计算方式，请参阅[反复阻止阈值](#repeated-block-thresholds)。
* **分类器未给出裁决**：当独立于自动模式的安全检查拒绝了分类器自身的请求，或分类器的响应无法解析时，Claude Code 会拒绝该操作，且不显示通知，也不会添加 **Recently denied** 条目。有关每种情况显示的消息及处理方法，请参阅[自动模式无法确定操作的安全性](/docs/zh-CN/errors#auto-mode-cannot-determine-the-safety-of-an-action)。
* **服务器未给出裁决**：在[服务器端分类器审查](#server-side-classifier-review)下，Claude Code 会拒绝服务器未给出裁决的操作，并在连续十个响应均无裁决后停止当前轮次。请参阅[服务器未返回安全裁决](/docs/zh-CN/errors#the-server-returned-no-safety-verdict)。
* **检查期间切换模式**：如果您在分类器检查尚未完成时切换权限模式，Claude Code 会丢弃新模式本不会请求的裁决。此时会改为提示您批准，或者在 [`dontAsk` 模式](#allow-only-pre-approved-tools-with-dontask-mode)下自动拒绝该操作。

<h4 id="repeated-block-thresholds">
  反复阻止阈值
</h4>

连续 3 次阻止和累计 20 次阻止的阈值不可配置。累计计数器在整个会话期间持续存在，仅当其自身的限制触发回退时才会重置。当独立于自动模式的安全检查拒绝了分类器自身的请求时，Claude Code 不会将该拒绝计入任一阈值。

未使用 [`--permission-prompt-tool`](/docs/zh-CN/cli-reference#cli-flags) 的[非交互式](/docs/zh-CN/headless) `-p` 运行没有可回退的提示。当反复阻止达到阈值时，该操作不会运行，Claude 会继续工作。Claude Code 不会停止该运行。

反复阻止通常意味着分类器缺少有关您基础设施的上下文。请使用 `/feedback` 报告误报，或请管理员[配置受信任的基础设施](/docs/zh-CN/auto-mode-config)。

<h3 id="how-auto-mode-evaluates-actions">
  自动模式如何评估操作
</h3>

以下各节介绍 Claude Code 评估操作的顺序、分类器如何审查子代理的工作，以及分类器调用在成本和延迟方面带来的额外开销。

<span id="how-the-classifier-evaluates-actions" />

<AccordionGroup>
  <Accordion title="分类器如何评估操作">
    每个操作都会经过固定的决策顺序。第一个匹配的步骤生效：

    1. 与您的 [allow、ask 或 deny 规则](/docs/zh-CN/permissions#manage-permissions)匹配的操作会立即得到处理，但以下情况除外：
       * 对[受保护路径](#protected-paths)的写入即使匹配了 allow 规则，也会交由分类器处理
       * 任何 allow 规则都不会批准针对[关键路径](#critical-paths)的 `rm` 和 `rmdir` 删除操作
       * 标记为 [`requiresUserInteraction`](/docs/zh-CN/mcp#require-approval-for-a-specific-tool) 的 MCP 工具即使匹配了 allow 规则，也会直接提示您；在[您的组织设置为 `ask`](/docs/zh-CN/mcp#organization-controls-on-connector-tools) 的连接器工具上也是如此（在该设置传达到 Claude Code 的会话中）
       * 携带[按命令允许的域名](/docs/zh-CN/sandboxing#per-command-allowed-domains-in-auto-mode)的 shell 命令即使匹配了 allow 规则，也会交由分类器处理，因为规则批准的是命令，而不是其主机
       * 基于命令内容进行匹配的 ask 规则（例如 `Bash(git push *)`）会回退为权限提示
       * 当 Claude 请求的路径本身不受保护，但[符号链接检查](/docs/zh-CN/permissions#symlinks)将写入解析到受保护路径时，会提示您
    2. 工作目录中的只读操作和文件编辑会被自动批准，但对[受保护路径](#protected-paths)的写入以及[首次读取工作目录之外的内容](#first-read-outside-the-working-directories)除外，后者会提示您
       * 在启用了[服务器端分类器审查](#server-side-classifier-review)的会话中，只读和[沙箱化](/docs/zh-CN/sandboxing#sandbox-modes)的 shell 命令会等待该审查，如果审查标记了它们，则会被阻止
       * 当[符号链接检查](/docs/zh-CN/permissions#symlinks)将工作目录内的写入解析到工作目录之外的位置时，会提示您
       * 当 Claude 读取[他人制作的 Artifact](/docs/zh-CN/artifacts#read-an-artifact-shared-with-you) 时，适用该部分列出的批准情况
    3. 其他所有操作都会交给分类器处理，按默认方式处理的[关键路径删除](#critical-paths)除外。在第 1 步中直接提示您的连接器工具和 `requiresUserInteraction` MCP 工具也永远不会到达分类器，因此组织要求的批准和同意步骤都不会被自动批准
    4. 如果分类器阻止了操作，Claude 会收到原因。在大多数会话中，原因会指明分类器匹配的规则，例如 `[Data Exfiltration]`，而不是给出书面解释；请参阅[查看拒绝记录](/docs/zh-CN/auto-mode-config#review-denials)

    您安装的处理 `tool.check` 的 [mod](/docs/zh-CN/plugins/mods/overview) 可以在第 3 步之前批准操作，分类器不会检查 mod 所批准的操作。请参阅[使用 hook 扩展权限](/docs/zh-CN/permissions#extend-permissions-with-hooks)。

    在 VS Code 扩展中，[Claude in Chrome](/docs/zh-CN/chrome) 浏览器操作如何获得批准取决于会话连接到浏览器的方式：请参阅 [VS Code 会话中的权限提示](/docs/zh-CN/chrome#permission-prompts-in-vs-code-sessions)。

    进入自动模式时，授予任意代码执行能力的宽泛 allow 规则会被丢弃：

    * 通配的 `Bash(*)` 或 `PowerShell(*)`
    * 带通配符的解释器，例如 `Bash(python*)`
    * 包管理器的 run 命令
    * `Agent` allow 规则
    * [`Monitor`](/docs/zh-CN/tools-reference#monitor-tool) allow 规则，因为 Claude Code 通过 shell 运行 Monitor 命令

    像 `Bash(npm test)` 这样的窄范围规则会保持有效。当您退出自动模式时，Claude Code 会恢复被丢弃的规则。在 v2.1.236 之前，Claude Code 在自动模式下保留了 `Monitor` allow 规则，因此匹配整个工具的规则会在没有分类器审查的情况下批准 Monitor 命令。

    在执行会丢弃未提交工作的命令（例如 `git reset --hard` 或 `rm -rf`）之前，Claude Code 还会自行运行 `git status`，并向分类器显示是否存在已暂存、已修改或未跟踪的工作。即使仓库的 git 配置设置了 `status.showUntrackedFiles=no`，Claude Code 也会在该检查中报告未跟踪的文件。

    在 Claude Code 自身发送的分类器请求中，分类器可以看到用户消息、除只读查询（例如文件读取和搜索）以外的工具调用，以及您的 CLAUDE.md 内容。工具结果会从这些请求中剥离，因此文件或网页中的恶意内容无法直接操纵分类器。

    您可以使用 [PostToolUse hook 的 `classifierContext` 字段](/docs/zh-CN/hooks#annotate-a-result-for-the-auto-mode-classifier)为调用结果添加注释，分类器会将其作为应用提供的上下文读取。该字段需要 Claude Code v2.1.236 或更高版本。

    一个独立的服务器端探测器会扫描传入的工具结果，并在 Claude 读取之前标记可疑内容。有关这些层如何协同工作的更多信息，请参阅[自动模式公告](https://claude.com/blog/auto-mode)和[工程深度解析](https://www.anthropic.com/engineering/claude-code-auto-mode)。
  </Accordion>

  <Accordion title="自动模式如何处理子代理">
    分类器会在三个时间点检查[子代理](/docs/zh-CN/sub-agents)的工作：

    1. 在子代理启动之前，会评估委派的任务描述，因此看起来危险的任务会在生成时被阻止。
    2. 在子代理运行期间，它的每个操作都会经过与父会话相同的[决策顺序](#how-the-classifier-evaluates-actions)，并使用相同的阻止和允许规则。子代理 frontmatter 中的任何 `permissionMode` 都会被忽略。
    3. 当子代理完成时，分类器会在父级读取报告之前审查其工作和最终报告。当分类器标记了子代理的工作或报告，或者独立的 API 安全检查拒绝了该审查时，报告仍会被送达，但会在前面附加安全警告。当分类器无法进行审查时，报告送达时会附带一条说明，提醒您在据此采取行动之前先核实子代理的工作。
  </Accordion>

  <Accordion title="成本和延迟">
    分类器默认在 Claude Sonnet 5 上运行，而不是在您通过 `/model` 选择的模型上运行。Anthropic 在服务器端配置的分类器模型优先于该默认值。当您会话的模型是 Claude Sonnet 4.6，或者 [`availableModels`](/docs/zh-CN/model-config#restrict-model-selection) 排除了 Sonnet 5 时，分类器会改为在会话的模型上运行；当会话在 [Fable 模型](/docs/zh-CN/model-config#work-with-fable)上运行时，则在 Opus 模型上运行。在 Anthropic API 以外的提供商上，该备用 Opus 模型是您在 [`ANTHROPIC_DEFAULT_OPUS_MODEL`](/docs/zh-CN/model-config#environment-variables) 中设置的模型，如果您未设置，则为 Opus 5。

    会话的第一个自动模式请求会验证 Sonnet 5 默认值：如果请求成功，Sonnet 5 将保持为该会话的分类器模型；如果因模型不可用而失败，该会话将改用备用模型。

    在 Enterprise 计划以及使用 Claude API、[Claude Platform on AWS](/docs/zh-CN/claude-platform-on-aws)、Amazon Bedrock、Google Cloud's Agent Platform 或 Microsoft Foundry 的账户上，分类器调用会计入您的 token 用量。每次检查都会发送部分会话记录以及待执行的操作，从而在执行前增加一次往返。受保护路径之外的读取和工作目录编辑会跳过分类器，因此开销主要来自 shell 命令和网络操作。当服务器在会话的模型请求中审查操作时，不存在需要计算的单独分类器调用；请参阅[服务器端分类器审查](#server-side-classifier-review)。

    沙箱化的网络访问不会为每个连接增加分类器请求。分类器会在一次审查中将[命令所指明的主机](/docs/zh-CN/sandboxing#per-command-allowed-domains-in-auto-mode)与命令一起判断，Claude Code 会根据获批的列表检查每个连接，而无需再次调用分类器。
  </Accordion>
</AccordionGroup>

<h2 id="allow-only-pre-approved-tools-with-dontask-mode">
  使用 dontAsk 模式仅允许预先批准的工具
</h2>

如果您设置 `dontAsk` 模式，Claude Code 会自动拒绝所有原本会提示的工具调用。Claude 仍然运行在 Manual 模式下不需要批准的操作，例如您工作目录内的文件读取和[只读 Bash 命令](/docs/zh-CN/permissions#read-only-commands)，以及与您的 `permissions.allow` 规则匹配的操作和由 [PreToolUse hook](/docs/zh-CN/permissions#extend-permissions-with-hooks) 批准的调用。在 CI 管道或受限环境中使用此模式，您可以预先定义 Claude 可以执行的操作；会话永远不会等待输入。当此模式处于活动状态时，状态栏显示 `⏵⏵ don't ask on`。

Claude Code 拒绝与您的显式 [`ask` 规则](/docs/zh-CN/permissions#manage-permissions)匹配的调用，而不是提示。它还拒绝内置的 `AskUserQuestion` 工具，即使您的 allow 规则与其匹配，以及您的组织[设置为 `ask`](/docs/zh-CN/mcp#organization-controls-on-connector-tools) 的连接器工具在该设置到达 Claude Code 的会话中。它以相同的方式拒绝标记为 [`_meta["anthropic/requiresUserInteraction"]`](/docs/zh-CN/mcp#require-approval-for-a-specific-tool) 的 MCP 工具，因为其批准卡需要此模式永远不会收集的答案。

`rm` 和 `rmdir` 移除针对[关键路径](#critical-paths)的操作，如 `rm -rf /` 和 `rm -rf ~`，即使 allow 规则与其匹配或 `PreToolUse` hook 允许它们，也被拒绝。

[网络上的 Claude Code](/docs/zh-CN/claude-code-on-the-web)上的云会话忽略 `defaultMode: "dontAsk"`；有关详细信息，请参阅 [bypassPermissions](#skip-all-checks-with-bypasspermissions-mode)。

在启动时使用标志设置它：

```bash theme={null}
claude --permission-mode dontAsk
```

<h2 id="skip-all-checks-with-bypasspermissions-mode">
  使用 bypassPermissions 模式跳过所有检查
</h2>

`bypassPermissions` 模式禁用权限提示和安全检查，以便工具调用立即执行，包括对[受保护路径](#protected-paths)的写入。

[任何模式都不会自动批准的操作](#actions-no-mode-auto-approves)在此模式下仍会提示。读取[其他组织的公开 Artifact](/docs/zh-CN/artifacts#read-an-artifact-shared-with-you) 需要您的批准，而此模式不会请求批准，因此 Claude 无法读取此类 Artifact。[PowerShell 中的 Remove-Item](#remove-item-in-powershell) 拒绝也适用于此模式。

两个[跨会话消息传递](/docs/zh-CN/cross-session-messaging)保护措施在此模式下仍然适用，在可使用绕过权限的交互式终端计划模式会话中同样适用：

* 针对发送到此机器之外的您的会话的消息，[`isolatePeerMachines`](/docs/zh-CN/settings-reference#isolatepeermachines) 批准提示仍会出现。
* 当没有 [`crossSessionInbound`](/docs/zh-CN/cross-session-messaging#control-inbound-messages) 值适用时，Claude Code 会保留来自您另一个会话的入站消息以供您批准，仅当发送会话将自己标识为同样绕过权限提示时才无需询问即可传递。如果您在消息被保留期间离开该权限模式，Claude Code 会重新应用入站规则，并传递现在被接受的任何保留消息。

在可使用绕过权限的交互式终端会话中，Claude Code 也不强制执行[计划模式的](#analyze-before-you-edit-with-plan-mode)阻止。Claude 仍然被指示在不编辑的情况下进行计划，但它在计划期间尝试的文件编辑或 shell 命令无需提示即可运行。显式[询问规则](/docs/zh-CN/permissions#manage-permissions)和针对[关键路径](#critical-paths)的 `rm` 和 `rmdir` 删除仍会提示。

在 Claude Code 没有交互式终端运行的任何地方，计划模式都会保留其阻止，包括[非交互式运行](/docs/zh-CN/headless)（带 `-p`）、[Agent SDK](/docs/zh-CN/agent-sdk/permissions#plan-mode-plan) 会话和 [VS Code 扩展](/docs/zh-CN/vs-code)的聊天面板中的对话。在这些环境中，`--allow-dangerously-skip-permissions` 使 `bypassPermissions` 稍后可选。

<Warning>
  仅在隔离环境（如容器、虚拟机或没有互联网访问的开发容器）中使用此模式，其中 Claude Code 无法损害您的主机系统。
</Warning>

您无法从未启用此模式的会话进入 `bypassPermissions`。在启动时使用 [`permissions.defaultMode: "bypassPermissions"`](/docs/zh-CN/settings-reference#permissions-defaultmode) 或使用启用标志启用它：

```bash theme={null}
claude --permission-mode bypassPermissions
```

`--dangerously-skip-permissions` 标志是等效的。

Claude Code 在您使用 [`--restricted`](/docs/zh-CN/cli-reference#cli-flags) 启动的会话中拒绝 `bypassPermissions`。`--restricted` 需要 Claude Code v2.1.248 或更高版本。

第一次使用此模式启动交互式会话时，Claude Code 会显示一个警告对话框，要求您接受对在没有权限检查的情况下执行的操作的责任：

* **如果您接受**：Claude Code 在 `~/.claude/settings.json` 中将 `skipDangerousModePermissionPrompt` 设置为 `true`，因此后续会话会跳过对话框。要再次看到对话框，请从该文件中删除该键或将其设置为 `false`。[`skipDangerousModePermissionPrompt` 参考](/docs/zh-CN/settings-reference#skipdangerousmodepermissionprompt)列出了您或您的组织可以设置它的其他设置文件。
* **如果您拒绝**：Claude Code 退出。

在[非交互模式](/docs/zh-CN/headless)中不显示对话框，使用 `--bg` 启动的[后台会话](/docs/zh-CN/agent-view)会被拒绝，直到您在交互式会话中接受对话框。

在 Linux 和 macOS 上，当以 root 身份或在 `sudo` 下运行时，Claude Code 拒绝以此模式启动：

```text theme={null}
--dangerously-skip-permissions cannot be used with root/sudo privileges for security reasons
```

在识别的沙箱内自动跳过检查。要在容器中自主运行，请使用[开发容器](/docs/zh-CN/devcontainer)配置，该配置以非 root 用户身份运行 Claude Code。

[云端会话](/docs/zh-CN/claude-code-on-the-web)不遵守来自您的设置文件的 `defaultMode: "bypassPermissions"` 或 `"dontAsk"`，因此仓库中签入的设置无法以绕过权限模式启动云端会话。该设置会被静默忽略，会话改为以模式下拉菜单中显示的权限模式启动。有关云端会话提供哪些模式，请参阅[切换权限模式](#switch-permission-modes)。

<Warning>
  `bypassPermissions` 不提供针对提示词注入或意外操作的保护。对于权限提示少得多的后台安全检查，请改用[自动模式](#eliminate-prompts-with-auto-mode)。管理员可以通过在[托管设置](/docs/zh-CN/managed-settings)中将 `permissions.disableBypassPermissionsMode` 设置为 `"disable"` 来阻止此模式。
</Warning>

<h2 id="protected-paths">
  受保护的路径
</h2>

对一小组路径的写入永远不会自动批准，唯一的例外是 `bypassPermissions` 模式，以及可使用[绕过权限](#skip-all-checks-with-bypasspermissions-mode)的 plan 模式交互式终端会话。这可以防止意外损坏存储库状态和 Claude 自己的配置。

| 模式 | 受保护路径写入 |
| :- | :- |
| `default`、`acceptEdits` | 提示 |
| `plan` | 在[绕过权限](#skip-all-checks-with-bypasspermissions-mode)可用的交互式终端会话中允许。否则，当[自动模式](#eliminate-prompts-with-auto-mode)在规划期间可用时路由到分类器，当它不可用时提示 |
| `auto` | 路由到分类器 |
| `dontAsk` | 拒绝 |
| `bypassPermissions` | 允许 |

在使用 [`--restricted`](/docs/zh-CN/cli-reference#cli-flags) 启动的会话中，需要 Claude Code v2.1.248 或更高版本，分类器无法批准受保护路径的写入。

在将受保护路径写入路由到分类器的模式中，当 Claude 请求的路径本身不受保护时，[符号链接检查](/docs/zh-CN/permissions#symlinks)解析为受保护路径的写入会提示你。

设置文件中的 [`permissions.allow`](/docs/zh-CN/permissions#manage-permissions) 规则不会预先批准受保护路径的写入。安全检查在 Claude Code 评估设置中的允许规则之前运行，因此 `~/.claude/settings.json` 或 `.claude/settings.json` 中的条目（如 `Edit(.claude/**)`）不会改变上表中的每个模式结果。在提示的模式中，对项目的 `.claude/` 文件夹或 `~/.claude/` 的写入提示可以提供以下这些会话范围的选项之一：

* 对于项目的 `.claude/` 文件夹：**是的，允许 Claude 在此会话中编辑此项目的 .claude 文件夹中的文件**
* 对于 `~/.claude/`：**是的，允许 Claude 在此会话中编辑其 \~/.claude 文件夹中的文件**

受保护的目录：

* `.git`
* `.config/git`
* `.vscode`
* `.idea`
* `.husky`
* `.cargo`
* `.devcontainer`
* `.yarn`
* `.mvn`
* `.claude`，但有少数例外，例如：
  * Claude 自己位于 `.claude/worktrees/` 下的 git worktree
  * 当前会话自己的计划文件，位于 `~/.claude/plans/` 或您设置的 [`plansDirectory`](/docs/zh-CN/settings-reference#plansdirectory) 中
  * [后台会话](/docs/zh-CN/agent-view#where-state-is-stored)自己位于 `~/.claude/jobs/<id>/tmp/` 的临时目录
  * 在未使用 `--restricted` 启动的会话中，项目[自动记忆](/docs/zh-CN/memory#storage-location)目录（例如 `~/.claude/projects/<project>/memory/`）中的 markdown 文件
  * 在未使用 `--restricted` 启动的会话中，[子代理记忆](/docs/zh-CN/sub-agents#enable-persistent-memory)目录（例如 `.claude/agent-memory/`）中的 markdown 文件
* 使用 [`--plugin-dir`](/docs/zh-CN/plugins/mods/create#change-a-mod-with-claude) 加载的目录，因为当文件发生更改时，Claude Code 会从该目录重新加载并运行 mod 的代码

受保护的文件：

* `.gitconfig`、`.gitmodules`
* `.bashrc`、`.bash_profile`、`.bash_login`、`.bash_aliases`、`.bash_logout`、`.zshrc`、`.zprofile`、`.zshenv`、`.zlogin`、`.zlogout`、`.profile`、`.envrc`
* `.npmrc`、`.yarnrc`、`.yarnrc.yml`、`.pnp.cjs`、`.pnp.loader.mjs`、`.pnpmfile.cjs`、`bunfig.toml`、`.bunfig.toml`
* `.bazelrc`、`.bazelversion`、`.bazeliskrc`
* `.pre-commit-config.yaml`、`lefthook.yml`、`lefthook.yaml`、`.lefthook.yml`、`.lefthook.yaml`
* `gradle-wrapper.properties`、`maven-wrapper.properties`
* `.devcontainer.json`
* `.ripgreprc`、`pyrightconfig.json`
* `.mcp.json`、`.claude.json`

<h2 id="critical-paths">
  关键路径
</h2>

关键路径是 Claude Code 保护的目录，防止 `rm` 和 `rmdir` 命令，例如文件系统根目录、您的主目录和您的工作目录。

Claude Code 永远不会让 [`permissions.allow`](/docs/zh-CN/permissions#manage-permissions) 规则或返回 `"allow"` 的 [`PreToolUse` hook](/docs/zh-CN/permissions#extend-permissions-with-hooks) 批准针对关键路径的 `rm` 或 `rmdir` 命令，即使在跳过其他提示的模式下。此断路器防止模型错误。匹配的拒绝规则仍然完全阻止命令。

会发生什么取决于您的权限模式（[见下文](#critical-path-removals-in-each-permission-mode)）。`Remove-Item` 和 `cmd` 移除内置命令有自己的检查，详见 [PowerShell 中的 Remove-Item](#remove-item-in-powershell)。

<h3 id="which-paths-are-critical">
  哪些路径是关键路径
</h3>

Claude Code 将 `rm` 或 `rmdir` 目标视为关键路径，当它是以下任何一个时：

* 文件系统根目录
* 顶级目录，意味着根目录的任何直接子目录，如 `/usr`、`/etc` 或 `/data`
* 您的主目录
* Windows 驱动器根目录及其顶级目录，如 `C:\` 和 `C:\Windows`
* 您的工作目录及其父目录
* 您的额外工作目录及其父目录，但仅当移除是其下的 glob 时，如 `rm -rf <dir>/*`。`rm -rf <dir>` 在目录本身上不会触发此检查

<h3 id="other-targets-that-count-as-critical-paths">
  计为关键路径的其他目标
</h3>

Claude Code 也将以下 `rm` 和 `rmdir` 目标视为关键路径。最后一列说明每个目标为什么计为关键路径。

| 目标 | 示例 | 为什么计为关键路径 |
| :- | :- | :- |
| shell 变量下的 glob 或尾部斜杠 | `rm -rf "$DIR"/*` | 当变量为空时，命令变成从文件系统根目录的移除 |
| 位置参数下的相同形式，如 `$1` 或 `$@`，当命令中没有任何内容给它赋值时 | `rm -rf "$1"/*` | 命令扩展为从根目录的移除 |
| shell 变量后跟一个常见的顶级目录名称，如 `mnt`、`tmp`、`usr` 或 `Users` | `rm -rf "$TMPDIR/mnt"` | 当变量扩展为空时，命令移除 `/mnt` |
| 变量由同一命令从目录打印替换分配，如 `$(pwd)` 或 `$(git rev-parse --show-toplevel)` | `D=$(pwd); rm -rf "$D"` | 该值可以命名您的工作目录或存储库根目录 |
| 仅命令替换的输出的目标，当 `rm` 是递归的时 | `rm -rf "$(pwd)"` | Claude Code 无法在命令运行前检查目标 |
| 关键路径后的尾部命令替换 | `rm -rf ~/$(cmd)` | Claude Code 检查如果替换扩展为空将保留的路径，此处为您的主目录 |
| 仅反斜杠的目标 | `rm -rf "\\"` | Windows 上的 Git Bash 将单个反斜杠读取为当前驱动器的根目录，因此检查适用于每个平台 |
| 部分以 `/*` 或 `/*/` 结尾的目标 | `rm -rf logs/*/*`、`rm -rf logs/*/`、`cd logs && rm -rf a/*` | Claude Code 无法在命令运行前判断它们会涉及哪些目录 |

要关闭仅命令替换输出的目标上的检查，请在启动 Claude Code 的环境中设置 [`CLAUDE_CODE_DISABLE_SUBSTITUTION_RM_PROMPT=1`](/docs/zh-CN/env-vars#variables)。

<h3 id="removals-inside-nested-commands-and-inline-scripts">
  嵌套命令和内联脚本中的移除
</h3>

Claude Code 也查看这些构造内部：

* **嵌套命令**：带有 `(...)` 的子 shell、带有 `{ ...; }` 的大括号组、带有 `$(...)` 或反引号的命令替换，或带有 `<(...)` 的进程替换。Claude Code 找到关键路径移除，无论它位于嵌套形式内部（如 `(rm -rf ~)` 或 `echo "$(rm -rf ~)"`），还是位于同一命令中的其他地方。
* **内联脚本**：通过 `-c` 传递给 `sh`、`bash`、`zsh` 或类似 POSIX shell 的脚本，如 `bash -c 'rm -rf ~'`。
  * 当脚本是双引号时，调用 shell 在内部 shell 接收脚本之前扩展其变量。在 `find . -name '*.tmp' -exec sh -c "rm -rf \"$1\"/*" _ {} \;` 中，命令对每个匹配扩展为从文件系统根目录的移除，Claude Code 将其视为关键路径移除。
  * 绑定 `$1` 到真实值的单引号脚本（如 `sh -c 'rm -rf "$1"/*' _ {}` 所做的）不被标记。

要关闭对直接写在 `-c` 脚本中的关键路径（如 `~`）的检查，请在启动 Claude Code 的环境中设置 [`CLAUDE_CODE_DISABLE_INLINE_SHELL_RM_PROMPT=1`](/docs/zh-CN/env-vars#variables)。

<h3 id="rewrite-a-flagged-command">
  重写被标记的命令
</h3>

如何重写命令以通过检查取决于它使用的[其他目标](#other-targets-that-count-as-critical-paths)：

* **变量下的 glob 或尾部斜杠，如 `$DIR`**：保护每个扩展，以便当变量未设置或为空时 shell 停止出错，如 `rm -rf "${DIR:?}"/*`，或使用文字路径。其扩展都以这种方式保护的移除通过此检查，因此在 `bypassPermissions` 模式下它运行而不提示，除非另一个[关键路径](#critical-paths)检查标记它。
* **通常设置的变量下的 glob 或尾部斜杠，如 `$HOME`**：使用文字路径。
* **从目录打印替换分配的变量**：使用文字路径。`"${D:?}"` 保护不会清除此检查，因为变量不为空。
* **仅命令替换输出的目标**：首先自己运行替换，然后移除它打印的文字路径。提示告诉 Claude 做同样的事情。

对于变量下的 glob 或尾部斜杠，提示命名被标记的 `rm` 并说明如何重写它以便检查通过。

<h3 id="critical-path-removals-in-each-permission-mode">
  每个权限模式中的关键路径移除
</h3>

Claude Code 对关键路径移除的处理取决于您的权限模式：

| 模式 | 结果 |
| :- | :- |
| `default`、`acceptEdits` | 要求您批准它 |
| `plan` | 要求您批准它。当[分类器在规划期间审查命令](#analyze-before-you-edit-with-plan-mode)且没有可用的绕过权限时，按 `auto` 模式处理 |
| `auto` | 在终端中要求您批准它，有[时间限制](#time-limits-and-denials-in-auto-and-bypasspermissions-modes)。在其他地方，拒绝它 |
| `dontAsk` | 拒绝它 |
| `bypassPermissions` | 要求您批准它，在终端中有时间限制 |

如果显式[询问规则](/docs/zh-CN/permissions#manage-permissions)与命令匹配，Claude Code 即使在 `auto` 模式下也会询问您，且没有时间限制。在询问的模式中，[`PermissionRequest` hook](/docs/zh-CN/hooks#permissionrequest) 可以回答提示。

<h3 id="time-limits-and-denials-in-auto-and-bypasspermissions-modes">
  auto 和 bypassPermissions 模式中的时间限制和拒绝
</h3>

在 `auto` 和 `bypassPermissions` 模式下，关键路径移除的终端提示显示两分钟倒计时：

* 如果倒计时在您回答之前用完，Claude Code 拒绝命令并告诉 Claude 改为做什么，以便无人值守的会话继续工作。
* 在提示打开时按任何键停止倒计时并保持提示等待您的回答。
* 在一个会话中这样的提示运行完三次后无人回答，Claude Code 停止显示它们并立即拒绝进一步的关键路径移除。发送新消息会重新开始计数。

在 `auto` 模式下，无论 Claude Code 无法向您显示终端提示的地方，它都立即拒绝命令，例如在[非交互式运行](/docs/zh-CN/headless)中使用 `-p`、在 [Agent SDK](/docs/zh-CN/agent-sdk/permissions) 会话中，以及在 VS Code 扩展的聊天面板和桌面应用中。拒绝告诉 Claude 报告它想删除的内容并将移除留给您。

`auto` 和 `bypassPermissions` 处理需要 Claude Code v2.1.281 或更高版本。要关闭它，请在启动 Claude Code 的环境中设置 [`CLAUDE_CODE_DISABLE_DANGEROUS_RM_TIMEOUT=1`](/docs/zh-CN/env-vars#variables)。在 `auto` 模式下，关键路径移除随后转到分类器，在 `bypassPermissions` 模式下提示没有时间限制。

<h3 id="remove-item-in-powershell">
  PowerShell 中的 Remove-Item
</h3>

当您启用 [PowerShell 工具](/docs/zh-CN/tools-reference#powershell-tool)时，Claude Code 给 `Remove-Item` 和 `cmd` 内置命令 `rd`、`rmdir`、`del` 和 `erase` 自己的检查，与 `rm` 关键路径列表分开。对于 `Remove-Item`，结果取决于目标，第一个匹配的情况适用：

* **系统路径**：文件系统根目录及其顶级目录、驱动器根目录及其顶级目录和您的主目录。Claude Code 在每种模式下拒绝命令，不询问您。
* **通配符**：裸 `*` 或任何以 `/*` 或 `\*` 结尾的目标，包括 shell 变量下的 glob，如 `$dir/*`。Claude Code 在每种模式下拒绝命令，不询问您，在[分类器](#eliminate-prompts-with-auto-mode)看到它之前。
* **您的工作目录或其父目录之一，带有 `-Recurse`**：Claude Code 将命令视为任何其他需要在您的权限模式下批准的命令，因此它在询问的模式下询问您，在 `auto` 模式下将其发送到分类器，在 `dontAsk` 模式下拒绝它。`bypassPermissions` 模式跳过此检查。

系统路径情况也适用于 `rd`、`rmdir`、`del` 和 `erase`，当 Claude 通过 `cmd` 运行它们时，如 `cmd /c rd /s /q C:\Users`。默认情况下，Claude Code 在每种模式下拒绝此类命令，不询问您。此 `cmd` 检查需要 Claude Code v2.1.283 或更高版本。

在判断 `cmd` 目标时，Claude Code 将跟随文字文本的 PowerShell 变量视为空。这使得 `cmd /c rd /s /q "C:\$name"` 成为 `C:\` 的移除，因此它也被拒绝。尾部通配符计为它清空的文件夹，因此 `cmd /c del /q C:\*` 被拒绝，而您项目中的 `cmd /c del /q dist\*` 不被拒绝。

要关闭 `cmd` 检查，请在启动 Claude Code 的环境中设置 [`CLAUDE_CODE_DISABLE_POWERSHELL_CMD_RM_DENY=1`](/docs/zh-CN/env-vars#variables)。Claude Code 在设置文件的 `env` 块中忽略此变量。系统路径上的 `Remove-Item` 无论如何都保持被拒绝。

<h2 id="see-also">
  另请参阅
</h2>

* [权限](/docs/zh-CN/permissions)：允许、询问和拒绝规则；托管策略
* [配置自动模式](/docs/zh-CN/auto-mode-config)：告诉分类器您的组织信任哪些基础设施
* [Hooks](/docs/zh-CN/hooks)：通过 `PreToolUse` 和 `PermissionRequest` hooks 的自定义权限逻辑
* [安全](/docs/zh-CN/security)：保障措施和最佳实践
* [沙箱](/docs/zh-CN/sandboxing)：Bash 命令的文件系统和网络隔离
* [非交互模式](/docs/zh-CN/headless)：使用 `-p` 标志运行 Claude Code
