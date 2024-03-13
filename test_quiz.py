from HttpQuestionRepo import HttpQuestionRepo
from Quiz import Quiz

def create_test_quiz():
    questions = [
        {"name": "What color are apples?","description": "?", "answer": "red", "level": 1, 'category': 'fruit'},
        {"name": "What color are bananas?","description": "?", "answer": "yellow", "level": 2, 'category': 'fruit'},
        {"name": "What color are oranges?","description": "?", "answer": "orange", "level": 3, 'category': 'fruit'},
    ]
    return Quiz(questions)

def create_quiz_single_question():
    questions = [
        {"name": "What color are apples?", "description": "?", "answer": "red", "level": 1, 'category': 'fruit'},
    ]
    return Quiz(questions)
    

def test_get_current_question():
    quiz = create_quiz_single_question()
    assert quiz.get_current_question() == 'What color are apples?: ?'

def test_answer_question():
    quiz = create_quiz_single_question()
    result = quiz.answer_question('red')
    assert result is True
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
    quiz = Quiz([{"name": "What color are apples?","description": "?", "answer": "red", 'level':1, 'category': 'fruit'}], reps=2)
    assert quiz.get_total_questions() == 2

def test_incorrect_answer():
    quiz = create_quiz_single_question()
    result = quiz.answer_question('blue')
    assert result is False
    assert quiz.get_score() == 0

def test_previous_question():
    quiz = create_test_quiz()
    question = quiz.current_question.name + quiz.current_question.description
    quiz.answer_question(quiz.current_question.answer)
    prev = quiz.get_previous_question()
    assert prev == (question, True)

def test_final_question_no_repeat():
    '''
    Test that we don't test the final question more than once in a row
    '''
    questions = [
        {"name": "What color are apples?", "description": "?", "answer": "red", "level": 1, 'category': 'fruit'},
    ]
    quiz = Quiz(questions, reps=3)
    quiz.answer_question('red')
    assert quiz.get_current_question() == "Quiz Complete!"
    assert quiz.get_score() == quiz.get_total_questions()

def test_get_questions_for_difficulty():
    questions = [
        {"name": "What color are apples?", "description": "?","answer": "red", "level": 1, 'category': 'fruit'},
        {"name": "What color are bananas?", "description": "?", "answer": "yellow", "level": 2, 'category': 'fruit'},
        {"name": "What color are oranges?", "description": "?", "answer": "orange", "level": 3, 'category': 'fruit'},
    ]
    question_bank = HttpQuestionRepo(questions)
    quiz = Quiz(question_bank.get_questions(difficulty=1))
    assert quiz.get_current_question() == "What color are apples?: ?"

    quiz = Quiz(question_bank.get_questions(difficulty=2))
    assert quiz.get_current_question() == "What color are bananas?: ?"

    quiz = Quiz(question_bank.get_questions(difficulty=3))
    assert quiz.get_current_question() == "What color are oranges?: ?"

def test_get_scores_by_category():
    questions = [
        {"name": "What color are apples?","description": "?", "answer": "red", "level": 1, 'category': 'fruit'},
        {"name": "What color are bananas?","description": "?", "answer": "yellow", "level": 2, 'category': 'fruit'},
        {"name": "What color are oranges?","description": "?", "answer": "orange", "level": 3, 'category': 'fruit'},
    ]
    question_bank = HttpQuestionRepo(questions)
    quiz = Quiz(question_bank.get_questions(), reps=2)
    quiz.answer_question(quiz.current_question.answer)
    scores = quiz.get_scores_by_category()
    print(scores)
    assert quiz.get_scores_by_category()['fruit']['score'] == 1
    assert quiz.get_scores_by_category()['fruit']['total_questions'] == 6