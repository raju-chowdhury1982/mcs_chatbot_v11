import requests
import streamlit as st

# verify the URL
API_BASE = st.secrets.get(
    "api_base", "http://localhost:8000/chat"
)  # Adjust as API is hosted
print(f"Trying to reach: {API_BASE}")


# Test if the server is running
try:
    response = requests.get(API_BASE.replace("/chat", ""), timeout=5)
    print(f"Server status: {response.status_code}")
except Exception as e:
    print(f"Cannot reach server: {e}")


st.set_page_config(page_title="MCS Q&A Chatbot", page_icon="🤖")
st.title("🚢 MCS Q&A Chatbot 🤖")


with st.sidebar:
    st.header("Settings")
    consignee_code = st.text_input(
        "Consignee Code", value="", help="Your unique consignee code."
    )
    conversation_id = st.text_input(
        "Conversation ID (optional)",
        value="demo",
        help="Optional conversation ID to maintain context.",
    )

question = st.text_area("Enter your question about your shipments:", height=150)
if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    elif not consignee_code.strip():
        st.warning("Please enter your consignee code in the sidebar.")
    else:
        with st.spinner("Getting answer..."):
            payload = {  # type: ignore
                "question": question,
                "consignee_code": consignee_code,
                "conversation_id": conversation_id or None,
            }
            response = requests.post(API_BASE, json=payload, headers={"X-Consignee-Code": consignee_code})  # type: ignore
            if response.status_code == 200:
                data = response.json()
                # st.subheader("Answer:")
                # st.write(data.get("answer", "No answer provided."))
                st.markdown(data["answer"])
                with st.expander("Debug"):
                    st.json(data.get("debug", {}))

                # fact checker
                citations = data.get("citations", [])
                if citations:
                    st.subheader("Citations:")
                    for cit in citations:
                        st.write(
                            f"- Document ID: {cit.get('document_id')}, Container Number: {cit.get('container_number')}"
                        )

                # latency monitoring
                timings = data.get("timing_ms", {})
                if timings:
                    st.subheader("Timings:")
                    for k, v in timings.items():
                        st.write(f"- {k}: {v:.2f} ms")
            else:
                st.error(f"Error from API: {response.status_code} - {response.text}")
