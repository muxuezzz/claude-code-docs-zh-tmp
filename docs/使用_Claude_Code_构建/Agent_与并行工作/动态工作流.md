> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用动态工作流大规模编排子代理

> 动态工作流从 Claude 编写的脚本中编排许多子代理，您可以重新运行。用于代码库审计、大型迁移和交叉检查研究。

<Note>
  动态工作流在所有付费计划上可用，具有 Anthropic API 访问权限，以及在 Amazon Bedrock、Google Cloud 的 Agent Platform 和 Microsoft Foundry 上可用。在 Pro 上，从 `/config` 中的 Dynamic workflows 行启用它们。
</Note>

动态工作流是一个 JavaScript 脚本，可大规模编排许多[子代理](/docs/zh-CN/sub-agents)。Claude 为您描述的任务编写脚本，运行时在后台执行它，同时您的会话保持响应。

当任务需要比一个对话能协调的更多代理时，或当您想将编排编纂为可以读取和重新运行的脚本时，请使用工作流。示例包括代码库范围的错误扫描、500 文件迁移、需要相互交叉检查来源的研究问题，以及在提交一个之前值得从多个独立角度起草的困难计划。

<h2 id="when-to-use-a-workflow">
  何时使用工作流
</h2>

[子代理](/docs/zh-CN/sub-agents)、[skills](/docs/zh-CN/skills)、[agent teams](/docs/zh-CN/agent-teams) 和工作流都可以运行多步骤任务。区别在于谁掌握计划：

| | 子代理 | Skills | Agent teams | 工作流 |
| :- | :- | :- | :- | :- |
| 它是什么 | Claude 生成的工作者 | Claude 遵循的指令 | 监督对等会话的主导代理 | 运行时执行的脚本 |
| 谁决定接下来运行什么 | Claude，逐轮 | Claude，遵循提示 | 主导代理，逐轮 | 脚本 |
| 中间结果在哪里 | Claude 的上下文窗口 | Claude 的上下文窗口 | 共享任务列表 | 脚本变量 |
| 什么是可重复的 | 工作者定义 | 指令 | 团队定义 | 编排本身 |
| 规模 | 每轮几个委派任务 | 与子代理相同 | 少数几个长期运行的对等体 | 每次运行数十到数百个代理 |
| 中断 | 重启轮次 | 重启轮次 | 队友继续运行 | 在同一会话中可恢复 |

工作流将计划移入代码。使用子代理、skills 和 agent teams，Claude 是编排者：它逐轮决定接下来生成或分配什么，每个结果都进入上下文窗口。工作流脚本持有循环、分支和中间结果本身，所以 Claude 的上下文只持有最终答案。

将计划移入代码也让工作流应用可重复的质量模式，而不仅仅是运行更多代理：它可以让独立代理在报告之前对彼此的发现进行对抗性审查，或从多个角度起草计划并相互权衡，所以您获得比单次通过更可信的结果。

<h2 id="run-a-bundled-workflow">
  运行捆绑工作流
</h2>

