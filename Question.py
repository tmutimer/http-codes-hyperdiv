class Question:
    def __init__(self, prompt, answer, category=None, reps=1):
        self.prompt = prompt
        self.answer = answer
        self.score = 0
        self.reps = reps
        self.category = category
        self.answer_history = []

    def check_answer(self, answer):
        return answer == self.answer

    def is_complete(self):
        return self.score >= self.reps
