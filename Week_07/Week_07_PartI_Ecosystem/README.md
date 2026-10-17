# Part I: Ecosystem Awareness (MCP, Semantic Kernel & Local Models)

## Objectives & Scope
Part I expands our architectural perspective across the modern AI systems landscape beyond single-framework agent patterns. We evaluate standard protocol discovery, alternative enterprise stacks, and cost-efficient inference models:

1. **Model Context Protocol (MCP)**:
   - Standardized client-server protocol (JSON-RPC) for decoupling tool execution from model orchestrators.
   - Cross-host interoperability (Claude Desktop, Antigravity IDE, custom agents).
   - Trust boundary and identity propagation trade-offs.

2. **Microsoft Semantic Kernel**:
   - Native C#/.NET agent orchestration directly inside ASP.NET Core.
   - Enterprise DI and Entity Framework Core direct integration vs. loss of cyclic graph checkpointing.

3. **Small Language Models (SLMs) & Local Inference**:
   - Quantized local models (e.g., Llama 3.2 3B or Phi-3 via Ollama) for zero-cost, low-latency deterministic intent classification.

---

## Deliverables & Documentation Reports

- 📄 **[week7-mcp-vs-langchain-tools.md](../docs/week7-mcp-vs-langchain-tools.md)**:
  - Deep-dive architectural comparison of in-process LangChain tools vs. MCP client-server protocol.
  - Detailed analysis of tool reuse, .NET domain integration, trust boundaries, token forwarding risks, and indirect prompt injection attack vectors.

- 📄 **[week7-semantic-kernel-comparison.md](../docs/week7-semantic-kernel-comparison.md)**:
  - Detailed evaluation of Semantic Kernel vs. LangGraph.
  - Analyzes benefits of single-stack C# integration vs. the trade-offs in cyclic state management, time-travel debugging, and checkpoint persistence.
  - Formulates a strategic architecture recommendation defending why Nexa Solutions retains LangGraph for stateful HITL workflows while leveraging ASP.NET Core for gateway security.
