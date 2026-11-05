
# --------------------------------------------------
# MODERN STREAMLIT USER INTERFACE
# --------------------------------------------------

st.markdown("""
<style>

/* Import fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #F6F7FC;
    color: #1E1B4B;
}

/* Remove default header */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Main container */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Headings */
h1, h2, h3 {
    color: #1E1B4B !important;
    font-weight: 800 !important;
    letter-spacing: -0.7px;
}

/* Hero section */
.hero {
    background: linear-gradient(
        120deg,
        #312E81,
        #5B21B6,
        #7C3AED
    );
    padding: 38px;
    border-radius: 24px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 12px 35px rgba(91, 33, 182, 0.20);
}

.hero h1 {
    color: white !important;
    font-size: 35px !important;
    margin-bottom: 8px;
}

.hero p {
    color: #EDE9FE !important;
    font-size: 15px;
    line-height: 1.7;
}

.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.16);
    border: 1px solid rgba(255,255,255,0.25);
    color: white;
    padding: 7px 14px;
    border-radius: 30px;
    font-size: 12px;
    margin-bottom: 15px;
}

/* Feature cards */
.feature-card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #E9E5F5;
    box-shadow: 0 4px 16px rgba(30, 27, 75, 0.04);
    min-height: 115px;
}

.feature-icon {
    font-size: 25px;
    margin-bottom: 9px;
}

.feature-title {
    font-weight: 700;
    color: #312E81;
    font-size: 14px;
}

.feature-desc {
    font-size: 12px;
    color: #77748F;
    margin-top: 5px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #1E1B4B,
        #312E81
    );
}

[data-testid="stSidebar"] * {
    color: white;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* Sidebar divider */
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.2);
}

/* Sidebar uploader */
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.10);
    border: 1px dashed #A78BFA;
    border-radius: 14px;
    padding: 10px;
}

[data-testid="stSidebar"] [data-testid="stFileUploader"] * {
    color: white !important;
}

/* Sidebar metric */
[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: rgba(255,255,255,0.10);
    padding: 15px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.16);
}

[data-testid="stSidebar"] [data-testid="stMetricLabel"],
[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    color: white !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(
        110deg,
        #6D28D9,
        #7C3AED
    );
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 11px 18px;
    font-weight: 600;
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(109,40,217,0.16);
}

.stButton > button:hover {
    background: #4C1D95;
    transform: translateY(-2px);
    box-shadow: 0 7px 18px rgba(109,40,217,0.25);
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: white;
    border: 1px solid #E9E5F5;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 15px;
    box-shadow: 0 4px 14px rgba(30,27,75,0.04);
}

/* Chat input */
[data-testid="stChatInput"] {
    background: white;
    border: 2px solid #DDD6FE;
    border-radius: 18px;
    box-shadow: 0 5px 20px rgba(91,33,182,0.07);
}

[data-testid="stChatInput"]:focus-within {
    border-color: #7C3AED;
}

[data-testid="stChatInput"] textarea {
    color: #1E1B4B !important;
}

/* Expanders */
[data-testid="stExpander"] {
    border: 1px solid #E9E5F5;
    border-radius: 14px;
    background: white;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Captions */
.stCaption {
    color: #77748F;
}

/* Footer */
.footer {
    text-align: center;
    padding: 20px;
    margin-top: 40px;
    color: #77748F;
    font-size: 12px;
    border-top: 1px solid #E9E5F5;
}

/* Mobile */
@media(max-width: 768px) {
    .hero {
        padding: 25px;
    }

    .hero h1 {
        font-size: 27px !important;
    }

    .block-container {
        padding: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown("""
<div class="hero">

    <div class="hero-tag">
        🎓 OFFICIAL ADMISSION ASSISTANT
    </div>

    <h1>Welcome to Indala College</h1>

    <p>
        Your intelligent admission companion.
        Get instant answers about courses, eligibility,
        fees, admission procedures and required documents.
    </p>

    <div style="
        margin-top:20px;
        font-size:13px;
        color:#DDD6FE;
    ">
        ✨ Powered by AI &nbsp; | &nbsp;
        📚 Official College Documents &nbsp; | &nbsp;
        🤝 Student Support
    </div>

</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# FEATURE CARDS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📚</div>
        <div class="feature-title">Courses</div>
        <div class="feature-desc">
            Explore available academic programmes.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📝</div>
        <div class="feature-title">Admissions</div>
        <div class="feature-desc">
            Understand admission procedures.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📋</div>
        <div class="feature-title">Requirements</div>
        <div class="feature-desc">
            Find eligibility and document details.
        </div>
    </div>
    """, unsafe_allow_html=True)


st.write("")
st.write("")


# --------------------------------------------------
# SIDEBAR - ADMINISTRATION
# --------------------------------------------------

with st.sidebar:

    st.markdown("""
    <div style="padding:10px 0 20px 0;">

        <div style="font-size:32px;">🎓</div>

        <h2 style="
            color:white;
            margin-bottom:0;
            font-size:22px;
        ">
            Indala College
        </h2>

        <p style="
            color:#C4B5FD;
            font-size:12px;
        ">
            Admission Assistant Dashboard
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 📂 Document Management")

    st.caption(
        "Upload official college PDF files "
        "and add them to the knowledge base."
    )

    uploaded_files = st.file_uploader(
        "Choose PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button(
        "💾 Save Uploaded PDFs",
        use_container_width=True
    ):

        if not uploaded_files:
            st.warning("Please select at least one PDF.")

        else:
            saved = save_uploaded_files(uploaded_files)

            st.success(
                f"{len(saved)} PDF file(s) saved successfully."
            )

    st.write("")

    if st.button(
        "⚡ Process Documents",
        type="primary",
        use_container_width=True
    ):

        try:

            with st.spinner("Processing documents..."):

                result = ingest_documents()

            st.success(
                f"Successfully processed "
                f"{result['stored_chunks']} chunks."
            )

            if result["skipped_files"]:

                st.warning(
                    "No selectable text found in: "
                    + ", ".join(result["skipped_files"])
                    + ". OCR may be required."
                )

        except Exception as exc:

            st.error(f"Processing failed: {exc}")

    st.divider()

    st.markdown("### 📊 Knowledge Base")

    try:

        count = get_collection().count()

        st.metric(
            "Stored Text Chunks",
            count,
            delta="Connected"
        )

    except Exception:

        st.metric("Stored Text Chunks", 0)

    st.markdown("""
    <div style="
        background:rgba(255,255,255,0.08);
        border-radius:12px;
        padding:14px;
        margin-top:20px;
        font-size:12px;
        color:#DDD6FE;
        line-height:1.7;
    ">
        🔒 <b>Admin Notice</b><br>
        Only upload official documents
        that the college is authorized to share.
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# CHAT SECTION
# --------------------------------------------------

st.markdown("""
<h2 style="font-size:25px;">
    💬 Ask Your Admission Questions
</h2>

<p style="color:#77748F; font-size:14px;">
    Chat with our AI assistant to get information
    from official Indala College documents.
</p>
""", unsafe_allow_html=True)


# Initialize chat history

if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message.get("sources"):

            with st.expander("📄 View source documents"):

                for source in message["sources"]:

                    st.write(
                        f"📘 **{source['source']}** "
                        f"— Page {source['page']}"
                    )


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

question = st.chat_input(
    "Ask anything about admissions..."
)


if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.chat_message("assistant"):

        try:

            with st.spinner(
                "🔍 Searching official college documents..."
            ):

                matches = retrieve_context(
                    question,
                    top_k=TOP_K
                )

            relevant_matches = [
                item
                for item in matches
                if item["distance"] <= MAX_DISTANCE
            ]

            if not relevant_matches:

                answer = UNAVAILABLE
                sources = []

            else:

                with st.spinner(
                    "🤖 Preparing your answer..."
                ):

                    answer = generate_answer(
                        question,
                        relevant_matches
                    )

                unique_sources = []
                seen = set()

                for item in relevant_matches:

                    key = (
                        item["source"],
                        item["page"]
                    )

                    if key not in seen:

                        seen.add(key)

                        unique_sources.append({
                            "source": item["source"],
                            "page": item["page"]
                        })

                sources = unique_sources

            st.markdown(answer)

            if sources:

                with st.expander("📄 View source documents"):

                    for source in sources:

                        st.write(
                            f"📘 **{source['source']}** "
                            f"— Page {source['page']}"
                        )

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })

        except Exception as exc:

            error_message = (
                f"Unable to generate an answer: {exc}"
            )

            st.error(error_message)

            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message,
                "sources": []
            })


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">

    <div style="font-size:22px;">🎓</div>

    <b style="color:#312E81;">
        Indala College
    </b>

    <p>
        AI-Powered Admission Assistance System
    </p>

    <p>
        For official confirmation of admission details,
        please contact the Indala College Admission Office.
    </p>

    <p style="font-size:11px;">
        © Indala College | Powered by AI & RAG Technology
    </p>

</div>
""", unsafe_allow_html=True)
