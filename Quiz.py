import random
import hyperdiv as hd
from Question import Question

class Quiz():
    def __init__(self, questions, reps=1):
        self.reps = reps
        self.questions = [Question(q['prompt'], q['answer'], q['category'], reps=self.reps) for q in questions]
        self.current_question = None
        self.previous_question = None
        self.select_new_question()

    def get_current_question(self):
        return self.current_question.prompt if self.current_question else "Quiz Complete!"
    
    def answer_question(self, answer):
        (result, _) = self.submit_answer(self.current_question, answer)
        self.select_new_question()
        return result
    
    def submit_answer(self, question, answer):
        correct = question.check_answer(answer)
        question.answer_history.append(correct)
        if correct:
            if self._is_final_question():
                question.score = self.reps
            else:
                question.score += 1

        else:
            question.score = max(0, question.score - 1)
        return (correct, question.score)
    
    def _is_final_question(self):
        # if there are no other incomplete questions, this is the final question
        return len([q for q in self.questions if not q.is_complete() and q != self.current_question]) == 0

    def select_new_question(self):
        incomplete_questions = [q for q in self.questions if not q.is_complete() and q != self.current_question]
        
        self.previous_question = self.current_question
        
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
    
    def get_previous_question(self):
        return (self.previous_question.prompt, self.previous_question.answer_history[-1])
    
    
    def get_scores_by_category(self):
        categories = set([q.category for q in self.questions])
        scores_by_category = {}
        
        for category in categories:
            category_score = sum([q.score for q in self.questions if q.category == category])
            category_total_questions = sum([q.reps for q in self.questions if q.category == category])
            
            scores_by_category[category] = {
                'score': category_score,
                'total_questions': category_total_questions 
                }
        
        return scores_by_category