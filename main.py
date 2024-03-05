import hyperdiv as hd
from Quiz import Quiz
import json

QUESTIONS_PATH = "questions.json"

def main():
    state = hd.state(quiz=None)
    if state.quiz is None:
        with open(QUESTIONS_PATH, "r") as f:
            questions = json.load(f)
            state.quiz = Quiz(questions, reps=2)

    with hd.box(
        gap=1, 
        grow=1,
        margin=8,
        height="100%",
        align="center",
        justify="center",):

        hd.h1("Learn HTTP Codes")

        if not state.quiz.is_complete():
            question = state.quiz.get_current_question()
            hd.h3(state.quiz.get_current_question())
            with hd.form(direction="horizontal", gap=1, grow=1) as form:
                with hd.box():
                    hd.text("Type your answer and press Enter:")
                    answer_box = form.text_input(value="", name="answer", grow=1)
                # form.submit_button("Submit", variant="success")

                if form.submitted:
                    state.quiz.answer_question(form.form_data['answer'])
                    hd.text(form.form_data['answer'])
                    answer_box.value = ""

            success = hd.alert("Correct!", variant='success')

            if not state.quiz.is_complete():
                hd.text("(Ans: " + state.quiz.current_question.answer + ")")
        else:
            hd.text("Well done!")

        with hd.box(width="100%"):
            progress_percent = state.quiz.get_score()*100/state.quiz.get_total_questions()
            bar = hd.progress_bar(str(progress_percent) + "%", value=int(progress_percent))
            

hd.run(main)