查看工作流运行的最快方式是运行 `/deep-research`，这是 Claude Code 包含的[内置工作流](#bundled-workflows)，用于跨许多来源调查问题。您将看到代理在后台通过一组阶段工作，同时您的会话保持空闲，最后获得一份报告而不是逐轮记录。

<Steps>
  <Step title="运行工作流">
    使用您想要调查的问题运行 `/deep-research`。它在多个角度上扇出网络搜索，获取并交叉检查它找到的来源，并综合一份引用的报告。

    ```text wrap theme={null}
    /deep-research What changed in the Node.js permission model between v20 and v22?
    ```
  </Step>

  <Step title="允许工作流">
    Claude Code 询问是否允许工作流。选择**是**继续。确切的提示取决于您的权限模式。有关每种模式的选项，请参阅[在运行前批准计划](#approve-the-plan-before-it-runs)。
  </Step>

  <Step title="观看进度">
    运行在后台启动。运行 `/workflows` 打开其进度视图：

    ```text wrap theme={null}
    /workflows
    ```

    如果 `/workflows` 显示的是运行列表，请选择您刚启动的运行并按 Enter。该视图显示每个阶段及其 Agent 计数。深入任何阶段以查看其 Agent 及每个 Agent 发现的内容。有关完整的控制集，请参阅[观看运行](#watch-the-run)。

    您也可以从输入框下方的任务面板观看：运行进行时会出现一行进度摘要。按向下箭头聚焦它，然后按 Enter 展开。
  </Step>

  <Step title="阅读报告">
    运行完成后，报告进入您的会话。它引用每个声明来自的来源，未通过交叉检查的声明已被过滤掉。

    当验证代理无法检查声明时，例如在速率限制或 API 错误之后，报告将该声明列为未验证，而不是计为被驳回。
  </Step>
</Steps>

要为您自己的任务运行工作流，[让 Claude 编写一个](#have-claude-write-a-workflow)，一旦运行完成您想要的操作，您可以[保存它](#save-the-workflow-for-reuse)作为您自己的命令。

<h3 id="bundled-workflows">
  捆绑工作流
</h3>

Claude Code 包含 `/deep-research` 作为内置工作流：

| 命令 | 它做什么 |
| :- | :- |
| `/deep-research <question>` | 在多个角度上扇出网络搜索问题，获取并交叉检查它找到的来源，对每个声明投票，并返回一份引用的报告，其中未通过交叉检查的声明已被过滤掉。需要[WebSearch 工具](/docs/zh-CN/tools-reference#websearch-tool-behavior)可用 |

`/deep-research` 仅在您调用它时运行。

[您自己保存的工作流](#save-the-workflow-for-reuse)以相同方式成为命令，并在 `/` 自动完成中与捆绑的工作流一起出现。

<h3 id="watch-the-run">
  观看运行
</h3>

工作流在后台运行，所以会话在 Agent 工作时保持响应。随时运行 `/workflows` 列出运行中和已完成的工作流，然后选择一个打开其进度视图。当会话只有一个运行时，`/workflows` 会跳过列表并直接打开该运行。要从列表中停止运行中的工作流而不打开它，请选择它并按 `x`。

进度视图显示每个阶段及其 Agent 计数。页脚列出每个操作的键：

| 键 | 操作 |
| :- | :- |
| `↑` / `↓` | 选择一个阶段或代理 |
| `Enter` 或 `→` | 深入选定的阶段，然后进入代理的详情。在详情中，`Enter` 展开或折叠它 |
| `Esc` 或 `←` | 返回一个级别。在 v2.1.203 至 v2.1.205 中，`←` 没有退出阶段或代理；在这些版本上使用 `Esc` |
| `j` / `k` | 当代理详情溢出时在其中滚动 |
| `f` | 按状态过滤选定阶段中的代理列表。再次按下以循环 |
| `p` | 暂停或恢复运行 |
| `x` | 停止选定的代理，或当焦点在运行上时停止整个工作流 |
| `r` | 重启选定的运行中代理 |
| `s` | [保存](#save-the-workflow-for-reuse)运行的脚本作为命令 |

代理详情列出代理的提示、其最近的工具调用和其结果。每个调用显示其状态，例如仍在运行或失败。当代理保持自己的任务列表时，详情显示它，以及每个任务的状态。

按 `Enter` 展开详情。提示和结果然后完整显示，每个列出的调用显示其输入和其结果的开始。

<h2 id="have-claude-write-a-workflow">
  让 Claude 编写工作流
</h2>

您可以通过两种方式让 Claude 为您的任务编写工作流：

* [在您的提示中请求工作流](#ask-for-a-workflow-in-your-prompt)，使用关键字 `ultracode`，Claude 为任务编写一个。
* [让 Claude 使用 ultracode 决定](#let-claude-decide-with-ultracode)：设置 `/effort ultracode`，Claude 为会话中的每个实质性任务规划工作流。

您也可以运行已存在的工作流命令：一个[捆绑工作流](#bundled-workflows)如 `/deep-research`，或一个您已[保存](#save-the-workflow-for-reuse)的。

<h3 id="ask-for-a-workflow-in-your-prompt">
  在您的提示中请求工作流
</h3>

要在不改变会话的努力级别的情况下将单个任务作为工作流运行，在您的提示中包含关键字 `ultracode`。用您自己的话提问，例如"使用工作流"或"运行工作流"，也可以工作：Claude 将直接请求视为相同的选择加入。

```text wrap theme={null}
ultracode: audit every API endpoint under src/routes/ for missing auth checks
```

Claude Code 在您的输入中突出显示该关键字，Claude 为任务编写工作流脚本，而不是逐轮处理它。该关键字仅选择 Claude 如何组织工作：代理的工具调用接收与会话中任何其他工具调用相同的权限检查和[沙箱化](/docs/zh-CN/sandboxing)。

如果运行完成了您想要的操作，您可以之后[将其保存为命令](#save-the-workflow-for-reuse)。如果您已经用另一种方式构建了编排器，例如子代理提示的文件夹或一个分散工作的技能，您可以指向 Claude 并要求一个执行相同操作的工作流。

<h4 id="dismiss-or-turn-off-the-keyword">
  忽略或关闭关键字
</h4>

如果您不打算启动工作流，在 macOS 上按 `Option+W` 或在 Windows 和 Linux 上按 `Alt+W` 来忽略此提示的突出显示，或在突出显示的关键字后面的光标处按退格键。要完全停止该关键字触发，请在 `/config` 中关闭 Ultracode 关键字触发。

<h4 id="where-the-keyword-works">
  关键字的工作位置
</h4>

该关键字仅在您自己输入的提示中选择加入：在交互式提示、IDE 扩展面板、[Remote Control](/docs/zh-CN/remote-control) 客户端或在 Agent SDK 应用程序中，该应用程序将您的键盘输入的 [`origin`](/docs/zh-CN/agent-sdk/typescript#sdkmessageorigin) 标记为 `{ kind: "human" }`。当它通过另一种方式到达会话时，它不会启动工作流：

* 使用 `-p` 传递的提示
* Agent SDK 应用程序发送的未标记为人类输入的提示
* 计划任务提示
* 中继到对话中的 webhook 有效负载或拉取请求评论

<Note>
  在 v2.1.210 之前，该关键字也从这些路由中的任何一个启动工作流，包括中继到对话中的 webhook 有效负载或拉取请求评论。
</Note>

<h3 id="let-claude-decide-with-ultracode">
  让 Claude 使用 ultracode 决定
</h3>

Ultracode 是一个 Claude Code 设置，它为会话启用自动工作流编排，在会话运行的任何[努力级别](/docs/zh-CN/model-config#adjust-effort-level)。启用它后，Claude 为每个实质性任务规划工作流，而不是等待您要求。在 Claude Code 提示处启用它：

```text wrap theme={null}
/effort ultracode
```

要启动已启用 ultracode 的会话，请使用 `claude --effort ultracode` 启动，这也会将努力级别设置为 `xhigh`。需要 Claude Code v2.1.203 或更高版本。

要从 `/effort` 滑块启用它，按 `Tab` 翻转 **Ultracode** 切换，然后按 `Enter` 应用它。[调整努力级别](/docs/zh-CN/model-config#adjust-effort-level)列出启用 ultracode 的路由。

启用 ultracode 后，Claude 决定任务何时值得工作流。单个请求可以变成一系列工作流：一个理解代码，一个进行更改，一个验证它。这适用于会话中的每个任务，所以每个请求使用更多令牌并花费比没有工作流的相同请求更长的时间。在订阅计划上，这些令牌会计入您的使用限制，所以启用 ultracode 的会话比关闭时进行相同工作更快达到会话或每周限制。

启用 ultracode 已经选择加入大型运行，所以启用它时这些检查不适用：

* 工作流运行时不会出现 [`Large workflow` 警告](#cost)
* 会话的[并发子代理限制](/docs/zh-CN/sub-agents#concurrent-subagent-limit)对 Claude 使用 Agent 工具生成的子代理不强制执行
* 在自动权限模式下，您不会被要求[批准第一个工作流启动](#approve-the-plan-before-it-runs)

`/effort ultracode` 持续当前会话；要让每个会话都以它开始，设置 [`ultracode`](/docs/zh-CN/settings-reference#ultracode) 设置。当您返回日常工作时，使用 `/effort ultracode off` 关闭它。`/effort` 滑块仅在 [ultracode 可用时](/docs/zh-CN/model-config#when-ultracode-is-available)提供切换。

<h3 id="approve-the-plan-before-it-runs">
  在运行前批准计划
</h3>

在 CLI 中，每次运行的提示显示计划的阶段和这些选项：

* **是，运行它**：启动运行
* **是，不再为 `<path>` 中的 `<name>` 询问**：启动，并从现在起跳过此项目中此工作流的此提示。Claude Code 在您按名称运行捆绑、保存或插件工作流时提供此选项，而不是为当前任务编写的脚本。
* **查看原始脚本**：在决定前读取脚本
* **否**：取消

`Ctrl+G` 在您的编辑器中打开脚本。选中**是，运行它**或**否**时，按 `Tab` 可为您的回答[添加评论](/docs/zh-CN/permissions#add-a-comment-when-you-answer-a-permission-prompt)。

您是否看到此提示取决于您的[权限模式](/docs/zh-CN/permission-modes)：

| 权限模式 | 何时提示您 |
| :- | :- |
| 自动 | 仅首次启动。任何**是**在您的用户设置中记录同意，之后启动无需提示。当 ultracode 启用时完全跳过 |
| 手动，接受编辑 | 每次运行，除非您已为此项目中的该工作流选择**是，不再询问** |
| 绕过权限 | Claude Code 不提示您。运行立即启动 |
| `claude -p`，Agent SDK | Claude Code 不提示您 |

在 `claude -p` 和 Agent SDK 中，Claude Code 从不显示此提示。它通过与会话其余部分相同的[权限评估](/docs/zh-CN/agent-sdk/permissions#how-permissions-are-evaluated)运行 Workflow 工具调用，所以拒绝规则、询问规则和 `dontAsk` 模式适用于启动，就像它们适用于每个工具调用一样。要让工作流在这些运行中启动，使用以下之一：

* **权限规则**：您的允许规则中的 `Workflow` 批准每个工作流，`Workflow(<name>)` 按名称批准一个保存的工作流。
* **自动权限模式**：[分类器](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)审查调用并可以批准它。
* **绕过权限模式**：Claude Code 批准调用。
* **一个 hook**：一个允许该调用的 [`PreToolUse`](/docs/zh-CN/hooks#pretooluse) hook 会批准它。
* **您的主机**：一个 [`--permission-prompt-tool`](/docs/zh-CN/cli-reference#cli-flags)，或者在使用 Agent SDK 时，一个 [`canUseTool`](/docs/zh-CN/agent-sdk/permissions) 回调批准它。

在桌面应用中，批准卡显示工作流名称、阶段列表和令牌使用警告，带有**一次**、**总是**和**拒绝**操作。进度视图出现在"后台任务"侧窗格中。

工作流生成的子代理使用您的[权限规则](/docs/zh-CN/settings-reference#permission-settings)，Claude Code 按[子代理运行的权限模式](/docs/zh-CN/sub-agents#permission-modes)下的规则选择它们的权限模式。要在长时间运行中避免提示，在启动前将代理需要的工具添加到您的允许规则。

<h3 id="save-the-workflow-for-reuse">
  保存工作流以供重用
</h3>

当 Claude 为您将重复的任务编写工作流时，您可以将该运行的脚本保存为命令。像您在每个分支上运行的审查这样的过程然后每次运行相同的编排。

运行 `/workflows`，选择您想保留的运行，然后按 `s`。在保存对话中，Tab 在两个保存位置之间切换：

* `.claude/workflows/` 在您的项目中：与克隆仓库的每个人共享
* `~/.claude/workflows/` 在您的主目录中：在每个项目中可用，仅对您可见。如果您设置了 [`CLAUDE_CONFIG_DIR`](/docs/zh-CN/env-vars)，此位置是该路径下的 `workflows/` 目录。

保存对话显示个人位置的已解析路径。

按 Enter 保存。工作流在未来会话中从任一位置作为 `/<name>` 运行。

Claude Code 在写入前检查保存位置是否有符号链接，并显示错误而不是通过一个写入。它检查的内容取决于您保存的位置：

* 项目位置：如果 `.claude`、`.claude/workflows` 或目标文件是符号链接，Claude Code 拒绝。
* 个人位置：Claude Code 仅在目标文件本身是符号链接时拒绝，所以由点文件工具管理的 `~/.claude` 目录仍然有效。

在 v2.1.216 之前，Claude Code 跟随链接，这可能会将文件放在您选择的位置之外。

在具有多个 `.claude/` 目录的单体仓库中，您可以将工作流保存在它们适用的包旁边。保存到项目位置会写入您的工作目录和仓库根之间已存在的最近的 `.claude/workflows/` 目录，或如果尚不存在则写入仓库根。项目工作流也从该路径上的每个 `.claude/workflows/` 加载，当多个定义相同名称时 Claude Code 运行最接近工作目录的那个。

如果项目工作流和个人工作流共享名称，项目工作流运行。

<h3 id="distribute-a-workflow-in-a-plugin">
  在插件中分发工作流
</h3>

要在团队或仓库中共享工作流，将其包含在[插件](/docs/zh-CN/plugins/overview)中。将脚本放在插件根目录的 `workflows/` 目录中，或使用 [`workflows` 清单字段](/docs/zh-CN/plugins/manifest-reference#fields)指向不同的位置。

插件工作流由插件名称命名空间。一个名为 `acme-tools` 的插件，其 `meta.name` 为 `release-audit` 的脚本作为 `/acme-tools:release-audit` 运行。

<h3 id="pass-input-to-a-saved-workflow">
  将输入传递给保存的工作流
</h3>

保存的工作流可以通过 `args` 参数接受输入。脚本将其读取为名为 `args` 的全局变量。使用此功能在调用时提供研究问题、目标路径列表或配置对象，而不是为每次运行编辑脚本。

以下提示使用问题编号列表运行保存的工作流：

```text wrap theme={null}
Run /triage-issues on issues 1024, 1025, and 1030
```

Claude 将列表作为结构化数据传递，所以脚本可以直接在 `args` 上调用数组和对象方法，无需先解析它。如果省略 `args`，脚本内的全局变量为 `undefined`。

<h2 id="example-workflow-prompts">
  工作流提示示例
</h2>

工作流最适合当任务大于一个代理可以在上下文中容纳的情况，或当相同的步骤需要在许多项目中运行时。下面的提示显示常见的形状。每一个都要求 Claude 为该任务编写并运行工作流；您不自己编写脚本。

<h3 id="audit-many-files-for-the-same-issue">
  审计许多文件以查找相同问题
</h3>

扇出每个文件一个代理，然后收集并验证发现。

```text wrap theme={null}
use a workflow to audit every route handler under src/routes/ for missing authentication checks, and adversarially verify each finding before reporting it
```

<h3 id="keep-fixing-until-a-check-passes">
  保持修复直到检查通过
</h3>

运行检查器，修复失败的内容，然后重复直到通过或停止取得进展。

```text wrap theme={null}
use a workflow to run npx tsc --noEmit and keep fixing the reported errors until the type check passes or two rounds in a row make no progress
```

<h3 id="migrate-many-files-in-parallel">
  并行迁移许多文件
</h3>

发现要迁移的文件，在隔离的副本中转换每个文件，以便编辑不会冲突，并验证每个结果。

```text wrap theme={null}
use a workflow to migrate every component under src/components/ from JavaScript to TypeScript, working on each file in its own isolated copy
```

<h3 id="review-every-changed-file-and-write-one-summary">
  审查每个更改的文件并写一份摘要
</h3>

为每个文件运行审查者，然后将所有发现交给一个代理，该代理对它们进行排名和去重。

```text wrap theme={null}
use a workflow to review every file changed in this PR for correctness issues, then merge the per-file findings into one ranked summary
```

<h3 id="research-a-topic-across-many-sources">
  跨许多来源研究一个主题
</h3>

在更改日志、问题和文档中扇出读者，然后综合。捆绑的 `/deep-research` 工作流执行此操作；您也可以描述一个更狭窄的版本。

```text wrap theme={null}
use a workflow to research how our three competitors handle rate limiting: read their public docs and recent changelog entries in parallel, then compare the approaches
```

<h3 id="find-issues-until-the-list-stops-growing">
  查找问题直到列表停止增长
</h3>

保持分轮搜索并在新轮次找不到任何新内容时停止。

```text wrap theme={null}
use a workflow to find flaky tests in this repo: run the suite repeatedly, record which tests fail intermittently, and stop once two rounds in a row find nothing new
```

<h3 id="what-the-saved-script-looks-like">
  保存的脚本看起来像什么
</h3>

当您[保存工作流](#save-the-workflow-for-reuse)时，`.claude/workflows/` 中的文件包含一个 `meta` 块，后跟编排子代理的脚本体。您通常不需要编辑它，但这是一个小的形状，所以您可以识别 Claude 生成的内容：

```javascript theme={null}
export const meta = {
  name: 'audit-routes',
  description: 'Audit every route handler for missing auth checks',
}

const found = await agent('List every .ts file under src/routes/.', {
  schema: { type: 'object', required: ['files'], properties: { files: { type: 'array', items: { type: 'string' } } } },
})

const audits = await pipeline(found.files, file =>
  agent(`Audit ${file} for missing authentication checks.`, { label: file }),
)

return audits.filter(Boolean)
```

主体是带有顶级 `await` 的纯 JavaScript。`agent()` 生成一个子代理，`pipeline()` 为列表中的每个项目运行一个，`parallel()` 同时运行一组代理任务并等待所有任务完成。

如果您在运行中途停止 `agent()` 调用或它遇到不可恢复的 API 错误，则 `agent()` 调用解析为 `null`。`pipeline()` 在结果数组中保留每个 `null`，这就是为什么示例以 `.filter(Boolean)` 结尾以删除这些条目，其中包括[每次尝试都停滞的 Agent](#when-an-agent-stalls-and-restarts) 所占的位置。

在[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)中，您的脚本传递给 `agent()` 的提示不会计为您的请求，当分类器审查该子代理的操作时，因为 Claude Code 将其标记为脚本计算的文本。

如果您在 `agent()` 调用上传递 `schema`，该子代理将返回与形状匹配的 JSON 而不是散文。Claude Code 在启动子代理之前检查架构：当它可以证明架构自相矛盾时，调用失败并显示一个错误，命名矛盾，子代理永远不会启动。它可以证明的一个矛盾是 `additionalProperties: false` 排除的 `required` 键。

如果子代理的输出在五次尝试后仍然无法通过验证，调用将失败并显示一个错误，其中包括最后的验证失败。要更改尝试次数，请设置 [`MAX_STRUCTURED_OUTPUT_RETRIES`](/docs/zh-CN/env-vars)。

<h3 id="edit-a-saved-script">
  编辑保存的脚本
</h3>

要更改[您保存的工作流](#save-the-workflow-for-reuse)，编辑其 `.js` 文件或要求 Claude 进行更改。在编辑或要求之前，运行 `/workflow-authoring` [捆绑技能](/docs/zh-CN/skills#bundled-skills)以加载 Claude 工作的脚本编写参考。该技能需要 Claude Code v2.1.248 或更高版本。

要在当前会话中运行编辑后的版本，运行 [`/reload-skills`](/docs/zh-CN/commands#all-commands) 以重新读取工作流目录，然后再次运行 `/<name>`。

Claude Code 在加载和运行脚本时对文件的每个部分应用这些规则：

* **`meta` 块**：将 `export const meta` 保持为第一个语句，并将其保持为带有 `name` 和 `description` 的纯对象字面量。如果它包含除字面值之外的任何内容，例如变量、函数调用或展开，Claude Code 会从 `/` 自动完成中删除 `/<name>`。
* **主体**：除了 `agent()`、`pipeline()` 和 `parallel()` 之外，您可以调用 `phase()` 在进度视图中对以下代理进行分组并添加标题，调用 `log()` 在阶段上方显示消息，并读取 [`args`](#pass-input-to-a-saved-workflow) 全局变量。如果主体有语法错误，Claude Code 会在您运行工作流时报告它。
* **`phases`**：如果您在 `meta` 中列出它们，为每个条目提供您传递给 `phase()` 的确切标题。没有条目的 `phase()` 标题会获得自己的进度组。
* **时间戳和随机性**：Claude Code 使脚本内的 `Date.now()`、`Math.random()` 和无参数 `new Date()` 抛出异常，以便[重新启动的运行](#resume-after-a-pause)重复相同的 `agent()` 调用。改为通过 `args` 传入时间戳。

您也可以编辑[单个运行的脚本](#how-a-workflow-runs)而不是保存的副本。[在暂停后恢复](#resume-after-a-pause)涵盖当您重新启动编辑的脚本时哪些代理再次运行。有关 Workflow 工具的输入，请参阅其在 [Agent SDK 参考](/docs/zh-CN/agent-sdk/typescript#workflow)中的条目。

<h2 id="how-a-workflow-runs">
  工作流如何运行
</h2>

工作流运行时在隔离的环境中执行脚本，与您的对话分离。中间结果保留在脚本变量中，而不是进入 Claude 的上下文。

每次运行都会将其脚本写入您会话目录下 `~/.claude/projects/` 中的文件。Claude 在运行开始时接收路径，因此您可以要求它提供路径。您可以打开该文件来读取 Claude 编写的编排，将其与之前运行的脚本进行对比，或编辑它并要求 Claude 从编辑后的版本重新启动。

Claude 只能从会话已允许读取的脚本文件启动工作流。要运行保存在工作目录外的脚本，请先使用 [`/add-dir`](/docs/zh-CN/permissions#working-directories) 或 [Read allow rule](/docs/zh-CN/permissions#read-and-edit) 添加其目录。

运行时在运行进行时跟踪每个代理的结果，这正是使运行在同一会话内 [可恢复](#resume-after-a-pause) 的原因。

<h3 id="prompt-caching-in-a-fan-out">
  扇出中的 prompt caching
</h3>

同一运行中的代理可以读取彼此的 [prompt cache](/docs/zh-CN/prompt-caching#subagents-and-the-cache)。两个使用相同模型、努力级别、代理类型、工具、输出架构和工作目录运行的代理会构建相同的工具和系统提示前缀，因此在匹配的兄弟代理响应开始后启动的代理会在其第一个请求中读取该兄弟代理的缓存。

工作流代理的请求落在主对话的 [cache TTL bucket](/docs/zh-CN/prompt-caching#which-ttl-each-request-gets) 之外，因此其缓存默认保持五分钟，包括在 Claude 订阅上。要将其保持一小时，请将 [`subagentPromptCacheTtl`](/docs/zh-CN/settings-reference#subagentpromptcachettl) 设置为 `1h`。API 以更高的费率计费 1 小时缓存写入。

当扇出同时启动多个匹配的代理时，Claude Code 会保留除第一个之外的所有代理，直到第一个代理的响应开始，然后一起释放保留的代理，以便它们的第一个请求读取共享前缀，而不是每个都未缓存地处理它。Claude Code 将保留限制在 [`CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS`](/docs/zh-CN/env-vars) 毫秒，默认为 `5000`。将其设置为 `0` 以禁用保留。

<h3 id="behavior-and-limits">
  行为和限制
</h3>

运行时应用以下约束：

| 约束 | 原因 |
| :- | :- |
| 无中途用户输入 | 运行仅在代理权限提示和 [使用限制等待](#when-a-run-hits-your-usage-limit) 时暂停。对于阶段之间的签署，将每个阶段作为其自己的工作流运行 |
| 工作流本身无直接文件系统或 shell 访问 | 代理读取、写入和运行命令。脚本协调代理 |
| 无模块加载：包含 `import()` 的脚本在运行开始前失败 | 脚本体是纯 JavaScript。将需要库的工作放在代理的任务中 |
| 最多 16 个并发代理，当 Claude Code 可用的 CPU 较少时更少，包括在 CPU 受限的容器内。要更改限制，请将 [`CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS`](/docs/zh-CN/env-vars#variables) 设置为 1 到 256 之间的值，这需要 Claude Code v2.1.269 或更高版本 | 限制本地资源使用 |
| 在扇出中，共享第一个代理的 prompt-cache 前缀的代理最多在其后 5 秒启动，默认情况下 | 除第一个外的所有代理都读取 [第一个代理缓存的前缀](#prompt-caching-in-a-fan-out)，而不是每个都未缓存地处理它 |
| 单个 `parallel()` 或 `pipeline()` 调用中最多 4,096 个项目：运行时以错误拒绝更长的列表 | 无声上限会在不告知脚本的情况下丢弃部分工作负载 |
| 每次运行总共 1,000 个代理 | 防止失控循环 |

<h2 id="manage-runs">
  管理运行
</h2>

运行启动后，您可以从 `/workflows` 视图管理它，或通过展开输入框下方任务面板中的其进度行来管理。

当您停止运行时，它会保留在任务面板中，直到其任何代理的进程仍在运行。如果您再次停止它，Claude Code 会重新向这些进程发送信号。

<h3 id="resume-after-a-pause">
  暂停后恢复
</h3>

从 `/workflows` 恢复暂停的运行，选择它并按 `p`。对于您停止的运行，要求 Claude 使用相同脚本重新启动工作流。如果来自已停止运行的代理尚未退出，Claude Code 会拒绝重新启动，直到它们退出，这样这些代理的第二个副本就不会与它们并行运行。

Claude Code 按代理启动的顺序重放运行，每个代理要么返回其保存的结果，要么再次运行：

* **已完成**：返回其保存的结果。第一个提示与之前运行不同的代理（因为您编辑了脚本或较早的代理返回了不同的内容）会再次运行，之后的每个代理也会再次运行，即使是已完成的代理。
* **停止时仍在运行**：重新开始。停止整个运行不会将任何代理计为失败。
* **失败**：再次运行，之后启动的每个代理也会再次运行，即使是已完成的代理。通过在 [`/workflows`](#watch-the-run) 中选择单个代理并按 `x` 来停止它，会将其计为失败。

最后一种情况意味着在扇出中间的失败会重新运行已经完成的工作。如果脚本按该顺序启动 A、B、C 和 D，并且 B 失败，重新启动会从缓存返回 A 并再次运行 B、C 和 D。

您可以在同一 Claude Code 会话中恢复运行。当您离开会话时，运行中的工作流会发生什么取决于您如何离开：

* 如果您[后台运行会话](/docs/zh-CN/agent-view#what-carries-over-when-you-background)，Claude Code 会在后台会话中以相同方式重放运行并继续它。
* 如果您在工作流运行时退出 Claude Code 并且[代理视图已打开](/docs/zh-CN/agent-view#from-inside-a-session)，退出对话框会提供 `Move to background and exit`，它以相同方式转移运行。如果您选择 `Exit and stop tasks` 或未提供该选项，运行会随会话停止。Claude Code 会将运行的保存结果保存在 `~/.claude/projects/` 中该会话的目录下，所以您使用 `claude --resume` 恢复的会话可以在您要求 Claude 重新启动工作流时重放它们。在您全新启动的会话中，Claude 没有较早的运行可以重新启动，会将工作流作为新运行启动。

在[云会话](/docs/zh-CN/claude-code-on-the-web)中，Claude Code 也会将运行的结果与会话的对话历史一起保存，当会话的 VM 被回收时，这些历史会保留。当您[重新打开这样的会话](/docs/zh-CN/claude-code-on-the-web#environment-expired)并要求 Claude 重新启动工作流时，已完成的代理仍会返回其保存的结果。

在本地和云会话中，当 Claude 重新启动较早的运行并且 Claude Code 根本找不到该运行的保存结果时，重新启动会失败并显示 `nothing to resume` 错误，而不是自动启动运行。要求 Claude 将工作流作为新运行启动。

<h3 id="when-a-run-hits-your-usage-limit">
  当运行达到您的使用限制时
</h3>

当代理达到您的 claude.ai [使用限制](/docs/zh-CN/interactive-mode#wait-for-a-usage-limit-to-reset)时，运行会暂停而不是该代理失败：达到限制的代理会等待重置，并且不会启动新代理。限制重置后不久，等待的代理会再次运行，运行会自动继续。需要 Claude Code v2.1.271 或更高版本；在较早的版本上，受影响的代理会失败。

当运行等待时，其在任务面板中的进度行和 [`/workflows`](#watch-the-run) 标题显示限制何时重置。

运行仅在以下所有条件都成立时暂停；当其中一个不成立时，受影响的代理会失败：

* 会话是交互式的并使用 claude.ai 订阅登录。运行不会在[非交互模式](/docs/zh-CN/headless)中使用 `claude -p` 或 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 暂停，在[后台会话](/docs/zh-CN/agent-view)中，或在 [Remote Control](/docs/zh-CN/remote-control) 或[代理团队](/docs/zh-CN/agent-teams)队友会话中。
* [`autoContinueAtUsageLimit`](/docs/zh-CN/settings-reference#autocontinueatusagelimit) 已打开，这是让会话本身[等待使用限制重置](/docs/zh-CN/interactive-mode#wait-for-a-usage-limit-to-reset)的相同设置。如果您在等待期间关闭它，等待会结束，等待的代理会失败。
* 限制在 24 小时内重置。每周限制可能重置得更远。
* 运行还没有等待过两次。当它第三次达到限制时，代理会失败。

<h3 id="when-an-agent-stalls-and-restarts">
  当 Agent 停滞并重启时
</h3>

如果某个 Agent 的输出停止到达足够长的时间，它会使用相同的提示词重新开始。在 [`/workflows`](#watch-the-run) 中，其名称会添加 `(retry 1)` 后缀，其详细信息会显示 `attempt 2 (stalled)`。重启是自动的，因此您无需执行任何操作。

新的尝试在开始时不带有停滞尝试的会话记录。停滞尝试已更改的文件保持更改状态，其消耗的 token 仍计入运行的总量。停滞窗口是 Claude Code 在结束尝试之前等待 Agent 输出的时长。Agent 等待其自身工具调用或等待[用量限制重置](#when-a-run-hits-your-usage-limit)所花费的时间不计入停滞窗口。

一个 Agent 最多重启五次，包括您使用 `r` 请求的任何重启。如果第六次尝试也停滞，`agent()` 调用会失败，错误的开头会说明原因：

* `agent stalled on all 6 attempts`：每次尝试在整个窗口内都没有输出。如果 Agent 的工作使其保持静默这么长时间，请延长窗口
* `agent lost its reply on all 6 attempts`：每次尝试的响应流都变为静默，Claude Code 放弃了等待。延长停滞窗口没有帮助，因为[流式空闲看门狗](/docs/zh-CN/network-config#streaming-idle-watchdogs)先结束了响应，而 `CLAUDE_STREAM_IDLE_TIMEOUT_MS` 设置该看门狗的超时时间
* `agent abandoned after 6 attempts`：各次尝试以不同方式结束，错误会按顺序列出这些方式

要在窗口结束前给 Agent 更多时间来产生输出：

* **单个 Agent**：在其 `agent()` 调用中以毫秒为单位传入 `stallMs`，例如 `agent(prompt, { stallMs: 1800000 })` 表示 30 分钟
* **所有 Agent**：设置 [`CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS`](/docs/zh-CN/env-vars#variables)，它也适用于工作流之外的子代理

失败后运行是否继续取决于您的脚本如何调用该 Agent：

* **在 [`parallel()` 或 `pipeline()`](#what-the-saved-script-looks-like) 内部**：运行继续，用 `null` 代替该 Agent 的结果
* **直接 await**：运行以该错误结束

要重试，请要求 Claude 重新启动工作流。[暂停后恢复](#resume-after-a-pause)介绍了哪些内容会再次运行。

<h3 id="cost">
  成本
</h3>

工作流生成许多代理，所以单次运行可以使用比在对话中处理相同任务更多的令牌。运行计入您的计划使用和速率限制。

要在提交大型任务前评估支出，请先在小范围上运行工作流：一个目录而不是整个仓库，或一个狭窄的问题而不是一个宽泛的问题。`/workflows` 视图显示每个代理的令牌使用情况，随着运行进行，您可以随时在那里停止运行，通常不会丢失已完成的工作。[暂停后恢复](#resume-after-a-pause)涵盖了停止的运行保留的内容。运行时的[代理上限](#behavior-and-limits)限制单次运行可以生成多少个代理，这限制了失控脚本的成本。要保持运行的代理数量较少，选择 `small` [大小指南](#set-a-size-guideline)。

Claude Code 还会标记增长异常大的运行。当工作流调度超过 25 个代理，或其预计令牌总数超过 150 万时，输入框下方任务面板中的其进度行显示 `Large workflow` 警告。警告指向您可以停止运行的 [`/workflows`](#watch-the-run)。

警告是建议性的：它不会暂停或限制运行。当您看到它时，两个设置会改变：

* 如果您自己选择[大小指南](#set-a-size-guideline)，其代理计数替换 25 个代理的阈值。内置默认指南将阈值保留在 25。
* 启用[ultracode](#let-claude-decide-with-ultracode)的会话不显示警告，因为打开 ultracode 已经让您选择加入大型运行。

Claude Code 按照它用于子代理的相同[顺序选择每个工作流代理的模型](/docs/zh-CN/sub-agents#choose-a-model)。脚本为阶段命名的模型在该顺序中计为每次调用的模型。当没有其他东西分配一个时，代理在您的会话模型上运行。

要控制模型成本：

* 在大型运行前检查 `/model`，如果您通常为日常工作切换到较小的模型
* 当您描述任务时，要求 Claude 为不需要最强模型的阶段使用较小的模型

当您组织的 [`availableModels` 允许列表](/docs/zh-CN/model-config#restrict-model-selection)阻止脚本为代理请求的模型时，该代理会改为在替代模型上运行，遵循与子代理相同的[替代规则](/docs/zh-CN/sub-agents#choose-a-model)。[`/workflows`](#watch-the-run) 中的运行进度视图显示一个警告，命名请求的和替代的模型。

<h3 id="set-a-size-guideline">
  设置大小指南
</h3>

大小指南告诉 Claude 在编写动态工作流时应该针对多少个代理。Claude Code 将指南作为建议而不是上限发送给 Claude，所以调用不同规模的提示仍然会覆盖它。需要 Claude Code v2.1.202 或更高版本。

每个值映射到一个代理计数：

| 值 | Claude 针对的代理计数 |
| :- | :- |
| `unrestricted` | 无指南：Claude 根据任务调整工作流大小 |
| `small` | 少于 5 个代理 |
| `medium` | 少于 10 个代理 |
| `large` | 少于 50 个代理 |

默认值是 `medium`，或当您在使用 Claude Code v2.1.271 或更高版本的 Pro 计划上登录时为 `small`。在您选择值之前，`/config` 行将值标记为默认值，工作流的 `Running in background` 行命名生效的大小。需要 Claude Code v2.1.219 或更高版本；较早的版本默认为 `unrestricted`。

要更改指南，在 `/config` 中为 Dynamic workflow size 设置选择一个值，或运行 `/config workflowSizeGuideline=small`。在 v2.1.219 及更高版本上，您也可以在任何设置文件中设置 [`workflowSizeGuideline` 键](/docs/zh-CN/settings-reference#workflowsizeguideline)；该值优先于 `/config`，当设置文件提供一个时，Claude Code 会隐藏 `/config` 行。

更改在下一个提示时生效。[运行时代理上限](#behavior-and-limits)仍然适用，无论设置如何。

<h3 id="turn-workflows-off">
  关闭工作流
</h3>

工作流在 CLI、桌面应用、IDE 扩展、[非交互模式](/docs/zh-CN/headless)与 `claude -p` 和 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 中可用。相同的禁用设置在每个表面上应用。

要为自己关闭工作流：

* 在 `/config` 中切换 Dynamic workflows 关闭。在会话中持续。
* 在 `~/.claude/settings.json` 中设置 `"disableWorkflows": true`。在会话中持续。
* 设置 `CLAUDE_CODE_DISABLE_WORKFLOWS=1`。在启动时读取，所以它在您设置它的任何地方应用。

要为整个组织关闭工作流，在[托管设置](/docs/zh-CN/server-managed-settings)中设置 `"disableWorkflows": true`，或使用[Claude Code 管理员设置](https://claude.ai/admin-settings/claude-code)页面上的切换。

当工作流被禁用时：

* `/workflows`、工作流命令和 `/workflow-authoring` skill 不可用
* `ultracode` 关键字不再触发运行，**Ultracode** 开关会从 `/effort` 中移除

已在进行中的运行会继续进行。

关闭工作流也会使[ultracode](#let-claude-decide-with-ultracode)不可用。没有托管设置单独排除 ultracode：无论它在哪里[可用](/docs/zh-CN/model-config#when-ultracode-is-available)，用户可以使用 `/effort ultracode` 打开它。[努力上限](/docs/zh-CN/model-config#organization-effort-limits)降低了启用 ultracode 的会话运行的努力级别，但不会关闭 ultracode。

<h2 id="related-resources">
  相关资源
</h2>

* [并行运行代理](/docs/zh-CN/agents)：比较子代理、代理视图、代理团队和工作流
* [创建自定义子代理](/docs/zh-CN/sub-agents)：工作流编排的工作者原语
* [管理成本](/docs/zh-CN/costs)：多代理运行如何计入使用限制
