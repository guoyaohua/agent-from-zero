# 可观测性与调试 `[主线]`

Agent 上线后,最怕的不是它偶尔答错,而是你不知道它为什么答错。

用户看到的是最终答案,但 Agent 背后发生了很多事:

- 构建上下文。
- 检索记忆和文档。
- 调用模型。
- 选择工具。
- 填参数。
- 执行工具。
- 更新状态。
- 触发护栏。
- 生成最终输出。

任何一层出错,最终结果都可能错。没有可观测性,你只能反复改 prompt,像在黑盒上敲门。

![Agent 可观测性 Trace](../assets/part5-observability-trace.svg)

本章会讲:

- Agent 可观测性和普通日志有什么不同。
- Trace、span、artifact、state diff 应记录什么。
- 如何定位错误发生在上下文、模型、工具、状态还是策略。
- 如何调试长任务、多工具和多 Agent。
- 如何用可观测数据支撑评估和回归。

## 为什么普通日志不够

传统服务日志常记录:

```text
request_id, endpoint, status_code, latency, error
```

这对普通 API 有用,但对 Agent 不够。

因为 Agent 的结果不是单个函数决定的,而是多个概率决策和外部动作共同产生。

你需要知道:

- 模型看到了什么上下文。
- 它为什么选择这个工具。
- 工具参数从哪里来。
- 工具返回了什么。
- 哪些证据进入了最终回答。
- 哪个护栏允许或拦截了动作。
- 状态在每一步如何变化。

没有这些,你无法判断是模型错、检索错、工具错、状态错,还是系统规则没有生效。

## Trace 是 Agent 的时间线

Trace 是一次任务从开始到结束的完整时间线。

一个 trace 可以包含多个 span:

```text
trace: refund_task_17
  span: build_context
  span: model_call_plan
  span: tool_call_get_order
  span: retrieve_policy
  span: model_call_decide
  span: guardrail_check
  span: final_response
```

每个 span 记录一个可观察步骤。

Trace 的目标是让你能复盘:

```text
当时系统看到什么,做了什么,为什么这么做,结果是什么。
```

## Span 应记录什么

不同 span 记录内容不同。

### 模型调用 span

应记录:

- model name 和版本。
- prompt/context pack 的引用或脱敏快照。
- 输入 token、输出 token。
- temperature、top_p 等参数。
- 输出文本或结构化 tool call。
- latency 和 cost。
- 解析或 schema 校验结果。

### 工具调用 span

应记录:

- tool name。
- call id。
- 参数。
- 参数来源。
- 权限决策。
- 执行状态。
- 错误码。
- 原始 artifact。
- 副作用类型。
- 幂等 key。

### 检索 span

应记录:

- query 原文和改写结果。
- 检索源。
- top-k 候选。
- 分数和元数据。
- rerank 后排名。
- 最终证据包。

### 状态更新 span

应记录:

- state diff。
- 哪个事件触发更新。
- 哪些假设被确认或否定。
- 哪些约束新增、覆盖或废弃。

## Artifact:大对象不要塞进日志

工具输出、文件内容、长网页、测试日志可能很大。

不要把它们全部塞进 trace 主体。更好的做法是保存 artifact 引用:

```json
{
  "summary": "UserService test failed: active expected true, got undefined.",
  "artifact": "tool-result://test-17"
}
```

Trace 保存摘要和引用。需要复查时再打开 artifact。

这样既控制日志体积,也保留回源能力。

## Context pack 可观测

上下文工程如果不可观测,就很难调试。

每次模型调用前,最好保存 context pack 的结构:

```json
{
  "system_rules_tokens": 420,
  "state_summary_tokens": 310,
  "memory_ids": ["M12", "M19"],
  "evidence_ids": ["S1", "S3"],
  "tool_names": ["search_policy", "get_order"],
  "redactions": ["customer_email"],
  "total_tokens": 3900
}
```

这能回答很多问题:

- 关键证据是否进入上下文?
- 工具 schema 是否过多?
- 是否注入了过期记忆?
- 输出格式要求是否被长证据淹没?
- 敏感数据是否被脱敏?

## State diff 比最终 state 更重要

只保存最终状态还不够。要保存每步 state diff。

例如:

```json
{
  "before": {"status": "running", "current_step": "retrieve_policy"},
  "event": "evidence_pack_received",
  "after": {"status": "running", "current_step": "check_eligibility"}
}
```

