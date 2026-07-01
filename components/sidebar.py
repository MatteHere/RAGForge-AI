import streamlit as st


def render_sidebar():
    if "sidebar_open" not in st.session_state:
        st.session_state.sidebar_open = True

    toggle_label = "×" if st.session_state.sidebar_open else "☰"

    if st.button(toggle_label, key="sidebar_toggle"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open
        st.rerun()

    sidebar_class = "custom-sidebar open" if st.session_state.sidebar_open else "custom-sidebar closed"

    st.markdown(
        f"""
        <div class="{sidebar_class}">
            <div class="sidebar-logo">📄</div>
            <div class="sidebar-title">RAGForge AI</div>

            <div class="nav-item nav-active">🏠 &nbsp; Dashboard</div>
            <div class="nav-item">📁 &nbsp; Workspaces</div>
            <div class="nav-item">📄 &nbsp; Documents</div>
            <div class="nav-item">💬 &nbsp; AI Chat</div>
            <div class="nav-item">📊 &nbsp; Analytics</div>
            <div class="nav-item">🛡️ &nbsp; Evaluation</div>
            <div class="nav-item">⚙️ &nbsp; Settings</div>

            <div class="status-box">
                <div><span class="status-dot">●</span> <span class="status-title">System Status</span></div>
                <div class="status-text">All Systems Operational</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )