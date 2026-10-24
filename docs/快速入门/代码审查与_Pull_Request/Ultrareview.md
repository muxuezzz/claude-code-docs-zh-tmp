> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用 Ultrareview 查找错误

> 使用 /code-review ultra 在云中运行深度多代理代码审查，在合并前查找和验证错误。

> [!NOTE]
>
> Ultrareview 是一个研究预览功能。该功能、定价和可用性可能会根据反馈而改变。该命令是 `/code-review ultra`。当 ultrareview 对您的账户可用时，`/ultrareview` 是一个别名。

Ultrareview 是在 Anthropic 基础设施上运行的[云会话](https://code.claude.com/docs/zh-CN/claude-code-on-the-web.md)中进行的深度代码审查。当您运行 `/code-review ultra` 时，Claude Code 在云沙箱中启动一队审查代理来查找您的分支或拉取请求中的错误。

与本地 `/code-review` 相比，ultrareview 提供：

* **更高的信号质量**：每个报告的发现都经过独立复现和验证，因此结果专注于真实的错误而不是风格建议
* **更广泛的覆盖范围**：许多审查代理并行探索更改，这会发现本地审查可能遗漏的问题
* **无本地资源使用**：审查完全在云沙箱中运行，因此您的终端在运行时保持空闲，可用于其他工作

Ultrareview 需要使用 claude.ai 账户进行身份验证，因为它在 Anthropic 基础设施上作为云端会话运行。如果您仅使用 API 密钥登录，请先运行 `/login` 并使用 claude.ai 进行身份验证。当使用 Claude Code 与 Amazon Bedrock、Google Cloud 的 Agent Platform 或 Microsoft Foundry 时，Ultrareview 不可用；对于已启用零数据保留或已应用 [HIPAA 配置](https://code.claude.com/docs/zh-CN/hipaa-setup.md)的组织也不可用。在这些情况下，`/code-review ultra` 会改为在您的会话中运行本地审查。使用[客户管理的加密密钥](https://platform.claude.com/docs/en/manage-claude/cmek)（CMEK）的组织无法运行 ultrareview。要在本地审查您的更改，请运行 `/code-review`。

## 从 CLI 运行 ultrareview

从任何 git 存储库启动审查：

```text theme={null}
/code-review ultra
```

不带参数时，ultrareview 审查您当前分支与默认分支之间的 diff，包括未提交和暂存的更改。

对于分支审查，Claude Code 按照[将本地仓库上传到云端会话](https://code.claude.com/docs/zh-CN/claude-code-on-the-web.md#send-local-repositories-without-github)的规则捆绑仓库状态并将其上传到云沙箱，这些规则涵盖了大小限制、检出要求，以及名称类似凭据或密钥的文件（如 `.env` 和 `*.tfvars` 文件）中的未提交更改会如何处理。当您[审查拉取请求](#review-a-pull-request)时，Claude Code 不会从您的计算机上传任何内容。

启动前，Claude Code 显示一个确认对话框，其中包含审查范围、您剩余的免费运行次数和估计成本；对于分支审查，范围包括文件和行数。确认后，审查在后台继续进行，您可以继续使用您的会话。

该命令仅在您使用 `/code-review ultra` 调用时运行；Claude 不会自动启动 ultrareview。

### 针对不同的基础进行审查

要与默认分支以外的基础进行比较，请传递分支名称。此示例针对 `develop` 而不是默认分支审查您的当前分支：

```text theme={null}
/code-review ultra develop
```

基础分支不需要存在于您的本地克隆中；Claude Code 从 `origin` 获取它。如果名称有拼写错误，Claude Code 会在错误中建议最接近的分支名称。

提交 id 或标签也可以作为基础，审查将涵盖您的分支自该提交以来的更改。

### 审查拉取请求

要审查 `github.com` 上的拉取请求而不是本地分支，请传递 PR 编号：

```text theme={null}
/code-review ultra 1234
```

该命令也接受 `#1234`、`PR 1234` 和粘贴的 PR URL；粘贴的 URL 必须指向您当前目录中的存储库。

PR 模式需要 `github.com` 上的仓库。对于 [GitHub Enterprise Server](https://code.claude.com/docs/zh-CN/github-enterprise-server.md) 实例上的仓库，请运行不带 PR 编号的 `/code-review ultra` 来审查您的本地分支。

在 PR 模式下，云沙箱从 `github.com` 克隆拉取请求，而不是上传您的工作树。它使用连接到您的 Claude 账户的 GitHub 账户，因此该账户需要对仓库具有读取权限。

运行 [`/web-setup`](https://code.claude.com/docs/zh-CN/web-quickstart#connect-from-your-terminal) 将您的 GitHub CLI 登录连接到您的 Claude 账户。

### 将发现发布到拉取请求

在 Claude Code v2.1.227 或更高版本上，当您在 `github.com` 上审查拉取请求时，您可以让 Claude 将完成的发现作为来自您自己 GitHub 账户的单个纯文本评论发布到 PR。该评论不是审查或批准，并以"由 Claude Code 生成"的说明结尾。当您审查分支时，Claude Code 仅在您的会话中显示发现。

Claude Code 永远不会发布，除非您在该运行中选择，`--no-post` 是默认值。发布是您为每次运行做出的选择：

* **交互式**：在启动对话框中，选择**运行并将发现作为我发布到 PR**。如果您将 `--post` 添加到命令中，如 `/code-review ultra 1234 --post`，Claude Code 会预选该选择，但仍会在启动前询问。
* **非交互式**：使用 `--post` 运行 [`claude ultrareview` 子命令](#run-ultrareview-non-interactively)。通过使用该标志运行子命令，您同意发布，因此 Claude Code 会发布而不询问。在 `claude -p '/code-review ultra'` 运行中，Claude Code 在发现到达前退出，因此不会发布任何内容；改用子命令。

Claude Code 不会从您的计算机发布。它将审查的会话 ID 发送到 Anthropic API，该 API 通过您连接到 Claude 的 GitHub 账户将审查的存储发现作为评论发布。发布需要与审查本身相同的 claude.ai 登录，并且在第三方提供商上或当您设置 [`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`](https://code.claude.com/docs/zh-CN/env-vars) 时不可用。

在交互式会话中，Claude Code 在发现到达时启动发布，因此请保持会话打开直到审查完成。Claude Code 仅在该会话中保留发布选择。如果会话在审查完成前结束，Claude Code 不会发布任何内容，即使您稍后恢复对话。

当发布完成时，Claude 会告诉您结果：

* **已发布**：Claude 为您提供评论的链接。
* **已发布**：同一审查的早期发布已将评论放在 PR 上，因此 Claude 会链接您到拉取请求，而不是再次发布。
* **失败**：Claude 会告诉您原因，发现会保留在您的终端中，以便您可以手动发布。

### 用纯文本传递请求

在 Claude Code v2.1.218 或更高版本上，您也可以用纯文本描述您正在处理的内容：

```text theme={null}
/code-review ultra check my auth changes
```

审查仍然涵盖您的当前分支，与不带参数运行的范围相同。Claude 将您的文本保留为一个说明，显示在启动对话框中，并在发现到达时将其与发现相关联。

当 Claude Code 的文本超过一个单词且不是分支名称或 PR 引用时，它将您的文本视为说明。它将单个单词读取为分支名称或 PR 引用，因此拼写错误的分支名称会从[针对不同的基础进行审查](#review-against-a-different-base)获得最接近分支的错误，而不是使用说明启动。如果您的文本将 PR 引用与其他单词结合，如 `check PR 123 again`，Claude Code 也不会启动；它会要求您重新运行仅使用 PR 编号来审查该 PR，或不使用引用来审查您的当前分支。

> [!TIP]
>
> 如果您的仓库太大而无法捆绑，Claude Code 会提示您改用 PR 模式。对于 `github.com` 上的仓库，推送您的分支并打开草稿 PR，然后运行 `/code-review ultra <PR-number>`。

### 差异限制和回退

Ultrareview 在任何审查工作运行之前检查差异，并在无法按原样审查时告诉您：

* **差异过大**：分支审查默认最多可包括 500 个更改的文件和 8,000 个更改的行。确切的值可能会改变，[拒绝](https://code.claude.com/docs/zh-CN/errors.md#diff-is-too-large-for-ultrareview)会说明生效的值、您的差异大小以及更改行数最多的文件。Claude Code 以相同的方式拒绝过大的拉取请求，说明其文件和行数，但不说明每个文件的细分
* **没有要审查的内容**：当针对基础的差异为空时，ultrareview 拒绝并说明它比较的分支或提交以及您所处的情况，例如在基础分支本身上且没有未提交的内容，或一个分支的所有提交都已是基础的一部分。它还为该情况建议解决方法，例如切换到您的工作分支、暂存或提交本地编辑，或传递不同的基础
* **首次提交**：存储库的首次提交没有更早的内容可比较，因此 ultrareview 在您在启动对话框中确认后审查其中的每个文件。如果您有未跟踪的文件，它会拒绝并告诉您 `git add` 您想审查的文件。相同的大小限制适用。

  首次提交仅在该确认后才被整体审查，因此 `claude ultrareview` 子命令和 `claude -p` 拒绝它并指向您使用交互式会话。需要 Claude Code v2.1.277 或更高版本
* **没有合并基础**：当您的分支与基础分支没有共享历史时，或存储库没有基础分支可比较时，ultrareview 审查存储库中的每个跟踪文件。回退需要完整克隆并应用相同的大小限制。它仅在您在启动对话框中确认或自己运行 `claude ultrareview` 子命令时启动。在 `claude -p` 和任何其他两者都不发生的地方，ultrareview 拒绝，说审查将涵盖每个文件，并指向您使用交互式会话。

  在没有分支或其他引用的检出上，例如通过在获取 URL 后检出 `FETCH_HEAD` 创建的分离 HEAD，Claude Code [拒绝审查](https://code.claude.com/docs/zh-CN/errors.md#your-checkout-has-no-branches)并建议首先创建分支

## 定价和免费运行

Ultrareview 是一项高级功能，按额外使用量而不是您计划的包含使用量计费。

| 计划 | 包含的免费运行 | 免费运行后 |
| - | - | - |
| Pro | 3 次免费运行 | 按 [额外使用量](https://support.claude.com/zh-CN/articles/12429409-extra-usage-for-paid-claude-plans) 计费 |
| Max | 3 次免费运行 | 按 [额外使用量](https://support.claude.com/zh-CN/articles/12429409-extra-usage-for-paid-claude-plans) 计费 |

* **免费运行**：Pro 和 Max 的三次运行是每个账户的一次性分配，不会刷新。
* **每次审查的成本**：使用完免费运行后，通常花费 \$5 到 \$25 的使用额度，具体取决于更改的大小，与启动对话框在每次运行前显示的估计相匹配。
* **何时计数一次运行**：一旦云会话启动。您提前停止或未能完成的审查仍然会使用一次免费运行；付费审查仅对运行的部分计费。

由于 ultrareview 在免费运行之外始终按使用额度计费，您的账户或组织必须在启动付费审查之前启用使用额度。如果未启用使用额度，Claude Code 会阻止启动。如果您可以管理您账户的计费，Claude Code 会将您链接到计费设置，您可以在那里启用使用额度。

您也可以运行 `/usage-credits` 来检查或更改您的使用额度设置。

Claude Code 在每次对话中要求您确认一次使用额度计费：例如，当您使用 `/clear` 启动新对话时，Claude Code 会在下一次付费审查时再次显示确认。

## 跟踪正在运行的审查

审查通常需要 15 到 25 分钟。审查作为后台任务运行，因此您可以继续在会话中工作或启动其他命令。如果您选择了[将发现发布到拉取请求](#post-findings-to-the-pull-request)，请保持会话打开直到审查完成；如果会话先结束，Claude Code 将不会发布任何内容。

使用 `/tasks` 查看正在运行和已完成的审查、打开审查的详细视图或停止正在进行的审查。如果您停止审查，Claude Code 会存档云会话，不会返回部分发现。

Claude 还可以告诉您审查已停止或其会话未找到：

* 如果审查的云会话在审查完成前在 claude.ai 上停止或[存档](https://code.claude.com/docs/zh-CN/claude-code-on-the-web.md#archive-sessions)，Claude 会告诉您它已停止。
* 如果审查的云会话被删除，或者您自启动它以来已登录到不同的 Claude 账户或组织，Claude 会告诉您会话未找到。
* 如果您切换了账户，审查可能仍会在启动它的账户下完成。如果审查仍在运行，请以该账户重新登录，并使用 `claude --resume` 恢复对话以重新附加它。

审查完成后，Claude Code 会在您的会话中将验证的发现显示为通知。每个发现都包括文件位置和问题的解释，因此您可以要求 Claude 直接修复它。

## 以非交互方式运行 ultrareview

使用 `claude ultrareview` 子命令，可以在 CI 或脚本中启动 ultrareview，而无需交互式会话。该子命令启动的审查与 `/code-review ultra` 相同，会一直阻塞到远程审查完成，然后将发现的问题输出到 stdout。如果运行时以 `Error: Workspace not trusted` 退出，请参阅[在审查运行前信任文件夹](#trust-the-folder-before-the-review-runs)。

```bash theme={null}
claude ultrareview
claude ultrareview 1234
claude ultrareview origin/main
```

不带参数时，该子命令会审查当前分支与默认分支之间的 diff；当不存在合并基准时，会执行与 `/code-review ultra` 相同的[回退到整个仓库审查](#diff-limits-and-fallbacks)。传入 PR 编号可[审查 `github.com` 上的 Pull Request](#review-a-pull-request)，传入基准分支则以该分支为基准进行审查；[基准分支的处理方式](#review-against-a-different-base)与交互式命令一致。

当您运行该子命令时，即表示您同意回退到审查整个仓库，并同意计费和条款确认提示，因此运行过程中不会停下来请求您确认。由您亲自运行即视为同意。如果改由 Claude 代您运行该子命令（例如通过 Bash 工具），Claude Code 会拒绝执行整个仓库的审查。

`claude -p '/code-review ultra'` 无法获取发现的问题，因此请在脚本中使用 `claude ultrareview`。`-p` 运行会启动云端审查，但不等待其完成就退出。如果该审查会消耗使用额度，`-p` 运行会停止且不启动审查。在 v2.1.218 之前，非交互式会话中的 `/code-review ultra` 会运行本地审查。

| 标志 | 描述 |
| - | - |
| `--json` | 输出原始的 `bugs.json` 负载，而不是格式化后的发现结果 |
| `--timeout <minutes>` | 等待审查完成的最长分钟数。默认为 45 |
| `--post` | 以您的 GitHub 账户身份，将完成的发现结果作为一条纯文本评论[发布到 Pull Request](#post-findings-to-the-pull-request)。适用于 `github.com` 上的 Pull Request 目标；对于其他目标，Claude Code 会忽略该标志并给出提示。需要 Claude Code v2.1.227 或更高版本 |
| `--no-post` | 不发布发现结果。这是默认行为；如果同时传入两个标志，Claude Code 不会发布。需要 Claude Code v2.1.227 或更高版本 |
| `--trust-workspace` | 仅在本次运行中[信任当前文件夹](#trust-the-folder-before-the-review-runs)，且不进行询问，以便脚本或 CI 作业可以审查您尚未信任的检出目录。该标志不接受值：请将 PR 编号或基准分支放在它之前。需要 Claude Code v2.1.309 或更高版本 |

`claude ultrareview` 会将进度消息写入 stderr，以便 stdout 保持可解析。

运行 `claude ultrareview` 所需的身份验证和使用额度配置与 `/code-review ultra` 相同。

该子命令会以以下三种退出码之一退出：

* **0**：审查已完成，无论是否有发现结果
* **1**：审查启动失败或在完成前被停止、云端会话出错，或已超时。当[文件夹未被信任](#trust-the-folder-before-the-review-runs)时，退出码也为 1，包括您在信任询问处回答 `n` 或按下 Ctrl-C 的情况。
* **130**：您在该子命令启动审查、等待发现结果或发送 `--post` 评论期间按下了 Ctrl-C，而不是在信任询问处按下

如果子命令在发现结果返回之前退出，这些结果将永远不会到达您的终端。审查可能仍在云端运行。再次运行该子命令会启动一次新的审查，而不是恢复之前那次，并且新的审查会[使用一次免费运行或按使用额度计费](#pricing-and-free-runs)。

使用 `--post` 时，子命令会在输出发现结果后立即开始发布，并将链接输出到 stderr。

* 如果运行失败、被停止或超时，子命令不会发布任何内容。
* 如果审查完成但评论未能发布，Claude Code 会将原因输出到 stderr，发现结果仍保留在 stdout 中，以便您手动发布。

如需对 GitHub Pull Request 进行自动审查，[Code Review](https://code.claude.com/docs/zh-CN/code-review.md) 可直接与您的仓库集成，并以 PR 行内评论的形式发布发现结果，无需 CLI 步骤。

### 在审查运行前信任文件夹

当 `claude ultrareview` 询问 `Trust <folder>? [y/N]` 时，回答 `y` 即可[信任该文件夹](https://code.claude.com/docs/zh-CN/permissions.md#project-allow-rules-and-workspace-trust)。仅当您信任其中的代码时才应信任该文件夹，因为此后 git 和 Claude Code 可能会运行其 git 配置和项目设置中指定的程序。

当它无法询问您时（例如在 CI 作业中，或输出被重定向到文件时），它会以 [`Error: Workspace not trusted`](https://code.claude.com/docs/zh-CN/errors#workspace-not-trusted-when-running-claude-ultrareview) 退出。追加 `--trust-workspace` 即可在该次运行中信任该文件夹：

```bash theme={null}
claude ultrareview 1234 --trust-workspace
```

要审查不受信任的 Pull Request，请在您信任的分支上运行 `claude ultrareview <PR number> --trust-workspace`。与回答 `y` 不同，该标志不会保存任何内容。该 PR 会[在云端克隆](#review-a-pull-request)，因此您无需在本地拥有其分支。

## ultrareview 与 /code-review 的比较

两个审查都检查代码，但您在工作流的不同阶段使用它们。

| | `/code-review` | `/code-review ultra` |
| - | - | - |
| 目标 | 您的工作差异、pull request、分支或路径 | 您的工作差异或 pull request |
| 运行位置 | 在您的会话中本地运行 | 在云沙箱中运行 |
| 深度 | 随着 effort 参数扩展 | 具有独立验证的多代理队列 |
| 持续时间 | 几秒到几分钟 | 大约 15 到 25 分钟 |
| 成本 | 计入正常使用量 | 免费运行，然后大约 \$5 到 \$25 每次审查作为使用额度 |
| 最适合 | 迭代时的快速反馈 | 合并前对重大更改的信心 |

使用 `/code-review` 获得工作时的快速反馈，或传递 PR 编号以在批准前审查团队成员的 pull request。在合并重大更改前使用 `/code-review ultra`，当您想要更深入的审查来捕捉本地审查可能遗漏的问题时。

## 相关资源

* [在云端使用 Claude Code](https://code.claude.com/docs/zh-CN/claude-code-on-the-web.md)：了解云会话和云沙箱如何工作
* [有效管理成本](https://code.claude.com/docs/zh-CN/costs.md)：跟踪使用情况并设置支出限制
