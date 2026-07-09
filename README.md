# agent-from-zero

> 《从 0 到 1 的 AI Agent 教程》—— 一本面向中文读者的、从零基础到进阶生产实践的 AI Agent 学习指南。

本书以 Markdown 撰写,**概念为主、代码为辅**(示例用伪代码或最小片段,不绑定特定框架/语言),但内容力求**深入而非停留科普层**;对关键算法(如 Self-Attention、RLHF、KV Cache、Flash Attention、MoE、测试时计算等)会大篇幅讲透。全书既有"打开 LLM 黑盒"的原理线,也有"从 0 搭一个 Agent"的应用线,两线并行、循序渐进。

---

## 适合谁读

- **零基础(懂基本编程)**:想系统了解 AI Agent 是什么、怎么从头学起。
- **有经验的开发者**:想快速建立 Agent 的完整知识体系并落地到生产。
- **想深究原理者**:想吃透 Transformer、训练对齐、推理优化等底层机制。

每篇/每节都标注阅读层级:`[主线]` 初学者必读 · `[进阶]` 深度可选 · `[参考]` 速查辅料。带 `★` 的是可大篇幅深入的核心算法点。

---

## 如何阅读

- **零基础主线**:`frontmatter` → `part0` → `part1` 仅读主线 → `part2`(01/02/03/07/08/09/10/11)→ `part3`(01/02/04/09/11)→ `part4`(01/05)→ `part5`(01/02/04/06/07/08)→ `part6` 全部 → `part7`(08)。读完即可动手做出可用 Agent。
- **原理深潜支线**:完整精读 `part1`(算法篇)的全部 `[进阶]` 与 `★`,吃透 LLM 内部世界。
- **应用进阶支线**:`part2`–`part5` 的 `[进阶]` 项 + `part2` 的 Harness/Loop 深入章节 + `part7` 趋势、互操作、Agentic RL、OpenClaw 与可解释性。

> 怕数学的读者可先跳过 `part1` 直接进 `part2`,日后再回看;想深究原理者按序精读 `part1` 再进应用线。

---

## 目录

### 前言与导读 · `chapters/frontmatter/`
- [前言:为什么写这本书](chapters/frontmatter/01-preface.md) `[主线]`
- [读者对象与分层路径](chapters/frontmatter/02-who-should-read.md) `[主线]`
- [如何使用本书与标注体系](chapters/frontmatter/03-how-to-read.md) `[主线]`
- [全书地图:从 0 到 1 的旅程](chapters/frontmatter/04-roadmap-overview.md) `[主线]`

### Part 0 入门篇:认识 AI Agent 与它的来路 · `chapters/part0-intro/`
> 不涉数学,建立"Agent 是什么、从哪来、为何重要"的直觉,跑通最小 LLM 使用。
- [人工智能发展简史](chapters/part0-intro/01-ai-history.md) `[主线]`
- [大语言模型发展简史](chapters/part0-intro/02-llm-history.md) `[主线]`
- [什么是 AI Agent](chapters/part0-intro/03-what-is-agent.md) `[主线]`
- [为什么需要 Agent](chapters/part0-intro/04-why-agent.md) `[主线]`
- [LLM 使用基础:API 与参数](chapters/part0-intro/05-llm-usage-basics.md) `[主线]`
- [Prompt、Token 与上下文窗口](chapters/part0-intro/06-prompt-and-context-intro.md) `[主线]`

### Part 1 模型与算法原理篇:LLM 的内部世界 · `chapters/part1-algorithms/`
> 把 LLM 从黑盒打开:数学直觉 → 神经网络 → Transformer → 演进史 → 模型全景 → 训练 → 推理优化。核心算法点(★)大篇幅讲透。

**数学与算法直觉**
- [Tokenizer、词表与 Chat Template](chapters/part1-algorithms/00-tokenizer-vocabulary-chat-template.md) `[主线]` ★
- [向量、矩阵与概率直觉](chapters/part1-algorithms/01-vectors-and-probability.md) `[主线]`
- [Softmax 与交叉熵损失](chapters/part1-algorithms/02-softmax-and-loss.md) `[进阶]`
- [梯度下降与泛化](chapters/part1-algorithms/03-gradient-and-generalization.md) `[进阶]`

