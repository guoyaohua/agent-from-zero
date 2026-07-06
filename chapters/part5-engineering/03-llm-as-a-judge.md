# LLM-as-a-Judge `[进阶]`

很多 Agent 任务很难用精确规则评估。

例如:

- 回答是否完整?
- 总结是否抓住重点?
- 是否忠于证据?
- 解释是否清楚?
- 语气是否适合用户?
- 评审意见是否可执行?

这些问题需要语义判断。LLM-as-a-Judge,也就是让大模型充当评估器,因此变得很常见。

但 Judge 不是魔法。它也会偏见、漂移、误判、被长回答迷惑,甚至被被评估输出影响。

LLM-as-a-Judge 的核心不是“再问一个模型好不好”,而是:

**用明确 rubric、证据、输出契约和校准机制,把语义评估做成可审计的评估器。**

![LLM-as-a-Judge Rubric](../assets/part5-llm-judge-rubric.svg)

本章会讲:

- LLM Judge 适合评什么,不适合评什么。
- Rubric 如何设计。
- Judge 输入和输出应包含什么。
- 如何校准 Judge 和人工标注的一致性。
- 如何防止偏见、奖励黑客和评估漂移。
- 如何把 Judge 放进 Agent 评估流水线。

## Judge 适合什么

LLM Judge 适合语义和质量维度。

例如:

- 答案是否回答了问题。
- 是否覆盖关键要点。
- 是否基于给定证据。
- 是否说明不确定性。
- 是否遵守写作风格。
- 总结是否忠实原文。
- 评审意见是否具体可执行。

这些维度很难用简单字符串匹配判断。

## Judge 不适合什么

能确定性验证的,不要优先交给 Judge。

| 任务 | 更适合 |
| --- | --- |
| JSON 是否合法 | schema validator |
| 代码是否通过 | tests/typecheck/lint |
| 数学计算 | 计算器或符号工具 |
| 权限是否允许 | policy engine |
| 引用 ID 是否存在 | 程序检查 |
| 成本是否超限 | 指标规则 |

Judge 可以辅助解释失败,但不应替代确定性检查。

## Rubric 是 Judge 的核心

没有 rubric 的 Judge 只是主观点评。

一个好的 rubric 应包含:

- 评估维度。
- 每个维度的定义。
- 分数锚点。
- 通过/失败条件。
- 允许和不允许的行为。
- 示例。

例如评估 RAG 答案:

```text
维度: Evidence faithfulness
5: 所有关键结论都由给定证据明确支持,没有无依据补充。
3: 主要结论有证据,但遗漏部分限制或有轻微扩展。
1: 关键结论没有证据支持,或与证据矛盾。
```

分数锚点能减少 Judge 随意打分。

## Judge 输入

Judge 输入应包含足够上下文,但不要混乱。

常见输入:

```json
{
  "user_request": "高铁一等座能报销吗?",
  "candidate_answer": "可以报销,但需要部门负责人事前审批。",
  "evidence": [
    {"id": "S1", "quote": "高铁一等座需部门负责人事前审批..."}
  ],
  "rubric": "rag_faithfulness.v1",
  "task_constraints": ["Answer in Chinese", "Use evidence only"]
}
```

不要让 Judge 自己去猜任务标准。

## Judge 输出

Judge 输出也要结构化。

```json
{
  "pass": false,
  "scores": {
    "faithfulness": 2,
    "completeness": 4,
    "citation_quality": 3
  },
  "findings": [
    {
      "criterion": "faithfulness",
      "severity": "high",
      "issue": "Answer says reimbursement is allowed, but evidence says prior approval is required.",
      "evidence_ids": ["S1"]
    }
  ],
  "suggested_fix": "State that reimbursement is conditional on prior approval."
}
```

只输出一个分数没有太大价值。评估结果要能指导修正。

## Pairwise vs Pointwise

Judge 常见两种模式。

### Pointwise

单独给一个答案打分。

优点:

- 简单。
- 易于门禁。
- 能输出分项问题。

缺点:

- 分数校准难。
- 不同时间分数可能漂移。

### Pairwise

比较 A 和 B 哪个更好。

优点:

- 对版本比较有用。
- 有时比绝对打分稳定。

缺点:

- 不能直接得到绝对质量。
- 可能受顺序偏见影响。

实际系统可以组合:上线门禁用 pointwise,模型/Prompt 比较用 pairwise。

## 校准 Judge

Judge 需要和人工标注校准。

流程:

1. 准备一批人工标注样本。
2. 用 Judge 对同样样本评分。
3. 比较一致性。
4. 分析 disagreement。
5. 修改 rubric 或 Judge prompt。
6. 重复直到稳定。

