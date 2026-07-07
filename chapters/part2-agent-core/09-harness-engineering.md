# Harness Engineering:给 Agent 装上运行时外骨架 `[主线]` ★

如果说 Prompt 是你写给模型看的工作说明,Context 是你摆在模型面前的工作材料,那么 Harness 就是模型和真实世界之间的运行时外骨架。

没有 Harness 的 Agent 很像一个很会说话但没有安全边界的实习生:它能建议下一步,但你不能让它直接接触数据库、文件系统、支付接口、邮件系统和生产环境。

Harness Engineering 关心的问题是:

> 模型提出的动作,如何被系统验证、授权、执行、记录、恢复和评估?

公开工程讨论里,Harness 常被用来指“模型本体之外,让 Agent 能稳定干活的那套代码、配置、协议和基础设施”。这个词和测试里的 test harness 有相通之处:模型不是直接撞向真实世界,而是被一套外部结构固定、约束、供给输入、接收输出并观察结果。放到 Agent 里,Harness Engineering 就是系统化设计这套外部结构。

所以不要把 Harness 理解成某个特定框架名。它更像一个工程边界词:只要你在设计工具注册、schema、权限、执行器、sandbox、trace、错误协议和回滚,你就在做 Harness Engineering。

这是一层经常被低估的工程。很多 Agent Demo 可以没有强 Harness,因为它只读文件、只生成文本、失败了刷新一下就好。生产系统不行。只要 Agent 能调用工具、写状态、触发外部副作用,Harness 就不是可选项。

![Harness Engineering 运行时边界](../assets/part2-harness-engineering-runtime-boundary.svg)

本章会讲:

- Harness 到底是什么。
- 它和 API wrapper、Function Calling、ACI 的区别。
- Harness 的状态、动作、观察三个核心契约。
- 控制面和数据面如何分离。
- 权限、预算、sandbox、trace、回滚为什么属于 Harness。
- 如何评估一个 Harness 是否可靠。

## Harness 不是 API wrapper

很多人第一次写 Agent 工具时,会这样做:

```python
if model_wants_tool_call:
    result = call_api(model_arguments)
    append_to_messages(result)
```

这只是 API wrapper,不是完整 Harness。

API wrapper 只回答:

> 怎么把函数调起来?

Harness 要回答更多问题:

- 模型是否被允许调用这个工具?
- 参数是否有效?
- 参数是否来自可信来源?
- 工具是否会产生副作用?
- 当前任务状态是否允许执行?
- 是否需要用户确认?
- 失败后如何反馈给模型?
- 执行结果如何写回状态?
- 这次动作如何被审计和复现?
- 如果动作做错了,能否回滚或补偿?

少了这些问题,Agent 看起来能跑,但一遇到真实环境就会失控。

## Harness 的核心边界

最重要的边界是这句:

**模型提出动作,系统执行动作。**

模型可以输出:

```json
{
  "action": "delete_file",
  "path": "reports/final.md"
}
```

但系统不应该因为模型这么说就删除文件。

Harness 必须先判断:

- `delete_file` 是否在当前动作空间中。
- 当前用户是否有删除权限。
- 路径是否在允许工作区。
- 文件是否受保护。
- 删除是否需要确认。
- 是否已经生成 preview。
- 是否能恢复。
- trace 是否记录了发起原因和确认人。

这就是从“模型能调用工具”到“系统可以安全执行工具”的差别。

## 三个核心契约:State、Action、Observation

Harness 最核心的设计,不是某个框架类名,而是三个契约。

![Harness 的状态、动作和观察契约](../assets/part2-harness-engineering-contracts.svg)

### State 契约

State 是任务当前的系统事实。

它不应该只是聊天历史。一个可靠 State 至少包含:

| 字段 | 用途 |
| --- | --- |
| `goal` | 用户真正要完成什么 |
| `constraints` | 系统、用户、安全和业务约束 |
| `plan` | 当前计划和阶段 |
| `observations` | 工具和环境返回的事实 |
| `actions_taken` | 已执行动作和结果 |
| `artifacts` | 文件、报告、diff、证据包等产物 |
| `permissions` | 当前可用能力和授权范围 |
| `budget` | 轮数、成本、时间、工具调用限制 |
| `status` | running、needs_user、blocked、done、failed |

State 的关键是**由 runtime 维护**。

