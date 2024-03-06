import json

class HttpQuestionRepo:
    def __init__(self, data_source):
        self.data_source = data_source

    def _load_questions(self):
        """Load questions from the data source."""
        if isinstance(self.data_source, str):
            with open(self.data_source, "r") as f:
                questions = json.load(f)
        else:
            questions = self.data_source
        return questions

    def get_questions(self, difficulty=1):
        """Filter questions by difficulty."""
        questions = self._load_questions()
        return [q for q in questions if q['level'] == difficulty]
