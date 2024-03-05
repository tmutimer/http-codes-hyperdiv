import random
import hyperdiv as hd
from Question import Question

class Quiz():
    def __init__(self, questions, reps=1):
        self.reps = reps
        self.questions = [Question(q['prompt'], q['answer'],reps=self.reps) for q in questions]
        self.current_question = None
        self.select_new_question()

    def get_current_question(self):
        return self.current_question.prompt if self.current_question else "Quiz Complete!"
    
    def answer_question(self, answer):
        (result, _) = self.current_question.submit_answer(answer)
        self.select_new_question()
        return result
    
    def select_new_question(self):
        incomplete_questions = [q for q in self.questions if not q.is_complete()]
        
        if not incomplete_questions:
            self.current_question = None
            return
        
        selected_question = random.choice(incomplete_questions)
        self.current_question = selected_question

    def get_score(self):
        return sum([q.score for q in self.questions])
    
    def get_total_questions(self):
        return len(self.questions) * self.reps
    
    def is_complete(self):
        return all([q.is_complete() for q in self.questions])