# === file: review_engine.py ===
def run_reviews(reviewers, manuscript_text):
    review_prompt = f"Please review the following manuscript:\n\n{manuscript_text}"
    responses = {}

    for agent in reviewers:
        response = agent.run(message=review_prompt, max_turns=1, user_input=False)
        response.process()
        responses[agent.name] = response.messages[-1]["content"]

    return responses


def print_reviews(responses):
    for reviewer, review in responses.items():
        print(f"\n\n--- {reviewer} Review ---\n")
        print(review)