当 Agent 走错路时,state diff 能告诉你哪一步把状态更新错了。

很多“模型忘记了”其实是状态没有正确更新,或 context builder 没把状态放进去。

## 调试的分层方法

当一个 Agent 答错,不要先改 prompt。按层排查。

### 1. 目标层

用户目标和约束是否被正确解析?

### 2. 上下文层

模型是否看到了必要信息? 是否看到太多噪声?

### 3. 检索层

正确证据是否存在、召回、排前、进入证据包?

### 4. 模型层

模型是否误读证据、格式错误、错误调用工具?

### 5. 工具层

参数是否正确? 工具是否成功? 返回是否可信?

### 6. 状态层

观察是否正确写入 state? 旧假设是否被清除?

### 7. 策略层

权限、护栏、确认和数据流策略是否生效?

这种分层能避免把所有问题都归因于“模型不行”。

## 一个调试案例

用户问:

```text
这个订单能不能退款?
```

Agent 回答:

```text
可以退款,我已经提交了退款申请。
```

但实际系统要求用户确认后才能提交。

Trace 排查:

1. 目标层:用户只问能不能退款,没有要求提交。
2. 检索层:政策证据只支持“可创建退款草稿”。
3. 工具层:Agent 调用了 `submit_refund`,不是 `create_refund_draft`。
4. 策略层:runtime 没有阻止缺少确认的写工具。

根因不是单纯回答错误,而是工具权限和确认策略缺失。修复应该在 runtime 加策略门,不是只在 prompt 里写“提交前要确认”。

## 可观测性指标

Agent 指标可以分几类。

| 类别 | 指标 |
| --- | --- |
| 质量 | 任务成功率、引用准确率、工具参数正确率 |
| 成本 | tokens/task、cost/task、model calls/task |
| 延迟 | P50/P95 总延迟、工具等待时间、首 token 时间 |
| 稳定性 | schema 失败率、重试率、超时率 |
| 安全 | 被拦截动作数、未确认写操作数、数据流违规数 |
| 检索 | recall@k、rerank 命中率、无证据回答率 |
| 记忆 | 记忆命中率、过期记忆使用率、冲突处理率 |

指标要能连接到 trace。只有数字没有样本,很难改进。

## 多 Agent 可观测性

多 Agent 还要记录:

- 每个 Agent 的输入和输出。
- 消息 envelope。
- 角色间交接。
- Orchestrator 状态更新。
- 并行任务的 parent/child span。
- 冲突和仲裁。
- 哪个角色的产物进入最终答案。

多 Agent 没有 trace,就像看一场会议的最终纪要,却不知道谁说了什么、谁做了决定、依据是什么。

## 日志脱敏和隐私

可观测性会收集大量敏感信息。

必须设计:

- PII 脱敏。
- 密钥和 token 过滤。
- artifact 访问权限。
- 日志保留期限。
- 租户隔离。
- 用户删除请求处理。

不要为了调试把所有 prompt、工具结果和用户数据永久明文保存。

## 从 trace 到评估样本

可观测性不只是排查线上问题,也是评估数据来源。

失败 trace 可以回流成:

- 回归测试样本。
- hard negative。
- 工具使用错误样本。
- prompt injection 样本。
- 成本延迟异常样本。
- 人工标注任务。

成熟系统会把线上失败变成离线评估资产。

## 常见误解

### 误解一:有日志就有可观测性

不够。需要结构化 trace、span、artifact、state diff 和策略决策。

### 误解二:只看最终答案就能调试

不能。最终答案错可能来自上下文、检索、工具、状态或安全策略。

### 误解三:保存完整 prompt 最安全

不一定。完整 prompt 可能包含敏感数据。要脱敏、分层和控制访问。

### 误解四:指标越多越好

指标要能指导行动。没有 trace 支撑的指标很难定位问题。

### 误解五:可观测性是上线后的事

不是。没有 trace,开发阶段也很难迭代 Agent。

## 本章小结

Agent 可观测性要记录任务从用户目标到最终输出的完整过程:上下文、模型调用、检索、工具、状态更新、护栏、成本和延迟。Trace、span、artifact 和 state diff 是调试的基础。调试时应分层定位问题,不要把所有错误都归因于 prompt 或模型。可观测数据还应回流到评估集,让线上失败变成可回归的改进资产。

下一章会讲评估 Evaluation。可观测性告诉我们系统做了什么,评估则告诉我们这些行为是否真的更好。