**神经网络基础**
- [神经元、激活与前馈网络](chapters/part1-algorithms/04-neuron-and-ffn.md) `[主线]`
- [表示学习与嵌入](chapters/part1-algorithms/05-representation-learning.md) `[进阶]`
- [RNN 与 LSTM](chapters/part1-algorithms/06-rnn-and-lstm.md) `[进阶]`

**Transformer 架构**
- [为什么需要 Attention](chapters/part1-algorithms/07-why-attention.md) `[主线]` ★
- [Self-Attention 与 QKV](chapters/part1-algorithms/08-self-attention-qkv.md) `[主线]` ★
- [多头注意力](chapters/part1-algorithms/09-multi-head-attention.md) `[进阶]` ★
- [位置编码](chapters/part1-algorithms/10-positional-encoding.md) `[进阶]` ★
- [残差、LayerNorm 与 FFN](chapters/part1-algorithms/11-residual-layernorm-ffn.md) `[进阶]`
- [Transformer 完整架构与数据流](chapters/part1-algorithms/12-transformer-dataflow.md) `[主线]` ★

**Transformer 发展史与变体**
- [三大分支与 Decoder-only 为何主流](chapters/part1-algorithms/13-three-branches.md) `[进阶]` ★
- [注意力变体:稀疏/线性/滑窗](chapters/part1-algorithms/14-attention-variants.md) `[进阶]` ★
- [位置编码演进:RoPE 与 ALiBi](chapters/part1-algorithms/15-positional-encoding-evolution.md) `[进阶]` ★
- [归一化与激活的改良:RMSNorm、SwiGLU](chapters/part1-algorithms/16-norm-and-activation-evolution.md) `[进阶]`
- [长上下文技术](chapters/part1-algorithms/17-long-context.md) `[进阶]` ★

**主流大模型全景**
- [主流大模型全景:模型家族、闭源与开源](chapters/part1-algorithms/18-model-landscape.md) `[参考]`
- [多模态与推理型模型](chapters/part1-algorithms/19-multimodal-and-reasoning.md) `[进阶]`

**训练流程**
- [预训练与 Scaling Law](chapters/part1-algorithms/20-pretraining-and-scaling-law.md) `[进阶]` ★
- [监督微调 SFT](chapters/part1-algorithms/21-sft.md) `[主线]`
- [偏好对齐:RLHF 与 DPO](chapters/part1-algorithms/22-rlhf-and-dpo.md) `[进阶]` ★
- [参数高效微调:PEFT 与 LoRA](chapters/part1-algorithms/23-peft-and-lora.md) `[进阶]` ★
- [蒸馏与量化](chapters/part1-algorithms/24-distillation-and-quantization.md) `[进阶]`
- [微调 vs 提示 vs 检索:如何选](chapters/part1-algorithms/25-finetune-vs-prompt-vs-rag.md) `[主线]`

**推理优化**
- [自回归瓶颈与 KV Cache](chapters/part1-algorithms/26-autoregressive-and-kv-cache.md) `[主线]` ★
- [Flash Attention](chapters/part1-algorithms/27-flash-attention.md) `[进阶]` ★
- [PagedAttention 与连续批处理](chapters/part1-algorithms/28-paged-attention-batching.md) `[进阶]` ★
- [投机解码](chapters/part1-algorithms/29-speculative-decoding.md) `[进阶]` ★
- [测试时计算与推理型模型](chapters/part1-algorithms/30-test-time-compute-reasoning.md) `[进阶]` ★
- [MoE 与稀疏专家模型](chapters/part1-algorithms/31-moe-and-sparse-experts.md) `[进阶]` ★

