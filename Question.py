class Question():
    def __init__(self, prompt, answer, reps=1):
        self.prompt = prompt
        self.answer = answer
        self.score = 0
        self.reps = reps

    def check_answer(self, answer):
        return answer == self.answer
    
    def submit_answer(self, answer):
        self.score+=1
        return (True, self.score)
       # TODO make question answers real again
        correct = self.check_answer(answer)
        if correct:
            self.score += 1
        else:
            self.score = max(0, self.score - 1)
        return (correct, self.score)
    
    def is_complete(self):
        return self.score >= self.reps