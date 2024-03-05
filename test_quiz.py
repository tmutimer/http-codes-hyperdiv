import math
from Quiz import Quiz
from Question import Question

def create_test_quiz():
    questions = [
        {"prompt": "What color are apples?", "answer": "red"},
        {"prompt": "What color are bananas?", "answer": "yellow"},
        {"prompt": "What color are oranges?", "answer": "orange"},
    ]
    return Quiz(questions)

def create_quiz_single_question():
    questions = [
        {"prompt": "What color are apples?", "answer": "red"},
    ]
    return Quiz(questions)
    

def test_get_current_question():
    quiz = create_quiz_single_question()
    assert quiz.get_current_question() == 'What color are apples?'

def test_answer_question():
    quiz = create_quiz_single_question()
    result = quiz.answer_question('red')
    assert result == True
    assert quiz.get_score() == 1

def test_is_complete():
    quiz = create_quiz_single_question()
    assert not quiz.is_complete()
    quiz.answer_question('red')
    assert quiz.is_complete()

def test_get_total_questions():
    quiz = create_quiz_single_question()
    assert quiz.get_total_questions() == 1
    quiz = create_test_quiz()
    assert quiz.get_total_questions() == 3
    quiz = Quiz([{"prompt": "What color are apples?", "answer": "red"}], reps=2)
    assert quiz.get_total_questions() == 2