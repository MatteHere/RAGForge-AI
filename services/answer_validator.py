class AnswerValidator:
    def validate_answer(self, answer: str) -> str:
        if not answer or not answer.strip():
            return "I could not generate a valid answer from the uploaded documents."

        return answer.strip()