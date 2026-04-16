# 🔗 Asynchronous URL Shortener Microservice

A high-performance microservice designed to shorten URLs, built with a modern Python stack: **FastAPI**, **SQLAlchemy 2.0**, and **PostgreSQL**.

---

## ✨ Key Features & Technical Solutions

*   **Fully Asynchronous:** Built on top of `FastAPI`, `SQLAlchemy` (async mode), and `asyncpg` to ensure high throughput and non-blocking I/O operations.
*   **Atomic Counters:** To prevent **Race Condition** issues during analytics updates, the service utilizes a raw SQL query (`UPDATE links SET visit_counts = visit_counts + 1 ...`). This ensures 100% data accuracy under heavy concurrent load.
*   **Collision-Resistant ID Generation:** Uses the `shortuuid` library with an integrated database check to guarantee unique identifiers for every link.
*   **Dockerized Environment:** Fully containerized with Docker and Docker Compose for seamless deployment and consistent testing.
*   **Makefile Automation:** Includes a comprehensive `Makefile` to streamline routine development tasks.

---

## 🛠 Tech Stack

*   **Language:** Python 3.12+
*   **Framework:** FastAPI
*   **Database:** PostgreSQL 15
*   **ORM:** SQLAlchemy 2.0 (Async)
*   **Migrations:** Alembic
*   **Testing:** Pytest
*   **Infrastructure:** Docker / Docker Compose / Makefile

---

## 🚀 Quick Start (Docker)

This is the recommended way to evaluate the service.

### 1. Clone the Repository
```bash
git clone https://github.com/YesCodeUser/url-shortener.git
cd url-shortener
```

### 2.  **Create a .env.docker file in the root directory and add the following configuration:**
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=url_shortener
```

### 3.  **Launch the Service:**
```bash
make up
```

### 4.  **Apply Migrations:**
```bash
make migrate
```

*API URL:* **http://localhost:8000**  
*Interactive Documentation (Swagger):* **http://localhost:8000/docs**

---

## 🧪 Testing & Linting

All checks are executed inside the container via the `Makefile`:

*   **Run Automated Tests:** 
    ```bash
    make test
    ```
    *Note: The test suite implements transactional isolation. Each test executes within its own transaction and automatically rolls back changes to ensure a clean database state.*
    

*    **Local Formatting & Linting:**
```bash
black .
ruff check .
   ```

---

## 🛠 Local Development Setup

Required for IDE autocomplete and local linting tools.

1.  **Create and Activate venv:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    .venv\Scripts\activate     # Windows
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🛰 API Endpoints

| Method | Endpoint | Description |
|-------|----------|----------|
| **POST** | `/shorten` | Accepts a long URL and returns a unique `short_id`. |
| **GET** | `/{short_id}` | Redirects (307) to the original URL and increments the visit counter. |
| **GET** | `/stats/{short_id}` | Retrieves the current statistics for a specific ID. |


