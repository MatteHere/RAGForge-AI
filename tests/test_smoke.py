import pytest

from retrieval.citation_engine import CitationEngine
from services.answer_validator import AnswerValidator
from services.prompt_builder import PromptBuilder


def test_answer_validator():
    validator = AnswerValidator()

    assert validator.validate_answer("Hello") == "Hello"
    assert (
        validator.validate_answer("")
        == "I could not generate a valid answer from the uploaded documents."
    )


def test_prompt_builder():
    builder = PromptBuilder()

    prompt = builder.build_rag_prompt(
        question="What is Hybrid Retrieval?",
        chunks=[
            {
                "document_id": 1,
                "chunk_index": 0,
                "file_name": "test.txt",
                "chunk_text": "Hybrid Retrieval combines BM25 and Vector Search.",
            }
        ],
    )

    assert "Hybrid Retrieval" in prompt
    assert "BM25" in prompt
    assert "Vector Search" in prompt


def test_citation_engine():
    engine = CitationEngine()

    citations = engine.build_citations(
        [
            {
                "document_id": 1,
                "file_name": "demo.txt",
                "file_type": "txt",
                "chunk_index": 0,
                "chunk_text": "Example chunk",
                "retrieval_method": "hybrid",
            }
        ]
    )

    assert len(citations) == 1
    assert citations[0]["file_name"] == "demo.txt"


if __name__ == "__main__":
    pytest.main(["-v"])