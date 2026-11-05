import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from ingest import (
    BASE_DIR,
    DOCUMENTS_DIR,
    get_collection,
    ingest_documents,
    retrieve_context,
)

# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------

load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)

st.set_page_config(
    page_title="Indala College | Admission Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

TOP_K = int(os.getenv("TOP_K", "5"))
MAX_DISTANCE = float(os.getenv("MAX_DISTANCE", "1.2"))
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
UNAVAILABLE = (
    "I couldn't find this information in the official college documents "
    "currently available to me. Please contact the Indala College Admission "
    "Office for confirmation."
)


# ------------------------------------------------------------
# BACKEND HELPERS
# ------------------------------------------------------------

def save_uploaded_files(uploaded_files):
    """Save uploaded PDFs in the project's configured documents folder."""
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    saved_files = []

    for uploaded_file in uploaded_files:
        safe_name = Path(uploaded_file.name).name
        destination = DOCUMENTS_DIR / safe_name

        # Avoid accidentally overwriting an existing document.
        if destination.exists():
            stem = destination.stem
            suffix = destination.suffix
            counter = 1
            while destination.exists():
                destination = DOCUMENTS_DIR / f"{stem}_{counter}{suffix}"
                counter += 1

        destination.write_bytes(uploaded_file.getvalue())
        saved_files.append(destination.name)

    return saved_files


def generate_answer(question, matches):
    """Generate an answer using only the retrieved college-document context."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to the project's .env file."
        )

    context_parts = []
    for index, item in enumerate(matches, start=1):
        text_content = (
            item.get("text")
            or item.get("content")
            or item.get("document")
            or ""
        )
        source = item.get("source", "College document")
        page = item.get("page", "N/A")
        context_parts.append(
            f"[Source {index}: {source}, Page {page}]\n{text_content}"
        )

    context = "\n\n".join(context_parts)

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the official AI admission assistant for Indala "
                    "College. Answer the user's question using only the "
                    "provided college-document context. Do not invent fees, "
                    "dates, eligibility rules, courses, or procedures. If the "
                    "context does not contain the answer, clearly say that "
                    "the information is not available in the provided "
                    "documents and recommend contacting the college office. "
                    "Use clear, student-friendly language. When useful, "
                    "organize the answer with short headings or bullets."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"COLLEGE DOCUMENT CONTEXT:\n{context}\n\n"
                    f"STUDENT QUESTION:\n{question}"
                ),
            },
        ],
    )
    return response.choices[0].message.content.strip()


# ------------------------------------------------------------
# VISUAL DESIGN
# ------------------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --ink: #172B3A;
        --muted: #718096;
        --teal: #087E8B;
        --teal-dark: #075B66;
        --mint: #E8F5F3;
        --line: #E4ECEF;
        --surface: #FFFFFF;
        --page: #F4F8F9;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: var(--page);
        color: var(--ink);
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1240px;
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
    }

    h1, h2, h3 {
        font-family: 'Manrope', sans-serif !important;
        color: var(--ink) !important;
        letter-spacing: -0.6px;
    }

    /* Hero banner */
    .hero {
        position: relative;
        overflow: hidden;
        padding: 36px 40px;
        border-radius: 22px;
        color: #FFFFFF;
        background: linear-gradient(115deg, #103B4A 0%, #087E8B 58%, #20A39E 100%);
        box-shadow: 0 14px 35px rgba(8, 126, 139, 0.16);
        margin-bottom: 22px;
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        right: -70px;
        top: -115px;
        border: 1px solid rgba(255,255,255,.20);
        border-radius: 50%;
        box-shadow: 0 0 0 28px rgba(255,255,255,.04),
                    0 0 0 58px rgba(255,255,255,.035);
    }

    .hero-kicker {
        display: inline-block;
        padding: 6px 11px;
        border-radius: 30px;
        background: rgba(255,255,255,.14);
        border: 1px solid rgba(255,255,255,.22);
        color: #D9F5F2;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.1px;
        text-transform: uppercase;
    }

    .hero h1 {
        color: #FFFFFF !important;
        font-size: clamp(28px, 4vw, 40px) !important;
        line-height: 1.15;
        margin: 16px 0 10px 0;
    }

    .hero p {
        max-width: 700px;
        color: #E1F4F2 !important;
        font-size: 15px;
        line-height: 1.75;
        margin-bottom: 0;
    }

    .hero-meta {
        margin-top: 22px;
        color: #D5EFED;
        font-size: 12px;
        font-weight: 600;
    }

    /* Feature cards */
    .feature-card {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 18px 19px;
        min-height: 112px;
        box-shadow: 0 5px 18px rgba(23, 43, 58, .035);
    }

    .feature-icon {
        width: 37px;
        height: 37px;
        display: grid;
        place-items: center;
        border-radius: 11px;
        background: var(--mint);
        font-size: 19px;
        margin-bottom: 12px;
    }

    .feature-title {
        color: var(--ink);
        font-size: 14px;
        font-weight: 800;
    }

    .feature-desc {
        color: var(--muted);
        font-size: 12px;
        line-height: 1.5;
        margin-top: 4px;
    }

    .section-eyebrow {
        color: var(--teal);
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.25px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: var(--muted);
        font-size: 13px;
        margin-top: -7px;
        margin-bottom: 18px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #102F3C;
        border-right: 1px solid rgba(255,255,255,.08);
    }

    section[data-testid="stSidebar"] * {
        color: #EDF7F7;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] .stCaption {
        color: #B8CFD2;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,.15);
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background: rgba(255,255,255,.06);
        border: 1px dashed #5A9298;
        border-radius: 13px;
        padding: 9px;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploader"] small {
        color: #B8CFD2 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stMetric"] {
        background: rgba(255,255,255,.07);
        border: 1px solid rgba(255,255,255,.12);
        border-radius: 13px;
        padding: 13px;
    }

    section[data-testid="stSidebar"] [data-testid="stMetricLabel"],
    section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 11px;
        border: 1px solid #087E8B;
        background: #087E8B;
        color: #FFFFFF !important;
        font-weight: 700;
        min-height: 42px;
        transition: .18s ease;
    }

    .stButton > button:hover {
        background: #075B66;
        border-color: #075B66;
        box-shadow: 0 5px 14px rgba(8,126,139,.18);
        transform: translateY(-1px);
    }

    section[data-testid="stSidebar"] .stButton > button {
        background: #20A39E;
        border-color: #20A39E;
        color: #082F36 !important;
    }

    /* Chat */
    [data-testid="stChatMessage"] {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 16px 18px;
        box-shadow: 0 4px 15px rgba(23,43,58,.035);
        margin-bottom: 12px;
    }

    [data-testid="stChatInput"] {
        background: #FFFFFF;
        border: 1px solid #C9DADD;
        border-radius: 15px;
        box-shadow: 0 7px 22px rgba(23,43,58,.06);
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: var(--teal);
        box-shadow: 0 0 0 2px rgba(8,126,139,.10);
    }

    [data-testid="stChatInput"] textarea {
        color: var(--ink) !important;
    }

    [data-testid="stExpander"] {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 12px;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    .admin-note {
        background: rgba(255,255,255,.07);
        border: 1px solid rgba(255,255,255,.12);
        border-radius: 12px;
        padding: 13px;
        margin-top: 18px;
        color: #C9DDDF;
        font-size: 11px;
        line-height: 1.65;
    }

    .footer {
        border-top: 1px solid var(--line);
        margin-top: 42px;
        padding: 22px 8px 5px;
        text-align: center;
        color: var(--muted);
        font-size: 12px;
        line-height: 1.7;
    }

    .footer strong {
        color: var(--ink);
        font-size: 14px;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 1rem 2rem;
        }
        .hero {
            padding: 26px 23px;
            border-radius: 17px;
        }
        .feature-card {
            margin-bottom: 8px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# HERO / WELCOME
# ------------------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <span class="hero-kicker">🎓 Official admission helpdesk</span>
        <h1>Welcome to Indala College</h1>
        <p>
            Your digital guide to the admission journey. Ask questions about
            programmes, eligibility, fees, admission procedures and required
            documents using information from official college resources.
        </p>
        <div class="hero-meta">
            ✦ AI-POWERED SUPPORT &nbsp;&nbsp; • &nbsp;&nbsp;
            OFFICIAL DOCUMENT KNOWLEDGE &nbsp;&nbsp; • &nbsp;&nbsp;
            STUDENT-FIRST GUIDANCE
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# FEATURE OVERVIEW
# ------------------------------------------------------------

feature_columns = st.columns(3)
features = [
    ("📚", "Academic programmes", "Explore courses and programme information."),
    ("🧭", "Admission process", "Understand the steps involved in applying."),
    ("📄", "Eligibility & documents", "Check requirements from college documents."),
]

for column, (icon, title, description) in zip(feature_columns, features):
    with column:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")


# ------------------------------------------------------------
# ADMIN SIDEBAR
# ------------------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div style="padding:8px 0 15px;">
            <div style="font-size:30px;">🎓</div>
            <h2 style="font-size:21px; margin:4px 0 0;">Indala College</h2>
            <p style="font-size:11px; margin-top:4px;">
                ADMISSION ASSISTANT · ADMIN PANEL
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("### 📂 Document centre")
    st.caption(
        "Upload official college PDF documents and add them to the "
        "assistant's knowledge base."
    )

    uploaded_files = st.file_uploader(
        "Select PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help="You can select more than one PDF.",
    )

    if st.button("Save uploaded PDFs", use_container_width=True):
        if not uploaded_files:
            st.warning("Please select at least one PDF file.")
        else:
            try:
                saved = save_uploaded_files(uploaded_files)
                st.success(f"{len(saved)} PDF file(s) saved.")
                for filename in saved:
                    st.caption(f"✓ {filename}")
            except Exception as exc:
                st.error(f"Could not save files: {exc}")

    if st.button("Process knowledge base", use_container_width=True):
        try:
            with st.spinner("Reading and indexing documents..."):
                result = ingest_documents()

            st.success(
                f"Processing complete — {result.get('stored_chunks', 0)} "
                "text chunks stored."
            )

            skipped = result.get("skipped_files", [])
            if skipped:
                st.warning(
                    "No selectable text found in: "
                    + ", ".join(skipped)
                    + ". These PDFs may require OCR."
                )
        except Exception as exc:
            st.error(f"Document processing failed: {exc}")

    st.divider()
    st.markdown("### 📊 Knowledge base")

    try:
        chunk_count = get_collection().count()
        st.metric("Indexed text chunks", chunk_count)
        st.caption("Knowledge base connection available")
    except Exception:
        st.metric("Indexed text chunks", "—")
        st.caption("Knowledge base connection unavailable")

    st.markdown(
        """
        <div class="admin-note">
            <strong>🔐 Administrator note</strong><br>
            Upload only official college documents that the institution is
            authorized to share. Re-process the knowledge base after adding
            or replacing documents.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# CHAT ASSISTANT
# ------------------------------------------------------------

st.markdown('<div class="section-eyebrow">Student helpdesk</div>', unsafe_allow_html=True)
st.markdown("## Ask your admission question")
st.markdown(
    '<div class="section-subtitle">Answers are generated from the available '
    'Indala College documents. Check the cited source pages for details.</div>',
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

top_left, top_right = st.columns([5, 1])
with top_left:
    st.caption("💬 Your conversation")
with top_right:
    if st.button("＋ New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Suggested prompts are displayed only before the first question.
if not st.session_state.messages:
    st.markdown("**Not sure where to begin? Try one of these:**")
    prompt_columns = st.columns(3)
    suggested_questions = [
        "What courses are available?",
        "What documents are required for admission?",
        "Explain the admission procedure.",
    ]

    for column, prompt in zip(prompt_columns, suggested_questions):
        with column:
            if st.button(prompt, use_container_width=True, key=f"prompt_{prompt}"):
                st.session_state.pending_question = prompt
                st.rerun()

# Render conversation history.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("sources"):
            with st.expander("📎 View source documents"):
                for source in message["sources"]:
                    st.markdown(
                        f"**{source['source']}**  ·  Page {source['page']}"
                    )

question = st.chat_input("Type your question about admissions...")

# A suggested prompt is handled in the same way as typed input.
if not question and st.session_state.get("pending_question"):
    question = st.session_state.pop("pending_question")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching official college documents..."):
                matches = retrieve_context(question, top_k=TOP_K)

            relevant_matches = [
                item
                for item in matches
                if item.get("distance", float("inf")) <= MAX_DISTANCE
            ]

            if not relevant_matches:
                answer = UNAVAILABLE
                sources = []
            else:
                with st.spinner("Preparing your answer..."):
                    answer = generate_answer(question, relevant_matches)

                sources = []
                seen_sources = set()

                for item in relevant_matches:
                    source_key = (
                        item.get("source", "College document"),
                        item.get("page", "N/A"),
                    )
                    if source_key not in seen_sources:
                        seen_sources.add(source_key)
                        sources.append(
                            {
                                "source": source_key[0],
                                "page": source_key[1],
                            }
                        )

            st.markdown(answer)

            if sources:
                with st.expander("📎 View source documents"):
                    for source in sources:
                        st.markdown(
                            f"**{source['source']}**  ·  Page {source['page']}"
                        )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                }
            )

        except Exception as exc:
            error_message = f"Unable to generate an answer: {exc}"
            st.error(error_message)
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "sources": [],
                }
            )


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        <div style="font-size:24px;">🎓</div>
        <strong>Indala College</strong><br>
        AI-Powered Admission Assistance System<br>
        For official confirmation of admission details, please contact the
        Indala College Admission Office.<br>
        <span style="font-size:11px;">© Indala College · Powered by AI & RAG Technology</span>
    </div>
    """,
    unsafe_allow_html=True,
)
