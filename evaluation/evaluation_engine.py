import time

from services.answer_service import AnswerService


class EvaluationEngine:
    def __init__(self):
        self.answer_service = AnswerService()

    def evaluate_question(
        self,
        question: str,
        workspace_id: int,
        expected_keywords: list[str],
    ) -> dict:
        start_time = time.time()

        response = self.answer_service.answer_question(
            question=question,
            workspace_id=workspace_id,
        )

        response_time_ms = round((time.time() - start_time) * 1000, 2)

        answer = response["answer"]
        citations = response["citations"]
        sources = response["sources"]

        keyword_score = self._calculate_keyword_score(
            answer=answer,
            expected_keywords=expected_keywords,
        )

        citation_score = self._calculate_citation_score(citations)
        retrieval_score = self._calculate_retrieval_score(sources)

        overall_score = round(
            (keyword_score + citation_score + retrieval_score) / 3,
            2,
        )

        return {
            "question": question,
            "answer": answer,
            "keyword_score": keyword_score,
            "citation_score": citation_score,
            "retrieval_score": retrieval_score,
            "overall_score": overall_score,
            "response_time_ms": response_time_ms,
            "citation_count": len(citations),
            "source_count": len(sources),
        }

    def _calculate_keyword_score(
        self,
        answer: str,
        expected_keywords: list[str],
    ) -> float:
        if not expected_keywords:
            return 0.0

        answer_lower = answer.lower()

        matched_keywords = [
            keyword
            for keyword in expected_keywords
            if keyword.lower() in answer_lower
        ]

        return round(len(matched_keywords) / len(expected_keywords), 2)

    def _calculate_citation_score(self, citations: list[dict]) -> float:
        if not citations:
            return 0.0

        return 1.0

    def _calculate_retrieval_score(self, sources: list[dict]) -> float:
        if not sources:
            return 0.0

        return 1.0