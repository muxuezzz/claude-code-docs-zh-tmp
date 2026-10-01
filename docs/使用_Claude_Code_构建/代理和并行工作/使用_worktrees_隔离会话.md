> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用 worktrees 运行并行会话

> 在单独的 git worktrees 中隔离并行 Claude Code 会话，以便更改不会相互冲突。涵盖 `--worktree` 标志、子代理隔离、`.worktreeinclude`、清理和非 git VCS hooks。

[git worktree](https://git-scm.com/docs/git-worktree) 是一个单独的工作目录，具有自己的文件和分支，但与主检出共享相同的存储库历史和远程。在自己的 worktree 中运行每个 Claude Code 会话意味着一个会话中的编辑永远不会触及另一个会话中的文件，因此一个会话可以构建功能，而第二个会话可以修复错误。

<Note>
  Worktrees 需要 git 存储库；对于其他版本控制系统，请[配置 hooks 来替换 git 逻辑](#non-git-version-control)。在[桌面应用](/docs/zh-CN/desktop#work-in-parallel-with-sessions)中，启动会话时选择 **worktree** 选项，为其提供自己的 worktree。
</Note>

Worktrees 是运行 Claude 并行的几种方式之一。它们隔离文件编辑。[子代理](/docs/zh-CN/sub-agents)在一个会话内分割工作，[跨会话消息传递](/docs/zh-CN/cross-session-messaging)让 Claude 在您的 worktrees 中的会话之间传递发现。请参阅[并行运行代理](/docs/zh-CN/agents)来比较这些方法，或跳到[使用 worktrees 隔离子代理](#isolate-subagents-with-worktrees)以同时使用 worktrees 和子代理。

大多数会话只需要前两个部分：[在 worktree 中启动 Claude](#start-claude-in-a-worktree)，然后[退出时清理](#clean-up-worktrees)。当您需要[恢复会话](#resume-a-worktree-session)、[更改 worktrees 的创建方式](#customize-worktree-creation)或[调试失败](#troubleshooting)时，请返回页面的其余部分。

<h2 id="start-claude-in-a-worktree">
  在 worktree 中启动 Claude
</h2>

使用名称传递 `--worktree` 或 `-w` 来创建隔离的 worktree 并在其中启动 Claude。默认情况下，worktree 在您的存储库根目录下的 `.claude/worktrees/<name>/` 下创建，在名为 `worktree-<name>` 的新分支上：

```bash theme={null}
claude --worktree feature-auth
```

在另一个终端中使用不同的名称再次运行该命令以启动第二个隔离会话。如果您省略名称，Claude 会生成一个名称，例如 `bright-running-fox`。

交互式运行需要[工作区信任](/docs/zh-CN/security)：如果您之前没有在该目录中运行过 Claude，请在那里运行一次 `claude` 来接受信任对话框，否则 `--worktree` 会以错误退出并提示您这样做。使用 `-p` 的非交互式运行会跳过信任检查，因此 `claude -p --worktree` 会在没有信任检查的情况下进行。

<Tip>
  将 `.claude/worktrees/` 添加到您的 `.gitignore`，以便 worktree 内容不会在您的主检出中显示为未跟踪的文件。
</Tip>

<h3 id="set-up-the-worktree-environment">
  设置 worktree 环境
</h3>

Worktree 是一个新的检出，因此请在那里初始化您的开发环境：要求 Claude 安装依赖项，或在 `.claude/worktrees/` 下的 worktree 目录中自己运行您的项目设置。要自动将 gitignored 文件（如 `.env`）携带到每个新 worktree 中，请添加一个[`.worktreeinclude` 文件](#copy-gitignored-files-into-worktrees)。

<h3 id="ask-claude-to-create-a-worktree">
  要求 Claude 创建 worktree
</h3>

您也可以在会话期间要求 Claude "在 worktree 中工作"，它会使用 [`EnterWorktree`](/docs/zh-CN/tools-reference) 工具创建一个。一旦进入 worktree，Claude 可以通过调用 `EnterWorktree` 并指定目标路径，直接切换到 `.claude/worktrees/` 下的另一个 worktree；之前的 worktree 保留在磁盘上不变。

当 Claude 进入存储库的 `.claude/worktrees/` 目录之外的路径时，Claude Code 会首先要求您的批准，因为该移动会将会话的工作目录、写入访问权限和项目配置（如 `CLAUDE.md` 和设置）转移到该位置。`EnterWorktree` [权限规则](/docs/zh-CN/permissions)或选择"不再询问"不会抑制此提示；只有 `bypassPermissions` 模式会跳过它。在 v2.1.206 之前，Claude 可以进入任何现有的 worktree 路径而无需询问。

<Note>
  **Hook 路径不跟随 worktree。** 在 Claude 进入 worktree 后，Claude Code 会在您的 [hooks](/docs/zh-CN/hooks#reference-scripts-by-path) 中保持 `${CLAUDE_PROJECT_DIR}` 不变，并以不同的方式将 worktree 路径传递给它们：

  * **`${CLAUDE_PROJECT_DIR}` 保持不变**：它仍然指向会话启动的项目根目录，因此 hook 命令（如 `${CLAUDE_PROJECT_DIR}/.claude/hooks/check-style.sh`）仍然在主检出中运行脚本。
  * **`cwd` 跟随 Claude**：hook 的[输入 JSON](/docs/zh-CN/hooks#common-input-fields) 中的 `cwd` 字段是 worktree 根目录，当 Claude 运行 `cd` 时它会再次移动。当 hook 需要 worktree 路径时读取它。
</Note>

<h2 id="clean-up-worktrees">
  清理 worktrees
</h2>

当你退出交互式 worktree 会话时，Claude 会检查 worktree 中是否有删除会丢失的工作：已更改或未跟踪的文件、已检出子模块内的未提交工作，以及新提交。这些规则适用于 Claude 使用 git 创建的 worktrees。对于你的 [WorktreeCreate hook](/docs/zh-CN/hooks#worktreecreate) 创建的 worktree，请改为参阅 [WorktreeRemove](/docs/zh-CN/hooks#worktreeremove)。

* **worktree 是干净的**：对于未命名的会话，Claude 会自动删除 worktree 及其分支。[已命名](/docs/zh-CN/sessions#name-your-sessions)的会话会先提示你，以便你可以保留 worktree 供以后使用
* **worktree 中有工作**：Claude 会提示你保留或删除 worktree。保留会保留目录和分支。要稍后返回，请运行 Claude Code 在退出时打印的 `claude --worktree <name> --resume` 命令。删除会删除 worktree 目录及其分支，以及其中的所有工作
* **无法验证 worktree 的状态**：当 Claude Code 无法计算 worktree 的更改或无法检查其子模块检出时，它会提示你而不是自动删除 worktree。提示会说明它无法检查的内容

使用 `-p` 的非交互式运行没有退出提示，因此 Claude 不会清理它们的 worktrees，Claude Code 会保留它在创建时对每个 worktree 所取的锁，直到稍后会话的[陈旧锁扫描](#clean-up-subagent-and-background-session-worktrees)释放它。要删除一个，请运行 `git worktree remove`；如果 git 拒绝因为 worktree 被锁定，请先在其上运行 `git worktree unlock`。

在 Windows 上，删除 worktree 不会删除其外部的文件。如果 worktree 内的文件夹是指向其他地方的链接，例如 NTFS 接合点或目录符号链接，Claude Code 只删除链接并保留它指向的文件夹。在 v2.1.205 之前，删除嵌套在子目录中的链接的 worktree 可能会删除它指向的文件夹。

<h2 id="resume-a-worktree-session">
  恢复 worktree 会话
</h2>

当您恢复在 worktree 内结束的会话而未[退出它](#clean-up-worktrees)时，Claude Code 会将会话返回到该 worktree。这适用于交互式恢复、[非交互式模式](/docs/zh-CN/headless)中带有 `-p` 的 `--continue` 和 `--resume`，以及 Agent SDK。`--continue` 会选择从您启动的目录下记录的最近会话。回到 worktree 内，Claude 仍然可以使用 [`ExitWorktree`](/docs/zh-CN/tools-reference) 工具退出它。

在将会话返回到其 worktree 之前，Claude Code 会验证 worktree 仍然是与主检出分开的检出，并拒绝重新进入未通过检查的 worktree。对于 git worktree，检查会读取其 git 元数据。没有 git 元数据的 worktree（例如 [`WorktreeCreate` hook](#non-git-version-control) 创建的）可以通过检查；Claude Code 仍然拒绝的情况列在[Claude Code 拒绝使用 worktree](#claude-code-refuses-to-use-a-worktree) 下及其恢复。有关消息和如何从每个消息恢复，请参阅[会话在其 worktree 外恢复](#the-session-resumes-outside-its-worktree)。

您从哪里启动以及如何恢复会改变 Claude Code 重新进入的内容：

* **启动目录**：从主检出或存储库的另一个目录使用 `--resume` 恢复。Claude Code 会重新进入它使用 git 在 `.claude/worktrees/` 下创建的 worktree，即使您从其内部启动。当您从任何其他 worktree 内启动时，Claude Code 只有在能够从那里为其担保时才会重新进入它：一个是其自己的存储库的 worktree、一个没有 git 元数据的 worktree，或从您使用 `git worktree add` 创建的 worktree 的子目录启动会拒绝，因此从主检出启动这些。
* **`--fork-session`**：分叉的会话在您启动 Claude 的目录中启动，Claude Code 会保持原始会话的 worktree 不变。
* **已删除的 worktree**：如果 worktree 目录不再存在，Claude Code 会在您启动 Claude 的目录中恢复会话。它告诉您 worktree 已消失并清除会话的 worktree 绑定。

<Note>
  在 v2.1.212 之前，非交互式恢复停留在启动目录中，`ExitWorktree` 报告没有活跃的 worktree 会话可以退出。
</Note>

当 Claude 进入或退出 Claude Code 使用 git 创建的 worktree 时，记录会跟随：Claude Code 在会话的新工作目录下记录会话，与 [`/cd`](/docs/zh-CN/commands) 的方式相同，因此 `/desktop` 和 `--resume` 在那里找到它。退出以相同的方式将其移回。由 [`WorktreeCreate` hook](#non-git-version-control) 创建的 worktree 会在启动目录保留其记录。需要 Claude Code v2.1.198 或更高版本。

<h2 id="how-claude-code-enforces-isolation">
  Claude Code 如何强制隔离
</h2>

当会话在 worktree 中被隔离时，Claude Code 会阻止下面的检查定义的工具调用。无论您是使用 `--worktree` 启动会话、Claude 使用 `EnterWorktree` 进入 worktree，还是恢复 worktree 会话，相同的规则都适用。

相同的强制措施涵盖 Claude 从隔离会话生成的每个子代理。它适用于会话是交互式还是在[后台](/docs/zh-CN/agent-view#how-file-edits-are-isolated)运行。[在自己的 worktree 中运行的子代理](#isolate-subagents-with-worktrees)进行相同的检查。它们的版本历史在[写入子代理文件](/docs/zh-CN/sub-agents#write-subagent-files)下。

Claude Code 应用四个检查：

* **文件编辑**：Claude Code 阻止针对主检出中的路径的 `Edit`、`Write` 或 `NotebookEdit`。
* **命令工作目录**：Claude Code 阻止其工作目录解析为主检出的 Bash、PowerShell 或 Monitor 命令，或其工作目录它无法验证保持在其外的命令。
* **Git 重定向**：Claude Code 阻止将 git 重定向到主检出的 Bash 或 Monitor 命令。重定向可以通过 `git -C`、`--git-dir`、`GIT_DIR` 或 `GIT_WORK_TREE` 变量，或在运行 git 之前 `cd` 到主检出来进行。
* **命令形状**：当 Claude Code 无法从命令文本验证命令运行的任何 git 保持在 worktree 内时，它会阻止 Bash 或 Monitor 命令。例如，当命令名称在运行时计算、语法无法解析，或当诸如 `${!name}` 或 `${ command; }` 之类的扩展可能运行文本中未明确说明的命令时，就会发生这种情况。Claude Code 告诉 Claude 如何重写被拒绝的命令，例如将其分割成普通的单独命令。您无法关闭此检查。

检查适用于您启动 Claude Code 的存储库。它们也涵盖链接的 worktree 链接自的主检出。对于 PowerShell 命令，Claude Code 仅应用工作目录检查。

Claude 将每个拒绝视为命名 worktree 并说明如何继续的工具错误。有关被拒绝的命令，请参阅[拒绝消息的含义以及如何清除它](/docs/zh-CN/errors#command-blocked-by-the-worktree-isolation-checks)。

<h2 id="isolate-subagents-with-worktrees">
  使用 worktrees 隔离子代理
</h2>

子代理可以在自己的 worktrees 中运行，以便并行编辑不会冲突。要求 Claude "为您的代理使用 worktrees"，或通过向 frontmatter 添加 `isolation: worktree` 在[自定义子代理](/docs/zh-CN/sub-agents#supported-frontmatter-fields)上永久设置它。

`.claude/agents/` 中的这个子代理总是在自己的 worktree 中运行：

```markdown theme={null}
---
name: refactorer
description: Applies mechanical refactors across many files
isolation: worktree
---

Apply the requested refactor across every affected file, then run the tests
and report the results.
```

每个子代理都会获得一个临时 worktree，当子代理完成且没有更改时 Claude Code 会自动删除；带有更改的 worktree 会保留在磁盘上，直到下面的[定期扫描](#clean-up-subagent-and-background-session-worktrees)可以删除它而不会丢失工作。

子代理 worktrees 使用与 `--worktree` 相同的[基础分支](#choose-the-base-branch)，因此它们从您的存储库的默认分支分支，除非 `worktree.baseRef` 设置为 `"head"`。

<h3 id="clean-up-subagent-and-background-session-worktrees">
  清理子代理和后台会话 worktrees
</h3>

Claude Code 运行定期扫描，删除 Claude 为子代理和[后台会话](/docs/zh-CN/agent-view#how-file-edits-are-isolated)创建的 worktrees，一旦它们超过您的 [`cleanupPeriodDays`](/docs/zh-CN/settings-reference#cleanupperioddays) 设置，遵循[保留扫描规则](/docs/zh-CN/claude-directory#cleaned-up-automatically)。

当您[后台](/docs/zh-CN/agent-view#send-the-session-to-the-background)一个 `--worktree` 会话时，其 worktree 变成后台会话 worktree，扫描可以删除。扫描在这些情况下保留 worktree：

* worktree 仍然保留工作：已更改或未跟踪的文件，或未推送的提交。
* worktree 中已检出的子模块保留已更改或未跟踪的文件，或 Claude Code 无法检查 worktree 的子模块。此检查需要 Claude Code v2.1.274 或更高版本。
* Claude Code 无法确定存储库配置定义的过滤驱动程序，或在其中找到它无法关闭的设置，或[四种也阻止 worktree 创建的情况](#git-lfs-content-is-missing-from-a-worktree-claude-code-created)中的任何一种适用。
* worktree 属于您未后台的 `--worktree` 会话，无论其年龄如何。
* 您自己使用 `git worktree add` 创建了 worktree，即使您随后在其中运行了 `--worktree <name>` 会话并后台了该会话。

Claude Code 将标记写入它使用 git 创建的每个 worktree 的 git 元数据中，扫描会保留任何没有标记的 worktree，包括 [`WorktreeCreate` hook](#non-git-version-control) 创建的 worktree。在 v2.1.246 之前，扫描没有检查标记，当旧的后台会话记录指向它时可能会删除您自己创建的 worktree。

当代理运行时，Claude Code 在其 worktree 上持有 `git worktree lock`，以便并发清理无法删除它，当代理完成时释放锁。Claude Code 在为后台会话创建的 worktree 上持有相同的锁，同时会话运行，因此扫描会保留 worktree 并且 `git worktree remove` 拒绝删除它。

扫描也会释放 Claude Code 为其进程已退出的会话设置的锁，因此被杀死的后台会话不会永久锁定其 worktree。扫描永远不会释放您自己使用 `git worktree lock` 设置的锁。在 v2.1.210 之前，被杀死的会话留下的锁会保留在原位，直到您运行 `git worktree unlock`。

要清理扫描保留的 worktree，请运行 `git worktree remove`，如果 worktree 有未提交的更改或未跟踪的文件，请添加 `--force`。如果 git 拒绝因为 worktree 被锁定，请先在其上运行 `git worktree unlock`。

<h2 id="customize-worktree-creation">
  自定义 worktree 创建
</h2>

Claude Code 的 worktree 创建默认值涵盖大多数会话：它在 `.claude/worktrees/` 下创建它们，从您的存储库的默认分支分支它们，并仅检出跟踪的文件。本部分中的选项会改变这些默认值。

<h3 id="choose-the-base-branch">
  选择基础分支
</h3>

新 worktrees 从存储库的默认分支分支，因此大多数会话不需要此设置。在[设置](/docs/zh-CN/settings-reference#worktree)中设置 `worktree.baseRef` 以改为从您的当前工作分支。该设置接受两个值：

* `"fresh"`（默认）：从存储库在远程上的默认分支分支，通常是 `main`，因此 worktree 从与远程匹配的干净树开始。
* `"head"`：从您当前的本地 `HEAD` 分支，因此 worktree 携带您未推送的提交和功能分支状态。当隔离需要在进行中的工作上操作的子代理时使用此选项。在 worktree 内，`"head"` 解析为该 worktree 的 `HEAD`，而不是主检出的。

您无法将 `worktree.baseRef` 设置为分支名称。要从特定的现有分支启动 worktree，请[直接使用 git 创建它](#manage-worktrees-manually)。

对于 `"fresh"` 基础，Claude Code 会保持 `origin/HEAD` 最新：当存储库在过去 24 小时内没有被获取时，它会获取默认分支，上限为 5 秒，如果获取失败则使用本地缓存的引用。如果未配置远程，或 `origin/HEAD` 未在本地缓存且无法获取，worktree 会回退到您当前的本地 `HEAD`。在 v2.1.208 之前，新 worktree 使用已经本地缓存的任何 `origin/HEAD`。

此示例使每个新 worktree 从您的当前工作分支：

```json theme={null}
{
  "worktree": {
    "baseRef": "head"
  }
}
```

<h3 id="branch-from-a-pull-request">
  从拉取请求分支
</h3>

要从特定的拉取请求或合并请求分支，将 `--worktree` 传递以 `#` 为前缀的编号、GitHub 拉取请求 URL 或 GitLab 合并请求 URL，例如 `https://gitlab.com/group/repo/-/merge_requests/123`。Claude Code 从 `origin` 获取该更改的头提交并在 `.claude/worktrees/pr-<number>` 创建 worktree。引用参数以便您的 shell 不会将 `#` 视为注释的开始：

```bash theme={null}
claude --worktree "#1234"
```

Claude Code 仅从 URL 读取编号。它总是从您的存储库的 `origin` 远程获取，并按 `origin` 的主机选择获取路径：

* **github.com**：获取 `pull/<number>/head`
* **gitlab.com**：获取 `merge-requests/<number>/head`
* **GitHub Enterprise、自管理 GitLab 或任何其他主机**：首先尝试 `pull/<number>/head`，然后尝试 `merge-requests/<number>/head`

在 v2.1.233 之前，Claude Code 仅接受 `#<number>` 和 GitHub 风格的拉取请求 URL 用于 `--worktree`，并总是获取 `pull/<number>/head`。

<h3 id="copy-gitignored-files-into-worktrees">
  将 gitignored 文件复制到 worktrees
</h3>

Worktree 是一个新的检出，因此来自您主存储库的未跟踪文件（如 `.env` 或 `.env.local`）不存在。要在 Claude 创建 worktree 时自动复制它们，请将 `.worktreeinclude` 文件添加到您的项目根目录。

该文件使用 `.gitignore` 语法。只有匹配模式且也被 gitignored 的文件才会被复制，因此跟踪的文件永远不会被重复。

如果您写一个以 `**/` 开头的模式，并且您想要的文件在一个作为整体被 gitignored 的目录内，Claude Code 仅在该目录本身匹配模式时或当 `**/` 之后的第一个名称是目录路径中的名称之一时才复制它们。例如，如果您写 `**/.claude/skills/*.md`，该第一个名称是 `.claude`，因此 Claude Code 从被忽略的 `.claude/` 目录中复制匹配的文件。要从 `**/` 模式无法到达的被忽略目录中复制文件，请在模式中命名该目录：写 `vendor/**/config.json` 而不是 `**/config.json`。在 v2.1.239 之前，Claude Code 仅当目录本身匹配模式时才为 `**/` 模式从完全被忽略的目录中复制文件。

此 `.worktreeinclude` 将两个 env 文件和一个 secrets 配置复制到每个新 worktree：

```text .worktreeinclude theme={null}
.env
.env.local
config/secrets.json
```

这适用于 Claude Code 使用 git 创建的每个 worktree：`--worktree` worktrees、[子代理 worktrees](#isolate-subagents-with-worktrees) 和[桌面应用](/docs/zh-CN/desktop#work-in-parallel-with-sessions)中的并行会话。使用 [`WorktreeCreate` hook](#non-git-version-control)，在 hook 脚本内复制文件。

<h3 id="reuse-a-worktree-name">
  重用 worktree 名称
</h3>

传递 `--worktree` 一个其目录已存在的名称会打开该现有 worktree 而不是创建一个新的。

使用默认的 `"fresh"` [基础](#choose-the-base-branch)，当以下所有条件都成立时，重新打开的 worktree 会重置为存储库的默认分支而不是在其旧提示处继续：

* 它没有未提交的更改或未跟踪的文件。
* 它仍然在 Claude Code 为其创建的分支上。
* 它没有自己的提交，或其拉取请求或合并请求已合并且其远程分支已删除。

Claude Code 仅从 git 状态检测合并的情况：worktree 推送到的远程分支不再存在，worktree 中的每个提交都已在默认分支上。

在所有其他情况下，Claude Code 在其旧提示处重新打开 worktree：

* worktree 未通过任何条件。
* Claude Code 无法验证 worktree 的状态。
* `worktree.baseRef` 是 `"head"`。
* 名称是拉取请求或合并请求引用。

在 v2.1.208 之前，当您重用名称时，Claude Code 总是在其旧提示处重新打开旧 worktree。

<h3 id="replace-worktree-creation-with-a-hook">
  使用 hook 替换 worktree 创建
</h3>

配置 [`WorktreeCreate` hook](/docs/zh-CN/hooks#worktreecreate) 以完全替换默认的 `git worktree` 逻辑，包括将 worktrees 放在 `.claude/worktrees/` 之外的地方。有关完整示例，请参阅[非 git 版本控制](#non-git-version-control)。

<h2 id="what-worktrees-share-with-the-main-checkout">
  Worktrees 与主检出共享的内容
</h2>

Worktree 获得自己的文件和分支，但它与主检出共享以下内容：

* **存储库的 `.git` 目录**：worktree 中的 git 命令写入主存储库的共享 `.git` 目录，[沙箱](/docs/zh-CN/sandboxing#filesystem-isolation)允许这些写入，因此 `git commit` 等命令可以从启用沙箱的 worktree 内部工作。
* **插件**：从主检出在[项目范围](/docs/zh-CN/plugins/loading#find-where-a-plugin-is-enabled)安装的插件也会在同一存储库的 worktrees 中加载，因此您无需为每个 worktree 重新安装它们。需要 Claude Code v2.1.200 或更高版本。
* **权限批准**：在 worktree 会话中为 Bash 命令选择"是，不再询问"会将规则保存到主检出的 `.claude/settings.local.json`，因此它适用于主检出和存储库的每个其他 worktree，并在 worktree 的删除后存活。在 Windows 和 Claude Code [不使用存储库根](/docs/zh-CN/settings#where-claude-code-looks-for-each-file)的其他情况下，规则与该 worktree 保持一致。在 v2.1.211 之前，在 worktree 中授予的批准被保存在该 worktree 内，不适用于其他地方，并在 worktree 被删除时丢失。请参阅[批准保存的位置](/docs/zh-CN/permissions#permission-system)。
* **未跟踪的 skills、agents 和 commands**：当 worktree 检出在其根目录没有 `.claude/skills` 目录时（例如因为您的 `.claude/skills` 被 gitignored），Claude Code 会在 worktree 会话中加载主检出的[项目 skills](/docs/zh-CN/skills#where-skills-live)。在具有自己的 `.claude/skills` 目录的 worktree 中，只加载该副本。

  相同的读取覆盖也适用于 `.claude/agents` 和 `.claude/commands`。对于 skills，读取覆盖需要 Claude Code v2.1.277 或更高版本。

无论您是使用 `--worktree`、使用 `git worktree add` 还是通过[桌面应用](/docs/zh-CN/desktop#work-in-parallel-with-sessions)创建 worktree，所有这些都适用。

<h2 id="manage-worktrees-manually">
  手动管理 worktrees
</h2>

当您需要检出特定的现有分支或将 worktree 放在存储库外时，直接使用 Git 创建 worktrees。

在新分支上创建 worktree：

```bash theme={null}
git worktree add ../project-feature-a -b feature-a
```

从现有分支创建 worktree，将 `fix-issue-456` 替换为存储库中已存在的分支：

```bash theme={null}
git worktree add ../project-bugfix fix-issue-456
```

在 worktree 中启动 Claude：

```bash theme={null}
cd ../project-feature-a
claude
```

列出您的 worktrees：

```bash theme={null}
git worktree list
```

完成后删除一个：

```bash theme={null}
git worktree remove ../project-feature-a
```

有关完整的命令参考，请参阅 [Git worktree 文档](https://git-scm.com/docs/git-worktree)。

<h2 id="non-git-version-control">
  非 git 版本控制
</h2>

Worktree 隔离默认使用 git。对于 SVN、Perforce、Mercurial 或其他系统，配置 [`WorktreeCreate` 和 `WorktreeRemove` hooks](/docs/zh-CN/hooks#worktreecreate) 以提供自定义创建和清理逻辑。因为 hook 替换了默认的 git 行为，当您使用 `--worktree` 时，[`.worktreeinclude`](#copy-gitignored-files-into-worktrees) 不会被处理。改为在您的 hook 脚本内复制任何本地配置文件。

此 `WorktreeCreate` hook 使用 `jq` 从 stdin 上的 JSON 读取 worktree 名称，检出一个新的 SVN 工作副本，并打印目录路径，以便 Claude Code 可以将其用作会话的工作目录。将配置添加到您的 [`settings.json`](/docs/zh-CN/settings#where-settings-live)：

```json theme={null}
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'NAME=$(jq -r .name); DIR=\"$HOME/.claude/worktrees/$NAME\"; svn checkout https://svn.example.com/repo/trunk \"$DIR\" >&2 && echo \"$DIR\"'"
          }
        ]
      }
    ]
  }
}
```

将其与 `WorktreeRemove` hook 配对以在会话结束时进行清理。有关输入架构和删除示例，请参阅 [hooks 参考](/docs/zh-CN/hooks#worktreecreate)。

`WorktreeCreate` hook 还允许您在 git 存储库外运行 [`/batch`](/docs/zh-CN/commands#all-commands)。每个 `/batch` 子代理随后使用您项目的版本控制命令发布其更改，当它无法打开拉取请求时，报告它发布的内容。在 git 存储库外运行 `/batch` 需要 Claude Code v2.1.281 或更高版本。

<h2 id="troubleshooting">
  故障排除
</h2>

当 Claude Code 创建 worktree、在启动时进入一个或将恢复的会话返回到一个时，它会报告下面的错误。

<h3 id="claude-code-can’t-enter-the-worktree-at-startup">
  Claude Code 无法在启动时进入 worktree
</h3>

当 Claude Code 无法在启动时进入 worktree 目录时，它会打印一个命名该路径的错误并以代码 1 退出。这可能发生在 [`WorktreeCreate` hook](/docs/zh-CN/hooks#worktreecreate) 打印除了它创建的目录之外的其他内容时，或当目录在设置后被删除时。

<h3 id="worktree-creation-fails-on-a-symlinked-path">
  Worktree 创建在符号链接路径上失败
</h3>

当 `.claude`、`.claude/worktrees` 或 worktree 目录本身是符号链接时，Claude Code 拒绝创建 worktree，错误会命名符号链接的路径。删除符号链接并重试。在 v2.1.212 之前，如果存储库已经在这些路径之一包含提交的符号链接，worktree 创建会跟随它并可能在存储库外创建文件。

<h3 id="git-lfs-content-is-missing-from-a-worktree-claude-code-created">
  Git LFS 文件在 Claude Code 创建的 worktree 中是指针文件
</h3>

如果您使用 `git lfs install --local` 设置了 [Git LFS](https://git-lfs.com)，Claude Code 创建的 worktree 包含 LFS 指针文件而不是真实文件。`--local` 标志将 LFS 过滤器写入存储库自己的 `.git/config` 而不是您的全局 git 配置。普通的 `git lfs install` 写入您的全局配置并不受影响。相同的适用于在存储库自己的配置中定义的任何其他[过滤驱动程序](https://git-scm.com/docs/gitattributes)。

Claude Code 在创建 worktree 时跳过存储库自己的过滤驱动程序，因为过滤驱动程序是 shell 命令，任何可以写入存储库的东西（包括 Claude）都可能在那里放置一个。在 v2.1.247 之前，Claude Code 在 worktree 创建期间运行这些驱动程序。

要获取真实文件，请在 worktree 内运行 `git lfs pull`。

在四种罕见的情况下，Claude Code 无法判断存储库的配置定义的过滤驱动程序，或找到一个它无法关闭的设置，因此根本不创建 worktree。将错误与其修复匹配：

* **`Could not read the repository git config to neutralize filter drivers`**：Claude Code 无法读取存储库的 `.git/config`，例如因为其权限。修复它并重试。
* **`The repository git config defines a filter driver whose name cannot be neutralized (contains "=" or a newline)`**：在 `.git/config` 中重命名或删除该过滤驱动程序并重试。
* **`The repository git config has a conditional include (includeIf)`**：将 `includeIf` 在 `.git/config` 中拉入的设置直接移到该文件中，删除 `includeIf`，并重试。您全局 git 配置中的 `includeIf` 不会触发此问题。
* **`Git was not run: the repository's own git config sets <key>`**：消息命名一个指向 Git LFS 运行程序的键，例如 `lfs.customtransfer.<name>.path` 或 `lfs.standalonetransferagent`。如果该设置是您的，将其移到您的全局 git 配置。如果您不认识它，从存储库的 git 配置中删除它，因为您不信任的工具或检出可能已写入它。一旦键从存储库的配置中消失，重试。

<h3 id="claude-code-refuses-to-use-a-worktree">
  Claude Code 拒绝使用 worktree
</h3>

以 `Refusing to use <path> as an isolation worktree` 开头的错误意味着 Claude Code 在采用它作为会话或子代理的隔离检出之前检查了目录的 git 身份，并拒绝了它。检查运行无论 Claude Code 是创建 worktree、进入现有的还是重用早期运行中的。

在大多数情况下，消息的其余部分说目录的 git 元数据解析为主检出：例如，其 `.git` 文件指向主存储库自己的 `.git` 目录，或 git 通过 `core.worktree` 重定向将其工作树解析为主检出。从这样的目录，普通的 git 命令（如 `git reset --hard`）会作用于主检出而不是 worktree。Claude Code 也在目录有它无法读取的 `.git` 条目时拒绝，而不是假设 worktree 是安全的。

没有 git 元数据的目录（例如您的 [`WorktreeCreate` hook](#non-git-version-control) 创建的）仅当没有 git 存储库包含它时才通过检查。如果 hook 在存储库内创建目录，git 将其解析为该存储库的检出，Claude Code 拒绝它并显示 `git resolves its working tree to` 消息，因此让 hook 在任何存储库外创建其目录。

Claude Code 保留被拒绝的目录，因为它可能保留工作。将消息与其恢复匹配，无论它跟随 `Refusing to use <path>` 还是出现在[恢复消息](#the-session-resumes-outside-its-worktree)中；某些结尾仅在恢复消息中出现：

* **说 `launch from the parent checkout` 或 `Run the resume from the project checkout`**：您从 worktree 内启动了 Claude Code。改为从主检出启动；worktree 无需重新创建。
* **说 `it cannot be resumed or re-entered`**：此会话中没有任何东西从您启动的地方为 worktree 担保。重新创建它；目录及其工作保留在磁盘上以供手动恢复，当 worktree 有父检出时，从那里恢复也有效。
* **说 `it contains the protected checkout`**：被拒绝的目录是您主检出的父目录，例如您的主目录。不要删除它。更改 worktree 路径，例如您的 `WorktreeCreate` hook 返回的路径或 `EnterWorktree` 目标，以便 worktree 不包含检出。
* **说 `the protected checkout <path> has a .git entry that could not be examined` 或 `has git metadata that could not be resolved`**：问题是主检出的 git 元数据，而不是 worktree 的。不要删除 worktree，忽略消息的尾部建议重新创建它，这不适用于这两个结尾。修复主检出，例如权限问题或 git 对其 `.git` 的 `dubious ownership` 拒绝，并重试。
* **说 `its recorded path has a network spelling`**：Claude Code 永远不会恢复到网络路径上的 worktree。在本地路径重新创建 worktree。
* **任何其他结尾**：消息命名问题及其修复，例如删除 `core.worktree` 重定向或重新创建 worktree；遵循它。在删除消息说其 git 身份无法验证的目录之前，首先解决命名的原因，例如 worktree 路径中的符号链接或 git 本身无法运行，因为目录可能是健康的。当您确实重新创建时，从旧目录中拯救您需要的任何更改；它保留在磁盘上。

<h3 id="the-session-resumes-outside-its-worktree">
  会话在其 worktree 外恢复
</h3>

当您交互式恢复会话且 Claude Code 无法将其返回到其 worktree 时，Claude Code 会使用下面的消息之一说明。当 Claude Code 清除 worktree 绑定时，它在会话记录中记录清除。如果您[抑制记录写入](/docs/zh-CN/sessions#where-transcripts-are-stored)，消息改为说绑定无法被清除，Claude Code 将在稍后恢复时重新检查 worktree。

| 消息开头 | 发生了什么以及要做什么 |
| :- | :- |
| `Your worktree <path> no longer exists` | worktree 目录被删除。会话在当前目录中继续而不隔离，Claude Code 清除 worktree 绑定。无需操作。 |
| `Could not verify your worktree <path> this time` | Claude Code 无法验证 worktree，通常是由于暂时原因；绑定被保留，会话在当前目录中继续而不隔离。再次恢复以重试；如果它继续发生，在新会话中进入 worktree 并匹配[Claude Code 拒绝使用 worktree](#claude-code-refuses-to-use-a-worktree) 下的拒绝消息，它可能命名主检出的元数据而不是 worktree 的。 |
| `Did not re-enter your worktree <path>` | Claude Code 拒绝 worktree 绑定为不安全；它清除绑定，会话继续而不隔离。消息包括特定的拒绝：在[Claude Code 拒绝使用 worktree](#claude-code-refuses-to-use-a-worktree) 下匹配它，因为修复对某些拒绝是重新创建，对其他的是路径更改。 |
| `Could not re-enter your worktree <path>` | Claude Code 无法从您启动的地方为 worktree 担保，最常见的是因为您从其内部启动；绑定被保留。消息的其余部分命名修复；在[Claude Code 拒绝使用 worktree](#claude-code-refuses-to-use-a-worktree) 下匹配它。 |

在[非交互式模式](/docs/zh-CN/headless)中使用 `-p`，以及 [Agent SDK](/docs/zh-CN/agent-sdk/sessions) 运行的恢复中，Claude Code 对除了消失的 worktree 之外的每个拒绝停止恢复并显示 stderr 错误，而不是继续而不隔离。

使用 `--output-format stream-json`，拒绝也到达 stdout 作为 `result` 消息，子类型 `error_during_execution`，其 `errors` 数组携带相同的文本，因此 Agent SDK 应用程序接收原因而不仅仅是非零退出。在 v2.1.260 之前，worktree 恢复拒绝没有产生 `result` 消息。

消息与交互式消息表中的形状不同：

* `Error: cannot resume into worktree <path>: ...This session was not started.` 对于表中显示为 `Did not re-enter` 的拒绝。Claude Code 在退出前清除 worktree 绑定，错误说明了这一点；下次您恢复对话时，会话在当前目录中继续而不使用 worktree 隔离。在 v2.1.260 之前，Claude Code 没有写入清除的绑定，所以同一恢复的每次重试都以相同的错误失败。

  如果您[抑制记录写入](/docs/zh-CN/sessions#where-transcripts-are-stored)，清除无法被保存。错误然后说相同的命令将再次被拒绝，并命名 `--fork-session` 和启动新对话作为在没有 worktree 的情况下继续的方式。
* `Error: could not verify worktree <path> for this resume, so the resume was aborted...` 对于 `Could not verify`
* `Error: ...The worktree binding is kept.` 对于 `Could not re-enter`
* `Notice: the worktree <path> for this session no longer exists...` 对于消失的 worktree；Claude Code 打印它并继续会话，如交互式恢复一样

拒绝结尾嵌入在每个错误中与交互式通知共享，因此它仍然匹配[Claude Code 拒绝使用 worktree](#claude-code-refuses-to-use-a-worktree) 下的其条目。

在 stream-json 结果中，[`startup_failure_reason`](/docs/zh-CN/agent-sdk/typescript#startup_failure_reason) 对于 `could not verify worktree` 错误是 `worktree_unverified`，对于 `cannot resume into worktree` 和 `The worktree binding is kept` 错误是 `worktree_resume_refused`。应用程序可以基于它进行分支，而不是匹配错误文本。在 v2.1.274 之前，结果没有携带 `startup_failure_reason` 字段。

<h2 id="see-also">
  另请参阅
</h2>

Worktrees 处理文件隔离。下面的相关页面涵盖将工作委派到这些隔离的检出中、在它们之间传递发现以及在您创建的会话之间切换：

* [子代理](/docs/zh-CN/sub-agents)：在会话内将工作委派给隔离的代理
* [跨会话消息传递](/docs/zh-CN/cross-session-messaging)：让您的 worktrees 中的会话相互传递发现
* [代理团队](/docs/zh-CN/agent-teams)：自动协调多个 Claude 会话
* [管理会话](/docs/zh-CN/sessions)：命名、恢复和在对话之间切换
* [桌面并行会话](/docs/zh-CN/desktop#work-in-parallel-with-sessions)：桌面应用中由 worktree 支持的会话
