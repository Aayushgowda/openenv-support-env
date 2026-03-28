from env.models import Observation, Action, Reward
from env.tasks import get_tasks
from env.grader import grade


class SupportEnv:

    def __init__(self):
        self.tasks = get_tasks()
        self.current_task = None
        self.history = []
        self.steps = 0
        self.done = False

    def reset(self, task_name="easy"):
        self.current_task = self.tasks[task_name]
        self.history = []
        self.steps = 0
        self.done = False

        return Observation(
            ticket_id=self.current_task["ticket_id"],
            customer_message=self.current_task["message"],
            previous_messages=[],
            account_status=self.current_task["account_status"],
            urgency_level=self.current_task["urgency"],
            order_value=self.current_task["order_value"],
            days_since_order=self.current_task["days_since_order"]
        )

    def step(self, action: Action):
        if self.done:
            return None

        self.steps += 1
        self.history.append(action)

        reward_value = 0.0
        reason = ""

        # Correct or wrong action
        if action.action_type == self.current_task["expected_action"]:
            reward_value += 0.4
            reason = "correct action"
        else:
            reward_value -= 0.3
            reason = "wrong action"

        # Penalty for repeating same action
        if len(self.history) >= 2:
            if self.history[-1].action_type == self.history[-2].action_type:
                reward_value -= 0.2
                reason += " | repeated action"

        # Bonus for fast correct decision
        if self.steps == 1 and action.action_type == self.current_task["expected_action"]:
            reward_value += 0.3
            reason += " | fast resolution"

        # Business logic rewards

        # High value order handled correctly
        if self.current_task["order_value"] > 5000 and action.action_type == "escalate":
            reward_value += 0.2
            reason += " | high value handled correctly"

        # Wrong handling of fraud
        if self.current_task["account_status"] == "flagged" and action.action_type == "refund":
            reward_value -= 0.5
            reason += " | risky refund on flagged account"

        # End condition
        if action.action_type == self.current_task["expected_action"] or self.steps >= 3:
            self.done = True
            final_score = grade(self.current_task, self.history, self.steps)
            reward_value += final_score

        observation = Observation(
            ticket_id=self.current_task["ticket_id"],
            customer_message=self.current_task["message"],
            previous_messages=[a.action_type for a in self.history],
            account_status=self.current_task["account_status"],
            urgency_level=self.current_task["urgency"],
            order_value=self.current_task["order_value"],
            days_since_order=self.current_task["days_since_order"]
        )

        return observation, Reward(value=reward_value, reason=reason), self.done, {}

    def state(self):
        return {
            "task": self.current_task,
            "history": [a.dict() for a in self.history],
            "steps": self.steps,
            "done": self.done
        }