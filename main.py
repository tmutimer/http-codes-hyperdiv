import hyperdiv as hd
from Quiz import Quiz
import json

QUESTIONS_PATH = "questions.json"

def get_questions(difficulty=1):
    with open(QUESTIONS_PATH, "r") as f:
        questions = json.load(f)
        return [q for q in questions if q['level'] == difficulty]

def main():
    state = hd.state(quiz=None)
    if state.quiz is None:
            state.quiz = Quiz(get_questions(), reps=2)

    with hd.box(
        gap=1, 
        grow=1,
        margin=8,
        height="100%",
        align="center",
        justify="center",):

        hd.h1("Learn HTTP Codes")

        if not state.quiz.is_complete():
            with hd.box(height=5):
                hd.h3(state.quiz.get_current_question())
            with hd.form(direction="horizontal", gap=1, grow=1) as form:
                with hd.box():
                    hd.text("Type your answer and press Enter:")
                    answer_box = form.text_input(value="",
                                                 name="answer", 
                                                 grow=1, 
                                                 placeholder="e.g. 403",
                                                 input_type='number',
                                                 maxlength=3,
                                                 autocomplete='Off',
                                                 no_spin_buttons=True,
                                                 pill=True,
                                                 autofocus=True,
                                                 suffix_icon="arrow-return-left")
                # form.submit_button("Submit", variant="success")

                if form.submitted:
                    state.quiz.answer_question(form.form_data['answer'])
                    # hd.text(form.form_data['answer'])
                    answer_box.value = ""

            prev_question = state.quiz.previous_question if state.quiz.previous_question else None
            if prev_question:
                last_answer_correct = state.quiz.previous_question.answer_history[-1]
                if last_answer_correct:
                    with hd.hbox(gap=0.5):
                        hd.icon("check-circle")
                        hd.text("Correct!")
                        
                if last_answer_correct is False:
                    dialog = hd.dialog("Incorrect!", opened=True)
                    # must reset dialog from mutated state after close
                    dialog.reset_prop("opened")
                    with dialog:
                        hd.markdown("## The correct answer is: " + prev_question.answer)
                        hd.text(prev_question.prompt)
                        hd.markdown(f"[More info about this code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/{prev_question.answer})")
                        if hd.button("Continue").clicked:
                            dialog.opened = False

            # if not state.quiz.is_complete():
            #     hd.text("(Ans: " + state.quiz.current_question.answer + ")")
        else:
            hd.text("Well done!")

        with hd.box(width="90%", margin=5):
            hd.text("Progress:")
            progress_percent = int(state.quiz.get_score()*100/state.quiz.get_total_questions())
            bar = hd.progress_bar(str(progress_percent) + "%", value=int(progress_percent))
            

hd.run(main)