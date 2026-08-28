import os
import streamlit as st

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

from agents.orchestrator import OrchestratorAgent

st.set_page_config(page_title="Multi-Agent Research Assistant", page_icon="🔎")

st.title("🔎 Multi-Agent AI Research Assistant")
st.caption(
    "Retrieves from PDFs, datasets, and an API -> analyzes & cross-validates "
    "-> critiques -> reports -> distributes (file + dashboard + email)."
)

if not os.environ.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY") == "KEY":
    st.error(
        "No GROQ_API_KEY found. Add it in your Streamlit app's **Settings > Secrets** "
        "(or as an environment variable if running locally)."
    )
    st.stop()

if "orchestrator" not in st.session_state:
    with st.spinner("Starting up agents..."):
        st.session_state.orchestrator = OrchestratorAgent()

query = st.text_input("Ask a research question:", placeholder="e.g. What are the key findings across our sources?")

if st.button("Run", type="primary") and query:
    with st.spinner("Agents working: retrieval -> analysis -> critique -> report -> actions..."):
        result = st.session_state.orchestrator.run(query)

    st.subheader("📄 Final Report")
    st.write(result["report"])

    with st.expander("🔬 Analysis details"):
        st.json(result["analysis"])

    with st.expander("⚙️ Action results (file / dashboard / email)"):
        st.json(result["actions"])

st.divider()
st.caption(
    "Note: on free hosting, the filesystem resets between deploys/restarts, "
    "so saved reports and the dashboard file are not permanently persisted."
)
