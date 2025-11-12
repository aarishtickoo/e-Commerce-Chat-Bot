from mpmath.libmp.libintmath import small_trailing
from semantic_router import Route
from semantic_router.index import LocalIndex
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.routers import SemanticRouter

encoder = HuggingFaceEncoder(
    model="sentence-transformers/all-MiniLM-L6-v2"
)

# index = LocalIndex(
#     path="semantic_index_data",   # folder where index + config get stored
#     overwrite=True,               # recreate each run (or False to reuse)
# )

faq = Route(
    name="faq",
    utterances=[
        "What is the return of the products?",
        "Do I get discount with HDFC Credit Card",
        "How can I track my order",
        "What payment methods are accepted?",
        "How long does it take to process a refund?",
        # # add these
        # "How do I return a defective product?",
        # "I received a damaged item — what do I do?",
        # "What is your refund policy for broken products?",
        # "How do I report a defective product?"
    ]
)

sql = Route(
    name="sql",
    utterances=[
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of Adidas running shoes?",
    ]
)

small_talk = Route(
    name="small_talk",
    utterances=[
        "Hi",
        "Hello",
        "Hey",
        "How are you?",
        "What is your name?",
        "Who are you?",
        "What do you do?",
    ]
)

router = SemanticRouter(
    routes=[faq, sql,small_talk],
    encoder=encoder,
    auto_sync="local",
    # index=index
)

router.set_threshold(0.1)
# A threshold of 0.0 means “always return the best match no matter how low the score”; something like 0.2 is a gentler choice

if __name__ == "__main__":
    print(router("What is your policy on defective product?").name)
    print(router("Pink Puma shoes in price range of 500 and 1000").name)
    print(router("Hi what can you do for me today").name)
    print(router("Who is the president of India").name)