import hyperdiv as hd
from Quiz import Quiz
import json

QUESTIONS_PATH = "questions.json"

def main():
    state = hd.state(quiz=None)
    if state.quiz is None:
        with open(QUESTIONS_PATH, "r") as f:
            questions = json.load(f)
            state.quiz = Quiz(questions, reps=1)


    if not state.quiz.is_complete():
        question = state.quiz.get_current_question()
        hd.text(state.quiz.get_current_question())
        with hd.form(direction="horizontal", gap=1, grow=1) as form:
            with hd.box():
                form.text_input(value="", name="answer", grow=1)
            form.submit_button("Submit", variant="success")

            if form.submitted:
                print(form.form_data['answer'])
                state.quiz.answer_question(form.form_data['answer'])
                hd.text(form.form_data['answer'])
                        
        hd.text(state.quiz.get_score())
    else:
        hd.text("Quiz Complete!")

    progress_percent = state.quiz.get_score()*100/state.quiz.get_total_questions()
    bar = hd.progress_bar(str(progress_percent) + "%", value=int(progress_percent))
    
        


hd.run(main)