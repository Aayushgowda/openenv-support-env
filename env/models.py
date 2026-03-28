from pydantic import BaseModel
from typing import List, Optional


class Observation(BaseModel):
    ticket_id: str
    customer_message: str
    previous_messages: List[str]
    account_status: str
    urgency_level: str
    order_value: float
    days_since_order: int


class Action(BaseModel):
    action_type: str  # reply, refund, escalate, close_ticket
    message: Optional[str] = None
    refund_amount: Optional[float] = None


class Reward(BaseModel):
    value: float
    reason: str