> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 第37周 · 2026年9月7日–11日

> 使用 claude plugin eval 测试您的插件，并将 Claude Code Desktop 窗格弹出到各自的窗口中。

<div className="digest-meta">
  <span>发布版本 <a href="/docs/en/changelog#2-1-263">v2.1.263 → v2.1.269</a></span>
  <span>2 项功能 · 9月7日–11日</span>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">使用 claude plugin eval 测试插件</span>
    <span className="digest-feature-pill">v2.1.269</span>
  </div>

  <p className="digest-feature-lede"><code>claude plugin eval</code> 针对一套测试用例运行您的插件，对结果进行评分，默认情况下每个用例都会再次运行一次（不使用插件），以便您可以看到它的贡献。<code>claude plugin eval init</code> 询问您什么是好的结果，然后提议测试用例和对其进行评分的检查，尝试一次该套件，并写入文件。每次运行，以及每个有第二个模型判断回复的检查，都是您账户上的真实模型调用。</p>

  <Frame>
    <img className="w-full" src="https://mintcdn.com/claude-code/f9HTZGyMtxIFOUgt/images/whats-new/plugin-eval.jpg?fit=max&auto=format&n=f9HTZGyMtxIFOUgt&q=85&s=913066f6d4a2a15426e98a627802f47f" alt="claude plugin eval 的终端输出：一个包含七个用例的表格，每个用例都显示有插件和无插件的分数、两者之间的差值、运行次数和成本，后面是一个汇总行，显示平均差值、总持续时间和总成本" width="1600" height="900" data-path="images/whats-new/plugin-eval.jpg" />
  </Frame>

  <p className="digest-feature-try">从您的插件根目录，让 Claude 起草该套件：</p>

  ```bash terminal theme={null}
  claude plugin eval init
  ```

  <p className="digest-feature-try">当 Claude 告诉您该套件已准备好时，退出 <code>claude plugin eval init</code> 打开的会话，并运行 <code>claude plugin eval .</code> 来对每个用例进行评分。汇总表在您的终端中打印，<code>evals/results/</code> 下的 <code>report.html</code> 包含每次运行的详细信息。</p>

  <a className="digest-feature-link" href="/docs/zh-CN/plugin-evals">使用 evals 测试插件</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">将 Desktop 窗格弹出到各自的窗口中</span>
    <span className="digest-feature-pill">Desktop</span>
  </div>

  <p className="digest-feature-lede">在 Claude Code Desktop 应用中，您可以将任何窗格弹出到其自己的窗口中。将 diff 或终端拖到第二个屏幕，同时 Claude 在主窗口中继续工作，然后在完成后将窗格停靠回去。</p>

  <Frame>
    <video autoPlay muted loop playsInline className="w-full" src="https://mintcdn.com/claude-code/f9HTZGyMtxIFOUgt/images/whats-new/desktop-pop-out-panes.mp4?fit=max&auto=format&n=f9HTZGyMtxIFOUgt&q=85&s=ff3770dd09bb15ed9cf17a460f3d1e23" data-path="images/whats-new/desktop-pop-out-panes.mp4" />
  </Frame>

  <a className="digest-feature-link" href="/docs/zh-CN/desktop#arrange-your-workspace">整理您的工作区</a>
</div>

<div className="digest-wins">
  <p className="digest-wins-title">其他改进</p>

  <div className="digest-wins-grid">
    <div>在顶级或 <code>modelSettings</code> 下按模型设置 <a href="/docs/zh-CN/settings-reference#maxeffortlevel"><code>maxEffortLevel</code></a> 以限制每个提供商（包括 Amazon Bedrock、Google Cloud 的 Agent Platform 和 Microsoft Foundry）上的努力级别；任何更高的级别都以上限运行</div>
    <div>将 `--plugin-dir` 指向一个插件文件夹，以 <a href="/docs/zh-CN/plugins/create#load-a-directory-or-archive-for-one-session">加载每个具有清单的直接子文件夹</a></div>
    <div>如果 WebFetch 在五分钟内未完成下载页面，<a href="/docs/zh-CN/tools-reference#webfetch-tool-behavior">获取失败并显示截止时间错误</a>，而不是挂起；设置 <code>CLAUDE\_CODE\_WEBFETCH\_DEADLINE\_MS</code> 以更改截止时间，或设置为 <code>0</code> 以移除限制</div>
    <div>将 `--json` 传递给 <code>claude plugin install</code>、<code>uninstall</code>、<code>update</code>、<code>enable</code> 或 <code>disable</code> 以将结果打印为 <a href="/docs/zh-CN/plugins/cli-reference#plugin-json-result">stdout 最后一行的一个 JSON 对象</a></div>
    <div>当自动模式分类器阻止一个操作时，Claude 收到的原因 <a href="/docs/zh-CN/auto-mode-config#fix-a-denial-with-an-allow-rule-an-environment-entry-or-a-retry">通常会命名匹配的规则</a>，例如 <code>\[Data Exfiltration]</code></div>
    <div>当您在提示中途键入 <code>/</code> 时，您现在可以从 <a href="/docs/zh-CN/interactive-mode#complete-a-command-mid-prompt">匹配命令的列表</a>中选择，而不是单个建议。该列表在全屏渲染中键入时打开。插件技能也可以按其名称（不带插件前缀）进行匹配</div>
    <div>在 VS Code 扩展中，单击提示框底部的代理计数以打开 <a href="/docs/zh-CN/vs-code#use-the-prompt-box">代理地图</a>，您可以在其中打开子代理的只读记录或停止它</div>
    <div>在 VS Code 扩展中，在命令菜单的"自定义"部分中选择 <strong>Hooks</strong> 或 <strong>Permissions</strong> 以 <a href="/docs/zh-CN/vs-code#use-the-prompt-box">在您的用户、项目和本地设置中添加或删除 hooks 和权限规则</a></div>
    <div>Claude 可以选择一个 <a href="/docs/zh-CN/artifacts#create-an-artifact">浏览器标签图标</a>来匹配它发布的每个工件</div>
    <div>在 Claude Code 网页版中，在 Claude 读取之前在云会话中取回一条排队的消息：从队列中删除它，或按 <code>Esc</code> 或 <code>Up</code>，文本返回到消息框</div>
  </div>
</div>

[v2.1.263–v2.1.269 的完整更新日志 →](/docs/en/changelog#2-1-263)
