> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Ship

> 了解用于 GitHub Pull Request 的 Claude Ship Agent：Code Review、PR Steward 和 Claude Approvals

Claude Ship 是一组 Agent，可帮助您团队的 GitHub Pull Request 做好合并准备：

* [Code Review](https://code.claude.com/docs/zh-CN/code-review.md)：查找逻辑错误、安全漏洞和边界情况处理失误等问题
* [PR Steward](https://code.claude.com/docs/zh-CN/pr-steward.md)：处理审查反馈和失败的检查
* [Claude Approvals](https://code.claude.com/docs/zh-CN/approvals.md)：根据您编写的审批策略检查 Pull Request

它们协同工作，可以让一个 Pull Request 依次完成审查、修复和审批决定，您的团队无需手动管理每个步骤。哪些内容会被合并，由您的设置和 GitHub 分支规则决定。Claude Ship 适用于 [Team 和 Enterprise 计划](#who-can-use-claude-ship)。

要启用这些 Agent，请前往[设置 Claude Ship](#set-up-claude-ship)。

> [!NOTE]
>
> 要在本地对您自己的某个 Pull Request 进行审查和修复，请在 Claude Code 中运行 [`/ship`](https://code.claude.com/docs/zh-CN/ship-command)。

## Claude Ship Agent

下图展示了每个 Agent 在 Pull Request 中承担的部分，以及仍由您和 GitHub 负责的部分：

![启用全部三个 Claude Ship Agent 的 Pull Request 示意图：Code Review 发现问题，PR Steward 推送修复，一次修复可以触发另一次审查。Claude Approvals 应用您的策略，合并遵循您的分支规则。](https://mintcdn.com/claude-code/sMH7RDpTvyWlAkrg/images/claude-ship-overview.svg?fit=max\&auto=format\&n=sMH7RDpTvyWlAkrg\&q=85\&s=6c972cdcb9dfc1c7a9a54e421bcf35a5)

> [!NOTE]
>
> Claude Ship 使用 AI，可能会遗漏 bug、安全漏洞或其他问题。

### Code Review 发现问题

[Code Review](https://code.claude.com/docs/zh-CN/code-review.md) 会结合周围的代码阅读变更。发现的问题以行内评论的形式出现在相关代码行上，并按严重程度排序。

### PR Steward 推送修复

[PR Steward](https://code.claude.com/docs/zh-CN/pr-steward.md) 处理失败的检查、合并冲突，以及来自人员和 Code Review 等审查机器人的审查评论。它会推送包含其修复的提交。

Steward 的设计是不批准也不合并 Pull Request。请使用分支保护，要求在任何内容合并之前获得您所需的审批。请参阅[审批和合并的限制](https://code.claude.com/docs/zh-CN/pr-steward-security.md#limits-on-approvals-and-merges)。

### Claude Approvals 应用您的策略

[Claude Approvals](https://code.claude.com/docs/zh-CN/approvals.md) 是一项检查，用于报告还有谁需要审批。您编写它的策略文件，该文件可以设定对某个路径的更改需要多少人审批，以及 Claude 可以在哪些地方发布批准性审查。只有在您[将其设为 GitHub 中的必需检查](https://code.claude.com/docs/zh-CN/approvals-setup.md#enforce-your-policy-and-require-claude-approvals)的地方，该检查才会阻止合并，并且在观察模式下通常不会阻止。

> [!WARNING]
>
> 如果您将 GitHub 自动合并或合并队列与不要求人员审批的策略一起使用，变更可能会在无人操作的情况下被合并。请参阅[未经人工审查的合并](https://code.claude.com/docs/zh-CN/approvals-github-rules.md#merges-without-human-review)。

## 设置 Claude Ship

前往 [**Organization settings > Claude Ship**](https://claude.ai/admin-settings/claude-ship) 查看 Claude Ship 的设置。您需要拥有 [Owner 角色](https://code.claude.com/docs/zh-CN/server-managed-settings.md#access-control)。

请在一个仓库中按以下顺序逐个启用 Agent：

1. [设置 Code Review](https://code.claude.com/docs/zh-CN/code-review-setup.md)
2. [设置 PR Steward](https://code.claude.com/docs/zh-CN/pr-steward-setup.md)。对于选择 PR Steward 何时启动的设置，请先从 [**Manual (@claude steward)**](https://code.claude.com/docs/zh-CN/pr-steward-setup.md#choose-when-pr-steward-starts-in-each-repository) 开始。在您设置支出限额之前，PR Steward 本身没有支出限额。
3. [设置 Claude Approvals](https://code.claude.com/docs/zh-CN/approvals-setup.md)。仓库中的策略文件会启动它，因此请查看[谁可以启用它](https://code.claude.com/docs/zh-CN/approvals.md#who-can-turn-approvals-on-or-off)。请从观察模式开始，在该模式下，**Claude Approvals** 检查会报告您的策略将做出的决定。观察模式会计费。请参阅 [Approvals 的费用](https://code.claude.com/docs/zh-CN/approvals-setup.md#what-approvals-costs)。

### 如果您已在使用 Code Review

Code Review 的设置已移至 [**Organization settings > Claude Ship**](https://claude.ai/admin-settings/claude-ship)。

Claude Approvals 策略文件 `.claude/approvals.yml` 会改变 Code Review 自动审查哪些 Pull Request。一旦该文件位于默认分支上，无论处于观察模式还是强制执行模式，在没有匹配规则指定 `claude/code_review` 的地方，自动审查通常会停止。要保留自动审查，请[将 `claude/code_review` 添加到规则中](https://code.claude.com/docs/zh-CN/approvals-policy#advisory)。

## 计划和计费

Claude Ship 适用于使用 Team 和 Enterprise 计划的组织。

### 谁可以使用 Claude Ship

Code Review 已正式发布。PR Steward 和 Claude Approvals 处于公开测试版阶段。启用了 [Zero Data Retention](https://code.claude.com/docs/zh-CN/zero-data-retention.md)、应用了 [HIPAA 配置](https://code.claude.com/docs/zh-CN/hipaa-setup.md)或使用客户管理加密密钥的组织无法使用这些 Agent。Approvals 还有[更多限制](https://code.claude.com/docs/zh-CN/approvals.md#availability)。

### 每个 Claude Ship Agent 如何计费

每个 Agent 根据 token 使用量，通过您组织的[使用额度](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)计费，与您计划中包含的用量分开计算。Approvals 会对[分类器](https://code.claude.com/docs/zh-CN/approvals-classifiers.md)运行以及策略要求的 Code Review 计费。

> [!NOTE]
>
> 符合条件的 Enterprise 组织可以领取 Claude Ship 促销额度。有关资格、金额和日期，请参阅[额度条款](https://support.claude.com/en/articles/17603594-free-code-review-promotional-credits-for-claude-enterprise)。

如果您在 [**Organization settings > Usage**](https://claude.ai/admin-settings/usage) 中关闭使用额度，已启用的 Agent 会继续运行并向您的组织计费。要停止其费用，请按照[关闭 Claude Ship](#turn-off-claude-ship) 操作。

查看每个 Agent 的费用：

* [Code Review](https://code.claude.com/docs/zh-CN/code-review-costs.md)
* [PR Steward](https://code.claude.com/docs/zh-CN/pr-steward-setup.md#set-pr-steward’s-spend-limits)
* [Claude Approvals](https://code.claude.com/docs/zh-CN/approvals-setup.md#what-approvals-costs)

## 关闭 Claude Ship

请先关闭 Approvals，再关闭 Code Review，因为即使 Code Review 已关闭，策略仍可能启动计费的审查：

1. [关闭 Approvals](https://code.claude.com/docs/zh-CN/approvals-setup.md#turn-off-approvals)
2. [关闭 PR Steward](https://code.claude.com/docs/zh-CN/pr-steward-setup.md#turn-off-pr-steward)
3. [关闭 Code Review](https://code.claude.com/docs/zh-CN/code-review-setup.md#turn-off-code-review-or-remove-a-repository)

这些步骤不会关闭 `/ship` 和 `/steward` 命令。请参阅[如何关闭它们](https://code.claude.com/docs/zh-CN/ship-command.md#turn-off-%2Fship-and-%2Fsteward-for-your-organization)。

## 相关资源

* [GitHub Actions](https://code.claude.com/docs/zh-CN/github-actions.md) 和 [GitLab CI/CD](https://code.claude.com/docs/zh-CN/gitlab-ci-cd.md)：在您自己的 CI 中运行 Claude Code
* [在本地审查代码](https://code.claude.com/docs/zh-CN/code-review-local.md)：在推送之前于终端中获取审查
