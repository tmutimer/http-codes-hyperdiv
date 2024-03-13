import hyperdiv as hd
from Quiz import Quiz
from HttpQuestionRepo import HttpQuestionRepo


def main():
    state = hd.state(quiz=None, difficulty=1)
    if state.quiz is None:
        questions = HttpQuestionRepo().get_questions(difficulty=state.difficulty)
        state.quiz = Quiz(questions, reps=2)

    with hd.box(
        gap=1,
        grow=1,
        margin=8,
        height="100%",
        align="center",
        justify="center",
    ):
        hd.h1("Learn HTTP Codes")

        with hd.button_group(margin=2):
            level1 = hd.button("Level 1") if state.difficulty != 1 else hd.button("Level 1", variant="primary")
            level2 = hd.button("Level 2") if state.difficulty != 2 else hd.button("Level 2", variant="primary")
            level3 = hd.button("Level 3") if state.difficulty != 3 else hd.button("Level 3", variant="primary")
            level4 = hd.button("All") if state.difficulty is not None else hd.button("All", variant="primary")
            if level1.clicked:
                state.difficulty = 1
                state.quiz = Quiz(
                    HttpQuestionRepo().get_questions(difficulty=state.difficulty),
                    reps=2,
                )
            if level2.clicked:
                state.difficulty = 2
                state.quiz = Quiz(
                    HttpQuestionRepo().get_questions(difficulty=state.difficulty),
                    reps=2,
                )
            if level3.clicked:
                state.difficulty = 3
                state.quiz = Quiz(
                    HttpQuestionRepo().get_questions(difficulty=state.difficulty),
                    reps=2,
                )
            if level4.clicked:
                state.difficulty = None
                state.quiz = Quiz(
                    HttpQuestionRepo().get_questions(difficulty=state.difficulty),
                    reps=2,
                )

        if state.quiz is None or not state.quiz.is_complete():
            with hd.box(height=5):
                hd.h3(state.quiz.get_current_question())
            with hd.form(direction="horizontal", gap=1, grow=1) as form:
                with hd.box():
                    hd.text("Type your answer and press Enter:")
                    answer_box = form.text_input(
                        value="",
                        name="answer",
                        grow=1,
                        placeholder="e.g. 403",
                        input_type="number",
                        maxlength=3,
                        autocomplete="Off",
                        no_spin_buttons=True,
                        pill=True,
                        autofocus=True,
                        suffix_icon="arrow-return-left",
                    )

                if form.submitted:
                    state.quiz.answer_question(form.form_data["answer"])
                    answer_box.value = ""

            prev_question = (
                state.quiz.previous_question if state.quiz.previous_question else None
            )
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
                        hd.markdown(
                            f"[More info about this code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/{prev_question.answer})"
                        )
                        if hd.button("Continue").clicked:
                            dialog.opened = False
        else:
            hd.text("Well done!")

        with hd.box(width="90%", margin=5):
            hd.text("Progress:")
            progress_percent = int(
                state.quiz.get_score() * 100 / state.quiz.get_total_questions()
            )
            hd.progress_bar(str(progress_percent) + "%", value=int(progress_percent))

        with hd.box(height=30, width="90%", margin=5):
            category_scores = state.quiz.get_scores_by_category()
            dataset = []
            labels = []
            for category, scores in category_scores.items():
                dataset.append(max(scores["score"] * 100 / scores["total_questions"],10))
                labels.append(category)
            hd.radar_chart(
                tuple(dataset), 
                axis=tuple(labels),
                r_min=0,
                r_max=100,
                show_tick_labels=False
                )


hd.run(main)
