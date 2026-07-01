class PromptBuilder:
    def build_rag_prompt(
        self,
        question: str,
        chunks: list[dict],
    ) -> str:
        context_blocks = []

        for index, chunk in enumerate(chunks, start=1):
            context_blocks.append(
                f"""
Source {index}
File Name: {chunk.get("file_name", "Unknown Document")}
Document ID: {chunk["document_id"]}
Chunk Index: {chunk["chunk_index"]}

{chunk["chunk_text"]}
"""
            )

        context = "\n\n".join(context_blocks)

        return f"""
You are RAGForge AI, an enterprise Retrieval-Augmented Generation assistant.

Answer the user's question using ONLY the provided context.

Rules:
- Do not make up information.
- If the answer is not present in the context, say:
  "I could not find this information in the uploaded documents."
- Keep the answer clear, structured, and professional.
- Reference the relevant source number when making claims.
- Do not cite documents that were not provided in the context.

Context:
{context}

User Question:
{question}

Answer:
"""
    