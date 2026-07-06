# 术语表 `[参考]`

本术语表用于快速查阅本书常见概念。它不是严格学术定义,而是面向工程理解的解释。

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

## J

### Judge

评估器。LLM-as-a-Judge 指用大模型根据 rubric 对输出质量进行评估。

## K

### KV Cache

自回归推理中缓存历史 token 的 Key/Value,避免重复计算注意力。

## L

### Long-term Memory

长期记忆。跨任务保存的偏好、项目约定或确认经验。需要来源、scope 和删除机制。

### LoRA

Low-Rank Adaptation,一种参数高效微调方法。

## M

### MCP

Model Context Protocol,模型上下文协议。用于模型应用连接外部工具、资源和提示能力。

### Multi-Agent

多 Agent 系统。多个职责不同的 Agent 通过编排、消息和共享状态协作。

## P

### PEFT

Parameter-Efficient Fine-Tuning,参数高效微调方法集合。

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

## V

### Vector Database

向量数据库。存储 embedding 并支持近似相似搜索的系统。

