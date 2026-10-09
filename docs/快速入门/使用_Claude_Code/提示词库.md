> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 提示词库

> 复制粘贴提示词到 Claude Code，按任务和角色标记。

export const PromptLibrary = ({text = {}, labels = {}, tagLabels = {}, phaseLabels = {}, sourceLabels = {}, catLabels = {}}) => {
  const RAW = useMemo(() => [{
    id: 'get-oriented-in-a',
    sdlc: 'discover',
    cat: 'Onboard',
    startN: 1,
    roles: [],
    prompt: 'give me an overview of this codebase: architecture, key directories, and how the pieces connect',
    nextHref: '/en/memory',
    src: 'workflows'
  }, {
    id: 'explain-unfamiliar-code',
    sdlc: 'discover',
    cat: 'Understand',
    roles: [],
    prompt: 'explain what {path} does and how data flows through it. write it up as {format}',
    slots: {
      path: 'src/scheduler/queue.ts',
      format: 'an HTML page with a diagram, then open it in my browser'
    },
    nextHref: '/en/output-styles',
    src: 'workflows'
  }, {
    id: 'find-where-something-happens',
    sdlc: 'discover',
    cat: 'Understand',
    startN: 2,
    roles: [],
    prompt: 'where do we {behavior}?',
    slots: {
      behavior: 'validate uploaded file types'
    },
    src: 'workflows'
  }, {
    id: 'see-what-depends-on',
    sdlc: 'discover',
    cat: 'Understand',
    roles: [],
    prompt: 'what would break if I deleted {target}?',
    slots: {
      target: 'the retryWithBackoff helper'
    },
    src: 'workflows'
  }, {
    id: 'trace-how-code-evolved',
    sdlc: 'discover',
    cat: 'Understand',
    roles: [],
    prompt: 'look through the commit history of {path} and summarize how it evolved and why',
    slots: {
      path: 'internal/auth/session.go'
    },
    src: 'best-practices'
  }, {
    id: 'scope-a-change-before',
    sdlc: 'discover',
    cat: 'Understand',
    roles: ['pm', 'design'],
    prompt: 'which files would I need to touch to {change}?',
    slots: {
      change: 'add a dark mode toggle to settings'
    },
    src: 'teams'
  }, {
    id: 'ask-the-codebase-a',
    sdlc: 'discover',
    cat: 'Understand',
    roles: ['pm'],
    prompt: 'I am a {role}. walk me through what happens when a user {action}, from the UI down to the result',
    slots: {
      role: 'PM',
      action: 'clicks Export to PDF'
    },
    nextHref: '/en/output-styles',
    src: 'teams'
  }, {
    id: 'plan-a-multi-file',
    sdlc: 'design',
    cat: 'Plan',
    roles: ['pm', 'design'],
    prompt: 'plan how to refactor the {target} to {goal}. list the files you would change, but don\'t edit anything yet',
    slots: {
      target: 'payment module',
      goal: 'support multiple currencies'
    },
    src: 'workflows'
  }, {
    id: 'draft-a-spec-by',
    sdlc: 'design',
    cat: 'Plan',
    roles: ['pm'],
    prompt: 'I want to build {feature}. interview me about implementation, UX, edge cases, and tradeoffs until we have covered everything, then write the spec to SPEC.md',
    slots: {
      feature: 'per-workspace rate limits'
    },
    nextHref: '/en/skills',
    src: 'best-practices'
  }, {
    id: 'turn-a-meeting-into',
    sdlc: 'design',
    cat: 'Plan',
    roles: ['pm'],
    prompt: 'read {input} and write up the action items, then create a ticket in {tracker} for each one, with acceptance criteria',
    slots: {
      input: '@meeting-notes.md',
      tracker: 'our issue tracker'
    },
    needs: 'tracker',
    nextHref: '/en/skills',
    src: 'teams'
  }, {
    id: 'map-edge-cases-before',
    sdlc: 'design',
    cat: 'Plan',
    roles: ['design', 'pm'],
    prompt: 'list the error states, empty states, and edge cases for {feature} that the design needs to cover',
    slots: {
      feature: 'the file upload flow'
    },
    src: 'teams'
  }, {
    id: 'turn-a-mockup-into',
    sdlc: 'design',
    cat: 'Prototype',
    roles: ['design', 'pm', 'marketing'],
    paste: 'mockup',
    prompt: 'here is a mockup. build a working prototype I can click through, matching the layout and states shown',
    src: 'teams'
  }, {
    id: 'implement-from-a-screenshot',
    sdlc: 'design',
    cat: 'Prototype',
    roles: ['design'],
    paste: 'design',
    needs: 'browser',
    prompt: 'implement this design, then take a screenshot of the result, compare it to the original, and fix any differences',
    nextHref: '/en/goal',
    src: 'best-practices'
  }, {
    id: 'follow-an-existing-pattern',
    sdlc: 'build',
    cat: 'Implement',
    roles: [],
    prompt: 'look at how {example} is implemented to understand the pattern, then build {new} the same way',
    slots: {
      example: 'the existing webhook handler',
      new: 'a payments webhook handler'
    },
    nextHref: '/en/memory',
    src: 'best-practices'
  }, {
    id: 'generate-docs-for-code',
    sdlc: 'build',
    cat: 'Implement',
    roles: ['docs'],
    prompt: 'find {scope} without {format} comments and add them, matching the style already used in the file',
    slots: {
      scope: 'the public functions in src/auth/',
      format: 'JSDoc'
    },
    src: 'workflows'
  }, {
    id: 'add-a-small-well',
    sdlc: 'build',
    cat: 'Implement',
    roles: [],
    prompt: 'add a {endpoint} endpoint that returns {payload}',
    slots: {
      endpoint: '/health',
      payload: 'the app version and uptime'
    },
    src: 'workflows'
  }, {
    id: 'build-a-small-internal',
    sdlc: 'build',
    cat: 'Implement',
    roles: ['pm', 'design', 'marketing', 'docs'],
    prompt: 'create a {tool} using HTML, CSS, and vanilla JavaScript, then open it in my browser',
    slots: {
      tool: 'drag-and-drop Kanban board with three columns'
    },
    src: 'teams'
  }, {
    id: 'work-an-issue-end',
    sdlc: 'build',
    cat: 'Implement',
    roles: [],
    prompt: 'read issue #{issue}, implement the fix, and run the tests',
    slots: {
      issue: '312'
    },
    needs: 'gh',
    src: 'workflows'
  }, {
    id: 'find-and-update-copy',
    sdlc: 'build',
    cat: 'Implement',
    roles: ['design', 'docs', 'marketing'],
    prompt: 'find every place we say "{copy}" or a close variant, show me each one in context, then update them all to "{new}". leave tests and the changelog alone',
    slots: {
      copy: 'Sign up free',
      new: 'Start free trial'
    },
    src: 'teams'
  }, {
    id: 'draft-from-past-examples',
    sdlc: 'build',
    cat: 'Implement',
    roles: ['docs', 'marketing', 'pm'],
    prompt: 'read the {examples} in {folder} to learn the structure and voice, then draft a new one for {topic}',
    slots: {
      examples: 'privacy impact assessments',
      folder: 'legal/pia/',
      topic: 'the new analytics integration'
    },
    nextHref: '/en/skills',
    src: 'legal'
  }, {
    id: 'write-tests-run-them',
    sdlc: 'build',
    cat: 'Test',
    startN: 4,
    roles: [],
    prompt: 'write tests for {path}, run them, and fix any failures',
    slots: {
      path: 'app/parsers/feed.py'
    },
    nextHref: '/en/memory',
    src: 'workflows'
  }, {
    id: 'drive-implementation-from-tests',
    sdlc: 'build',
    cat: 'Test',
    roles: [],
    prompt: 'write tests for {feature} first, then implement it until they pass',
    slots: {
      feature: 'the password reset flow'
    },
    src: 'ebook'
  }, {
    id: 'fill-gaps-from-a',
    sdlc: 'build',
    cat: 'Test',
    roles: [],
    prompt: 'read {report} and add tests for the lowest-covered files until each is above {target}%',
    slots: {
      report: 'coverage/coverage-summary.json',
      target: '80'
    },
    nextHref: '/en/goal',
    src: 'workflows'
  }, {
    id: 'migrate-a-pattern-across',
    sdlc: 'build',
    cat: 'Refactor',
    roles: [],
    prompt: 'migrate everything from {from} to {to}: identify every place that needs to change, then make the changes',
    slots: {
      from: 'the old logging API',
      to: 'the structured logger'
    },
    src: 'workflows'
  }, {
    id: 'port-code-between-languages',
    sdlc: 'build',
    cat: 'Refactor',
    roles: [],
    prompt: 'port {source} to {target}, keeping the same {keep}',
    slots: {
      source: 'this Python module',
      target: 'Rust',
      keep: 'public API and test behavior'
    },
    src: 'teams'
  }, {
    id: 'optimize-against-a-measurable',
    sdlc: 'build',
    cat: 'Refactor',
    roles: ['data'],
    prompt: 'optimize {target} to bring {metric} from {current} down to under {goal}',
    slots: {
      target: 'the search query',
      metric: 'p95 latency',
      current: '2s',
      goal: '500ms'
    },
    nextHref: '/en/goal',
    src: 'ebook'
  }, {
    id: 'fix-a-precise-visual',
    sdlc: 'build',
    cat: 'Refactor',
    roles: ['design'],
    prompt: 'the {element} extends {amount} beyond the {container} on {viewport}. fix it.',
    slots: {
      element: 'login button',
      amount: '20px',
      container: 'card border',
      viewport: 'mobile'
    },
    nextHref: '/en/desktop#preview-your-app',
    src: 'ebook'
  }, {
    id: 'review-your-changes-before',
    sdlc: 'build',
    cat: 'Review',
    startN: 5,
    roles: [],
    prompt: 'review my uncommitted changes and flag anything that looks risky before I commit',
    nextHref: '/en/commands',
    src: 'workflows'
  }, {
    id: 'review-a-pull-request',
    sdlc: 'build',
    cat: 'Review',
    roles: [],
    prompt: 'review PR #{pr} and summarize what changed, then list any concerns',
    slots: {
      pr: '247'
    },
    needs: 'gh',
    nextHref: '/en/code-review',
    src: 'workflows'
  }, {
    id: 'review-infrastructure-changes-before',
    sdlc: 'build',
    cat: 'Review',
    roles: ['security', 'ops'],
    paste: 'plan',
    prompt: 'here is my Terraform plan output. what is this going to do, and is anything here going to cause problems?',
    src: 'teams'
  }, {
    id: 'run-a-security-review',
    sdlc: 'build',
    cat: 'Review',
    roles: ['security'],
    prompt: 'use a subagent to review {path} for security issues and report what it finds',
    slots: {
      path: 'src/api/'
    },
    nextHref: '/en/sub-agents',
    src: 'best-practices'
  }, {
    id: 'review-content-before-sending',
    sdlc: 'build',
    cat: 'Review',
    roles: ['marketing', 'docs'],
    prompt: 'review {file} for {concerns} and list anything I should fix before it goes to {reviewer}',
    slots: {
      file: 'launch-post.md',
      concerns: 'unsupported claims, missing attributions, and brand-guideline issues',
      reviewer: 'legal'
    },
    nextHref: '/en/skills',
    src: 'legal'
  }, {
    id: 'course-correct-a-wrong',
    sdlc: 'build',
    cat: 'Steer',
    roles: [],
    prompt: 'that is not right: {feedback}. try a different approach',
    slots: {
      feedback: 'the function signature needs to stay backward-compatible'
    },
    nextHref: '/en/checkpointing',
    src: 'best-practices'
  }, {
    id: 'narrow-the-scope-of',
    sdlc: 'build',
    cat: 'Steer',
    roles: [],
    prompt: 'that is too much. keep only the changes to {scope} and undo your other edits',
    slots: {
      scope: 'the validation logic in src/forms/'
    },
    src: 'best-practices'
  }, {
    id: 'turn-a-correction-into',
    sdlc: 'build',
    cat: 'Steer',
    roles: [],
    prompt: 'you keep {mistake}. add a rule to CLAUDE.md so this stops happening',
    slots: {
      mistake: 'using default exports when this project uses named exports'
    },
    nextHref: '/en/memory',
    src: 'best-practices'
  }, {
    id: 'resolve-merge-conflicts',
    sdlc: 'ship',
    cat: 'Git',
    roles: [],
    prompt: 'resolve the merge conflicts in this branch and explain what you kept from each side',
    src: 'workflows'
  }, {
    id: 'commit-with-a-generated',
    sdlc: 'ship',
    cat: 'Git',
    roles: [],
    prompt: 'commit these changes with a message that summarizes what I did',
    src: 'workflows'
  }, {
    id: 'open-a-pull-request',
    sdlc: 'ship',
    cat: 'Git',
    roles: [],
    prompt: 'find the ticket about {topic} in {tracker} and open a PR that implements it',
    slots: {
      tracker: 'our issue tracker',
      topic: 'the login timeout'
    },
    needs: 'tracker',
    src: 'workflows'
  }, {
    id: 'draft-release-notes-from',
    sdlc: 'ship',
    cat: 'Release',
    roles: ['pm', 'docs', 'marketing'],
    prompt: 'compare {from} to {to} and draft release notes grouped by feature, fix, and breaking change',
    slots: {
      from: 'v2.3.0',
      to: 'v2.4.0'
    },
    nextHref: '/en/skills',
    src: 'workflows'
  }, {
    id: 'write-a-ci-workflow',
    sdlc: 'ship',
    cat: 'Release',
    roles: ['ops'],
    prompt: 'write a GitHub Actions workflow that {steps} on every push to {branch}',
    slots: {
      steps: 'runs the tests and deploys to staging',
      branch: 'main'
    },
    src: 'workflows'
  }, {
    id: 'find-and-fix-a',
    sdlc: 'operate',
    cat: 'Debug',
    startN: 3,
    roles: [],
    prompt: 'the {test} test is failing, find out why and fix it',
    slots: {
      test: 'UserAuth'
    },
    src: 'workflows'
  }, {
    id: 'investigate-a-reported-error',
    sdlc: 'operate',
    cat: 'Debug',
    roles: ['ops'],
    prompt: 'users are seeing {symptom} on {where}. investigate and tell me what is going on',
    slots: {
      symptom: '500 errors',
      where: '/api/settings'
    },
    nextHref: '/en/web-quickstart#pre-fill-sessions',
    src: 'workflows'
  }, {
    id: 'fix-a-build-error',
    sdlc: 'operate',
    cat: 'Debug',
    roles: ['ops'],
    paste: 'error',
    prompt: 'here is a build error. fix the root cause and verify the build succeeds',
    src: 'best-practices'
  }, {
    id: 'investigate-a-production-incident',
    sdlc: 'operate',
    cat: 'Incident',
    roles: ['ops', 'security'],
    prompt: '{symptom}. check the logs, recent deploys, and config changes, then tell me the most likely cause',
    slots: {
      symptom: 'the checkout endpoint started returning 500s an hour ago'
    },
    nextHref: '/en/mcp',
    src: 'workflows'
  }, {
    id: 'diagnose-from-a-console',
    sdlc: 'operate',
    cat: 'Incident',
    roles: ['ops', 'data'],
    paste: 'screenshot',
    prompt: 'here is a screenshot of {console}. walk me through why {resource} is failing and give me the exact commands to fix it',
    slots: {
      console: 'our Kubernetes dashboard',
      resource: 'this pod'
    },
    src: 'teams'
  }, {
    id: 'query-logs-in-plain',
    sdlc: 'operate',
    cat: 'Incident',
    roles: ['security', 'ops', 'data'],
    prompt: 'show me all {events} for {scope} over {timeframe}. write the query, run it, and tell me what stands out',
    slots: {
      events: 'failed logins',
      scope: 'the auth service',
      timeframe: 'the past 24 hours'
    },
    needs: 'db',
    src: 'cybersecurity'
  }, {
    id: 'analyze-a-data-file',
    sdlc: 'operate',
    cat: 'Data',
    roles: ['data', 'pm', 'marketing'],
    paste: 'csv',
    prompt: 'read {file}, summarize the key patterns, and write the results to {output}',
    slots: {
      file: '@reports/q1-signups.csv',
      output: 'an HTML page with charts, then open it in my browser'
    },
    nextHref: '/en/mcp',
    src: 'teams'
  }, {
    id: 'generate-variations-from-performance',
    sdlc: 'operate',
    cat: 'Data',
    roles: ['marketing', 'data'],
    paste: 'csv',
    prompt: 'read {file}, find the underperforming {items}, and generate {n} new variations that stay under {limit} characters',
    slots: {
      file: '@ads-performance.csv',
      items: 'headlines',
      n: '20',
      limit: '90'
    },
    nextHref: '/en/mcp',
    src: 'teams'
  }, {
    id: 'turn-a-recurring-task',
    sdlc: 'operate',
    cat: 'Automate',
    roles: [],
    prompt: 'create a /{name} skill for this project that {steps}',
    slots: {
      name: 'ship',
      steps: 'runs the linter and tests, then drafts a commit message'
    },
    src: 'workflows'
  }, {
    id: 'add-a-hook-for',
    sdlc: 'operate',
    cat: 'Automate',
    roles: [],
    prompt: 'write a hook that {action} after every {event}',
    slots: {
      action: 'runs prettier',
      event: 'edit to a .ts or .tsx file'
    },
    src: 'best-practices'
  }, {
    id: 'connect-a-tool-with',
    sdlc: 'operate',
    cat: 'Automate',
    roles: [],
    prompt: 'connect {server} via MCP so you can read its {data} directly',
    slots: {
      server: 'our error tracker',
      data: 'stack traces'
    },
    src: 'workflows'
  }, {
    id: 'capture-what-to-remember',
    sdlc: 'operate',
    cat: 'Automate',
    roles: ['pm', 'docs'],
    prompt: 'summarize what we did this session and suggest what to add to CLAUDE.md',
    src: 'teams'
  }], []);
  const PROMPTS = useMemo(() => {
    if (typeof window !== 'undefined') {
      const rawIds = new Set(RAW.map(p => p.id));
      RAW.forEach(p => {
        if (!text[p.id]) console.warn('[prompt-library] no text[] entry for id:', p.id);
      });
      Object.keys(text).forEach(k => {
        if (!rawIds.has(k)) console.warn('[prompt-library] orphaned text[] key:', k);
      });
    }
    return RAW.map(p => ({
      ...p,
      title: p.id,
      teaches: '',
      ...text[p.id] || ({})
    }));
  }, [RAW, text]);
  const L = labels;
  const TL = k => tagLabels[k] || k;
  const CAT_TAG = useMemo(() => ({
    Onboard: 'understand',
    Understand: 'understand',
    Plan: 'plan',
    Prototype: 'prototype',
    Implement: 'build',
    Test: 'test',
    Refactor: 'refactor',
    Review: 'review',
    Steer: 'steer',
    Git: 'git',
    Release: 'release',
    Debug: 'debug',
    Incident: 'debug',
    Data: 'data',
    Automate: 'automate'
  }), []);
  const TAGS = useMemo(() => ['understand', 'plan', 'prototype', 'build', 'test', 'refactor', 'review', 'steer', 'debug', 'git', 'release', 'data', 'automate', 'pm', 'design', 'docs', 'marketing', 'security', 'ops'], []);
  const tagsOf = p => [CAT_TAG[p.cat], ...p.roles || []];
  const doc = useMemo(() => {
    const p = typeof window !== 'undefined' ? window.location.pathname : '';
    const base = p.startsWith('/docs/') ? '/docs' : '';
    const m = p.slice(base.length).match(/^\/([a-z]{2}(?:-[A-Z]{2})?)\//);
    const locale = m ? m[1] : 'en';
    return href => {
      if (!href) return undefined;
      if (href[0] === '#' || href.startsWith('https://')) return href;
      if (!(/^\/[A-Za-z0-9]/).test(href)) return undefined;
      return base + (href.startsWith('/en/') ? '/' + locale + href.slice(3) : href);
    };
  }, []);
  const SAFE_HREF = /^(\/(?![\/\\\s])|#|https?:\/\/)/;
  const linkify = s => {
    const out = [];
    let last = 0;
    const re = /\[([^\]]+)\]\(([^)]+)\)/g;
    for (let m; m = re.exec(s); ) {
      if (m.index > last) out.push(s.slice(last, m.index));
      out.push(SAFE_HREF.test(m[2]) ? <a key={m.index} href={doc(m[2])}>{m[1]}</a> : m[1]);
      last = re.lastIndex;
    }
    if (last < s.length) out.push(s.slice(last));
    return out;
  };
  const codeify = s => s.split(/(`[^`]+`)/g).map((part, i) => part[0] === '`' ? <code key={i}>{part.slice(1, -1)}</code> : part);
  const SOURCES = useMemo(() => ({
    'workflows': '/en/common-workflows',
    'teams': 'https://claude.com/blog/how-anthropic-teams-use-claude-code',
    'legal': 'https://claude.com/blog/how-anthropic-uses-claude-legal',
    'cybersecurity': 'https://claude.com/blog/how-anthropic-uses-claude-cybersecurity',
    'best-practices': '/en/best-practices',
    'ebook': 'https://resources.anthropic.com/hubfs/Scaling%20agentic%20coding%20across%20your%20organization.pdf'
  }), []);
  const [mounted, setMounted] = useState(false);
  const [q, setQ] = useState('');
  const [start, setStart] = useState(true);
  const [sel, setSel] = useState(null);
  const [openId, setOpenId] = useState(null);
  const [copied, setCopied] = useState(null);
  const [fills, setFills] = useState({});
  const copyTimer = useRef(null);
  useEffect(() => {
    setMounted(true);
    return () => clearTimeout(copyTimer.current);
  }, []);
  const setFill = (id, key, val) => setFills(f => ({
    ...f,
    [id + '.' + key]: val
  }));
  const fillOf = (p, key) => {
    const v = fills[p.id + '.' + key];
    return v !== undefined ? v : p.slots && p.slots[key] !== undefined ? p.slots[key] : '';
  };
  const assemble = p => p.prompt.replace(/\{(\w+)\}/g, (_, k) => fillOf(p, k) || p.slots && p.slots[k] || k);
  const preview = p => p.prompt.replace(/\{(\w+)\}/g, (_, k) => p.slots && p.slots[k] || k);
  const bodyText = p => preview(p) + ' ' + p.teaches.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') + ' ' + (p.next || '');
  const WIDE_RE = /[\u1100-\u115F\u2E80-\uA4CF\uAC00-\uD7A3\uF900-\uFAFF\uFE30-\uFE4F\uFF00-\uFF60\uFFE0-\uFFE6]/g;
  const widthFor = s => {
    const t = typeof s === 'string' ? s : '';
    return t.length + (t.match(WIDE_RE) || []).length + 3 + 'ch';
  };
  const ql = q.trim().toLowerCase();
  const toggleTag = k => {
    setStart(false);
    setSel(s => !ql && s === k ? null : k);
  };
  const clear = () => {
    setStart(false);
    setSel(null);
    setQ('');
  };
  const results = useMemo(() => {
    const list = PROMPTS.filter(p => {
      if (ql) return p.title.toLowerCase().includes(ql) || bodyText(p).toLowerCase().includes(ql);
      if (start) return !!p.startN;
      if (sel) return tagsOf(p).includes(sel);
      return true;
    });
    if (ql) return list;
    if (start) return list.sort((a, b) => a.startN - b.startN);
    if (sel) return list.sort((a, b) => (a.roles || []).length - (b.roles || []).length || (b.sdlc === 'operate') - (a.sdlc === 'operate'));
    return list;
  }, [PROMPTS, ql, start, sel]);
  const matchSnippet = p => {
    if (!ql || p.title.toLowerCase().includes(ql)) return null;
    const txt = bodyText(p);
    const at = txt.toLowerCase().indexOf(ql);
    if (at < 0) return null;
    const lo = Math.max(0, at - 30), hi = Math.min(txt.length, at + ql.length + 50);
    return [lo > 0 ? '…' : '', txt.slice(lo, at), <mark key="m">{txt.slice(at, at + ql.length)}</mark>, txt.slice(at + ql.length, hi), hi < txt.length ? '…' : ''];
  };
  const grouped = useMemo(() => {
    if (start && !q.trim()) return [];
    const g = {};
    for (const p of results) {
      const key = p.sdlc + '|' + p.cat;
      (g[key] = g[key] || ({
        sdlc: p.sdlc,
        cat: p.cat,
        items: []
      })).items.push(p);
    }
    return Object.values(g);
  }, [results, start, q]);
  const copy = async (str, id) => {
    try {
      await navigator.clipboard.writeText(str);
    } catch {
      const ta = document.createElement('textarea');
      ta.value = str;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    }
    clearTimeout(copyTimer.current);
    setCopied(id);
    copyTimer.current = setTimeout(() => setCopied(null), 1600);
  };
  const promptBody = p => {
    if (!p.slots) return <code>{p.prompt}</code>;
    const parts = p.prompt.split(/(\{\w+\})/g);
    return <code>
        {parts.map((part, idx) => {
      const m = part.match(/^\{(\w+)\}$/);
      if (!m) return <span key={idx}>{part}</span>;
      const k = m[1];
      const val = fillOf(p, k);
      return <input key={idx} type="text" className="pl-slot" value={val} placeholder={p.slots[k] || k} aria-label={k} style={{
        width: widthFor(val || p.slots[k])
      }} onChange={e => setFill(p.id, k, e.target.value)} onFocus={e => e.target.select()} onClick={e => e.stopPropagation()} />;
    })}
      </code>;
  };
  const card = p => {
    const open = openId === p.id;
    const srcHref = SOURCES[p.src];
    const srcLabel = sourceLabels[p.src];
    const snip = matchSnippet(p);
    return <div key={p.id} className={'pl-card' + (open ? ' pl-open' : '')}>
        <button type="button" className="pl-head" onClick={() => setOpenId(open ? null : p.id)} aria-expanded={open}>
          <span className="pl-title">{p.title}</span>
          {!!p.startN && <span className="pl-chip">{L.startHere} · {p.startN}</span>}
        </button>
        {snip ? <div className="pl-match">{snip}</div> : <code className="pl-prompt-preview">{preview(p)}</code>}
        {open && <div className="pl-body">
            <div className="pl-label">{p.slots ? L.fillAndCopy : L.copyThis}</div>
            {p.needs && L.needs && L.needs[p.needs] && <div className="pl-hint pl-needs">
                <span className="pl-needs-label">{L.needsLabel}</span> {linkify(L.needs[p.needs])}
              </div>}
            {p.paste && L.paste && L.paste[p.paste] && <div className="pl-hint pl-paste">{L.paste[p.paste]}</div>}
            {p.slots && <div className="pl-hint">
                {L.hintBefore} <span className="pl-hint-chip">{L.hintChip}</span> {L.hintAfter}
              </div>}
            <div className="pl-prompt-box">
              <span className="pl-caret">{'❯'}</span>
              {promptBody(p)}
              <button type="button" className="pl-copy" onClick={() => copy(assemble(p), p.id)}>
                {copied === p.id ? L.copied : L.copy}
              </button>
            </div>
            <div className="pl-label">{L.whyWorks}</div>
            <div className="pl-teaches">{linkify(p.teaches)}</div>
            {p.nextHref && p.next && SAFE_HREF.test(p.nextHref) && <div className="pl-next">
                <span className="pl-next-label">{L.makeItStick}</span>
                <a href={doc(p.nextHref)}>{codeify(p.next)} →</a>
              </div>}
            {srcLabel && <div className="pl-src">{L.from} {srcHref ? <a href={doc(srcHref)}>{srcLabel}</a> : srcLabel}</div>}
          </div>}
      </div>;
  };
  const STYLES = useMemo(() => `
.pl {
  --pl-accent: #D97757;
  --pl-accent-bg: rgba(217,119,87,0.07);
  --pl-bg: #fff;
  --pl-surface: #FAFAF7;
  --pl-border: #E8E6DC;
  --pl-border-subtle: rgba(31,30,29,0.08);
  --pl-text: #141413;
  --pl-text-2: #5E5D59;
  --pl-text-3: #73726C;
  --pl-text-4: #9C9A92;
  --pl-mono: var(--font-mono, ui-monospace, SFMono-Regular, Menlo, monospace);
  font-family: 'Anthropic Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 16px; color: var(--pl-text); margin: 8px 0 32px;
}
.dark .pl {
  --pl-bg: #1f1e1d;
  --pl-surface: #262624;
  --pl-border: #3d3d3a;
  --pl-border-subtle: rgba(240,238,230,0.08);
  --pl-text: #f0eee6;
  --pl-text-2: #bfbdb4;
  --pl-text-3: #91908a;
  --pl-text-4: #73726c;
}
.pl *, .pl *::before, .pl *::after { box-sizing: border-box; }
.pl button { font-family: inherit; cursor: pointer; }
.pl a { color: var(--pl-accent); text-decoration: none; }
.pl a:hover { text-decoration: underline; }

.pl-search {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 18px; background: var(--pl-surface);
  border: 1px solid var(--pl-border); border-radius: 12px;
  margin-bottom: 14px;
}
.pl-search input {
  flex: 1; border: none; outline: none; background: transparent;
  font-size: 16px; color: var(--pl-text);
}
.pl-search input::placeholder { color: var(--pl-text-4); }

.pl-tags { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin-bottom: 18px; }
.pl-tag {
  padding: 7px 14px; border: 1px solid var(--pl-border); background: var(--pl-bg);
  font-size: 14px; color: var(--pl-text-2); border-radius: 999px;
}
.pl-tag:hover { background: var(--pl-surface); }
.pl-tag.pl-on { background: var(--pl-text); border-color: var(--pl-text); color: var(--pl-bg); }
.pl-tag.pl-start { color: var(--pl-accent); font-weight: 500; }
.pl-tag.pl-start.pl-on { background: var(--pl-accent); border-color: var(--pl-accent); color: #fff; }
.pl-tags.pl-dim .pl-tag { opacity: 0.5; }
.pl-tags.pl-dim .pl-tag:hover { opacity: 1; }
.pl-sep { width: 1px; height: 22px; background: var(--pl-border); margin: 0 4px; }
.pl-clear { border: none; background: none; font-size: 13px; color: var(--pl-text-4); padding: 4px 6px; }
.pl-clear:hover { color: var(--pl-text-2); }
.pl-count { margin-left: auto; font-size: 14px; color: var(--pl-text-4); }

.pl-group-h {
  font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--pl-text-4); margin: 24px 0 12px;
}
.pl-group-h .pl-phase { color: var(--pl-text-3); }
.pl-card {
  border: 1px solid var(--pl-border-subtle); border-radius: 10px;
  margin-bottom: 12px; background: var(--pl-bg); overflow: hidden;
  padding: 14px 18px;
}
.pl-card.pl-open { border-color: var(--pl-border); background: var(--pl-surface); }
.pl-head {
  width: 100%; display: flex; align-items: baseline; gap: 12px;
  border: none; background: transparent; text-align: left; padding: 0;
}
.pl-head:focus-visible { outline: 2px solid var(--pl-accent); outline-offset: 2px; border-radius: 6px; }
.pl-title {
  flex: 1; font-size: 17px; font-weight: 500; color: var(--pl-text);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.pl-prompt-preview {
  display: block; font-family: var(--pl-mono); font-size: 13.5px; color: var(--pl-text-3);
  margin-top: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.pl-chip {
  font-size: 11px; letter-spacing: 0.05em; text-transform: uppercase;
  padding: 3px 9px; border-radius: 999px; flex-shrink: 0;
  background: var(--pl-accent-bg); color: var(--pl-accent);
}

.pl-body { margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--pl-border-subtle); }
.pl-label {
  font-size: 11.5px; letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--pl-text-4); margin: 12px 0 8px;
}
.pl-prompt-box {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 16px; background: #141413; color: #f0eee6;
  border-radius: 8px; font-family: var(--pl-mono); font-size: 15px;
}
.pl-caret { color: var(--pl-accent); flex-shrink: 0; }
.pl-prompt-box code { flex: 1; background: none; padding: 0; color: inherit; white-space: pre-wrap; line-height: 1.9; }
.pl-slot {
  font-family: var(--pl-mono); font-size: inherit;
  background: rgba(217,119,87,0.15); color: #f0eee6;
  border: none; border-bottom: 1.5px dashed var(--pl-accent);
  border-radius: 4px 4px 0 0; padding: 2px 6px; margin: 0 1px;
  outline: none; min-width: 6ch; max-width: 100%;
  box-sizing: content-box; cursor: text;
}
.pl-slot:hover { background: rgba(217,119,87,0.22); }
.pl-slot:focus { background: rgba(217,119,87,0.28); border-bottom-style: solid; }
.pl-slot::placeholder { color: rgba(240,238,230,0.4); font-style: italic; }
.pl-hint { font-size: 14px; color: var(--pl-text-3); margin: 0 0 10px; }
.pl-paste { color: var(--pl-text-2); }
.pl-needs { color: var(--pl-text-2); }
.pl-needs-label {
  display: inline-block; font-size: 10.5px; letter-spacing: 0.06em;
  text-transform: uppercase; padding: 2px 7px; margin-right: 6px;
  border-radius: 4px; background: var(--pl-accent-bg); color: var(--pl-accent);
}
.pl-hint-chip {
  font-family: var(--pl-mono); font-size: 0.92em;
  background: var(--pl-accent-bg); color: var(--pl-accent);
  border-bottom: 1.5px dashed var(--pl-accent);
  border-radius: 3px 3px 0 0; padding: 1px 5px;
}
.pl-copy {
  font-size: 12.5px; padding: 6px 12px; border-radius: 6px;
  background: var(--pl-accent); color: #fff; border: none; flex-shrink: 0;
}
.pl-teaches { display: block; font-size: 15.5px; color: var(--pl-text-2); margin: 4px 0 0; line-height: 1.6; }
.pl-match {
  display: block; font-size: 13.5px; color: var(--pl-text-3);
  margin-top: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.pl-match mark { background: var(--pl-accent-bg); color: var(--pl-text); padding: 1px 2px; border-radius: 3px; }
.pl-next {
  display: flex; align-items: baseline; gap: 10px;
  margin: 14px 0 0; padding: 10px 12px;
  background: var(--pl-accent-bg); border-radius: 8px; font-size: 14.5px;
}
.pl-next-label {
  font-size: 11px; letter-spacing: 0.06em; text-transform: uppercase;
  color: var(--pl-accent); font-weight: 600; flex-shrink: 0;
}
.pl-src { display: block; font-size: 14px; color: var(--pl-text-4); margin: 14px 0 0; }

.pl-show-all {
  display: block; width: 100%; padding: 14px; margin-top: 4px;
  border: 1px dashed var(--pl-border); border-radius: 10px;
  background: transparent; font-size: 15px; color: var(--pl-accent);
  text-align: center;
}
.pl-show-all:hover { background: var(--pl-accent-bg); border-style: solid; }

.pl-empty {
  padding: 32px; text-align: center; color: var(--pl-text-4);
  border: 1px dashed var(--pl-border); border-radius: 10px;
}
`, []);
  if (!mounted) return <div className="pl" style={{
    minHeight: 480
  }} />;
  return <div className="pl">
      <style>{STYLES}</style>

      <div className="pl-search">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{
    color: 'var(--pl-text-4)'
  }}>
          <circle cx="11" cy="11" r="7" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <input type="text" placeholder={L.search} value={q} onChange={e => {
    setQ(e.target.value);
    if (e.target.value) setStart(false);
  }} aria-label={L.search} />
      </div>

      <div className={'pl-tags' + (ql ? ' pl-dim' : '')}>
        <button type="button" className={'pl-tag pl-start' + (!ql && start ? ' pl-on' : '')} onClick={() => {
    setQ('');
    setStart(!start);
    if (!start) setSel(null);
  }}>
          ★ {L.startHere}
        </button>
        <span className="pl-sep" />
        {TAGS.map(k => <button key={k} type="button" aria-pressed={!ql && sel === k} className={'pl-tag' + (!ql && sel === k ? ' pl-on' : '')} onClick={() => {
    setQ('');
    toggleTag(k);
  }}>
            {TL(k)}
          </button>)}
        {(start || sel || q) && <button type="button" className="pl-clear" onClick={clear}>{L.clear}</button>}
        <span className="pl-count">{results.length} {results.length === 1 ? L.prompt : L.prompts}</span>
      </div>

      {results.length === 0 ? <div className="pl-empty">
          {L.noMatch} {ql ? <code>{q}</code> : null} <button type="button" className="pl-clear" onClick={clear}>{L.clear}</button>
        </div> : !ql && start ? <div>
          <div className="pl-group-h">{L.startHereHeader}</div>
          {results.map(card)}
          <button type="button" className="pl-show-all" onClick={clear}>
            {L.showAll && L.showAll.replace('{n}', PROMPTS.length)} →
          </button>
        </div> : grouped.map(g => <div key={g.sdlc + '|' + g.cat}>
            <div className="pl-group-h"><span className="pl-phase">{phaseLabels[g.sdlc] || g.sdlc}</span> · {catLabels[g.cat] || g.cat}</div>
            {g.items.map(card)}
          </div>)}
    </div>;
};

