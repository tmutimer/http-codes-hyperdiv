import hyperdiv as hd
from Quiz import Quiz
import json

QUESTIONS_PATH = "questions.json"

def main():

    with open(QUESTIONS_PATH, "r") as f:
        questions = json.load(f)
        quiz = Quiz(questions, reps=3)

        hd.text(quiz.get_current_question())

        with hd.form(direction="horizontal", gap=1, grow=1) as form:
                with hd.box():
                    form.text_input(value="", name="answer", grow=1)
                form.submit_button("Submit", variant="success")

                if form.submitted:
                    quiz.answer_question(form.answer)
                    hd.text(quiz.get_score())
        


hd.run(main)