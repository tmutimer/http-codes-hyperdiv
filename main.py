import hyperdiv as hd
from Quiz import Quiz
from HttpQuestionRepo import HttpQuestionRepo


def main():
    with hd.box(align="end", margin=1):
        hd.theme_switcher()
    state = hd.state(quiz=None, difficulty=1)
    if state.quiz is None:
        questions = HttpQuestionRepo().get_questions(difficulty=state.difficulty)
        state.quiz = Quiz(questions, reps=2)

    with hd.box(
        gap=1,
        margin=8,
        height="100%",
        align="center",
        justify="center",
    ):
        hd.h1("Learn HTTP Codes")

        with hd.button_group(margin=2):
            level1 = (
                hd.button("Level 1")
                if state.difficulty != 1
                else hd.button("Level 1", variant="primary")
            )
            level2 = (
                hd.button("Level 2")
                if state.difficulty != 2
                else hd.button("Level 2", variant="primary")
            )
            level3 = (
                hd.button("Level 3")
                if state.difficulty != 3
                else hd.button("Level 3", variant="primary")
            )
            level4 = (
                hd.button("All")
                if state.difficulty is not None
                else hd.button("All", variant="primary")
            )
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
            hd.text("Which HTTP code is this?")
            with hd.hbox(border="1px solid gray-300", border_radius="large"):
                hd.markdown(
                    f"**{state.quiz.current_question.name}**:",
                    align="end",
                    width=10,
                    padding=1,
                    background_color="gray-50",
                    border_radius="large",
                )
                hd.text(
                    state.quiz.current_question.description,
                    padding=1,
                    width=30,
                )
            with hd.form(direction="horizontal", gap=1, grow=1) as form:
                with hd.box(width=20, align="center"):
                    hd.text("Type your answer and press Enter:")
                    answer_box = form.text_input(
                        value="",
                        name="answer",
                        grow=1,
                        placeholder="e.g. 403",
                        input_type="number",
                        inputmode="numeric",
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
                state.quiz.previous_question or None
            )
            if prev_question:
                dialog = hd.dialog("Incorrect")                
                with dialog:
                    with hd.box(gap=1):
                        hd.markdown("## The correct answer is: " + prev_question.answer)
                        hd.text(f"{prev_question.name}: {prev_question.description}")
                        hd.markdown(
                            f"[More info about this code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/{prev_question.answer})"
                        )
                        if hd.button("Continue").clicked:
                            dialog.opened = False

                last_answer_correct = state.quiz.previous_question.answer_history[-1]
                if not last_answer_correct:
                    dialog.opened = True
        else:
            hd.text("Well done!")

        with hd.box(height=25, width="90%", margin_left=5, margin_right=5):
            category_scores = state.quiz.get_scores_by_category()
            dataset = []
            labels = []
            for category, scores in category_scores.items():
                dataset.append(
                    max(scores["score"] * 100 / scores["total_questions"], 10)
                )
                labels.append(category)
            hd.radar_chart(
                tuple(dataset),
                axis=tuple(labels),
                r_min=0,
                r_max=100,
                show_tick_labels=False,
            )


hd.run(main)