这是一个提示词库，可以复制到 Claude Code 中使用。使用它来探索你还没有尝试过的工作方式，或者当你不确定从哪里开始时。

这些提示词来自各种 Anthropic 指南，包括[常见工作流](/docs/zh-CN/common-workflows)、[最佳实践](/docs/zh-CN/best-practices)和[Anthropic 团队如何使用 Claude Code](https://claude.com/blog/how-anthropic-teams-use-claude-code)。它们是起点而不是脚本。打开任何提示词下的**为什么这样做有效**来查看其背后的模式，这样你可以编写自己的提示词。

export const labels = {
  startHere: "从这里开始",
  startHereHeader: "五个首先尝试的提示词",
  showAll: "显示全部 {n} 个提示词",
  search: "搜索提示词…",
  clear: "清除",
  prompt: "提示词",
  prompts: "提示词",
  noMatch: "没有匹配的提示词",
  fillAndCopy: "填写并复制",
  copyThis: "复制此提示词",
  hintBefore: "在",
  hintChip: "高亮显示的",
  hintAfter: "字段中输入以自定义，然后复制。",
  copy: "复制",
  copied: "已复制",
  whyWorks: "为什么这样做有效",
  makeItStick: "使其坚持",
  from: "来自",
  paste: {
    mockup: "粘贴、拖动或 @-提及你的模型图像，然后发送此内容：",
    design: "粘贴、拖动或 @-提及你的设计图像，然后发送此内容：",
    screenshot: "粘贴、拖动或 @-提及你的屏幕截图，然后发送此内容：",
    plan: "首先将你的计划输出粘贴到提示词中，然后发送此内容：",
    error: "首先将错误输出粘贴到提示词中，然后发送此内容：",
    csv: "将你的文件拖到提示词中，或将下面的路径替换为你自己的 @-提及："
  },
  needsLabel: "需要",
  needs: {
    tracker: "你的问题跟踪器添加为 [claude.ai 连接器](/docs/zh-CN/mcp#use-mcp-servers-from-claude-ai) 或 [MCP 服务器](/docs/zh-CN/mcp)。",
    gh: "[gh CLI](https://cli.github.com) 已认证，或 GitHub 添加为 [claude.ai 连接器](/docs/zh-CN/mcp#use-mcp-servers-from-claude-ai)。",
    browser: "Claude 能够呈现和截图结果的方式。[桌面应用](/docs/zh-CN/desktop#preview-your-app)内置了此功能。在终端中，安装 [Chrome 扩展](/docs/zh-CN/chrome)或 Playwright [MCP](/docs/zh-CN/mcp) 服务器。",
    db: "你的数据仓库或日志存储添加为 [claude.ai 连接器](/docs/zh-CN/mcp#use-mcp-servers-from-claude-ai) 或 [MCP 服务器](/docs/zh-CN/mcp)。"
  }
};

export const tagLabels = {
  understand: "理解",
  plan: "计划",
  prototype: "原型",
  build: "构建",
  test: "测试",
  refactor: "重构",
  review: "审查",
  steer: "引导",
  debug: "调试",
  git: "Git",
  release: "发布",
  data: "数据",
  automate: "自动化",
  pm: "产品",
  design: "设计",
  docs: "文档",
  marketing: "营销",
  security: "安全",
  ops: "值班"
};

export const phaseLabels = {
  discover: "发现",
  design: "设计",
  build: "构建",
  ship: "发布",
  operate: "运营"
};

export const sourceLabels = {
  workflows: "常见工作流",
  teams: "Anthropic 团队如何使用 Claude Code",
  legal: "Anthropic 如何在法律中使用 Claude",
  cybersecurity: "Anthropic 如何在网络安全中使用 Claude",
  "best-practices": "最佳实践",
  ebook: "扩展代理编码指南"
};

export const catLabels = {
  Onboard: "入职",
  Understand: "理解",
  Plan: "计划",
  Prototype: "原型",
  Implement: "实现",
  Test: "测试",
  Refactor: "重构",
  Review: "审查",
  Steer: "引导",
  Git: "Git",
  Release: "发布",
  Debug: "调试",
  Incident: "事件",
  Data: "数据",
  Automate: "自动化"
};

export const text = {
  "get-oriented-in-a": {
    title: "快速熟悉新仓库",
    teaches: "描述您想了解的内容，而不是要读哪些文件。Claude 会自行探索项目，并返回一份关于各部分如何组合在一起的摘要。",
    next: "运行 `/init` 来设置 `CLAUDE.md`，以便 Claude 在每个会话中记住这些内容",
    prompt: "给我概述一下这个代码库：架构、关键目录，以及各部分之间如何关联"
  },
  "explain-unfamiliar-code": {
    title: "解释不熟悉的代码",
    teaches: "指明文件，并说明您希望答案采用的格式。可以把 HTML 页面换成图表、要点列表，或任何适合您学习方式的形式。",
    next: "设置输出样式，以便 Claude 始终以您喜欢的格式进行解释",
    prompt: "解释 {path} 的作用以及数据如何在其中流动。将其写成{format}",
    slots: {
      path: "src/scheduler/queue.ts",
      format: "一个带图表的 HTML 页面，然后在我的浏览器中打开它"
    }
  },
  "find-where-something-happens": {
    title: "找到某个行为发生的位置",
    teaches: "按行为而不是按文件名搜索。即使您不知道文件叫什么或位于哪个目录，搜索也同样有效。",
    prompt: "我们在哪里{behavior}？",
    slots: {
      behavior: "验证上传的文件类型"
    }
  },
  "see-what-depends-on": {
    title: "删除前检查会破坏什么",
    teaches: "在删除任何内容之前先询问。调用方列表和下游影响会告诉您，这只是一行代码的清理，还是一项需要协调的更改。",
    prompt: "如果我删除{target}，会破坏什么？",
    slots: {
      target: "retryWithBackoff 辅助函数"
    }
  },
  "trace-how-code-evolved": {
    title: "追踪代码如何演变",
    teaches: "当问题是“为什么”而不是“是什么”时，请指向提交历史。Claude 会读取您所用版本控制系统的日志和 blame 信息，并解释当前实现背后的决策。",
    prompt: "查看 {path} 的提交历史，总结它是如何演变的以及原因",
    slots: {
      path: "internal/auth/session.go"
    }
  },
  "scope-a-change-before": {
    title: "开始前确定更改的范围",
    teaches: "在将工作列入路线图之前先评估其规模。文件列表会告诉您，这只涉及一个组件，还是一项跨越多个部分的更改。",
    prompt: "要{change}，我需要修改哪些文件？",
    slots: {
      change: "在设置中添加深色模式开关"
    }
  },
  "ask-the-codebase-a": {
    title: "向代码库提出产品问题",
    teaches: "说明您的角色，以便答案处于合适的深度。Claude 会根据源代码解释产品实际做了什么，您无需亲自阅读代码。",
    next: "设置输出样式，以便 Claude 始终以这一深度给出回答",
    prompt: "我是{role}。请带我了解当用户{action}时会发生什么，从 UI 一直到最终结果",
    slots: {
      role: "PM",
      action: "点击导出为 PDF"
    }
  },
  "plan-a-multi-file": {
    title: "在改动代码前规划多文件更改",
    teaches: "加上“暂时不要编辑”可以将探索与更改分开，让您在任何代码变动之前先看到方案。要让每个提示词都默认先做计划，请按 Shift+Tab 进入[计划模式](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode)。",
    prompt: "规划如何重构{target}以{goal}。列出需要修改的文件，但暂时不要编辑任何内容",
    slots: {
      target: "支付模块",
      goal: "支持多种货币"
    }
  },
  "draft-a-spec-by": {
    title: "通过访谈起草规范",
    teaches: "请 Claude 采访您，而不是自己编写规范。Claude 会向您提出结构化问题，直到需求完整为止，然后将结果写入文件。",
    next: "将您的访谈问题保存为 `/spec` skill，让每份规范都以相同方式开始",
    prompt: "我想构建{feature}。就实现、UX、边界情况和权衡向我提问，直到所有内容都覆盖到，然后将规范写入 SPEC.md",
    slots: {
      feature: "按工作区划分的速率限制"
    }
  },
  "turn-a-meeting-into": {
    title: "将会议转化为工单",
    teaches: "省去整理文字稿这一步。Claude 会从非结构化输入中提取行动项，并通过 [MCP](/docs/zh-CN/mcp) 直接写入您的跟踪器，因此您审查的是工单，而不是文字稿。",
    next: "将此保存为 `/tickets` skill",
    prompt: "阅读 {input} 并整理出行动项，然后在{tracker}中为每一项创建一个包含验收标准的工单",
    slots: {
      input: "@meeting-notes.md",
      tracker: "我们的问题跟踪器"
    }
  },
  "map-edge-cases-before": {
    title: "构建前梳理边界情况",
    teaches: "询问缺少什么，而不是已有什么。Claude 会列出只考虑理想路径的设计往往会遗漏的错误状态、空状态和边界情况。",
    prompt: "列出设计中需要覆盖的{feature}的错误状态、空状态和边界情况",
    slots: {
      feature: "文件上传流程"
    }
  },
  "turn-a-mockup-into": {
    title: "将设计稿转化为可运行的原型",
    teaches: "可点击的原型能回答静态设计稿无法回答的问题。把可运行的代码交给工程团队，而不是在文档中解释交互。",
    prompt: "这是一份设计稿。构建一个可以点击操作的可运行原型，与其中展示的布局和状态保持一致"
  },
  "implement-from-a-screenshot": {
    title: "根据截图实现并自行检查",
    teaches: "这为 Claude 提供了一个验证循环：它会渲染结果、与原始图像比较并反复迭代，无需您逐一指出差距。",
    next: "使用 `/goal` 让 Claude 持续迭代，直到截图一致",
    prompt: "实现这个设计，然后对结果截图，与原图进行比较，并修复所有差异"
  },
  "follow-an-existing-pattern": {
    title: "遵循现有模式",
    teaches: "指向您已经认可的代码。没有参考时，Claude 会默认采用通用的最佳实践；有了参考，它会匹配您的代码库实际使用的约定。",
    next: "请 Claude 将其遵循的模式写入 `CLAUDE.md`，以便以后的会话无需参考也能保持一致",
    prompt: "查看 {example} 的实现方式以理解其模式，然后用相同的方式构建 {new}",
    slots: {
      example: "现有的 webhook 处理程序",
      new: "支付 webhook 处理程序"
    }
  },
  "add-a-small-well": {
    title: "添加一个小而明确的功能",
    teaches: "说明输入和输出，而不是如何构建。Claude 会找到类似代码所在的位置，并在旁边添加您的代码。",
    prompt: "添加一个 {endpoint} 端点，返回{payload}",
    slots: {
      endpoint: "/health",
      payload: "应用版本和运行时长"
    }
  },
  "build-a-small-internal": {
    title: "从零构建一个小型内部工具",
    teaches: "您不需要项目、框架或构建步骤。描述工具并请 Claude 打开它，即可立即看到它运行。",
    prompt: "使用 HTML、CSS 和原生 JavaScript 创建一个{tool}，然后在我的浏览器中打开它",
    slots: {
      tool: "包含三列的拖放式看板"
    }
  },
  "work-an-issue-end": {
    title: "端到端处理一个 issue",
    teaches: "给出 issue 编号，而不是摘要。Claude 会自行读取完整工单，因此您可能忘记提及的需求也会被考虑在内，并且它会在汇报前验证更改。",
    prompt: "阅读 issue #{issue}，实现修复，并运行测试",
    slots: {
      issue: "312"
    }
  },
  "find-and-update-copy": {
    title: "在代码库中查找并更新文案",
    teaches: "要求查找变体，并说明要跳过的内容。Claude 会找出字面搜索会遗漏的措辞，同时不改动测试夹具和历史记录，因此您只需审查用户实际看到的文案。",
    prompt: "找到所有提到“{copy}”或类似说法的地方，逐一展示其上下文，然后将它们全部更新为“{new}”。不要改动测试和 changelog",
    slots: {
      copy: "免费注册",
      new: "开始免费试用"
    }
  },
  "draft-from-past-examples": {
    title: "根据以往示例起草文档",
    teaches: "指向存放已完成工作的文件夹，而不是描述您的风格。Claude 会从您已经发布的内容中学习结构和语气，因此初稿读起来就像出自您之手。",
    next: "将这种语气保存为 skill，让每份草稿都以此为起点",
    prompt: "阅读 {folder} 中的{examples}以学习其结构和语气，然后为{topic}起草一份新的",
    slots: {
      examples: "隐私影响评估",
      folder: "legal/pia/",
      topic: "新的分析集成"
    }
  },
  "write-tests-run-them": {
    title: "编写测试、运行测试、修复失败",
    teaches: "同时要求编写、运行和修复，让 Claude 持续迭代，无需停下来等待指示。",
    next: "运行 `/init`，让 Claude 自动了解您的测试命令",
    prompt: "为 {path} 编写测试，运行它们，并修复所有失败",
    slots: {
      path: "app/parsers/feed.py"
    }
  },
  "drive-implementation-from-tests": {
    title: "用测试驱动实现",
    teaches: "测试驱动开发：由测试来定义工作何时完成，Claude 会不断迭代实现，直到测试通过。",
    prompt: "先为{feature}编写测试，然后实现它，直到测试通过",
    slots: {
      feature: "密码重置流程"
    }
  },
  "fill-gaps-from-a": {
    title: "根据覆盖率报告填补空白",
    teaches: "指向覆盖率报告，而不是猜测哪些部分未被测试。Claude 会读取实际数据，并为最需要测试的文件编写测试。",
    next: "将此设置为 `/goal`，让 Claude 持续编写测试，直到达到覆盖率目标",
    prompt: "阅读 {report}，为覆盖率最低的文件添加测试，直到每个文件都超过 {target}%",
    slots: {
      report: "coverage/coverage-summary.json",
      target: "80"
    }
  },
  "port-code-between-languages": {
    title: "将代码移植到另一种语言",
    teaches: "说明需要保留的内容，而不仅仅是目标语言。指明必须保持不变的 API 或行为，相当于给 Claude 一份契约，用来检验移植结果。",
    prompt: "将{source}移植到 {target}，保持相同的{keep}",
    slots: {
      source: "这个 Python 模块",
      target: "Rust",
      keep: "公共 API 和测试行为"
    }
  },
  "generate-docs-for-code": {
    title: "为缺少文档的代码生成文档",
    teaches: "指明范围和格式。Claude 会找出缺失的内容，并匹配文件中已有的注释风格，让新文档与其余部分保持一致。",
    prompt: "找出没有 {format} 注释的{scope}并添加注释，与文件中已有的风格保持一致",
    slots: {
      scope: "src/auth/ 中的公共函数",
      format: "JSDoc"
    }
  },
  "migrate-a-pattern-across": {
    title: "在整个代码库中迁移模式",
    teaches: "描述旧模式和新模式。要求 Claude 先找出每一处需要修改的地方，这样调用位置会列在回复中，方便您检查是否有遗漏。对于涉及大量文件的迁移，请运行 [/batch](/docs/zh-CN/commands)。Claude 会将工作拆分为多个单元供您批准，然后由后台子代理进行更改。",
    prompt: "将所有内容从{from}迁移到{to}：先找出每一处需要修改的地方，然后进行修改",
    slots: {
      from: "旧的日志 API",
      to: "结构化日志记录器"
    }
  },
  "optimize-against-a-measurable": {
    title: "针对可量化目标进行优化",
    teaches: "说明指标和目标，能为 Claude 提供明确的完成标准。",
    next: "将此设置为 `/goal`，让 Claude 持续测量和迭代，直到达到目标数值",
    prompt: "优化{target}，将{metric}从 {current} 降低到 {goal} 以下",
    slots: {
      target: "搜索查询",
      metric: "p95 延迟",
      current: "2s",
      goal: "500ms"
    }
  },
  "fix-a-precise-visual": {
    title: "修复精确的视觉问题",
    teaches: "精确的视觉反馈才能换来精确的修复。请说明具体的元素、尺寸和视口。",
    next: "添加预览工具，让 Claude 自行截图并验证修复",
    prompt: "在{viewport}上，{element}超出{container} {amount}。请修复。",
    slots: {
      element: "登录按钮",
      amount: "20px",
      container: "卡片边框",
      viewport: "移动端"
    }
  },
  "review-your-changes-before": {
    title: "提交前审查您的更改",
    teaches: "趁问题修复成本还低时发现它们。Claude 会完整读取更改过的文件，而不仅仅是 diff 行，因此能发现快速自查时容易遗漏的问题。",
    next: "运行 `/code-review`，一条命令完成同样的检查",
    prompt: "审查我尚未提交的更改，在我提交前标出任何看起来有风险的地方"
  },
  "review-a-pull-request": {
    title: "审查 Pull Request",
    teaches: "Claude 审查时会结合整个代码库的上下文，而不仅仅是 diff。它会读取更改的代码及其调用的内容，因此能发现只看 diff 的审查会遗漏的问题。",
    next: "运行 `/code-review <pr#>` 一条命令完成，或为每个 PR 启用 Code Review",
    prompt: "审查 PR #{pr}，总结更改内容，然后列出任何疑虑",
    slots: {
      pr: "247"
    }
  },
  "review-infrastructure-changes-before": {
    title: "应用前审查基础设施更改",
    teaches: "plan 输出内容密集，难以快速浏览。将其粘贴进来，即可在应用之前获得一份通俗易懂的摘要，了解实际将发生哪些更改。",
    prompt: "这是我的 Terraform plan 输出。它会做什么？其中有没有会导致问题的内容？"
  },
  "run-a-security-review": {
    title: "使用子代理运行安全审查",
    teaches: "[子代理](/docs/zh-CN/sub-agents)会在自己的上下文窗口中运行审计并汇报摘要，因此冗长的安全审查不会占满您的主会话。内置的通用子代理无需额外设置即可处理此任务。",
    next: "设置一个专用的安全审查子代理，供整个团队使用",
    prompt: "使用子代理审查 {path} 中的安全问题，并报告其发现",
    slots: {
      path: "src/api/"
    }
  },
  "review-content-before-sending": {
    title: "在正式审查前发现问题",
    teaches: "在他人投入时间之前先过一遍。指明您希望检查的关注点，让审查更有针对性，然后修复发现的问题，再发送一份更完善的草稿。",
    next: "将您的审查清单保存为整个团队都能运行的 skill",
    prompt: "审查 {file} 中的{concerns}，并列出在提交给{reviewer}之前需要修复的内容",
    slots: {
      file: "launch-post.md",
      concerns: "无依据的说法、缺失的出处标注以及品牌规范问题",
      reviewer: "法务"
    }
  },
  "course-correct-a-wrong": {
    title: "纠正错误的方向",
    teaches: "指出 Claude 遗漏的约束，而不只是说它错了。具体的原因能给 Claude 一个在重试时需要满足的明确约束，而不是再次猜测。",
    next: "按两次 `Esc` 打开回退菜单，恢复代码和对话，让重试从干净的状态开始",
    prompt: "这不对：{feedback}。换一种方法试试",
    slots: {
      feedback: "函数签名需要保持向后兼容"
    }
  },
  "narrow-the-scope-of": {
    title: "缩小更改的范围",
    teaches: "当方向正确但更改过于宽泛时，请 Claude 保留其中一部分，而不是全部回退。明确的边界能避免一个小修复演变成一次重构。",
    prompt: "改动太多了。只保留对{scope}的更改，撤销其他编辑",
    slots: {
      scope: "src/forms/ 中的验证逻辑"
    }
  },
  "turn-a-correction-into": {
    title: "将纠正转化为规则",
    teaches: "在聊天中的纠正不会与团队共享。而项目 [CLAUDE.md](/docs/zh-CN/memory) 中的规则在您提交后即可共享，Claude 会在每个会话开始时读取它。",
    next: "打开 `/memory` 查看 Claude 写入的内容",
    prompt: "反复出现{mistake}的问题。请在 CLAUDE.md 中添加一条规则，避免再次发生",
    slots: {
      mistake: "在本项目使用具名导出的情况下使用默认导出"
    }
  },
  "resolve-merge-conflicts": {
    title: "解决合并冲突",
    teaches: "说明您想要的最终状态，而不是要保留哪些标记。要求说明理由，能让合并结果可审查，而不是一个黑盒。",
    prompt: "解决此分支中的合并冲突，并说明从每一方各保留了哪些内容"
  },
  "commit-with-a-generated": {
    title: "使用生成的提交信息进行提交",
    teaches: "让 Claude 根据 diff 生成提交信息。它会匹配您仓库现有的提交风格。",
    prompt: "提交这些更改，并附上一条总结我所做工作的提交信息"
  },
  "open-a-pull-request": {
    title: "根据工单创建 Pull Request",
    teaches: "省去在跟踪器、编辑器和 GitHub 之间来回切换。一个提示词即可读取需求、完成更改并创建 PR。",
    prompt: "在{tracker}中找到关于{topic}的工单，并创建一个实现它的 PR",
    slots: {
      tracker: "我们的问题跟踪器",
      topic: "登录超时"
    }
  },
  "draft-release-notes-from": {
    title: "根据 git 历史起草发布说明",
    teaches: "给出两个参考点以及您想要的结构。Claude 会读取两者之间的提交日志，并起草一份可供您编辑的更新日志。",
    next: "将此保存为 `/changelog` skill",
    prompt: "比较 {from} 和 {to}，按功能、修复和破坏性变更分组起草发布说明",
    slots: {
      from: "v2.3.0",
      to: "v2.4.0"
    }
  },
  "write-a-ci-workflow": {
    title: "编写 CI 工作流",
    teaches: "描述它应在何时运行以及应做什么；系统会为您生成 YAML，并与项目的构建和测试命令相匹配。",
    prompt: "编写一个 GitHub Actions 工作流，在每次推送到 {branch} 时{steps}",
    slots: {
      steps: "运行测试并部署到预发布环境",
      branch: "main"
    }
  },
  "find-and-fix-a": {
    title: "找到并修复失败的测试",
    teaches: "描述症状即可；您无需知道是哪个文件出了问题。Claude 会运行测试查看失败情况，追踪到源代码中，并进行修复。",
    prompt: "{test} 测试失败了，找出原因并修复",
    slots: {
      test: "UserAuth"
    }
  },
  "investigate-a-reported-error": {
    title: "调查报告的错误",
    teaches: "描述症状和位置；Claude 会读取相关代码路径并追踪可能的原因。如果您有堆栈跟踪或日志，请一并粘贴。",
    next: "在您的运行手册中放置一个深层链接，打开 Claude 时自动预填此提示词",
    prompt: "用户在 {where} 上遇到了{symptom}。请调查并告诉我发生了什么",
    slots: {
      symptom: "500 错误",
      where: "/api/settings"
    }
  },
  "fix-a-build-error": {
    title: "从根源修复构建错误",
    teaches: "要求修复根本原因并进行验证，可以避免只是压制错误而未真正修复的表面补丁。",
    prompt: "这是一个构建错误。修复根本原因并验证构建成功"
  },
  "investigate-a-production-incident": {
    title: "调查生产事件",
    teaches: "列出需要关联分析的证据来源，而不是要采取的步骤。Claude 会综合读取日志、git 历史和配置，以缩小原因范围。",
    next: "通过 MCP 连接您的错误跟踪器或日志存储",
    prompt: "{symptom}。检查日志、最近的部署和配置更改，然后告诉我最可能的原因",
    slots: {
      symptom: "结账端点从一小时前开始返回 500"
    }
  },
  "query-logs-in-plain": {
    title: "用自然语言查询日志",
    teaches: "直接提出问题，而不是编写 SQL。Claude 会构建查询、在您连接的日志上运行，并同时展示查询语句和结果，方便您核对实际运行的内容。",
    prompt: "显示{scope}在{timeframe}内的所有{events}。编写查询、运行它，并告诉我哪些地方值得注意",
    slots: {
      events: "登录失败",
      scope: "认证服务",
      timeframe: "过去 24 小时"
    }
  },
  "diagnose-from-a-console": {
    title: "根据控制台截图进行诊断",
    teaches: "云控制台会向您展示问题，但不会给出修复命令。Claude 会读取截图，并将仪表板内容转换为需要运行的 kubectl、gcloud 或 aws 命令。",
    prompt: "这是{console}的截图。请带我分析{resource}为什么失败，并给出修复它的确切命令",
    slots: {
      console: "我们的 Kubernetes 仪表板",
      resource: "这个 pod"
    }
  },
  "analyze-a-data-file": {
    title: "分析数据文件",
    teaches: "一次性的问题不需要一次性的脚本。指向项目文件夹中的文件，Claude 会直接读取它、找出规律，并将输出写到您指定的位置。",
    next: "通过 MCP 连接数据源，而不是导出文件",
    prompt: "读取 {file}，总结关键规律，并将结果写入{output}",
    slots: {
      file: "@reports/q1-signups.csv",
      output: "一个带图表的 HTML 页面，然后在我的浏览器中打开它"
    }
  },
  "generate-variations-from-performance": {
    title: "根据效果数据生成变体",
    teaches: "在一开始就说明约束，让生成内容不超出限制。Claude 会读取指标，挑选需要替换的内容，并生成符合要求的替代方案。",
    next: "通过 MCP 连接广告平台，而不是导出文件",
    prompt: "读取 {file}，找出表现不佳的{items}，并生成 {n} 个不超过 {limit} 个字符的新变体",
    slots: {
      file: "@ads-performance.csv",
      items: "标题",
      n: "20",
      limit: "90"
    }
  },
  "turn-a-recurring-task": {
    title: "将重复任务转化为 skill",
    teaches: "只需说明一次步骤，即可作为命令反复使用。Claude 会编写一个团队中任何人都能运行的 [skill](/docs/zh-CN/skills)。",
    prompt: "为此项目创建一个 /{name} skill，用于{steps}",
    slots: {
      name: "ship",
      steps: "运行 linter 和测试，然后起草提交信息"
    }
  },
  "add-a-hook-for": {
    title: "为重复行为添加 hook",
    teaches: "hook 能让某个行为自动发生，而不必每次都记得提出要求。描述触发条件和操作，Claude 就会编写 [hook](/docs/zh-CN/hooks) 配置。",
    prompt: "编写一个 hook，在每次{event}后{action}",
    slots: {
      action: "运行 prettier",
      event: "编辑 .ts 或 .tsx 文件"
    }
  },
  "connect-a-tool-with": {
    title: "使用 MCP 连接工具",
    teaches: "一次性连接数据源，而不是每个会话都粘贴数据。完成 [MCP](/docs/zh-CN/mcp) 设置后，当您询问相关内容时，Claude 会直接从该工具读取数据。",
    prompt: "通过 MCP 连接{server}，以便你能直接读取其{data}",
    slots: {
      server: "我们的错误跟踪器",
      data: "堆栈跟踪"
    }
  },
  "capture-what-to-remember": {
    title: "记录下次需要记住的内容",
    teaches: "趁还没忘记时询问。Claude 知道它在本次会话中需要摸索出哪些内容，并会建议添加到 [CLAUDE.md](/docs/zh-CN/memory) 的条目，让下一个会话从这些上下文开始。",
    prompt: "总结我们在本次会话中做了什么，并建议向 CLAUDE.md 添加哪些内容"
  }
};

<PromptLibrary text={text} labels={labels} tagLabels={tagLabels} phaseLabels={phaseLabels} sourceLabels={sourceLabels} catLabels={catLabels} />

<h2 id="what-makes-these-prompts-work">
  这些提示词为什么有效
</h2>

上面的提示词共享一些模式。识别它们有助于你将此处的任何提示词调整到你自己的任务。

**描述结果，而不是步骤。** 说出你想要的内容，让 Claude 找到文件。下面的提示词无需命名单个文件路径即可工作。

```text wrap theme={null}
add rate limiting to the public API and make sure existing tests still pass
```

**给它一种检查自己工作的方式。** 在同一提示词中要求运行、测试、比较或验证，以便 Claude 迭代而不是在一次尝试后停止。要检查完成的更改与运行中的应用程序，请运行 [`/verify`](/docs/zh-CN/skills#run-and-verify-your-app)。

```text wrap theme={null}
write the migration, run it against the dev database, and confirm the schema matches
```

**指向参考。** 命名现有文件、测试或模式以匹配，以便新代码与你已有的内容一致。

```text wrap theme={null}
add a settings page that follows the same layout as the profile page
```

**说明可测量的目标。** 当目标是性能或覆盖率时，给出指标和阈值，以便完成是明确的。

```text wrap theme={null}
get the bundle size under 200KB and show me what you removed
```

**给它工件。** 直接在提示词中粘贴错误、日志、屏幕截图和计划输出，或键入 `@` 来引用文件。Claude 读取源而不是你对它的描述。

```text wrap theme={null}
why is the build failing? @build.log
```

**说出你想要答案的方式。** 命名格式、长度或受众，以便解释适合你将如何使用它。要使格式成为每个响应的默认值，请设置 [输出样式](/docs/zh-CN/output-styles)。

```text wrap theme={null}
explain how the payment retry logic works as an HTML page with a diagram, then open it in my browser
```

有关每个模式的更多信息，请参阅[最佳实践](/docs/zh-CN/best-practices)。

<h2 id="where-these-come-from">
  这些来自哪里
</h2>

这些提示词基于已发布的 Anthropic 资源中的模式。每张卡片都链接到其来源：

* [常见工作流](/docs/zh-CN/common-workflows)：核心任务的分步指南
* [最佳实践](/docs/zh-CN/best-practices)：提示词模式和项目设置
* [Anthropic 团队如何使用 Claude Code](https://claude.com/blog/how-anthropic-teams-use-claude-code)：来自工程、产品、设计和数据团队的真实工作流，深入探讨[法律](https://claude.com/blog/how-anthropic-uses-claude-legal)、[营销](https://claude.com/blog/how-anthropic-uses-claude-marketing)和[网络安全](https://claude.com/blog/how-anthropic-uses-claude-cybersecurity)
* [扩展代理编码指南](https://resources.anthropic.com/hubfs/Scaling%20agentic%20coding%20across%20your%20organization.pdf)：企业采用指南

有关这些模式的视频演练，请参阅 [Claude Academy](https://academy.claude.com/) 上的免费 [Claude Code in Action](https://academy.claude.com/courses/claude-code-in-action) 课程。

<h2 id="related-resources">
  相关资源
</h2>

此页面上的提示词是起点。一旦一个对你的项目有效，下一步是使其可重复：将其保存为 [技能](/docs/zh-CN/skills)，以便团队中的任何人都可以将其作为 `/command` 运行，并在 [CLAUDE.md](/docs/zh-CN/memory) 中记录 Claude 学到的约定，以便每个会话都以该上下文开始，而不是 Claude 重新学习它。对于更大或更危险的更改，[Plan Mode](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode) 在任何编辑发生前显示文件列表。

如果你在团队中引入 Claude Code，请参阅[管理](/docs/zh-CN/admin-setup)以获取托管设置和策略，以及[成本和使用](/docs/zh-CN/costs)以了解此工作如何在你的计划上计费。
