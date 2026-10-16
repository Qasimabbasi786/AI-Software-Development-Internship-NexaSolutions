# Week 7 Ecosystem Analysis: Model Context Protocol (MCP) vs. LangChain Tools

## Executive Summary
This document examines the Model Context Protocol (MCP) by Anthropic and evaluates its impact, benefits, and architectural risks when compared to in-process LangChain tools.

---

## 1. What MCP Changes
- **Standardized Client-Server Protocol**: MCP decouples the tool implementation from the AI orchestrator. Tools are exposed as independent servers communicating over JSON-RPC (stdio or HTTP/SSE).
- **Interoperability**: A single tool server (e.g., SQLite, PostgreSQL, GitHub) can be consumed seamlessly by Claude Desktop, Antigravity, LangGraph, or custom agents without rewriting bindings.

---

## 2. Benefits for Our Library Architecture
- **Language Agnostic Tooling**: A .NET-native tool server could directly query EF Core and SQL Server without exposing intermediate REST endpoints to Python.
- **Dynamic Tool Discovery**: Agents discover available tools and argument schemas dynamically at runtime.

---

## 3. Risks & Trust Boundaries
- **Expanded Attack Surface**: Moving from internal function calls to an external protocol introduces RPC transport risks, authentication negotiation vulnerabilities, and supply chain exposure if third-party MCP servers are mounted.
- **Auditability**: Tool execution boundaries must strictly enforce user token forwarding to prevent unauthorized privilege escalation across the MCP boundary.
