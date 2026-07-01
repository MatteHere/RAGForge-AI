from llm.ollama_client import OllamaClient
from retrieval.citation_engine import CitationEngine
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.reranker import CrossEncoderReranker
from services.answer_validator import AnswerValidator
from services.prompt_builder import PromptBuilder


class AnswerService:
    def __init__(self):
        self.hybrid_retriever = HybridRetriever()
        self.reranker = CrossEncoderReranker()
        self.citation_engine = CitationEngine()
        self.prompt_builder = PromptBuilder()
        self.answer_validator = AnswerValidator()
        self.llm_client = OllamaClient()

    def answer_question(self, question: str, workspace_id: int) -> dict:
        if not question.strip():
            raise ValueError("Question cannot be empty.")

        retrieved_chunks = self.hybrid_retriever.search(
            query=question,
            workspace_id=workspace_id,
            top_k=10,
        )

        if not retrieved_chunks:
            return {
                "answer": "I could not find relevant information in your uploaded documents.",
                "sources": [],
                "citations": [],
            }

        reranked_chunks = self.reranker.rerank(
            query=question,
            results=retrieved_chunks,
            top_k=5,
        )

        citations = self.citation_engine.build_citations(reranked_chunks)

        prompt = self.prompt_builder.build_rag_prompt(
            question=question,
            chunks=reranked_chunks,
        )

        raw_answer = self.llm_client.generate(prompt)

        validated_answer = self.answer_validator.validate_answer(raw_answer)

        final_answer = self.citation_engine.enforce_citations(
            answer=validated_answer,
            citations=citations,
        )

        return {
            "answer": final_answer,
            "sources": reranked_chunks,
            "citations": citations,
        }