模型可以建议如何更新状态,但最终写入必须由系统控制。否则模型可能把猜测写成事实,把失败写成成功,把临时假设写成长期记忆。

### Action 契约

Action 是模型提出的动作请求。

一个好的 Action 不只是工具名和参数,还应该包含:

| 字段 | 用途 |
| --- | --- |
| `type` | final、tool_call、ask_user、handoff、abort |
| `tool` | 工具名 |
| `arguments` | 参数 |
| `reason_summary` | 简短说明为什么需要这步 |
| `risk_level` | none、low、medium、high |
| `idempotency_key` | 防止重复执行 |
| `requires_confirmation` | 是否需要确认 |

注意 `reason_summary` 不是要求暴露完整思维链。它是工程解释,用于审计和用户确认。例如:

```json
{
  "type": "tool_call",
  "tool": "run_tests",
  "arguments": {"target": "UserService.test.ts"},
  "reason_summary": "验证刚才修改是否修复 active 默认值问题",
  "risk_level": "low",
  "requires_confirmation": false
}
```

Action 契约越清楚,Harness 越容易做校验。

### Observation 契约

Observation 是工具或环境返回给系统的反馈。

它不应该只是一段自然语言。

例如测试工具失败时,不要只返回:

```text
Tests failed.
```

更好的 Observation 是:

```json
{
  "ok": false,
  "error_type": "test_failure",
  "summary": "1 test failed: creates active user by default",
  "details_ref": "trace://run_tests/turn-4/full-log",
  "key_facts": [
    "expected user.active === true",
    "actual user.active === undefined",
    "failure points to src/user-service.ts:18"
  ],
  "retryable": true
}
```

这样下一轮模型看到的是可行动信息,不是一团日志。

Observation 契约还可以防止模型假装成功。只要 `ok=false`,Loop 就不能进入 `done` 状态。

## 控制面和数据面

Harness 可以分成两部分:控制面和数据面。

![Harness 控制面和数据面](../assets/part2-harness-engineering-control-plane.svg)

### 数据面

数据面负责搬运信息:

- 构建 Context。
- 接收 Action。
- 调用工具。
- 返回 Observation。
- 保存 artifact。
- 写 trace。

数据面关心的是“信息怎么流动”。

### 控制面

控制面负责决定什么可以发生:

- 权限。
- 策略。
- 风险分级。
- 预算。
- 速率限制。
- 用户确认。
- sandbox。
- 回滚策略。

控制面关心的是“动作是否被允许”。

真正危险的设计,是把控制面写进 Prompt:

```text
请不要做危险操作。
```

这可以作为模型行为提示,但不能作为系统边界。

更可靠的设计是:

```python
if action.risk_level == "high":
    require_user_confirmation(action)

if not policy.allowed(user, action, state):
    reject_action(action)

if not sandbox.within_scope(action):
    reject_action(action)
```

模型可以犯错,控制面不能跟着犯错。

## Harness 和 Function Calling 的关系

Function Calling 解决的是:

> 模型如何用结构化形式表达工具调用?

Harness 解决的是:

> 这个结构化工具调用是否应该执行,如何执行,如何记录,失败后如何处理?

它们是相邻但不同的层。

| 维度 | Function Calling | Harness |
| --- | --- | --- |
| 关注点 | 模型输出结构化动作 | 系统执行动作的边界 |
| 典型内容 | tool schema、arguments | validation、policy、executor、trace |
| 错误类型 | JSON 不合法、参数缺失 | 越权、副作用、重复执行、失败恢复 |
| 谁负责 | 模型接口 + prompt/schema | runtime |

所以有 Function Calling 不等于有 Harness。

## Harness 和 ACI 的关系

ACI 强调工具要适合 Agent 使用。比如工具名清晰、参数少、返回结构化、错误可恢复。

Harness 则是运行这些工具的系统外骨架。

可以这样理解:

- ACI 设计“工具长什么样”。
- Harness 设计“工具如何被安全使用”。

一个好工具 schema 是 ACI 的成果。但这个工具是否能被当前用户调用,调用是否需要确认,失败如何重试,这些属于 Harness。

## 动作风险分级

Harness 必须知道不同动作的风险不同。

