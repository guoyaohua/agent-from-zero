# 术语表 `[参考]`

本术语表用于快速查阅本书常见概念。它不是严格学术定义,而是面向工程理解的解释。

![术语分类地图](../assets/appendix-glossary-map.svg)

## 如何使用术语表

Agent 领域的很多争论来自“同一个词指代不同层”。遇到陌生概念时,先判断它属于哪一层:

| 层 | 典型词 | 关键问题 |
| --- | --- | --- |
| 模型层 | Attention、SFT、RLHF、KV Cache | 模型能力和推理成本从哪里来 |
| 上下文层 | Prompt、Context、Evidence Pack、Memory | 模型这一轮能看见什么 |
| 运行时层 | Tool Call、Harness、Guardrails、Trace | 模型建议如何变成可控动作 |
| 循环层 | Agent Loop、Planning、Loop Engineering | 多轮任务如何推进并停止 |
| 工程层 | Evaluation、Observability、Cost、Security | 系统如何上线、监控和迭代 |

不要把不同层的词互相替代。例如 Prompt 不能替代 Harness,长上下文不能替代 Memory 治理,Function Calling 不能替代权限控制。

## A

### Agent

能围绕目标进行状态管理、推理、工具调用、观察反馈和迭代的系统。Agent 不只是一次 LLM 调用。

### Agent Loop

Agent 的基本循环:观察状态、思考下一步、执行动作、接收反馈、更新状态。

### ACI

Agent-Computer Interface,面向 Agent 的工具和计算机接口设计。强调工具名称、参数、返回、错误和权限要适合模型使用。

### Alignment

让模型或系统行为符合人类意图、规范和安全要求的过程。

### ANN

Approximate Nearest Neighbor,近似最近邻搜索。向量数据库常用它提高检索速度。

## B

### BM25

经典关键词检索算法,常用于 hybrid search 中补足向量检索对精确词的不足。

## C

### Chunk

RAG 中的检索单元。通常由文档切分而来,应保留语义完整性、来源和元数据。

### Context Engineering

上下文工程。选择、压缩、排序、标注和注入模型调用所需信息的工程能力。

### Critic

评审角色或评审节点,根据 rubric 检查输出、计划或工具行为。

## D

### DPO

Direct Preference Optimization,一种偏好对齐方法,可直接利用偏好数据优化模型。

## E

### Embedding

把文本、图像或其他对象映射为向量表示,用于检索、聚类或相似度计算。

### Eval Set

评估样本集,用于比较 Agent 或模型版本质量。

### Evidence Pack

证据包。RAG 系统中提供给模型的一组带编号、来源、版本和内容的证据。

## F

### Function Calling

模型以结构化方式表达工具调用的能力或接口形式。

### Fine-tuning

微调。用特定数据继续训练模型,改变模型行为倾向或能力。

## G

### Guardrails

护栏。在输入、上下文、工具、输出等阶段检查和控制风险的机制。

## H

### Hard Negative

看起来相关但不能支持正确答案的负样本。常用于检索评估。

### Hybrid Search

混合检索,通常结合关键词检索和向量检索。

### Harness

Agent Harness,模型和真实工具/环境之间的运行时外骨架。负责动作 schema 校验、权限、策略、sandbox、执行、错误协议、trace 和回滚。

### Harness Engineering

围绕 Harness 的工程设计方法。重点是把模型动作建议变成可验证、可授权、可执行、可记录、可恢复的系统事件,而不是只包装 API 调用。

## J

### Judge

评估器。LLM-as-a-Judge 指用大模型根据 rubric 对输出质量进行评估。

## K

### KV Cache

自回归推理中缓存历史 token 的 Key/Value,避免重复计算注意力。

## L

### Loop Engineering

围绕 Agent 多轮任务收敛的工程设计。重点不是写 while 循环,而是状态摘要、进展不变量、预算、停止条件、重规划、检查点和过程评估。

### Long-term Memory

长期记忆。跨任务保存的偏好、项目约定或确认经验。需要来源、scope 和删除机制。

### LoRA

Low-Rank Adaptation,一种参数高效微调方法。

## M

### MCP

Model Context Protocol,模型上下文协议。用于模型应用连接外部工具、资源和提示能力。

### Multi-Agent

多 Agent 系统。多个职责不同的 Agent 通过编排、消息和共享状态协作。

## O

### OpenClaw

一个开源、自托管的个人 AI 助手和多渠道 Agent Gateway。它把 WhatsApp、Telegram、Slack、Discord、Signal、iMessage、WebChat 等消息入口连接到本地或自托管的 Agent runtime、workspace、skills、tools、nodes 和控制界面。

## P

### PEFT

Parameter-Efficient Fine-Tuning,参数高效微调方法集合。

### Prompt / Context / Harness / Loop

Agent 工程的四层边界:Prompt 管任务表达,Context 管信息供应,Harness 管运行时边界,Loop 管多轮收敛。

### Prompt Injection

提示注入。不可信内容试图覆盖系统规则、改变模型行为或诱导工具调用。

## R

### RAG

Retrieval-Augmented Generation,检索增强生成。通过检索外部证据增强模型回答。

### ReAct

Reasoning + Acting,让模型交替进行推理和行动的 Agent 模式。

### Reranker

重排器。对初召回候选进行更精细排序的模型或算法。

### RLHF

Reinforcement Learning from Human Feedback,基于人类反馈的强化学习对齐方法。

## S

### SFT

Supervised Fine-Tuning,监督微调。使用输入输出样本训练模型遵循任务格式和指令。

### Short-term Memory

短期记忆。当前任务内的目标、计划、观察、约束和状态。

## T

### Tool Call

工具调用。模型请求外部工具执行动作或查询数据。

### Trace

一次任务的完整过程记录,包含模型调用、工具调用、状态更新、成本和错误。

## 易混概念对照

| 概念 A | 概念 B | 核心区别 |
| --- | --- | --- |
| Prompt | Context | Prompt 是任务表达;Context 是模型实际可见的全部工作材料 |
| Function Calling | Harness | Function Calling 让模型结构化表达动作;Harness 决定动作能否执行以及如何执行 |
| Memory | RAG | Memory 保存用户/任务经验;RAG 检索外部知识证据 |
| Workflow | Agent | Workflow 路径由系统预定义;Agent 可根据观察动态选择下一步 |
| Guardrails | Alignment | Guardrails 是系统运行时控制;Alignment 是模型或系统行为对齐过程 |
| Trace | Explanation | Trace 是可观察事实记录;解释是基于事实对行为的说明 |
| Loop | Loop Engineering | Loop 是循环形态;Loop Engineering 是让循环收敛、可恢复、可评估的工程设计 |

## V

### Vector Database

向量数据库。存储 embedding 并支持近似相似搜索的系统。