### Part 2 Agent 核心原理篇 · `chapters/part2-agent-core/`
> Agent 之所以为 Agent 的核心机制——循环、推理-行动、工具、规划、工作流编排,以及 Prompt/Context/Harness/Loop 四层工程边界。
- [Agent 循环](chapters/part2-agent-core/01-agent-loop.md) `[主线]`
- [ReAct:推理与行动交织](chapters/part2-agent-core/02-react.md) `[主线]` ★
- [Function Calling 工具调用](chapters/part2-agent-core/03-function-calling.md) `[主线]` ★
- [工具设计与 ACI](chapters/part2-agent-core/04-tool-design-aci.md) `[进阶]`
- [Planning 任务规划](chapters/part2-agent-core/05-planning.md) `[进阶]`
- [五大工作流模式](chapters/part2-agent-core/06-workflow-patterns.md) `[进阶]`
- [工作流 vs 自主 Agent:如何选](chapters/part2-agent-core/07-workflow-vs-agent.md) `[主线]`
- [Prompt、Context、Harness、Loop:四层如何区分](chapters/part2-agent-core/08-prompt-context-harness-loop.md) `[主线]` ★
- [Harness Engineering:给 Agent 装上运行时外骨架](chapters/part2-agent-core/09-harness-engineering.md) `[主线]` ★
- [Loop Engineering:让 Agent 多轮任务真正收敛](chapters/part2-agent-core/10-loop-engineering.md) `[主线]` ★
- [结构化输出与约束解码](chapters/part2-agent-core/11-structured-output-constrained-decoding.md) `[主线]` ★

### Part 3 能力构建篇 · `chapters/part3-capabilities/`
> 给 Agent 装上记忆、知识检索、自我修正与上下文管理,从"能跑"到"好用"。
- [记忆系统总览](chapters/part3-capabilities/01-memory-overview.md) `[主线]`
- [短期记忆与对话历史](chapters/part3-capabilities/02-short-term-memory.md) `[主线]`
- [长期记忆](chapters/part3-capabilities/03-long-term-memory.md) `[进阶]`
- [RAG 与向量检索](chapters/part3-capabilities/04-rag-and-vector-retrieval.md) `[主线]` ★
- [嵌入与向量数据库](chapters/part3-capabilities/05-embeddings-and-vector-db.md) `[进阶]`
- [切块策略与检索质量](chapters/part3-capabilities/06-chunking-and-retrieval-quality.md) `[进阶]`
- [工具使用进阶](chapters/part3-capabilities/07-advanced-tool-use.md) `[进阶]`
- [反思与自我修正](chapters/part3-capabilities/08-reflection-self-correction.md) `[进阶]`
- [上下文工程](chapters/part3-capabilities/09-context-engineering.md) `[主线]`
- [Agentic RAG 与知识图谱](chapters/part3-capabilities/10-agentic-rag-and-knowledge-graph.md) `[进阶]` ★
- [知识入库、数据治理与 RAG 生命周期](chapters/part3-capabilities/11-knowledge-ingestion-governance.md) `[进阶]` ★

### Part 4 架构进阶篇 · `chapters/part4-architecture/`
> 从单 Agent 到多 Agent 系统:角色、编排、通信与标准协议。
- [为什么需要多 Agent](chapters/part4-architecture/01-why-multi-agent.md) `[主线]`
- [角色分工与职责设计](chapters/part4-architecture/02-roles-and-division.md) `[进阶]`
- [编排模式](chapters/part4-architecture/03-orchestration-patterns.md) `[进阶]`
- [通信协议与消息传递](chapters/part4-architecture/04-communication-protocols.md) `[进阶]`
- [MCP 模型上下文协议](chapters/part4-architecture/05-mcp.md) `[主线]` ★
- [Agent 互操作与 A2A](chapters/part4-architecture/06-agent-interoperability-a2a.md) `[进阶]` ★

### Part 5 工程实践篇 · `chapters/part5-engineering/`
> 把 Agent 送上生产线——可观测、可评估、可控成本、可保安全。
- [可观测性与调试](chapters/part5-engineering/01-observability-debugging.md) `[主线]`
- [评估 Evaluation 总览](chapters/part5-engineering/02-evaluation.md) `[主线]`
- [LLM-as-a-Judge](chapters/part5-engineering/03-llm-as-a-judge.md) `[进阶]`
- [成本与延迟优化](chapters/part5-engineering/04-cost-latency-optimization.md) `[主线]`
- [安全与对齐](chapters/part5-engineering/05-safety-and-alignment.md) `[进阶]`
- [护栏 Guardrails](chapters/part5-engineering/06-guardrails.md) `[主线]`
- [Prompt Injection 与防御](chapters/part5-engineering/07-prompt-injection.md) `[主线]` ★
- [发布、运行治理与变更管理](chapters/part5-engineering/08-release-ops-governance.md) `[主线]` ★

