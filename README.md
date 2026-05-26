# Order Lookup Agent

A minimal AI agent that looks up customer order status using tool use,
with a human approval checkpoint before it acts.

## The problem it solves

Support teams field endless "where is my order?" questions. A naive chatbot
would *guess* or hallucinate an answer. This agent instead recognizes when it
needs real data, looks it up from a system of record, and only then responds —
never inventing an order status.

## What it does

1. A customer asks about their order (e.g. "What's the status of order 12345?")
2. The AI (Claude) decides it needs to look up real data — it does not answer from memory
3. **A human approves the lookup before it runs** (human-in-the-loop checkpoint)
4. The agent calls a lookup tool, retrieves the real status, and replies in natural language
5. The reply is streamed back word-by-word for a responsive experience

## Key concepts demonstrated

- **Tool use / function calling** — the model decides to call a function, rather than guessing
- **Human-in-the-loop** — a human approves the action before execution (the safety brake on autonomy)
- **Graceful error handling** — unknown order IDs return "Order not found" instead of crashing
- **Streaming** — the final response is delivered incrementally for better UX

## How it works

Built with the Anthropic Claude API. The agent uses a two-step tool-use loop:
the first call lets Claude decide *whether* and *how* to use the lookup tool;
the human then approves; the function runs locally; and a second call hands the
result back to Claude to compose the final customer-facing reply.

The "database" here is a simple in-memory dictionary standing in for a real
system of record (CRM, order DB, or a sheet). Swapping it for a real source
would not change the agent logic — only the lookup function.

## Why I built it

I spent ~10 years leading customer-experience solution engineering teams.
I built this to understand agentic AI from the deployer's side — how tool use,
human oversight, and graceful failure actually fit together — rather than just
talking about it.

## Tech

Python · Anthropic Claude API

## Possible next steps

- Replace the in-memory dictionary with a real data source (CRM / order system)
- Add more tools (issue refund, update shipping) — each gated by human approval
- Add an evaluation harness to measure response accuracy across test cases
- Route high-risk actions (refunds, cancellations) through stricter approval