常见一致性指标包括:

- accuracy。
- precision/recall。
- Cohen's kappa。
- Spearman correlation。

不要追求 Judge 和人工 100% 一致。重点是它是否能稳定发现你关心的问题。

## Gold set 和 disagreement set

建议维护两类样本。

### Gold set

人工高质量标注,用于校准和回归。

### Disagreement set

Judge 和人工经常不一致的样本。

这类样本最能暴露 rubric 模糊点。

例如 Judge 总是偏好长答案,但人工认为简洁答案更好,说明 rubric 要明确“不要因篇幅给高分”。

## 常见偏见

Judge 可能有多种偏见。

| 偏见 | 表现 |
| --- | --- |
| 长度偏见 | 更长答案得分更高 |
| 位置偏见 | pairwise 中偏好第一个或第二个 |
| 自信偏见 | 语气更确定的答案得分更高 |
| 格式偏见 | 格式漂亮但事实错误仍高分 |
| 模型同源偏见 | 偏好同一模型家族风格 |
| 宽容偏见 | 对细小事实错误放过 |
| 过严偏见 | 对可接受表达过度扣分 |

Rubric 和校准样本要针对这些偏见设计。

## 防止奖励黑客

如果 Agent 知道 Judge 偏好什么,可能优化 Judge 分数而不是任务质量。

例子:

- Judge 偏好引用,Agent 塞很多无关引用。
- Judge 偏好详细,Agent 变得冗长。
- Judge 只检查格式,Agent 填无意义字段。
- Judge 不查证据,Agent 编造看似合理来源。

防御方式:

- 多评分器组合。
- 隐藏测试集。
- 人工抽检。
- 引用程序校验。
- 轨迹评估。
- 定期更新 hard cases。

Judge 分数只是信号,不是最终真理。

## Judge 和 Critic 的区别

Judge 和 Critic 很像,但用途不同。

| 角色 | 目标 |
| --- | --- |
| Judge | 给评估样本打分,支持版本比较和门禁 |
| Critic | 在运行中发现问题,要求修正或阻止输出 |

Judge 更偏离线评估和质量度量。Critic 更偏在线工作流和自我修正。

同一套 rubric 可以复用,但输出契约和成本要求不同。

## Judge 在 Agent 评估中的位置

一个评估流水线可以是:

```mermaid
flowchart LR
    A[Eval Sample] --> B[Run Agent]
    B --> C[Trace + Output]
    C --> D[Rule Checks]
    C --> E[LLM Judge]
    D --> F[Score Report]
    E --> F
    F --> G[Regression Gate]
```

规则检查先处理确定性问题,Judge 处理语义质量。

## Judge 自身也要可观测

Judge 调用也要保存 trace:

- Judge prompt 版本。
- rubric 版本。
- 输入样本。
- 输出分数和理由。
- 模型版本。
- 与人工标签差异。

否则 Judge 结果变化时,你不知道是模型变了、rubric 变了,还是样本变了。

## Judge 漂移

Judge 会漂移。

原因可能是:

- Judge 模型版本变化。
- rubric 修改。
- 任务分布变化。
- 被评估答案风格变化。
- 样本集过时。

要定期在 gold set 上跑 Judge,观察一致性是否下降。

## 成本控制

Judge 也花钱。

可以优化:

- 先用规则过滤明显失败。
- 只对关键样本用强 Judge。
- 对简单维度用小模型。
- 批量评估。
- 缓存相同样本结果。
- 抽样在线评估。

不要让 Judge 成本超过被评估系统本身的改进价值。

## 常见误解

### 误解一:Judge 比被评估模型大就一定准

不一定。没有 rubric 和校准,大模型也会误判。

### 误解二:Judge 可以替代所有测试

不能。确定性验证仍应优先用程序、规则和工具。

### 误解三:Judge 输出分数就够了

不够。需要分项理由、证据和可执行反馈。

### 误解四:Judge 不需要人工

不对。人工标注用于校准、抽检和发现 Judge 偏差。

### 误解五:Judge 分数提升就是产品变好

不一定。可能只是迎合 Judge 偏好。要结合线上指标和人工抽检。

## 本章小结

LLM-as-a-Judge 适合评估语义质量,但必须有明确 rubric、结构化输入输出、人工校准、偏见监控和反作弊机制。Judge 不应替代确定性测试,而应和规则、程序验证、人工评估组合使用。好的 Judge 输出不只是分数,还包括问题、依据和可执行修正。Judge 本身也要被观测和评估,否则评估器会成为新的黑盒。

下一章会讲成本与延迟优化。质量评估告诉我们系统好不好,成本和延迟决定它能不能被真实用户持续使用。

