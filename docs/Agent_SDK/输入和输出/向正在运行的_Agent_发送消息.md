> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 向正在运行的 Agent 发送消息

> 通过流式输入向同一个 Agent SDK 会话发送后续消息和图像，读取每条回复，并中断回复以重新引导 Claude。

流式输入会让 Agent SDK 会话保持打开状态，以便您的应用程序在其运行期间向其发送多条消息。您还可以在消息中附加图像，并在回复进行到一半时停止它以重新引导 Claude。

> [!NOTE]
>
> 流式输入涵盖您发送的消息。要在 Claude 生成回复时将其显示出来，请参阅[实时流式传输响应](https://code.claude.com/docs/zh-CN/agent-sdk/streaming-output.md)。

## 选择单次输入或流式输入

对于与 Claude 进行对话的应用程序（例如聊天界面），请选择流式输入。使用流式输入可以在消息中附加图像、中断回复，或在会话运行期间[切换模型或权限模式](https://code.claude.com/docs/zh-CN/agent-sdk/configuration.md#change-configuration-mid-session)。

单次调用会将一个提示词字符串传递给 `query()`。Claude 回答后，调用即结束。单次调用适用于单个任务，例如 serverless 函数。要在该调用结束后继续跟进，请启动一个恢复该会话的新调用。有关更多信息，请参阅[继续、恢复和分叉](https://code.claude.com/docs/zh-CN/agent-sdk/sessions.md#continue-resume-and-fork)。

## 向会话发送多条消息

* **TypeScript**：编写一个 yield [`SDKUserMessage`](https://code.claude.com/docs/zh-CN/agent-sdk/typescript#sdkusermessage) 对象的 [async generator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function%2A)，并将其作为 `query()` 的 `prompt` 传入。让生成器在两次 yield 之间等待用户的下一条消息。
* **Python**：打开一个 `ClaudeSDKClient`，并将每条消息传递给 `client.query()`。对于文本消息，传入字符串。要附加图像，请传入一个 yield 用户消息字典的 [async generator](https://docs.python.org/3/glossary.html#term-asynchronous-generator)。

要让 Claude 在各自独立的回复中回答每条消息，请在发送下一条消息之前，等待上一条回复的[结果消息](#read-each-response)：

* **TypeScript**：让您的生成器 await 一个 promise。在遍历 `query()` 的 `for await` 循环中，当结果消息到达时 resolve 该 promise。
* **Python**：在您的 [`receive_response()`](https://code.claude.com/docs/zh-CN/agent-sdk/python#claudesdkclient) 循环结束后，使用下一条消息调用 `client.query()`。

> [!NOTE]
>
> 您在工具调用期间发送的消息会在这些工具调用完成后到达 Claude。随后 Claude 会在一条回复中同时回答它和您之前的消息。如果该轮次先结束，Claude 会为它开始一个新的轮次。有关详细信息，请参阅[轮次和预算](https://code.claude.com/docs/zh-CN/agent-sdk/agent-loop.md#turns-and-budget)。

### 发送带有图像的后续消息

此示例先发送一个文本问题，然后发送一条带有图像的后续消息，并打印 Claude 对每条消息的回复。运行之前，请在工作目录中将一张 PNG 图像保存为 `diagram.png`：

```typescript TypeScript theme={null}
import { readFile } from "node:fs/promises";
import { query, type SDKUserMessage } from "@anthropic-ai/claude-agent-sdk";

let firstResponseDone!: () => void;
const firstResponseFinished = new Promise<void>((resolve) => {
  firstResponseDone = resolve;
});

async function* messages(): AsyncGenerator<SDKUserMessage> {
  yield {
    type: "user",
    message: {
      role: "user",
      content: "Explain in two sentences what a message queue does.",
    },
    parent_tool_use_id: null,
  };

  await firstResponseFinished;

  const image = await readFile("diagram.png");
  yield {
    type: "user",
    message: {
      role: "user",
      content: [
        { type: "text", text: "Describe this image in one sentence." },
        {
          type: "image",
          source: {
            type: "base64",
            media_type: "image/png",
            data: image.toString("base64"),
          },
        },
      ],
    },
    parent_tool_use_id: null,
  };
}

let responses = 0;
for await (const message of query({ prompt: messages() })) {
  if (message.type === "assistant") {
    for (const block of message.message.content) {
      if (block.type === "text") {
        console.log(block.text);
      }
    }
  } else if (message.type === "result") {
    responses += 1;
    console.log(`Response ${responses} finished: ${message.subtype}`);
    if (responses === 1) {
      firstResponseDone();
    }
  }
}
```

```python Python theme={null}
import asyncio
import base64
from pathlib import Path

from claude_agent_sdk import AssistantMessage, ClaudeSDKClient, ResultMessage, TextBlock


async def image_message():
    image_data = base64.b64encode(Path("diagram.png").read_bytes()).decode()
    yield {
        "type": "user",
        "message": {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image in one sentence."},
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data,
                    },
                },
            ],
        },
    }


async def main():
    async with ClaudeSDKClient() as client:
        await client.query("Explain in two sentences what a message queue does.")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
            elif isinstance(message, ResultMessage):
                print(f"Response 1 finished: {message.subtype}")

        await client.query(image_message())
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
            elif isinstance(message, ResultMessage):
                print(f"Response 2 finished: {message.subtype}")


asyncio.run(main())
```

运行任一版本时，示例都会打印 `Response 1 finished: success` 和 `Response 2 finished: success`。

如果 Claude 没有看到您的图像，请参阅[图像无法处理](https://code.claude.com/docs/zh-CN/agent-sdk/troubleshooting.md#image-could-not-be-processed)。

### 在 TypeScript 中从聊天界面传入消息

通过队列将用户的消息传入您的提示词生成器：

* **`pushMessage()`**：界面的输入处理程序会针对用户发送的每条消息调用此函数。
* **`closeInput()`**：当用户关闭聊天时，处理程序会调用此函数。
* **`userMessages()`**：您作为 `query()` 的 `prompt` 传入的生成器。

`pushMessage()` 会将每条消息添加到一个数组中，生成器从该数组中读取。当数组为空时，生成器会一直等待，直到有消息到达或聊天关闭：

```typescript theme={null}
import type { SDKUserMessage } from "@anthropic-ai/claude-agent-sdk";

const pending: string[] = [];
let wake: (() => void) | null = null;
let closed = false;

// The interface's input handler calls this with each message the user sends.
function pushMessage(text: string): void {
  pending.push(text);
  wake?.();
}

// The interface calls this when the user closes the chat.
function closeInput(): void {
  closed = true;
  wake?.();
}

async function* userMessages(): AsyncGenerator<SDKUserMessage> {
  while (true) {
    const text = pending.shift();
    if (text !== undefined) {
      yield { type: "user", message: { role: "user", content: text }, parent_tool_use_id: null };
    } else if (closed) {
      return;
    } else {
      await new Promise<void>((resolve) => (wake = resolve));
      wake = null;
    }
  }
}
```

您在回复期间推送的消息可能会共用一条回复。要选择 Claude 何时读取您在回复期间推送的消息，请设置该消息的 [`priority`](https://code.claude.com/docs/zh-CN/agent-sdk/typescript#sdkusermessage) 字段。

## 读取每条回复

Claude 会以一条结果消息结束每条回复。

* **TypeScript**：遍历 `query()` 的 `for await` 循环会按顺序 yield 每条回复的消息。在您的生成器返回后，该循环会在最后一条回复的结果消息之后结束。要将结果与其所回答的消息对应起来，请在您发送的每条消息上设置 `uuid`，并读取结果的 [`user_message_uuids`](https://code.claude.com/docs/zh-CN/agent-sdk/typescript#user_message_uuids)。
* **Python**：为每条回复启动一个 `receive_response()` 循环，因为每个循环都会在下一条 [`ResultMessage`](https://code.claude.com/docs/zh-CN/agent-sdk/python#resultmessage) 之后停止。客户端会在消息之间保留对话的上下文。有关更多信息，请参阅[自动会话管理](https://code.claude.com/docs/zh-CN/agent-sdk/sessions.md#automatic-session-management)。

结果消息的 `subtype` 字段会报告回复是如何结束的，例如 `success` 或 `error_during_execution`。

如果最后一条回复以错误结果结束：

* **TypeScript**：遍历 `query()` 的循环会 yield 该结果，然后抛出异常。将循环包装在 `try`/`catch` 中以处理该异常。要在抛出异常后继续对话，请启动一个新的 `query()` 调用来[恢复会话](https://code.claude.com/docs/zh-CN/agent-sdk/sessions.md#continue-resume-and-fork)。当您的生成器仍有消息要发送时，较早回复的错误结果不会抛出异常。
* **Python**：`ClaudeSDKClient` 上的 `receive_response()` 会 yield 错误结果，而不会引发异常。

有关每种结果子类型的含义，请参阅[处理结果](https://code.claude.com/docs/zh-CN/agent-sdk/agent-loop.md#handle-the-result)。

## 中断 Claude 的回复

要在回复进行到一半时停止它并保持会话打开，请在运行会话的对象上调用 `interrupt()`：

* **TypeScript**：将 async generator 作为 `prompt` 传入，保存 `query()` 返回的 [`Query` 对象](https://code.claude.com/docs/zh-CN/agent-sdk/typescript#query-object)，并在其上调用 `interrupt()`。
* **Python**：在 `ClaudeSDKClient` 上调用 `interrupt()`。如果有 `receive_response()` 循环正在读取该回复，该循环会在被中断回复的 `ResultMessage` 处结束。请在该结果到达后再发送下一条消息。

当您在回复期间调用 `interrupt()` 时，该回复会以 `error_during_execution` 结果结束。您在中断之前发送但 Claude 尚未读取的消息，仍会在被中断的回复结束后到达 Claude。有关最后一条回复为错误结果时 TypeScript 循环的行为，请参阅[读取每条回复](#read-each-response)。

此示例要求 Claude 写一篇长文章。示例在会话开始三秒后调用 `interrupt()`，然后在被中断的回复结束后向同一会话发送第二条消息：

```typescript TypeScript theme={null}
import { query, type SDKUserMessage } from "@anthropic-ai/claude-agent-sdk";

let firstResponseDone!: () => void;
const firstResponseFinished = new Promise<void>((resolve) => {
  firstResponseDone = resolve;
});

async function* messages(): AsyncGenerator<SDKUserMessage> {
  yield {
    type: "user",
    message: {
      role: "user",
      content: "Write a 2,000-word essay on the history of the printing press.",
    },
    parent_tool_use_id: null,
  };

  await firstResponseFinished;

  yield {
    type: "user",
    message: {
      role: "user",
      content: "In one sentence, what is a prime number?",
    },
    parent_tool_use_id: null,
  };
}

const conversation = query({ prompt: messages() });

let responses = 0;
for await (const message of conversation) {
  if (message.type === "system" && message.subtype === "init" && responses === 0) {
    setTimeout(async () => {
      await conversation.interrupt();
      console.log("Interrupt sent");
    }, 3000);
  } else if (message.type === "assistant") {
    for (const block of message.message.content) {
      if (block.type === "text") {
        console.log(block.text);
      }
    }
  } else if (message.type === "result") {
    responses += 1;
    console.log(`Response ${responses} finished: ${message.subtype}`);
    if (responses === 1) {
      firstResponseDone();
    }
  }
}
```

```python Python theme={null}
import asyncio

from claude_agent_sdk import AssistantMessage, ClaudeSDKClient, ResultMessage, TextBlock


async def main():
    async with ClaudeSDKClient() as client:
        await client.query("Write a 2,000-word essay on the history of the printing press.")
        await asyncio.sleep(3)
        await client.interrupt()
        print("Interrupt sent")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
            elif isinstance(message, ResultMessage):
                print(f"Response 1 finished: {message.subtype}")

        await client.query("In one sentence, what is a prime number?")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
            elif isinstance(message, ResultMessage):
                print(f"Response 2 finished: {message.subtype}")


asyncio.run(main())
```

运行任一版本时，第一条回复会在文章写到一半时停止，示例会打印 `Response 1 finished: error_during_execution`。随后 Claude 会回答第二条消息。输出以 `Response 2 finished: success` 结束。

## 后续步骤

* [实时流式传输响应](https://code.claude.com/docs/zh-CN/agent-sdk/streaming-output.md)：在 Claude 生成文本和工具调用时将其显示出来
* [处理批准和用户输入](https://code.claude.com/docs/zh-CN/agent-sdk/user-input.md)：回应 Claude 的权限请求和澄清问题
* [在会话中途更改配置](https://code.claude.com/docs/zh-CN/agent-sdk/configuration.md#change-configuration-mid-session)：在会话运行期间切换模型或权限模式
* TypeScript 中的 [`Query` 对象](https://code.claude.com/docs/zh-CN/agent-sdk/typescript#query-object)和 Python 中的 [`ClaudeSDKClient`](https://code.claude.com/docs/zh-CN/agent-sdk/python#claudesdkclient)：向正在运行的会话发送消息或控制会话的方法
* [使用会话](https://code.claude.com/docs/zh-CN/agent-sdk/sessions.md)：恢复、继续或分叉对话
