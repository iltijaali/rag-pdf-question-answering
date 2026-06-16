# ==================================================
# STEP 1: IMPORT LIBRARIES
# ==================================================

from langchain_chroma import Chroma
import warnings
from langchain_huggingface import HuggingFaceEmbeddings


warnings.filterwarnings("ignore")


# ==================================================
# STEP 1.1: SET NOT FOUND SETTINGS
# ==================================================

NOT_FOUND_SCORE = 1.45
CHUNKS_TO_PRINT = 1

FIELD_KEYWORDS = {
    "ceo": ["ceo", "chief executive"],
    "price": ["price", "pricing", "cost"],
    "revenue": ["revenue"],
    "percentage": ["percentage", "percent", "%"],
    "share price": ["share price", "stock price", "closing price"],
}


# ==================================================
# STEP 2: LOAD SAME EMBEDDING MODEL
# ==================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ==================================================
# STEP 3: CONNECT TO CHROMADB
# ==================================================

db = Chroma(
    persist_directory="db",
    embedding_function=embeddings
)


# ==================================================
# STEP 4: TAKE USER QUESTION
# ==================================================

question = input("\nAsk Question From PDF: ")


# ==================================================
# STEP 5: SEARCH MOST RELEVANT CHUNKS
# ==================================================

results = db.similarity_search_with_score(
    question,
    k=3
)


# ==================================================
# STEP 6: CHECK IF DATA EXISTS OR NOT
# ==================================================

if not results:

    print("\nData you search is not found in documents.")

    exit()


best_score = results[0][1]

all_context = " ".join(
    doc.page_content.lower()
    for doc, score in results
)

question_lower = question.lower()

for field, keywords in FIELD_KEYWORDS.items():

    if field in question_lower:

        field_found = any(keyword in all_context for keyword in keywords)

        if not field_found:

            print("\nData you search is not found in documents.")

            exit()


if best_score > NOT_FOUND_SCORE:

    print("\nData you search is not found in documents.")

    exit()


# ==================================================
# STEP 7: PRINT RETRIEVED CHUNKS
# ==================================================

print("\nMost Relevant Chunks Found:\n")

for index, result in enumerate(results[:CHUNKS_TO_PRINT], start=1):

    doc = result[0]

    print("=" * 60)

    print(f"\nChunk #{index}\n")

    print(doc.page_content)

    print("\n")
