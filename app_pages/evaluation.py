import streamlit as st

from evaluation.evaluation_engine import EvaluationEngine
from evaluation.system_validator import SystemValidator
from services.workspace_service import WorkspaceService


def score_label(score: float) -> str:
    if score >= 0.85:
        return "Excellent"
    if score >= 0.65:
        return "Good"
    if score >= 0.40:
        return "Needs Improvement"
    return "Poor"


def render_score_card(title: str, value: float):
    st.metric(title, f"{value:.2f} / 1.00")
    st.progress(max(0.0, min(value, 1.0)))
    st.caption(score_label(value))


def render_validation_results(results: list[dict]):
    st.subheader("🔍 System Validation")

    for result in results:
        if result["status"] == "PASS":
            st.success(f"✅ {result['check']}")

        else:
            st.error(f"❌ {result['check']}")

        if result["message"]:
            st.caption(result["message"])


def render_evaluation():
    workspace_service = WorkspaceService()
    evaluation_engine = EvaluationEngine()
    validator = SystemValidator()

    st.title("📈 Evaluation")

    st.caption(
        "Evaluate answer quality and validate the complete RAG pipeline."
    )

    workspaces = workspace_service.get_all_workspaces()

    if not workspaces:
        st.info("Create a workspace first.")
        return

    workspace_map = {
        workspace.name: workspace.id
        for workspace in workspaces
    }

    tab1, tab2 = st.tabs(
        [
            "Evaluation",
            "System Validation",
        ]
    )

    # ---------------- Evaluation ---------------- #

    with tab1:

        selected_workspace = st.selectbox(
            "Workspace",
            workspace_map.keys(),
        )

        question = st.text_area(
            "Evaluation Question",
            placeholder="What is Hybrid Retrieval?",
            height=120,
        )

        expected_keywords = st.text_input(
            "Expected Keywords",
            placeholder="BM25, Vector Search, Retrieval",
        )

        if st.button(
            "Run Evaluation",
            type="primary",
            use_container_width=True,
        ):

            keywords = [
                keyword.strip()
                for keyword in expected_keywords.split(",")
                if keyword.strip()
            ]

            result = evaluation_engine.evaluate_question(
                question=question,
                workspace_id=workspace_map[selected_workspace],
                expected_keywords=keywords,
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                render_score_card(
                    "Overall",
                    result["overall_score"],
                )

            with col2:
                render_score_card(
                    "Keyword",
                    result["keyword_score"],
                )

            with col3:
                render_score_card(
                    "Citation",
                    result["citation_score"],
                )

            with col4:
                render_score_card(
                    "Retrieval",
                    result["retrieval_score"],
                )

            st.metric(
                "Response Time",
                f'{result["response_time_ms"]} ms',
            )

            st.divider()

            st.subheader("Generated Answer")

            st.write(result["answer"])

            st.info(
                f'Sources Used: {result["source_count"]} | '
                f'Citations: {result["citation_count"]}'
            )

    # ---------------- Validation ---------------- #

    with tab2:

        st.write(
            "Validate every major component of the RAG pipeline."
        )

        if st.button(
            "Run System Validation",
            type="primary",
            use_container_width=True,
        ):

            with st.spinner("Running validation..."):

                validation_results = validator.run_validation()

            render_validation_results(validation_results)