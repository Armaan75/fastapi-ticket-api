# 🎫 FastAPI Ticket API

A **production-style backend API** for managing support tickets.

Built using **FastAPI, SQLAlchemy, and Python**, this project demonstrates clean backend architecture including authentication, pagination, filtering, automated testing, and CI.

This project is designed as a **backend portfolio project** that showcases best practices used in real backend systems.

---

# 🚀 Features

✅ User authentication  
✅ Token-based authorization  
✅ Ticket CRUD operations  
✅ Ticket ownership protection  
✅ Pagination support  
✅ Filtering by priority and status  
✅ Search functionality  
✅ Sorting support  
✅ Automated tests with Pytest  
✅ Continuous Integration with GitHub Actions  
✅ Environment-based configuration  

---

# 🛠 Tech Stack

### Backend

🐍 Python  
⚡ FastAPI  
🗄 SQLAlchemy  

### Validation

📦 Pydantic  

### Testing

🧪 Pytest  

### DevOps

🔁 GitHub Actions (CI)

---

# 📂 Project Structure


app/
├── core/
│ └── config.py
│
├── routers/
│ └── tickets.py
│
├── services/
│ └── tickets_service.py
│
├── auth.py
├── db.py
├── main.py
├── models.py
└── schemas.py

tests/


This structure separates responsibilities clearly:

- **Routers** → HTTP endpoints  
- **Services** → business logic  
- **Models** → database structure  
- **Schemas** → request/response validation  

This mirrors real production backend architecture.

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Armaan75/fastapi-ticket-api.git

Navigate into the project

cd fastapi-ticket-api

Install dependencies

pip install -r requirements.txt

Run the development server

uvicorn app.main:app --reload
📖 API Documentation

Once the server is running, open:

http://127.0.0.1:8000/docs

FastAPI automatically provides an interactive Swagger UI where you can test all endpoints.

🧪 Running Tests

Run the full test suite:

pytest

Tests cover:

ticket pagination

ticket filtering

search functionality

sorting validation

📌 Example Endpoint

Get tickets with pagination:

GET /tickets?skip=0&limit=5

Example response:

{
  "items": [
    {
      "id": 1,
      "title": "Bug: login issue",
      "priority": "high",
      "status": "open"
    }
  ],
  "limit": 5,
  "skip": 0,
  "total": 10
}
🔐 Security

This API implements:

token-based authentication

ticket ownership protection

restricted access to user resources

Users can only view and modify their own tickets.

🔁 Continuous Integration

GitHub Actions automatically runs:

pytest

on every push to ensure the application remains stable.

📈 Future Improvements

Possible extensions for this project:

👥 Team / organization ticket support

🔑 Role-based permissions

📧 Email notifications

📊 Ticket analytics

🐳 Docker containerization

🌐 Frontend dashboard