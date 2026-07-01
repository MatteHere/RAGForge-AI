from retrieval.bm25_retriever import BM25Retriever
from retrieval.citation_engine import CitationEngine
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.reranker import CrossEncoderReranker
from retrieval.vector_retriever import VectorRetriever
from services.answer_service import AnswerService
from services.document_service import DocumentService
from services.workspace_service import WorkspaceService


class SystemValidator:
    def __init__(self):
        self.workspace_service = WorkspaceService()
        self.document_service = DocumentService()
        self.bm25_retriever = BM25Retriever()
        self.vector_retriever = VectorRetriever()
        self.hybrid_retriever = HybridRetriever()
        self.reranker = CrossEncoderReranker()
        self.citation_engine = CitationEngine()
        self.answer_service = AnswerService()

    def run_validation(self, query: str = "hybrid retrieval") -> list[dict]:
        results = []

        workspaces = self.workspace_service.get_all_workspaces()
        results.append(self._result("Workspace Loading", bool(workspaces)))

        documents = self.document_service.get_all_documents()
        results.append(self._result("Document Loading", bool(documents)))

        if not workspaces:
            return results

        workspace_id = workspaces[0].id

        bm25_results = self.bm25_retriever.search(query, workspace_id, top_k=5)
        results.append(self._result("BM25 Retrieval", bool(bm25_results)))

        vector_results = self.vector_retriever.search(query, workspace_id, top_k=5)
        results.append(self._result("Vector Retrieval", bool(vector_results)))

        hybrid_results = self.hybrid_retriever.search(query, workspace_id, top_k=5)
        results.append(self._result("Hybrid Retrieval", bool(hybrid_results)))

        reranked_results = self.reranker.rerank(query, hybrid_results, top_k=5)
        results.append(self._result("Cross-Encoder Reranking", bool(reranked_results)))

        citations = self.citation_engine.build_citations(reranked_results)
        results.append(self._result("Citation Generation", bool(citations)))

        try:
            answer_response = self.answer_service.answer_question(query, workspace_id)
            results.append(self._result("Answer Generation", bool(answer_response.get("answer"))))
        except Exception as error:
            results.append(self._result("Answer Generation", False, str(error)))

        return results

    def _result(self, check_name: str, passed: bool, message: str = "") -> dict:
        return {
            "check": check_name,
            "status": "PASS" if passed else "FAIL",
            "message": message or ("OK" if passed else "Needs attention"),
        }