| 风险级别 | 例子 | 控制策略 |
| --- | --- | --- |
| L0 纯文本 | 生成摘要、解释概念 | 可直接执行 |
| L1 只读查询 | 搜索文档、读取文件 | 权限和范围校验 |
| L2 临时计算 | 运行测试、生成草稿 | sandbox、超时、资源限制 |
| L3 可回滚写入 | 修改草稿文件、创建 PR | diff preview、回滚点 |
| L4 外部副作用 | 发邮件、付款、删数据 | 强确认、审计、最小权限 |

风险分级不是为了吓人,而是为了给不同动作配置不同 Harness。

不要用同一套规则处理“读取 README”和“发送客户邮件”。

## 参数来源追踪

一个经常被忽视的问题是:工具参数从哪里来?

例如模型要调用:

```json
{
  "tool": "refund_order",
  "arguments": {
    "order_id": "O-1024",
    "amount": 199
  }
}
```

Harness 不应该只检查 `order_id` 是字符串、`amount` 是数字。

还要问:

- `order_id` 来自用户输入、数据库查询,还是模型猜的?
- `amount` 是否来自可信订单记录?
- 当前用户是否有权退款这个订单?
- 退款金额是否超过订单金额?
- 是否需要人工确认?

所以 Action 契约最好支持参数来源:

```json
{
  "order_id": {
    "value": "O-1024",
    "source": "tool:lookup_order#turn-3",
    "trust": "verified"
  }
}
```

这对防止模型编造关键参数非常重要。

## Sandbox 和执行环境

只要工具能执行代码、命令、浏览器操作或文件写入,Harness 就应该考虑 sandbox。

Sandbox 可以限制:

- 文件系统范围。
- 网络访问。
- 环境变量。
- 命令白名单。
- CPU、内存和时间。
- 可写目录。
- 外部凭据。

例如代码修复 Agent 可以在临时工作区中修改文件、运行测试,确认 diff 后再应用到真实仓库。

这种设计让错误更容易恢复。

## Idempotency:避免重复副作用

Loop 中常会发生重试。如果工具有副作用,重复执行可能很危险。

例如:

- 重复发送邮件。
- 重复创建工单。
- 重复扣款。
- 重复写入数据库。

Harness 应给副作用动作设计 idempotency key。

```json
{
  "tool": "create_ticket",
  "arguments": {...},
  "idempotency_key": "task-123:create-ticket:billing-error"
}
```

如果同一个 key 已经成功执行,Harness 应返回已有结果,而不是再次执行。

## Preview、Confirm、Commit

高风险写操作最好分三段:

```text
preview -> confirm -> commit
```

例如发送邮件:

1. `draft_email`:生成草稿,无副作用。
2. `preview_email`:展示收件人、主题、正文、附件。
3. `send_email`:用户确认后发送。

例如修改代码:

1. `propose_patch`:生成 diff。
2. `run_tests`:验证。
3. `apply_patch`:写入。

这种拆分比在 Prompt 里写“发送前请小心”可靠得多。

## Trace:Harness 的黑匣子

Harness 必须留下 trace。一个动作 trace 至少包括:

```json
{
  "turn": 5,
  "state_id": "task-17:v8",
  "model": "model-version",
  "prompt_version": "research-agent-v3",
  "action": {
    "type": "tool_call",
    "tool": "send_email",
    "arguments_hash": "...",
    "risk_level": "high"
  },
  "validation": {
    "schema_ok": true,
    "permission_ok": true,
    "confirmation": "user-confirmed"
  },
  "result": {
    "ok": true,
    "artifact_ref": "email://draft-123"
  }
}
```

Trace 的价值不是“记录越多越好”,而是让系统可以回答:

- 为什么执行了这个动作?
- 执行前看到了什么状态?
- 谁授权了它?
- 工具返回了什么?
- 后续回答是否基于真实 Observation?
- 失败能否复现?

没有 trace 的 Harness,几乎无法生产化。

## 错误协议

Harness 不应该把所有错误都丢给模型猜。

错误返回应结构化:

```json
{
  "ok": false,
  "error_type": "permission_denied",
  "message": "当前用户不能访问 billing 数据源",
  "retryable": false,
  "suggested_next_actions": ["ask_user_for_permission", "continue_without_billing_data"]
}
```

错误类型至少包括:

| 错误 | 含义 | 后续策略 |
| --- | --- | --- |
| `schema_error` | 参数结构不合法 | 让模型修参数 |
| `permission_denied` | 权限不足 | 请求授权或停止 |
| `policy_blocked` | 策略拒绝 | 不应重试同动作 |
| `timeout` | 工具超时 | 有限重试或降级 |
| `not_found` | 资源不存在 | 改查询或请求用户 |
| `side_effect_failed` | 写操作失败 | 报告状态,不要假装成功 |

错误协议是 Loop 能否自我修正的基础。

## Harness 的最小伪代码

下面是一个框架无关的 Harness 形状:

```python
def handle_action(action, state, user, tool_registry):
    if not action_schema_valid(action):
        return observation_error("schema_error", retryable=True)

    tool = tool_registry.get(action.tool)
    if tool is None:
        return observation_error("unknown_tool", retryable=True)

    risk = classify_risk(tool, action.arguments, state)
    if not policy_allowed(user, action, risk, state):
        return observation_error("policy_blocked", retryable=False)

    if risk.requires_confirmation:
        preview = tool.preview(action.arguments)
        return ask_user_confirmation(preview, action)

    with sandbox_for(tool, state) as sandbox:
        result = tool.execute(action.arguments, sandbox=sandbox)

    observation = normalize_result(result)
    trace_action(action, state, observation, risk)
    return observation
```

关键点是:

- schema 校验在执行前。
- policy 校验在执行前。
- 高风险动作先 preview/confirm。
- 工具运行在受控环境。
- 返回 Observation,不是随便一段字符串。
- 每次动作都写 trace。

## Harness 的质量指标

评估 Harness 不能只看任务成功率。还要看边界是否真的生效。

| 指标 | 说明 |
| --- | --- |
| schema 拒绝率 | 模型生成非法动作时是否被拦住 |
| 未知工具拒绝率 | 模型幻觉工具时是否被拦住 |
| 权限拦截率 | 越权动作是否被拒绝 |
| 高风险确认覆盖率 | L3/L4 动作是否都有确认 |
| 工具失败显式率 | 失败是否进入 Observation |
| 重复副作用防护率 | 幂等机制是否避免重复执行 |
| trace 完整率 | 动作是否可复现和审计 |
| 回滚成功率 | 写操作失败后能否恢复 |

这些指标比“模型看起来听话”更重要。

## Harness 设计清单

给一个实用检查表:

| 问题 | 是否必须回答 |
| --- | --- |
| 工具动作空间是否显式注册? | 是 |
| 每个工具是否有 schema、描述、风险等级? | 是 |
| 参数是否校验类型、范围、来源和业务规则? | 是 |
| 当前用户权限是否参与工具决策? | 是 |
| 高风险动作是否 preview/confirm? | 是 |
| 写操作是否有幂等或回滚策略? | 是 |
| 工具失败是否结构化返回? | 是 |
| Observation 是否写回 State? | 是 |
| 每次动作是否可审计? | 是 |

如果这些问题大多答不上来,系统还不能算有可靠 Harness。

## 常见误解

### 误解一:有 Function Calling 就有 Harness

不是。Function Calling 只是结构化表达动作,Harness 负责动作能否执行和如何执行。

### 误解二:工具都是内部 API,所以不需要权限

不对。内部 API 也可能读敏感数据、写生产状态、触发外部副作用。Agent 的调用路径更需要最小权限。

### 误解三:只读工具都安全

不一定。只读工具可能泄露隐私、商业机密或跨租户数据。读取也需要权限和数据最小化。

### 误解四:让模型解释理由就能审计

不够。模型解释只是补充。真正的审计来自状态、动作、校验、确认、工具返回和 trace。

### 误解五:Harness 会限制 Agent 智能

Harness 限制的是不可控动作,不是智能本身。好的 Harness 让模型在安全动作空间中发挥能力,并让错误可恢复。

## 本章小结

Harness Engineering 是 Agent 从 Demo 走向生产的关键层。它把模型的动作建议变成可验证、可授权、可执行、可记录、可恢复的系统事件。Harness 的核心不是包装 API,而是设计 State、Action、Observation 契约,分离控制面和数据面,实现 schema 校验、权限策略、sandbox、预算、preview/confirm、幂等、错误协议和 trace。模型可以建议下一步,但系统必须控制下一步是否真的发生。

下一章会讲 Loop Engineering。Harness 保证单步动作可控,Loop 则保证多步任务能持续推进并最终收敛。
