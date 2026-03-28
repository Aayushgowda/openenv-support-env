# OpenEnv — AI Customer Support Triage

A structured simulation environment for training and evaluating AI agents on real-world customer support workflows, including refund processing, delivery issue handling, and fraud detection.

Designed to benchmark agent decision-making under realistic business constraints.

---

## Why This Exists

Support systems handle thousands of tickets daily. Automation requires:

- **Fast resolution** — minimize time-to-close
- **Correct decision-making** — match action to intent
- **Risk-aware handling** — flag fraud, protect high-value orders

This environment provides a reproducible and deterministic evaluation setup to develop and benchmark such agents.

---

## OpenEnv Compliance

This environment follows the OpenEnv specification:

- Implements `step()`, `reset()`, and `state()` APIs
- Uses typed Pydantic models for Observation, Action, and Reward
- Includes `openenv.yaml` for schema definition
- Designed to pass `openenv validate`

---

## Episode Definition

- Each episode represents a single customer ticket
- Episode starts with `reset()`
- Episode ends when:
  - The correct action is taken, or
  - Maximum 3 steps are reached

---

## State Representation

The internal state includes:

- Current task details
- Action history
- Step count
- Completion status

This allows debugging and agent introspection.

---

## Environment Design

### Observation Space

Each step exposes the following fields:

| Field | Description |
|---|---|
| `ticket_id` | Unique identifier for the support ticket |
| `customer_message` | Latest message from the customer |
| `previous_messages` | Conversation history |
| `account_status` | Standing of the customer account |
| `urgency_level` | Priority score of the ticket |
| `order_value` | Monetary value of the associated order |
| `days_since_order` | Age of the order in days |

### Action Space

The agent selects one action per step:

| Action | Description |
|---|---|
| `reply` | Send a message to the customer |
| `refund` | Issue a refund (optionally specify `refund_amount`) |
| `escalate` | Escalate to a human agent |
| `close_ticket` | Mark the ticket as resolved |

Optional fields: `message`, `refund_amount`

### Action Constraints

- Only one action allowed per step
- Invalid or irrelevant actions reduce reward
- Repeated actions are penalized

---

## Reward Function

The reward function provides dense feedback across the trajectory, encouraging:

- Early correct decisions
- Avoidance of repetitive or unsafe actions
- Business-aware handling of high-risk scenarios

| Event | Reward |
|---|---|
| Correct action taken | `+0.4` |
| Fast resolution | `+0.3` |
| High-value order handled correctly | `+0.2` |
| Wrong action taken | `−0.3` |
| Repeated actions | `−0.2` |
| Risky refund on flagged account | `−0.5` |

Final score combines step-level rewards with a grader evaluation. **Range: 0.0 – 1.0**

---

## Task Difficulty

| Level | Scenario | Key Challenge |
|---|---|---|
| Easy | Refund request | Clear intent, single-step resolution |
| Medium | Delivery delay | Multi-turn handling, managing dissatisfaction |
| Hard | Fraud detection | High-risk scenario requiring escalation |

---

## Grader

Each task is scored deterministically across four dimensions:

1. **Correct final action** — did the agent choose the right outcome?
2. **Presence of correct action** — was the correct action used at any point?
3. **Efficiency** — how many steps did resolution take?
4. **Repetition penalty** — deduction for redundant actions

All grading logic is fully deterministic and reproducible. No randomness is used.

---

## Baseline Agent

A rule-based agent is included for reproducible benchmarking. It:

- Detects keywords in the customer message
- Maps keywords to actions
- Produces consistent, deterministic outputs

### Expected Baseline Output

```
easy   actions: ['refund']
medium actions: ['reply']
hard   actions: ['escalate']
```

---

## Setup

### Prerequisites

```bash
pip install -r requirements.txt
```

### Run Baseline Agent

```bash
python -m scripts.baseline
```

---

## Docker

**Build the image:**

```bash
docker build -t openenv-support .
```

**Run the container:**

```bash
docker run openenv-support
```

---

## Validation

This environment is designed to pass:

```bash
openenv validate
```

---

## Roadmap

- [ ] Multi-turn conversation support
- [ ] Policy-based decision constraints
- [ ] Integration with real support datasets
- [ ] LLM-based agent implementations
