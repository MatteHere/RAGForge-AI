import pandas as pd
import streamlit as st

from services.analytics_service import AnalyticsService


def render_search_analytics():
    analytics_service = AnalyticsService()

    st.title("📊 Search Analytics")
    st.caption("Monitor retrieval activity, latency, and search performance across RAGForge AI.")

    metrics = analytics_service.get_summary_metrics()
    logs = analytics_service.get_search_logs()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Searches", metrics["total_searches"])

    with col2:
        st.metric("Average Latency", f'{metrics["average_response_time_ms"]} ms')

    with col3:
        st.metric("Total Results Returned", metrics["total_results"])

    st.divider()

    if not logs:
        st.info("No search logs found yet. Run a search in Knowledge Base first.")
        return

    dataframe = pd.DataFrame(logs)

    st.subheader("Search History")
    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True,
    )