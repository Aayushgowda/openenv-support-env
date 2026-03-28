def get_tasks():
    return {
        "easy": {
            "ticket_id": "T1",
            "message": "I ordered shoes yesterday but want to return them and get a refund.",
            "account_status": "active",
            "urgency": "low",
            "order_value": 2000,
            "days_since_order": 1,
            "expected_action": "refund"
        },
        "medium": {
            "ticket_id": "T2",
            "message": "My package is delayed by 5 days and I am really unhappy.",
            "account_status": "active",
            "urgency": "medium",
            "order_value": 1500,
            "days_since_order": 5,
            "expected_action": "reply"
        },
        "hard": {
            "ticket_id": "T3",
            "message": "I see an order on my account that I did not place. This looks like fraud.",
            "account_status": "flagged",
            "urgency": "high",
            "order_value": 10000,
            "days_since_order": 0,
            "expected_action": "escalate"
        }
    }