### Part 6 实战篇:个人研究助手项目 · `chapters/part6-project/`
> 用前六篇全部知识,从 0 搭一个"个人研究助手",按步骤递进。
- [项目总览与需求分析](chapters/part6-project/01-overview-and-requirements.md) `[主线]`
- [架构设计](chapters/part6-project/02-architecture-design.md) `[主线]`
- [核心循环与工具实现](chapters/part6-project/03-core-loop-and-tools.md) `[主线]`
- [加入记忆与 RAG](chapters/part6-project/04-adding-memory-and-rag.md) `[主线]`
- [评估与迭代](chapters/part6-project/05-evaluation-and-iteration.md) `[主线]`
- [复盘与扩展方向](chapters/part6-project/06-recap-and-extensions.md) `[进阶]`

### Part 7 前沿展望篇 · `chapters/part7-frontier/`
> 站在当下看未来——新兴方向、个人 Agent Gateway、未解难题、给读者的结语。
- [趋势:Computer Use 与 GUI Agent](chapters/part7-frontier/01-trends-computer-use.md) `[进阶]`
- [趋势:长时程自主任务](chapters/part7-frontier/02-trends-long-horizon.md) `[进阶]`
- [趋势:标准化与互操作](chapters/part7-frontier/03-trends-standardization.md) `[进阶]`
- [开放问题与局限](chapters/part7-frontier/04-open-problems.md) `[进阶]`
- [大模型可解释性](chapters/part7-frontier/05-interpretability.md) `[进阶]`
- [OpenClaw:小龙虾与个人 Agent Gateway](chapters/part7-frontier/06-openclaw.md) `[进阶]` ★
- [Agentic RL 与真实环境反馈](chapters/part7-frontier/07-agentic-rl.md) `[进阶]` ★
- [结语:从 0 到 1 之后](chapters/part7-frontier/08-epilogue.md) `[主线]`

### 附录 · `chapters/appendix/`
> 速查与延伸资源。
- [术语表](chapters/appendix/01-glossary.md) `[参考]`
- [延伸阅读](chapters/appendix/02-further-reading.md) `[参考]`
- [Prompt 速查](chapters/appendix/03-prompt-cheatsheet.md) `[参考]`

---

## 写作进度

本书大纲已定并完成正文写作,共 **10 个部分、95 篇文章**。目前 **前言与导读**、**Part 0 入门篇**、**Part 1 模型与算法原理篇**、**Part 2 Agent 核心原理篇**、**Part 3 能力构建篇**、**Part 4 架构进阶篇**、**Part 5 工程实践篇**、**Part 6 实战项目篇**、**Part 7 前沿展望篇** 与 **附录** 均已完成。

> 大纲参考了李宏毅《生成式 AI 导论》与吴恩达 DeepLearning.AI《Generative AI with LLMs》课程做查漏补缺,正文会继续通过复审、评估和读者反馈迭代完善。

---

## 内容约定

- **整体深入,不停留科普**:每篇讲到"能据此做判断/做设计"的程度,多用"为什么这样设计 / 不这样会怎样 / 有何取舍"的追问式展开。
- **关键算法可大篇幅**:带 `★` 的核心算法点允许显著超常规篇幅,配公式、示意图、数据流图、伪代码与"常见误解"提示。
- **数学处理**:直觉 + 图解为主,关键处给公式并解释每个符号的含义与作用,不强求完整推导,给"看得懂、用得上"的深度。
- **代码**:伪代码或最小片段为主,框架无关。

---

## 许可

本书内容采用 [CC BY 4.0](LICENSE) 许可:你可以自由分享与改编,但需署名。
