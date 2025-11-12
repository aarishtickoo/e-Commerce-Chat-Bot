# e-commerce chatbot (Gen AI RAG project)

[//]: # (**Personal project — e-Commerce Chatbot &#40;Streamlit + RAG + Web Scraping&#41;**)

A end-to-end e-commerce question-answering chatbot built as a resume project.  
It demonstrates local retrieval (FAQ + SQL-backed product lookup), lightweight semantic routing, and a simple web-scraping pipeline to collect product data.

---

Folder structure
1. app: All the code for chatbot
2. web-scraping: Code to scrap e-commerce website 

This chatbot currently supports two intents:

- **faq**: Triggered when users ask questions related to the platform's policies or general information. eg. Is online payment available?
- **sql**: Activated when users request product listings or information based on real-time database queries. eg. Show me all nike shoes below Rs. 3000.

![product screenshot](app/resources/product-ss.png)

---

## Architecture
![architecture diagram of the e-commerce chatbot](app/resources/architecture-diagram.png)

---

## Highlights / Folder Structure / What this repo contains

- `app/` — All the code for chatbot i.e. streamlit front-end and core application code:
  - `main.py` — Streamlit app entry (chat UI + routing to handlers).
  - `router.py` — Semantic router configuration (uses `sentence-transformers` encoder).
  - `faq.py` — FAQ ingestion and FAQ retrieval / RAG utilities.
  - `sql.py` — Simple SQL-based product lookup logic (connects to `db.sqlite`).
  - `small_talk.py` — Small-talk / fallback responses module.
  - `resources/` — bundled assets and CSVs (FAQ CSVs, product screenshots, diagrams).
- `web-scraping/` — Code to scrap e-commerce website:
  - `flipkart_data_extraction.py` — Flipkart scraping logic (notebook + script versions).
  - `csv_to_sqlite.py` — Helper to import scraped CSV data into `db.sqlite`.
  - sample CSVs: `flipkart_product_data.csv`, `flipkart_product_links.csv`, etc.
- `requirements.txt` — Python packages used for the project.
- `.git/` — Git repository metadata (present in the uploaded archive).
- `app/db.sqlite` — Example SQLite database (populated from scrapes).

---

## Quick demo (local)

### 1) Clone / extract
If you already have this directory locally (from the upload), skip this step. Otherwise:
```bash
# if uploaded as a zip, extract it locally:
unzip e-Commerce-Chat-Bot.zip
cd e-Commerce-Chat-Bot
```

### 2) Create a Python virtualenv and install dependencies
```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate       # Windows PowerShell

pip install -r requirements.txt
```

> Note: The `requirements.txt` pins the packages used in the project. If you run into package issues, create a fresh environment and install the requirements.

### 3) Run the Streamlit app
```bash
cd app
streamlit run main.py
```

The app exposes a small chat UI. Type a question — the router will attempt to classify it as:
- **FAQ** — answers fetched from the FAQ CSV via a retrieval flow, or
- **SQL** — queries the `db.sqlite` product table for product-related questions, or
- **small-talk / fallback** — casual replies.

---

## How it works — architecture summary

1. **Routing**
   - `router.py` uses a sentence-transformer encoder (`all-MiniLM-L6-v2`) and a lightweight semantic router to decide whether a query should hit the FAQ retriever, the SQL product lookup, or small-talk fallback.
   - The reasoning and language generation are powered by Meta’s `llama-3.3-70b-versatile` model.
2. **FAQ retrieval / RAG**
   - `faq.py` ingests CSV FAQ data (`resources/faq_data.csv`) and exposes a `faq_chain` function to answer user FAQ queries via semantic retrieval (Chroma / embeddings-based).

3. **Product lookup (SQL)**
   - `sql.py` provides `sql_chain` to run templated SQL queries against `app/db.sqlite`. The `web-scraping/csv_to_sqlite.py` script helps convert scraped CSV tables into the `product` table that `sql.py` expects.

4. **Web scraping**
   - `web-scraping/flipkart_data_extraction.py` is a practical example of scraping product pages / search results and saving them into CSVs. Use responsibly and follow robots.txt / terms of service.



---

## Next improvements (ideas)

- Add unit tests for router + SQL chain.
- Dockerize the app for easy deployment.
- Add CI to run linting and tests on pushes.
- Replace local embedding/index with a managed vector DB or add persistent Chroma index directory.
- Improve the scraping resiliency and add polite rate-limiting and caching.

---

## License & attribution

This project is for personal / portfolio use.  
Licensed under the [MIT License](LICENSE) © 2025 Aarish Tickoo.

---



## Contact / Owner

Author: *Aarish Tickoo* (repo owner)  
E-mail: aarishtickootch@gmail.com