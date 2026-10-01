> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# CLI 参考

> Claude Code 命令行界面的完整参考，包括命令和标志。

<h2 id="cli-commands">
  CLI 命令
</h2>

您可以使用这些命令启动会话、管道内容、恢复对话和管理更新：

| 命令 | 描述 | 示例 |
| :- | :- | :- |
| `claude` | 启动交互式会话 | `claude` |
| `claude "query"` | 使用初始提示启动交互式会话 | `claude "explain this project"` |
| `claude -p "query"` | 通过 SDK 查询，然后退出 | `claude -p "explain this function"` |
| `cat file \| claude -p "query"` | 处理管道内容 | `cat logs.txt \| claude -p "explain"` |
| `claude -c` | 在当前目录中继续最近的对话 | `claude -c` |
| `claude -c -p "query"` | 通过 SDK 继续 | `claude -c -p "Check for type errors"` |
| `claude -r "<session>" "query"` | 按 ID 或名称恢复会话 | `claude -r "auth-refactor" "Finish this PR"` |
| `claude update` | 更新到最新版本 | `claude update` |
| `claude gateway` | 启动自托管 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 服务器，供在 Amazon Bedrock、Google Cloud 的 Agent Platform 或 Microsoft Foundry 上部署 SSO 和策略在 Claude Code 前面的管理员使用。需要 `--config` 指向 [`gateway.yaml`](/docs/zh-CN/claude-apps-gateway-config)。 | `claude gateway --config gateway.yaml` |
| `claude install [version]` | 安装或重新安装本机二进制文件。接受版本号如 `2.1.118`、`stable` 或 `latest`。请参阅 [安装特定版本](/docs/zh-CN/setup#install-a-specific-version) | `claude install stable` |
| `claude auth login` | 登录您的 Anthropic 账户。使用 `--email` 预填充您的电子邮件地址，使用 `--sso` 强制 SSO 身份验证，使用 `--console` 使用 Anthropic Console 登录以进行 API 使用计费而不是 Claude 订阅 | `claude auth login --console` |
| `claude auth logout` | 从您的 Anthropic 账户登出 | `claude auth logout` |
| `claude auth status` | 以 JSON 格式显示身份验证状态。使用 `--text` 获取人类可读的输出。如果已登录，则以代码 0 退出，如果未登录，则以代码 1 退出。JSON 包含一个 `configDirectory` 字段，命名 CLI 使用的 [配置目录](/docs/zh-CN/claude-directory)。该字段需要 Claude Code v2.1.268 或更高版本 | `claude auth status` |
| `claude agents` | 打开 [agent view](/docs/zh-CN/agent-view) 以监控和分派并行后台会话。使用 `--cwd <path>` 仅显示在该目录下启动的会话，或使用 `--json` 将实时会话打印为 JSON 数组以供脚本使用（`--json --all` 也包括已完成的后台会话）。传递 `--permission-mode`、`--model`、`--effort` 或 `--agent` 以设置 [分派会话的默认值](/docs/zh-CN/agent-view#permission-mode-model-and-effort)。接受 `--settings`、`--add-dir`、`--plugin-dir` 和 `--mcp-config`，如顶级 `claude` 命令。打开 agent view 需要交互式终端 | `claude agents --json` |
| `claude attach <id>` | 在此终端中附加到 [后台会话](/docs/zh-CN/agent-view#manage-sessions-from-the-shell) | `claude attach 7c5dcf5d` |
| `claude auto-mode defaults` | 以 JSON 格式打印内置 [auto mode](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode) 分类器规则。使用 `claude auto-mode config` 查看应用了设置的有效配置。`--label <prefix>` 仅打印标签以该前缀开头的规则，不区分大小写匹配。需要 Claude Code v2.1.208 或更高版本 | `claude auto-mode defaults --label 'Git Destructive'` |
| `claude auto-mode reset` | 通过从用户设置文件中删除 `autoMode` 部分来恢复默认 [auto mode](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode) 配置。在写入前提示确认；传递 `-y`/`--yes` 以跳过提示。来自 [managed settings](/docs/zh-CN/server-managed-settings) 或 `--settings` 标志的规则仍然适用。需要 Claude Code v2.1.212 或更高版本。请参阅 [检查默认值和您的有效配置](/docs/zh-CN/auto-mode-config#inspect-the-defaults-and-your-effective-config) | `claude auto-mode reset --yes` |
| `claude daemon status` | 打印后台会话 [supervisor](/docs/zh-CN/agent-view#the-supervisor-process) 的状态、版本、套接字目录和工作进程数以进行诊断。如果 supervisor 未运行，则退出代码 1 | `claude daemon status` |
| `claude daemon stop --any` | 停止后台会话 [supervisor](/docs/zh-CN/agent-view#the-supervisor-process) 及其托管的会话。传递 `--keep-workers` 以保持后台会话运行，以便下一个 supervisor 重新连接到它们。`--any` 确认停止按需 supervisor，这是默认值。使用此命令从 [无响应的 supervisor](/docs/zh-CN/agent-view#agent-view-says-the-background-service-did-not-respond) 恢复 | `claude daemon stop --any --keep-workers` |
| `claude doctor` | 从终端打印只读安装和设置诊断，无需启动会话，包括安装健康状况、设置文件验证错误和远程控制资格。对于可以应用修复的会话内设置检查，请运行 [`/doctor`](/docs/zh-CN/commands#all-commands) | `claude doctor` |
| `claude import [source]` | 启动交互式会话，运行 [`/import`](/docs/zh-CN/commands#all-commands) 以将来自其他编码代理的配置引入 Claude Code。接受与命令相同的 `--dry-run` 和 `--yes` 选项。在 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry 或 AWS 上的 Claude Platform 上不可用。当您关闭 [feature-flag fetching](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching) 时也不可用。需要 Claude Code v2.1.213 或更高版本 | `claude import codex --dry-run` |
| `claude logs <id>` | 从 [后台会话](/docs/zh-CN/agent-view#manage-sessions-from-the-shell) 打印最近的输出 | `claude logs 7c5dcf5d` |
| `claude mcp` | 配置 Model Context Protocol (MCP) 服务器 | 请参阅 [Claude Code MCP 文档](/docs/zh-CN/mcp)。 |
| `claude mcp login <name>` | 运行配置的 MCP 服务器的 OAuth 流程而不打开交互式 `/mcp` 面板。适用于 HTTP、SSE 和 claude.ai 连接器服务器。在 SSH 上添加 `--no-browser` 以打印授权 URL 而不是打开浏览器，然后在提示处粘贴重定向 URL。请参阅 [从命令行进行身份验证](/docs/zh-CN/mcp#authenticate-from-the-command-line) | `claude mcp login sentry` |
| `claude mcp logout <name>` | 清除 MCP 服务器的存储 OAuth 凭据 | `claude mcp logout sentry` |
| `claude plugin` | 管理 Claude Code [plugins](/docs/zh-CN/plugins/overview)。别名：`claude plugins`。请参阅 [plugin 参考](/docs/zh-CN/plugins/cli-reference#claude-plugin-commands) 了解子命令 | `claude plugin install code-review@claude-plugins-official` |
| `claude project purge [path]` | 删除项目的所有本地 Claude Code 状态：记录、任务列表、调试日志、文件编辑历史、提示历史行和项目在 `~/.claude.json` 中的条目。省略 `[path]` 以从交互式列表中选择。标志：`--dry-run` 预览，`-y`/`--yes` 跳过确认，`-i`/`--interactive` 确认每一项，`--all` 用于每个项目。请参阅 [清除本地数据](/docs/zh-CN/claude-directory#clear-local-data) | `claude project purge ~/work/repo --dry-run` |
| `claude remote-control` | 启动 [Remote Control](/docs/zh-CN/remote-control) 服务器以从 Claude.ai 或 Claude 应用控制 Claude Code。在服务器模式下运行（无本地交互式会话）。请参阅 [服务器模式标志](/docs/zh-CN/remote-control#start-a-remote-control-session)。停止服务器后，您可以恢复它正在服务的会话。请参阅 [停止服务器后恢复会话](/docs/zh-CN/remote-control#resume-sessions-after-stopping-the-server) | `claude remote-control --name "My Project"` |
| `claude respawn <id>` | 重启 [后台会话](/docs/zh-CN/agent-view#manage-sessions-from-the-shell)，运行或已停止，保持其对话完整。使用 `--all` 重启每个运行中的会话，例如以获取更新的 Claude Code 二进制文件 | `claude respawn 7c5dcf5d` |
| `claude rm <id>` | 从列表中删除 [后台会话](/docs/zh-CN/agent-view#manage-sessions-from-the-shell)。当删除被 [拒绝超过会话的 worktree](/docs/zh-CN/agent-view#what-deleting-a-session-removes) 且第二个 `claude rm` 可以解决它时，拒绝会打印要传递的确切标志和值：`--discard-unpushed <commit>@<worktree-id>` 丢弃具有未推送提交的 worktree 及其提交，`--force-remove-worktree <worktree-id>` 删除 git 或 `WorktreeRemove` 钩子无法删除的 worktree 目录。`--discard-unpushed` 需要 Claude Code v2.1.260 或更高版本，而 `--force-remove-worktree` 需要 v2.1.268 或更高版本。对话记录保留在您的本地计算机上，可通过 `claude --resume` 访问 | `claude rm 7c5dcf5d` |
| `claude self-hosted-runner` | 启动运行程序进程，将此计算机或容器注册到 [self-hosted environment](/docs/zh-CN/self-hosted-environments)，并在您的基础设施上托管 Claude Code 云会话。运行 `claude self-hosted-runner setup` 以获得引导式操作员演练，运行 `claude self-hosted-runner doctor` 以 [诊断已部署的运行程序](/docs/zh-CN/self-hosted-environments-deploy#troubleshooting)，运行 `claude self-hosted-runner orchestrator` 以生成 [on-demand runners](/docs/zh-CN/self-hosted-environments-configuration#on-demand-runners)。需要 Claude Code v2.1.224 或更高版本 | `claude self-hosted-runner setup` |
| `claude setup-token` | 为 CI 和脚本生成长期 OAuth 令牌。将令牌打印到终端而不保存。需要 Claude 订阅。请参阅 [生成长期令牌](/docs/zh-CN/authentication#generate-a-long-lived-token) | `claude setup-token` |
| `claude stop <id>` | 停止 [后台会话](/docs/zh-CN/agent-view#manage-sessions-from-the-shell)。也接受 `claude kill` | `claude stop 7c5dcf5d` |
| `claude ultrareview [target]` | 非交互式运行 [ultrareview](/docs/zh-CN/ultrareview#run-ultrareview-non-interactively)。将发现结果打印到标准输出，成功时退出代码 0，失败时退出代码 1。使用 `--json` 获取原始有效负载，使用 `--timeout <minutes>` 覆盖 45 分钟的默认值。在 `github.com` pull request 目标上使用 `--post` 以将完成的发现结果作为来自您的 GitHub 账户的一条纯文本评论发布到 PR。`--no-post` 是默认值。`--post` 和 `--no-post` 需要 Claude Code v2.1.227 或更高版本。请参阅 [将发现结果发布到 pull request](/docs/zh-CN/ultrareview#post-findings-to-the-pull-request) | `claude ultrareview 1234 --json` |

如果您输入错误的子命令，Claude Code 会建议最接近的匹配项并退出而不启动会话。例如，`claude udpate` 会打印 `Did you mean claude update?`。

从 v2.1.199 开始，`claude --dangerously-skip-permissions daemon <subcommand>` 运行 `daemon` 子命令。早期版本将 `daemon <subcommand>` 视为新交互式会话的提示，因此当标志在前面时子命令永远不会运行，这是 `claude` 别名为包含该标志时的常见设置。只有前导 `--dangerously-skip-permissions` 或 `--allow-dangerously-skip-permissions` 以这种方式路由到 `daemon`；任何其他前导标志仍然启动交互式会话。

<h2 id="cli-flags">
  CLI 标志
</h2>

使用这些命令行标志自定义 Claude Code 的行为。`claude --help` 不会列出每个标志，因此标志在 `--help` 中不出现并不意味着它不可用。

| 标志 | 描述 | 示例 |
| :- | :- | :- |
| `--add-dir` | 添加额外的工作目录供 Claude 读取和编辑文件。授予文件访问权限；Claude Code [不会发现](/docs/zh-CN/permissions#additional-directories-grant-file-access-not-configuration)这些目录中的大多数 `.claude/` 配置。验证每个路径是否作为目录存在。您不能添加大多数[网络路径](/docs/zh-CN/errors#working-directory-is-a-network-path)，例如 `\\server\share`。要在会话之间保持这些目录，请在设置中设置 [`permissions.additionalDirectories`](/docs/zh-CN/settings-reference#permissions-additionaldirectories) | `claude --add-dir ../apps ../lib` |
| `--advisor <model>` | 使用模型别名 `fable`、`opus` 或 `sonnet`，或完整模型 ID 为此会话启用服务器端[顾问工具](/docs/zh-CN/advisor)。优先于会话的 `advisorModel` 设置。`fable` 需要[Fable 访问权限](/docs/zh-CN/advisor#choose-an-advisor-model) | `claude --advisor opus` |
| `--agent` | 为当前会话指定代理（覆盖 `agent` 设置） | `claude --agent my-custom-agent` |
| `--agents` | 通过 JSON 动态定义自定义子代理。接受[为 CLI 定义的子代理列出的字段](/docs/zh-CN/sub-agents#choose-the-subagent-scope)。使用 `--print` 时，该值可以是包含该对象的 JSON 文件的路径；文件形式需要 Claude Code v2.1.281 或更高版本。Claude Code 在启动时验证该值并在值无效时退出；有关消息以及跳过验证的标志和环境变量，请参阅 [`Invalid --agents configuration`](/docs/zh-CN/errors#invalid-agents-configuration)。验证需要 Claude Code v2.1.242 或更高版本 | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |
| `--allow-dangerously-skip-permissions` | 将 `bypassPermissions` 添加到 `Shift+Tab` 模式循环中而不启动它。让您可以从不同的模式（如 `plan`）开始，稍后切换到 `bypassPermissions`。请参阅[权限模式](/docs/zh-CN/permission-modes#skip-all-checks-with-bypasspermissions-mode) | `claude --permission-mode plan --allow-dangerously-skip-permissions` |
| `--allowedTools`, `--allowed-tools` | 无需提示权限即可执行的工具。有关模式匹配，请参阅[权限规则语法](/docs/zh-CN/settings-reference#permission-rule-syntax)。要限制哪些工具可用，请改用 `--tools`。如果您在此处命名[任务跟踪工具](/docs/zh-CN/tools-reference#task-tool-availability)之一，Claude Code 也会选择加入会话 | `"Bash(git log *)" "Bash(git diff *)" "Read"` |
| `--append-subagent-system-prompt` | 将自定义文本附加到每个[子代理](/docs/zh-CN/sub-agents)的系统提示末尾，包括嵌套子代理，除了[分叉的子代理](/docs/zh-CN/sub-agents#fork-the-current-conversation)，它重用对话自己的提示。仅在使用 `-p` 的非交互模式下应用。需要 Claude Code v2.1.205 或更高版本 | `claude -p --append-subagent-system-prompt "Cite file paths in every answer" "query"` |
| `--append-subagent-system-prompt-file` | 从文件加载文本并将其附加到[子代理](/docs/zh-CN/sub-agents)系统提示。`--append-subagent-system-prompt` 的替代方案，用于命令行上传递的文本过长。这两个标志不能组合。仅在使用 `-p` 的非交互模式下应用。需要 Claude Code v2.1.261 或更高版本 | `claude -p --append-subagent-system-prompt-file ./subagent-rules.txt "query"` |
| `--append-system-prompt` | 将自定义文本附加到默认系统提示的末尾 | `claude --append-system-prompt "Always use TypeScript"` |
| `--append-system-prompt-file` | 从文件加载额外的系统提示文本并附加到默认提示 | `claude --append-system-prompt-file ./extra-rules.txt` |
| `--autocompact <auto\|tokens>` | 为此会话设置[自动压缩窗口](/docs/zh-CN/model-config#set-the-auto-compact-window)而不更改您保存的设置。接受与 `/autocompact` 相同的值；该部分涵盖值形式以及什么覆盖标志。需要 Claude Code v2.1.221 或更高版本 | `claude --autocompact 500k` |
| `--ax-screen-reader` | 呈现屏幕阅读器友好的输出：没有装饰性边框或动画的平面文本。强制使用经典渲染器，因此 [`tui`](/docs/zh-CN/settings-reference#tui) 设置无效；附加的[后台会话](/docs/zh-CN/agent-view)仍然全屏呈现。优先于 [`CLAUDE_AX_SCREEN_READER`](/docs/zh-CN/env-vars) 和 [`axScreenReader`](/docs/zh-CN/settings-reference#axscreenreader) 设置。需要 Claude Code v2.1.181 或更高版本 | `claude --ax-screen-reader` |
| `--bare` | 最小模式：跳过 hooks、skills、自定义命令、子代理、plugins、MCP 服务器、自动内存和 CLAUDE.md 的自动发现，以便脚本化调用启动更快。使用 `--add-dir` 传递的目录中的 Skills 仍然加载。Claude 可以访问 Bash、文件读取和文件编辑工具。设置 [`CLAUDE_CODE_SIMPLE`](/docs/zh-CN/env-vars)。请参阅[裸模式](/docs/zh-CN/headless#start-faster-with-bare-mode) | `claude --bare -p "query"` |
| `--betas` | 要包含在 API 请求中的 Beta 标头（仅限 API 密钥用户） | `claude --betas interleaved-thinking` |
| `--bg`, `--background` | 将会话作为[后台代理](/docs/zh-CN/agent-view)启动并立即返回。打印会话 ID 和管理命令。与 `--exec` 结合以将 shell 命令作为后台作业运行，而不是启动 Claude 会话，或与 `--agent` 结合以运行特定的子代理。检查[工作区信任](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)以在启动前检查目录。不能与 `-p`/`--print` 结合；请参阅[错误参考](/docs/zh-CN/errors#command-line-errors) | `claude --bg "investigate the flaky test"` |
| `--channels` | （研究预览）Claude 应在此会话中侦听其[频道](/docs/zh-CN/channels)通知的 MCP 服务器。空格分隔的 `plugin:<name>@<marketplace>` 条目列表。需要通过 claude.ai 或 Console API 密钥进行 Anthropic 身份验证 | `claude --channels plugin:my-notifier@my-marketplace` |
| `--chrome` | 启用[Chrome 浏览器集成](/docs/zh-CN/chrome)以进行网络自动化和测试 | `claude --chrome` |
| `--cloud` | 使用任务描述创建新的[云会话](/docs/zh-CN/claude-code-on-the-web)。使用会话 ID（`session_...` 或 `cse_...`）或 claude.ai/code URL，使用 `-p` 将消息排队到该现有会话。请参阅[发送后续消息](/docs/zh-CN/claude-code-on-the-web#send-follow-ups-from-the-cli)。 | `claude --cloud "Fix the login bug"` |
| `--continue`, `-c` | 加载当前目录中最近的对话，包括[已完成的后台会话](/docs/zh-CN/sessions#resume-a-session)；打开已完成的后台会话需要 Claude Code v2.1.257 或更高版本。跳过使用 `claude -p` 或 Agent SDK 创建的会话，以及第一个提示为 `/loop` 的会话。`claude -p --continue` 包括 `-p`、SDK 和 `/loop` 会话。包括使用 `/add-dir` 添加此目录的会话 | `claude --continue` |
| `--dangerously-load-development-channels` | 启用不在批准的允许列表上的[频道](/docs/zh-CN/channels-reference#test-during-the-research-preview)，用于本地开发。接受 `plugin:<name>@<marketplace>` 和 `server:<name>` 条目。提示确认 | `claude --dangerously-load-development-channels server:webhook` |
| `--dangerously-skip-permissions` | 跳过权限提示。等同于 `--permission-mode bypassPermissions`。请参阅[权限模式](/docs/zh-CN/permission-modes#skip-all-checks-with-bypasspermissions-mode)了解此操作跳过和不跳过的内容。对于使用 `--bg` 启动的会话，当主管重新启动会话时，该模式[持续存在](/docs/zh-CN/agent-view#permission-mode-model-and-effort) | `claude --dangerously-skip-permissions` |
| `--debug` | 启用调试模式，可选类别过滤，例如 `--debug='mcp,startup'` 或 `--debug='!1p'`。过滤器仅在 `=` 形式中绑定；空格分隔的过滤器启用调试模式而不进行过滤 | `claude --debug='mcp,startup'` |
| `--debug-file <path>` | 将调试日志写入特定文件路径。隐式启用调试模式。优先于 `CLAUDE_CODE_DEBUG_LOGS_DIR` | `claude --debug-file /tmp/claude-debug.log` |
| `--desktop` | 在当前目录上打开 [Claude Desktop 应用](/docs/zh-CN/desktop)并退出而不在终端中启动会话。添加 `--continue` 或 `--resume` 与会话 ID 以[在 Desktop 中打开该会话](/docs/zh-CN/desktop#coming-from-the-cli)。`--resume` 这里仅接受会话 ID，不接受名称或记录文件路径。不接受提示和除 `--verbose` 和 `--debug` 标志外的其他标志，因为应用自己启动会话。在 macOS 和 x64 Windows 上可用，当您使用 Claude 订阅登录时。需要 Claude Code v2.1.285 或更高版本 | `claude --desktop` |
| `--disable-slash-commands` | 为此会话禁用所有 skills 和命令 | `claude --disable-slash-commands` |
| `--disallowedTools`, `--disallowed-tools` | 拒绝规则。裸工具名称从 Claude 的上下文中删除匹配的工具：`"Edit"` 删除 Edit，`"*"` 删除每个工具，`"mcp__*"` 删除每个 MCP 工具。作用域规则（如 `Bash(rm *)`）使工具保持可用，仅拒绝[如所写](/docs/zh-CN/permissions#bash-rule-limits)匹配的调用。命名 [`EndConversation`](/docs/zh-CN/tools-reference#endconversation-tool-behavior) 的规则在任何其他工具保持时无法删除它 | `"Bash(git log *)" "Bash(git diff *)" "Edit"` |
| `--effort` | 为当前会话设置[努力级别](/docs/zh-CN/model-config#adjust-effort-level)。选项：`low`、`medium`、`high`、`xhigh`、`max` 或 `ultracode`。可用级别取决于模型。`ultracode` 请求 `xhigh` 努力，[ultracode](/docs/zh-CN/workflows#let-claude-decide-with-ultracode) 打开，需要 Claude Code v2.1.203 或更高版本。覆盖此会话的 [`modelSettings`](/docs/zh-CN/settings-reference#modelsettings) 和 [`effortLevel`](/docs/zh-CN/settings-reference#effortlevel) 设置，不持续 | `claude --effort high` |
| `--enable-auto-mode` | 在 v2.1.111 中删除。自动模式现在默认在 `Shift+Tab` 循环中；使用 `--permission-mode auto` 在其中启动 | `claude --permission-mode auto` |
| `--environment <environment-id>` | 创建在具有给定 ID 的[自托管环境](/docs/zh-CN/self-hosted-environments)上运行的新云会话。环境 ID 以 `ccpool_` 开头。有关调度行为和它拒绝的标志组合，请参阅 [`--environment` 调度行为](/docs/zh-CN/self-hosted-environments-testing#environment-dispatch-behavior)。需要 Claude Code v2.1.224 或更高版本 | `claude -p "Fix the login bug" --environment ccpool_abc123` |
| `--exclude-dynamic-system-prompt-sections` | 将每用户上下文（如自动内存位置）从系统提示移到第一条用户消息中。改进跨不同用户和运行相同任务的机器的提示缓存重用。仅适用于默认系统提示；当设置 `--system-prompt` 或 `--system-prompt-file` 时忽略。与 `-p` 一起用于脚本化的多用户工作负载 | `claude -p --exclude-dynamic-system-prompt-sections "query"` |
| `--exec` | 运行 shell 命令作为 PTY 支持的后台作业，而不是启动 Claude 会话。与 `--bg` 一起使用以从 shell 启动 | `claude --bg --exec 'pytest -x'` |
| `--fallback-model` | 启用当主模型过载或不可用时自动回退到指定的模型，例如已停用的模型。接受按顺序尝试的逗号分隔列表。请参阅[回退模型链](/docs/zh-CN/model-config#fallback-model-chains)。要在会话之间保持链，请使用此标志覆盖的 [`fallbackModel` 设置](/docs/zh-CN/settings-reference#fallbackmodel) | `claude --fallback-model sonnet,haiku` |
| `--fork-session` | 恢复时，创建新的会话 ID 而不是重用原始 ID（与 `--resume` 或 `--continue` 一起使用） | `claude --resume abc123 --fork-session` |
| `--forward-subagent-text` | 在输出流中发出[子代理](/docs/zh-CN/sub-agents)文本和思考块作为 `assistant` 和 `user` 消息，设置 `parent_tool_use_id`，以便您可以重建每个子代理的记录。没有此标志，Claude Code 会省略在[前台](/docs/zh-CN/sub-agents#run-subagents-in-foreground-or-background)运行的子代理的文本和思考块。需要 `--print` 和 `--output-format stream-json`。Claude Code 也转发来自[嵌套子代理](/docs/zh-CN/sub-agents#let-subagents-spawn-their-own-subagents)的消息，将 `parent_tool_use_id` 设置为生成每个子代理的 Agent 或 Skill 工具调用的 ID；这需要 Claude Code v2.1.219 或更高版本，分叉 skill 生成的子代理的消息以及嵌套分叉 skills 的消息需要 v2.1.275 或更高版本。[`CLAUDE_CODE_FORWARD_SUBAGENT_TEXT`](/docs/zh-CN/env-vars) 环境变量启用相同的行为。需要 Claude Code v2.1.211 或更高版本 | `claude -p --output-format stream-json --verbose --forward-subagent-text "query"` |
| `--from-pr` | 打开会话选择器，过滤到链接到特定拉取请求的会话。接受 PR 编号、GitHub 或 GitHub Enterprise PR URL、GitLab 合并请求 URL 或 Bitbucket 拉取请求 URL。当 Claude 创建拉取请求时，会话会自动链接 | `claude --from-pr 123` |
| `--ide` | 如果恰好有一个有效的 IDE 可用，在启动时自动连接到 IDE | `claude --ide` |
| `--init` | 在会话之前使用 `init` 匹配器运行[Setup hooks](/docs/zh-CN/hooks#setup)（仅打印模式） | `claude -p --init "query"` |
| `--init-only` | 运行[Setup](/docs/zh-CN/hooks#setup) 和 `SessionStart` hooks，然后退出而不启动对话 | `claude --init-only` |
| `--include-hook-events` | 在输出流中包含 hook 生命周期事件。`SessionStart` 和 `Setup` hook 事件始终包含，不需要此标志。某些 hook 事件（如 `Notification`、`SessionEnd`、`PreCompact` 和 `PostCompact`）永远不会产生 `hook_started` 事件，即使使用此标志也是如此。对于这些事件，Claude Code 仍然在命令 hook 运行超过一秒时发出 `hook_progress` 并输出，并仅在[在后台运行的 hook](/docs/zh-CN/hooks#run-hooks-in-the-background) 完成时发出 `hook_response`。需要 `--output-format stream-json` | `claude -p --output-format stream-json --verbose --include-hook-events "query"` |
| `--include-partial-messages` | 在输出中包含部分流事件。需要 `--print` 和 `--output-format stream-json` | `claude -p --output-format stream-json --verbose --include-partial-messages "query"` |
| `--input-format` | 为打印模式指定输入格式（选项：`text`、`stream-json`） | `claude -p --output-format json --input-format stream-json` |
| `--json-schema` | 在代理完成其工作流后获得与 JSON Schema 匹配的验证 JSON 输出（仅打印模式）。请参阅[结构化输出](/docs/zh-CN/agent-sdk/structured-outputs)。Claude Code 在无效架构上以错误退出，并接受 `format` 关键字作为注释而不进行客户端验证 | `claude -p --json-schema '{"type":"object","properties":{...}}' "query"` |
| `--maintenance` | 在会话之前使用 `maintenance` 匹配器运行[Setup hooks](/docs/zh-CN/hooks#setup)（仅打印模式） | `claude -p --maintenance "query"` |
| `--max-budget-usd` | 在停止之前在 API 调用上花费的最大美元金额（仅打印模式）。来自[子代理](/docs/zh-CN/sub-agents)的支出计入上限。当您使用 `--continue` 或 `--resume` 返回对话时，[从早期运行恢复的](/docs/zh-CN/agent-sdk/cost-tracking#accumulate-costs-across-multiple-calls)总数不计入它。一旦支出达到上限，生成另一个子代理失败，出现 `Budget limit reached`，Claude Code 停止仍在运行的后台子代理；上限执行行为需要 Claude Code v2.1.217 或更高版本 | `claude -p --max-budget-usd 5.00 "query"` |
| `--max-turns` | 限制代理转数（仅打印模式）。达到限制时以错误退出。默认无限制。使用 `--input-format stream-json` 时，当限制结束转时仍排队的消息保持排队并以其自己的限制启动新转 | `claude -p --max-turns 3 "query"` |
| `--mcp-config` | 从 JSON 文件或字符串加载 MCP 服务器（空格分隔）。当您使用 `-p` 传递此标志时，Claude Code 在运行第一个转之前等待仍待处理的服务器连接，最多 [`MCP_TIMEOUT`](/docs/zh-CN/env-vars) 启动超时，默认 30 秒；具有[缓存工具列表](/docs/zh-CN/mcp#managing-your-servers)的服务器跳过等待并在首次使用时连接。等待需要 Claude Code v2.1.221 或更高版本 | `claude --mcp-config ./mcp.json` |
| `--model` | 使用[模型别名](/docs/zh-CN/model-config#model-aliases)（如 `sonnet`、`opus`、`haiku` 或 `fable`）或模型的完整名称为当前会话设置模型。覆盖 [`model`](/docs/zh-CN/settings-reference#model) 设置和 [`ANTHROPIC_MODEL`](/docs/zh-CN/model-config#environment-variables) | `claude --model claude-sonnet-5` |
| `--name`, `-n` | 为会话设置显示名称，显示在 `/resume` 和终端标题中。您可以使用 `claude --resume <name>` 恢复命名会话。在交互式会话中，如果此机器上的另一个实时会话已使用该名称，Claude Code 会应用[其变体](/docs/zh-CN/sessions#name-your-sessions)。<br /><br />[`/rename`](/docs/zh-CN/commands) 在会话中期更改名称，也在提示栏上显示它 | `claude -n "my-feature-work"` |
| `--no-chrome` | 为此会话禁用[Chrome 浏览器集成](/docs/zh-CN/chrome) | `claude --no-chrome` |
| `--no-session-persistence` | 禁用会话持久性，以便会话不保存到磁盘且无法恢复。仅打印模式。[`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](/docs/zh-CN/env-vars) 环境变量在任何模式下执行相同操作 | `claude -p --no-session-persistence "query"` |
| `--output-format` | 为打印模式指定输出格式（选项：`text`、`json`、`stream-json`） | `claude -p "query" --output-format json` |
| `--permission-mode` | 在指定的[权限模式](/docs/zh-CN/permission-modes)中开始。接受 `default`、`acceptEdits`、`plan`、`auto`、`dontAsk`、`bypassPermissions` 或 `manual` 作为 `default` 的别名。`manual` 别名选择 UI 标记为 Manual 的权限模式，需要 Claude Code v2.1.200 或更高版本；`claude --help` 列出它代替 `default`，两个值都有效。覆盖设置文件中的 `defaultMode`。没有此标志或 `--dangerously-skip-permissions`，新会话在[会话启动的权限模式](/docs/zh-CN/permission-modes#which-mode-a-session-starts-in)中描述的权限模式中启动，这也涵盖 `-p` 运行启动的内容 | `claude --permission-mode plan` |
| `--permission-prompt-tool` | 指定 MCP 工具以在非交互模式下处理权限提示。Claude Code 在运行第一个转之前等待该工具的 MCP 服务器连接，最多 [`MCP_TIMEOUT`](/docs/zh-CN/env-vars) 启动超时，默认 30 秒。<br /><br />提示工具无法批准标记为[需要用户交互](/docs/zh-CN/mcp#require-approval-for-a-specific-tool)的 MCP 工具：Claude Code 将其 `allow` 结果转换为拒绝。此限制需要 Claude Code v2.1.199 或更高版本 | `claude -p --permission-prompt-tool mcp_auth_tool "query"` |
| `--permission-prompts` | 在打印模式下设置谁回答权限提示。使用默认 `host`，Claude Code 将它们发送到 Agent SDK 主机或 `--permission-prompt-tool` 工具。当没有人可以回答时传递 `none`，Claude Code 改为拒绝它们。请参阅[在无人值守运行中关闭权限提示](/docs/zh-CN/headless#turn-off-permission-prompts-in-unattended-runs)。需要 Claude Code v2.1.259 或更高版本 | `claude -p --permission-prompts none "query"` |
| `--plugin-dir` | 从目录或 `.zip` 存档加载 plugin，或从[plugins 文件夹](/docs/zh-CN/plugins/create#load-a-directory-or-archive-for-one-session)加载多个，仅用于此会话。每个标志采用一个路径。重复标志以获取更多路径：`--plugin-dir A --plugin-dir B.zip`。传递 plugins 文件夹需要 Claude Code v2.1.265 或更高版本 | `claude --plugin-dir ./my-plugin` |
| `--plugin-url` | 从 URL 获取 plugin `.zip` 存档，仅用于此会话。重复标志以获取多个 plugins，或在单个引用值中传递空格分隔的 URL | `claude --plugin-url https://example.com/plugin.zip` |
| `--print`, `-p` | 打印响应而不进行交互模式（有关编程使用详情，请参阅 [Agent SDK 文档](/docs/zh-CN/agent-sdk/overview)）。对于在仍在运行的后台会话上 `--resume`，请参阅[恢复会话](/docs/zh-CN/sessions#resume-a-running-background-session) | `claude -p "query"` |
| `--prompt-suggestions` | 在生成提示建议的每个转之后发出 `prompt_suggestion` 消息，其中包含预测的下一个用户提示；非常短的对话可能不会产生任何。需要 `--print`、`--output-format stream-json` 和 `--verbose`。请参阅[提示建议](/docs/zh-CN/interactive-mode#prompt-suggestions) | `claude -p --prompt-suggestions --output-format stream-json --verbose "query"` |
| `--ref <branch>` | 使用 `--environment`，基于命名的 ref 而不是本地 `HEAD` 的新会话检出 | `claude -p "Run the smoke test" --environment ccpool_abc123 --ref main` |
| `--remote` | `--cloud` 的已弃用别名，包括现有会话形式 | `claude --remote "Fix the login bug"` |
| `--remote-control`, `--rc` | 启动启用[远程控制](/docs/zh-CN/remote-control#start-a-remote-control-session)的交互式会话，以便您也可以从 claude.ai 或 Claude 应用控制它。可选地为会话传递名称 | `claude --remote-control "My Project"` |
| `--remote-control-session-name-prefix <prefix>` | 当未设置显式名称时，[远程控制](/docs/zh-CN/remote-control)自动生成会话名称的前缀。默认为您的机器主机名，生成名称如 `myhost-graceful-unicorn`。设置 `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX` 以获得相同效果 | `claude remote-control --remote-control-session-name-prefix dev-box` |
| `--replay-user-messages` | 从 stdin 重新发出用户消息回到 stdout 以进行确认。需要 `--input-format stream-json` 和 `--output-format stream-json` | `claude -p --input-format stream-json --output-format stream-json --verbose --replay-user-messages` |
| `--restricted` | 在受限模式下启动。当评估工具在共享机器上驱动 `claude` 且 Claude Code 不得运行命令或读取该机器的用户和项目设置时使用。Claude Code 删除运行命令或代码的内置工具和 WebFetch，除非您在 `--tools` 中单独命名它们，而不是通过 `default` 预设。它还将内置文件工具限制在[工作目录](/docs/zh-CN/permissions#working-directories)，仅加载[托管设置](/docs/zh-CN/managed-settings)和 `--settings`，拒绝 [`bypassPermissions`](/docs/zh-CN/permission-modes#skip-all-checks-with-bypasspermissions-mode)，并[拒绝从受限会话创建云会话](/docs/zh-CN/errors#cloud-sessions-cannot-be-created-from-a-restricted-session)。需要 Claude Code v2.1.248 或更高版本 | `claude --restricted -p "query"` |
| `--resume`, `-r` | 按 ID 或名称恢复特定会话，或显示交互式选择器以选择会话。代替 ID，您可以传递会话的 `.jsonl` [记录文件](/docs/zh-CN/sessions#where-transcripts-are-stored)的绝对路径。选择器和名称搜索包括使用 `/add-dir` 添加此目录的会话。当您传递会话 ID 时，Claude Code 搜索当前项目目录及其 git worktrees，然后搜索此机器上的所有其他项目。在 v2.1.223 之前，ID 搜索仅涵盖当前项目目录及其 git worktrees。[后台会话](/docs/zh-CN/agent-view)在选择器中显示，标记为 `bg`。恢复仍在运行的[打开该会话](/docs/zh-CN/sessions#resume-a-running-background-session)在此终端中通过 `claude attach`，您在命令行上传递的提示作为其下一个转进行。在 v2.1.285 之前，Claude Code 拒绝并打印 `claude attach` 命令以改为运行 | `claude --resume auth-refactor` |
| `--safe-mode` | 禁用所有自定义以排除故障的损坏配置：CLAUDE.md、skills、plugins、hooks、MCP 服务器、自定义命令和代理、输出样式、工作流、自定义主题、自定义快捷键、状态行和文件建议命令、LSP 服务器和自动内存不加载。身份验证、模型选择、内置工具和权限正常工作，这与 [`--bare`](/docs/zh-CN/headless#start-faster-with-bare-mode) 不同。托管设置策略仍然适用，包括策略配置的 hooks、状态行和文件建议命令；托管 plugins、托管 skills、托管 CLAUDE.md 和策略配置的 MCP 服务器不适用。用于检查自定义是否触发[自动模型回退](/docs/zh-CN/model-config#automatic-model-fallback)。设置 [`CLAUDE_CODE_SAFE_MODE`](/docs/zh-CN/env-vars) | `claude --safe-mode` |
| `--session-id` | 为对话使用特定的会话 ID（必须是有效的 UUID） | `claude --session-id "550e8400-e29b-41d4-a716-446655440000"` |
| `--setting-sources` | 要加载的设置源的逗号分隔列表（`user`、`project`、`local`）。请参阅[代理视图](/docs/zh-CN/agent-view#what-carries-over-when-you-background)和[代理团队](/docs/zh-CN/agent-teams#context-and-communication)以了解从此会话启动的会话继承列表 | `claude --setting-sources user,project` |
| `--settings` | 设置 JSON 文件的路径或内联 JSON 字符串。您在此处设置的值覆盖此会话的 `settings.json` 文件中的相同键。您省略的键保持其基于文件的值。文件必须是不超过 2 MiB 的常规文件。请参阅[设置优先级](/docs/zh-CN/settings#settings-precedence) | `claude --settings ./settings.json` |
| `--strict-mcp-config` | 仅使用 `--mcp-config` 中的 MCP 服务器，忽略所有其他 MCP 配置。有关标志在托管 MCP 文件下执行的操作，请参阅[使用 managed-mcp.json 的独占控制](/docs/zh-CN/managed-mcp#exclusive-control-with-managed-mcp-json) | `claude --strict-mcp-config --mcp-config ./mcp.json` |
| `--system-prompt` | 用自定义文本替换整个系统提示 | `claude --system-prompt "You are a Python expert"` |
| `--system-prompt-file` | 从文件加载系统提示，替换默认提示 | `claude --system-prompt-file ./custom-prompt.txt` |
| `--system-prompt-snapshot` | 传递 `off` 以在每个请求上重建系统提示，而不是重用在对话的第一个请求上[记录的提示](#system-prompt-flags-in-resumed-conversations)，例如在跨 `--continue` 运行迭代其措辞时。需要 Claude Code v2.1.257 或更高版本 | `claude --system-prompt-snapshot off` |
| `--teleport` | 在本地终端中恢复[云会话](/docs/zh-CN/claude-code-on-the-web) | `claude --teleport` |
| `--teammate-mode` | 设置[代理团队](/docs/zh-CN/agent-teams)队友的显示方式：`in-process`（默认）、`auto`、`tmux` 或 `iterm2`。覆盖此会话的 [`teammateMode`](/docs/zh-CN/settings-reference#teammatemode) 设置。请参阅[选择显示模式](/docs/zh-CN/agent-teams#choose-a-display-mode) | `claude --teammate-mode auto` |
| `--tmux` | 为 worktree 创建 tmux 会话。需要 `--worktree`。在可用时使用 iTerm2 本机窗格；传递 `--tmux=classic` 以获得传统 tmux | `claude -w feature-auth --tmux` |
| `--tools` | 限制 Claude 可以使用的内置工具。使用 `""` 禁用所有，`"default"` 用于默认集，或工具名称如 `"Bash,Edit,Read"`。在 macOS、Linux 和 WSL 上，默认集省略 `Glob` 和 `Grep`，如[Glob 工具行为](/docs/zh-CN/tools-reference#glob-tool-behavior)下所述。如果您在此处命名[任务跟踪工具](/docs/zh-CN/tools-reference#task-tool-availability)之一，Claude Code 也会选择加入。标志不影响 MCP 工具；要拒绝这些工具，请使用 `--disallowedTools "mcp__*"`。省略 [`EndConversation`](/docs/zh-CN/tools-reference#endconversation-tool-behavior) 的列表不会删除它；`""` 仅在没有 MCP 工具保持时删除它 | `claude --tools "Bash,Edit,Read"` |
| `--verbose` | 启用详细日志记录，显示完整的逐个转输出。覆盖此会话的 [`viewMode`](/docs/zh-CN/settings-reference#viewmode) 设置 | `claude --verbose` |
| `--version`, `-v` | 输出版本号 | `claude -v` |
| `--worktree`, `-w` | 在隔离的 [git worktree](/docs/zh-CN/worktrees) 中启动 Claude，位于 `<repo>/.claude/worktrees/<name>`。如果您不提供名称，Claude Code 会生成一个。传递 `#<number>`、GitHub 拉取请求 URL 或 GitLab 合并请求 URL 以[从 `origin` 获取该 PR 或 MR 并从其分支 worktree](/docs/zh-CN/worktrees#branch-from-a-pull-request)。从 GitLab 合并请求分支需要 Claude Code v2.1.233 或更高版本 | `claude -w feature-auth` |

<h3 id="system-prompt-flags">
  系统提示标志
</h3>

Claude Code 提供五个标志用于自定义系统提示。四个设置其文本，使用 `--system-prompt-snapshot` 您可以控制对话是否保持它启动时的文本。所有五个都在交互和非交互模式中工作。

| 标志 | 行为 | 示例 |
| :- | :- | :- |
| `--system-prompt` | 替换整个默认提示 | `claude --system-prompt "You are a Python expert"` |
| `--system-prompt-file` | 用文件内容替换 | `claude --system-prompt-file ./prompts/review.txt` |
| `--append-system-prompt` | 附加到默认提示 | `claude --append-system-prompt "Always use TypeScript"` |
| `--append-system-prompt-file` | 将文件内容附加到默认提示 | `claude --append-system-prompt-file ./style-rules.txt` |
| `--system-prompt-snapshot` | 使用 `off`，在每个请求上重建提示。使用 `on`（默认），重用[记录应用的](#system-prompt-flags-in-resumed-conversations)记录的提示 | `claude --append-system-prompt "Draft rules" --system-prompt-snapshot off` |

`--system-prompt` 和 `--system-prompt-file` 互斥。附加标志可以与任一替换标志组合。

当替换文本将每次运行相同的指令与每次运行变化的上下文结合时，添加仅包含 `__SYSTEM_PROMPT_DYNAMIC_BOUNDARY__` 的行在指令和上下文之间。Claude Code 在第一个这样的行处分割提示并删除该行，因此上面的部分保持缓存而下面的部分变化。需要 Claude Code v2.1.275 或更高版本。[缓存自定义提示的静态部分](/docs/zh-CN/agent-sdk/modifying-system-prompts#cache-the-static-part-of-a-custom-prompt)列出应用分割的配置。

根据 Claude Code 的默认身份是否仍适合您的任务进行选择。当 Claude 应保持编码助手同时遵循您的额外规则时使用附加标志：每次调用指令、输出格式或 `-p` 脚本的域上下文。附加保留默认工具指导、安全指令和编码约定，因此您只需提供不同的内容。当表面、身份或权限模型与 Claude Code 的不同时使用替换标志，例如管道中没有人监视的非编码代理。替换删除整个默认提示，包括工具指导和安全指令，因此您对任务仍然需要的任何内容负责。

对于您可以在项目之间切换和共享的持久角色，请使用[输出样式](/docs/zh-CN/output-styles)。对于 Claude 应始终遵循的项目约定，请使用 [CLAUDE.md](/docs/zh-CN/memory)。[Agent SDK 关于系统提示的指南](/docs/zh-CN/agent-sdk/modifying-system-prompts#decide-on-a-starting-point)更深入地涵盖了相同的决定。

<h4 id="system-prompt-flags-in-resumed-conversations">
  恢复对话中的系统提示标志
</h4>

默认情况下，Claude Code 在对话的第一个请求上构建系统提示一次，应用任何系统提示标志中的文本，并在会话中记录它。在对话被压缩之前，每个后续请求都使用该记录的提示，包括在您使用 `--resume` 或 `--continue` 返回对话后。如果您在该后续启动时传递不同的系统提示标志文本或无，它在对话被压缩或您启动新对话时生效。

在[云会话](/docs/zh-CN/cloud-environments)之外，如果您通过传递 `--bare` 或设置 `CLAUDE_CODE_SIMPLE=1` 在[裸模式](/docs/zh-CN/headless#start-faster-with-bare-mode)中启动 Claude Code，记录保持关闭，除非您传递 `--system-prompt-snapshot on`。在 v2.1.268 之前，不[获取功能标志](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)的会话，包括 Amazon Bedrock、Google Cloud 的 Agent Platform 和 Microsoft Foundry 上的会话，在每个请求上重建提示，`--system-prompt-snapshot` 无效。

要在每个请求上重建提示，例如在跨 `--continue` 运行迭代其措辞时，传递 `--system-prompt-snapshot off`。在 v2.1.265 之前，传递任何系统提示标志也关闭记录，除非您传递 `--system-prompt-snapshot on`。

<h2 id="see-also">
  另请参阅
</h2>

* [Chrome 扩展](/docs/zh-CN/chrome) - 浏览器自动化和网络测试
* [交互模式](/docs/zh-CN/interactive-mode) - 快捷键、输入模式和交互功能
* [快速入门指南](/docs/zh-CN/quickstart) - Claude Code 入门
* [常见工作流](/docs/zh-CN/common-workflows) - 高级工作流和模式
* [设置](/docs/zh-CN/settings) - 配置选项
* [Agent SDK 文档](/docs/zh-CN/agent-sdk/overview) - 编程使用和集成
