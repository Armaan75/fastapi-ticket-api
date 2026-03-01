import pytest


def _auth_header(token: str) -> dict:
    # Your auth uses HTTPBearer and reads creds.credentials,
    # so you must send Authorization: Bearer <token>
    return {"Authorization": f"Bearer {token}"}


def _register_and_login(client, email="listtester@example.com", password="Password123!"):
    # Create user
    r = client.post(
        "/users",
        json={"email": email, "full_name": "List Tester", "password": password},
    )
    # If user already exists, it might return 400; that's fine for tests
    assert r.status_code in (200, 201, 400), r.text

    # Login (your system likely returns auth_token)
    r = client.post("/users/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    data = r.json()

    # Your code stores User.auth_token, so most likely login returns "auth_token"
    token = data.get("auth_token") or data.get("token") or data.get("access_token")
    assert token, f"Login response missing token. Got: {data}"
    return token

    # Login
    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    data = r.json()

    # Support both shapes:
    #   {"access_token": "...", "token_type": "bearer"}
    #   {"token": "..."}
    token = data.get("access_token") or data.get("token") or data.get("auth_token")
    assert token, f"Login response missing token. Got: {data}"
    return token


def _create_ticket(client, headers, title, description=None, priority="medium"):
    r = client.post(
        "/tickets",
        headers=headers,
        json={"title": title, "description": description, "priority": priority},
    )
    assert r.status_code in (200, 201), r.text
    return r.json()


def test_ticket_list_pagination_shape(client):
    token = _register_and_login(client)
    headers = _auth_header(token)

    _create_ticket(client, headers, "Bug: login issue", "Cannot login sometimes", "high")
    _create_ticket(client, headers, "Feature: export CSV", "Need export", "low")

    r = client.get("/tickets?skip=0&limit=1", headers=headers)
    assert r.status_code == 200, r.text
    data = r.json()

    assert set(data.keys()) == {"items", "limit", "skip", "total"}
    assert data["skip"] == 0
    assert data["limit"] == 1
    assert data["total"] >= 2
    assert len(data["items"]) == 1


def test_ticket_list_filter_priority(client):
    token = _register_and_login(client, email="prio@example.com")
    headers = _auth_header(token)

    _create_ticket(client, headers, "High priority ticket", "Urgent", "high")
    _create_ticket(client, headers, "Low priority ticket", "Not urgent", "low")

    r = client.get("/tickets?priority=high", headers=headers)
    assert r.status_code == 200, r.text
    data = r.json()

    assert data["total"] >= 1
    assert all(item["priority"] == "high" for item in data["items"])


def test_ticket_list_search_q(client):
    token = _register_and_login(client, email="search@example.com")
    headers = _auth_header(token)

    _create_ticket(client, headers, "Add export", "export CSV feature", "medium")
    _create_ticket(client, headers, "Random", "nothing to see", "medium")

    r = client.get("/tickets?q=export", headers=headers)
    assert r.status_code == 200, r.text
    data = r.json()

    assert data["total"] >= 1
    assert any("export" in (item["title"].lower() + " " + (item["description"] or "").lower()) for item in data["items"])


def test_ticket_list_invalid_sort_returns_400(client):
    token = _register_and_login(client, email="sort@example.com")
    headers = _auth_header(token)

    r = client.get("/tickets?sort=-not_a_field", headers=headers)
    assert r.status_code == 400, r.text