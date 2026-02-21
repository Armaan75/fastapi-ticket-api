# 🚀 FastAPI Ticket API

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-success)
![Status](https://img.shields.io/badge/Project-Active-brightgreen)

A production-style REST API built with **FastAPI**, designed to simulate a real-world ticket management backend.

This project demonstrates:

- Clean API architecture  
- JWT authentication  
- Filtering, pagination & sorting  
- Professional Git workflow (feature branches + PRs)  
- CI integration with GitHub Actions  

---

## 📌 Project Overview

The **FastAPI Ticket API** allows authenticated users to create and manage support tickets.

It follows production-style backend principles:

- Layered architecture  
- Dependency injection  
- Ownership validation  
- Structured API responses  
- Feature-branch workflow with CI checks  

This project is being built incrementally using production practices.

---

## 🧱 Tech Stack

- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **JWT Authentication**
- **SQLite** (PostgreSQL-ready)
- **Uvicorn**
- **GitHub Actions (CI/CD)**

---

## 🔐 Authentication

- JWT-based login
- Protected endpoints using FastAPI dependencies
- Ticket ownership validation for update/delete operations

---

## 🎟 Ticket API Features

### CRUD Operations

- Create Ticket  
- Retrieve Single Ticket  
- Update Ticket  
- Delete Ticket  

### Pagination

GET /tickets?limit=10&offset=0

### Sorting

GET /tickets?sort=-created_at
GET /tickets?sort=priority

### Filtering

GET /tickets?status=open
GET /tickets?priority=high
GET /tickets?user_id=1

### Search

GET /tickets?q=bug

### Combined Example

GET /tickets?status=open&priority=high&q=login&limit=5&offset=0&sort=-id


### Structured Response Format

```json
{
  "items": [...],
  "limit": 5,
  "offset": 0,
  "total": 12
}

🗂 Project Structure

fastapi-ticket-api/
│
├── app/
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── tickets.py
│   └── services/
│       └── tickets_service.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── tests/
├── requirements.txt
└── README.md

▶️ Running Locally

git clone https://github.com/YOUR_USERNAME/fastapi-ticket-api.git
cd fastapi-ticket-api

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt

uvicorn app.main:app --reload


Open Swagger UI:

http://127.0.0.1:8000/docs


🧪 Continuous Integration

This project uses GitHub Actions to:

- Run automated checks
- Validate builds
- Protect the main branch
- Enforce PR-based merges

All features are developed using:

1. Feature branches
2. Pull Requests
3. CI validation before merge

🔮 Planned Improvements

- Role-based permissions (Admin vs User)
- Docker containerisation
- Alembic database migrations
- Expanded automated test coverage
- Production deployment