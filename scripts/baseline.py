from env.environment import SupportEnv
from env.models import Action


def choose_action(message):
    msg = message.lower()

    if "refund" in msg:
        return "refund"
    elif "fraud" in msg:
        return "escalate"
    elif "late" in msg or "delay" in msg:
        return "reply"
    else:
        return "close_ticket"


def run_task(task_name):
    env = SupportEnv()
    obs = env.reset(task_name)

    actions = []

    for _ in range(3):

        action_type = choose_action(obs.customer_message)

        action = Action(action_type=action_type)

        obs, reward, done, _ = env.step(action)

        actions.append(action_type)

        if done:
            break

    print(f"{task_name} actions:", actions)


if __name__ == "__main__":
    for t in ["easy", "medium", "hard"]:
        run_task(t)
