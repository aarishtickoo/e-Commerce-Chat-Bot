import os
import pandas as pd
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os, sys



# Get current file path
faqs_path = Path(__file__).parent / "resources" / "ecommerce_faq_100.csv"
chroma_client = chromadb.Client()
collection_name_faq = "faqs"
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ingest_faq_data(path):
    if collection_name_faq not in [c.name for c in chroma_client.list_collections()]:
        print (f"Collection does not exist. Creating collection {collection_name_faq}")
        collection = chroma_client.get_or_create_collection(
            name = collection_name_faq,
            embedding_function=ef)



        df = pd.read_csv(path)
        docs = df["question"].to_list()
        metadata = [{"answer" : ans} for ans in df["answer"].to_list()]
        ids = [f"id_{i}" for i in range(len(docs))]

        collection.add(
         documents=docs,
         metadatas=metadata,
         ids=ids
        )
        print (f"FAQ data succesfully ingested into Chroma collection: {collection_name_faq}")
    else:
        print (f"Collection {collection_name_faq} already exists.")

def get_relevant_qa(query):
    collection = chroma_client.get_collection(collection_name_faq)
    result = collection.query(
        query_texts=[query],
        n_results=2
    )

    return result

def faq_chain(query):
    result = get_relevant_qa(query)

    # context = ''.join([r.get_answer() for r in result["metadatas"][0] ])
    # join all metadata answers for the first query result into a single context string
    meta_list = result.get("metadatas", [[]])[0]  # protects if key missing
    context = " ".join([m.get("answer", "") for m in meta_list if isinstance(m, dict)])

    answer = generate_answer(query,context)
    return answer

def generate_answer(query, context):

    prompt = f'''
    Given the question and context below, generate the answer based on the context only.
    If you don't find the answer inside the context then say "I don't know".
    Do not make things up.

    QUESTION: {query},
    CONTEXT: {context}
    '''

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role" : "system",
                "content" : prompt
            },

        ],
        model = os.environ["GROQ_MODEL"]
    )

    response = chat_completion.choices[0].message
    return response.get("content") if isinstance(response, dict) else getattr(response, "content", str(response))


if __name__ == '__main__':
    print ("__main__ started here")
    ingest_faq_data(faqs_path)
    query = "“Is EMI available on all items or just on select products above a certain price?”"
    # result = get_relevant_qa(query)
    # print (result)
    answer = faq_chain(query)
    print (answer)


# 5 slightly complex user questions a RAG chatbot should handle using this dataset
#
# These go beyond simple one-liners, requiring semantic understanding + retrieval from the FAQ dataset:
#
# “I returned my product a week ago but haven’t got my money back yet. How long does it usually take for refunds to process?”
# → Should retrieve info: “Refunds are processed within 5–7 business days after the return is received.”
#
# “Is EMI available on all items or just on select products above a certain price?”
# → Should combine understanding of EMI availability and minimum order value (₹3,000).
#
# “I used a promo code and a gift card together, but only one discount applied — is that expected?”
# → Should recall: “Only one promo code or gift card can be used per transaction.”
#
# “I missed my delivery because I wasn’t home. What should I do to get it redelivered?”
# → Should find: “Our delivery partner will attempt delivery again or contact you to reschedule.”
#
# “I’m ordering from outside India — can I still get cash on delivery or international shipping?”
# → Should combine: “Cash on delivery is available on most domestic orders” + “International shipping is available to select countries.”