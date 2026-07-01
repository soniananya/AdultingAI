# Adulting AI

An event-driven AI assistant designed to help young adults manage important life decisions, financial documents, recurring obligations, and long-term planning through workflow-based AI automation.

## Problem

Most AI assistants are conversational and stateless.

They can answer questions, but they cannot reliably manage real-world life events such as:

* Receiving a salary slip
* Uploading an offer letter
* Tracking recurring bills
* Updating financial goals
* Maintaining long-term personal context

These tasks require persistence, structured workflows, document understanding, and memory beyond a single conversation.

Adulting AI was built to bridge that gap.

---

## Solution

Adulting AI combines workflow orchestration, document intelligence, and persistent user memory to automate financial and life-management tasks.

Instead of treating every message independently, the system maintains a centralized user life-state that evolves over time.

When a user uploads a document or triggers an event, Adulting AI:

1. Identifies the event type
2. Routes it through the appropriate workflow
3. Extracts structured information
4. Updates persistent user context
5. Generates personalized recommendations

---

## Core Architecture

```text
User Event
     │
     ▼
Document Processing
     │
     ▼
Workflow Classification
     │
     ▼
LangGraph Router
     │
 ┌───┼───────────┐
 │   │           │
 ▼   ▼           ▼
Salary   Offer   Bill
Flow     Flow    Flow
 │         │       │
 └────┬────┴───────┘
      ▼
LifeState Update
      ▼
Recommendation Engine
      ▼
Response
```

---

## Key Features

### Workflow-Based AI

Uses LangGraph to orchestrate event-driven workflows instead of relying on a single LLM call.

Different document types trigger different execution paths.

Examples:

* Salary Slip Workflow
* Offer Letter Workflow
* Bill Management Workflow
* Financial Profile Update Workflow

---

### Persistent LifeState

A centralized user profile stored in Supabase.

Stores information such as:

* Income history
* Financial obligations
* Goals
* Workflow outcomes
* Generated artifacts

Every workflow reads from and writes back to this shared state.

---

### Intelligent Document Processing

Supports extraction from uploaded documents such as:

* Salary slips
* Offer letters
* Bills
* Financial records

Documents are transformed into structured data that can be used by downstream workflows.

---

### Recommendation Generation

After updating user context, Adulting AI generates actionable recommendations such as:

* Budget planning
* Savings suggestions
* Expense monitoring
* Goal tracking
* Financial risk awareness

---

## Tech Stack

### Backend

* FastAPI
* Python
* REST APIs

### Workflow Orchestration

* LangGraph
* LangChain

### AI Models

* Anthropic Claude
* Google Gemini

### Database

* Supabase
* PostgreSQL

### Infrastructure

* Docker

---

## Example Workflow

### Salary Slip Upload

```text
Upload Salary Slip
       ▼
Text Extraction
       ▼
Document Classification
       ▼
Salary Workflow
       ▼
Salary Data Extraction
       ▼
LifeState Update
       ▼
Financial Recommendations
```

Extracted data:

```json
{
  "gross_salary": 85000,
  "net_salary": 72000,
  "deductions": 13000
}
```

LifeState automatically updates to reflect the user's latest financial status.

---

## Why LangGraph?

Traditional AI pipelines are linear.

Adulting AI requires:

* Conditional routing
* Shared state
* Workflow persistence
* Multi-step execution
* Event-driven processing

LangGraph enables these capabilities through graph-based workflow orchestration.

---

## Future Improvements

* Automated financial planning
* Goal forecasting
* Calendar integrations
* Investment recommendations
* Multi-agent collaboration
* Real-time notification system

---

## Project Status

Active Development

Built as an exploration of workflow-driven AI systems that move beyond simple chatbot interactions and toward persistent, action-oriented personal assistance.
