# 延伸阅读 `[参考]`

本附录提供继续学习方向。建议优先读官方文档、经典论文和高质量工程博客,并把阅读和自己的项目评估结合起来。

## 大模型基础

- Transformer 原论文:理解 self-attention 的起点。
- GPT 系列论文:理解 decoder-only 和 scaling。
- InstructGPT/RLHF 相关论文:理解指令对齐。
- DPO 论文:理解偏好优化的另一条路线。

## 推理优化

- KV Cache 相关资料。
- FlashAttention 论文和工程解释。
- PagedAttention/vLLM 资料。
- Speculative Decoding 论文和实践。

## Agent 框架和模式

- ReAct 论文。
- Toolformer 相关工作。
- Reflexion 相关工作。
- 工作流模式与 evaluator-optimizer 模式的工程文章。

## RAG 与检索

- RAG 原始论文和后续综述。
- Dense Passage Retrieval。
- ColBERT 和多向量检索。
- BM25、hybrid search、reranker 相关资料。
- 向量数据库官方文档。

## 评估

- LLM-as-a-Judge 相关论文。
- RAGAS、TruLens、DeepEval 等评估工具文档。
- OpenAI、Anthropic、Google 等公开评估实践文章。

## 安全

- Prompt Injection 攻击与防御资料。
- OWASP Top 10 for LLM Applications。
- 数据泄露、权限和 DLP 相关安全实践。
- AI 红队测试资料。

## MCP 和工具协议

- MCP 官方文档。
- Function Calling / Tool Calling 官方文档。
- JSON Schema 和 API 设计最佳实践。

## 可解释性

- Mechanistic Interpretability 入门材料。
- Transformer Circuits 系列文章。
- Sparse Autoencoder 相关研究。

## 学习建议

不要只读资料。每读一个方向,最好做一个小实验:

- 换一种 chunking 策略并跑 eval。
- 改一个工具 schema 看参数错误率。
- 加一个 guardrail 看误报和漏报。
- 用 Judge 校准 20 个样本。
- 对一个失败 trace 做归因。

Agent 工程的理解来自“读 + 做 + 评估”的循环。

