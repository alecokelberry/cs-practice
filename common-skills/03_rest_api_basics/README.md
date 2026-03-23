# 03 — REST API Basics

A REST API lets two programs talk over the web using HTTP. One program (the client) sends a **request**; the other (the server) sends back a **response**. This is how your frontend talks to a backend, and how services talk to each other.

---

## Mental Model

Think of a REST API like a restaurant:

- **Client** = you (the customer)
- **Server** = the kitchen
- **Endpoint (URL)** = the item on the menu
- **HTTP method** = what you're asking (order something new, modify your order, cancel it)
- **Request body** = the details you give (extra cheese, no onions)
- **Response** = what comes back from the kitchen (the food, or "sorry, we're out")

---

## HTTP Methods

The method tells the server *what you want to do* with the resource.

| Method | Meaning | Has Body | Idempotent? |
|--------|---------|----------|-------------|
| `GET` | Read a resource | No | Yes |
| `POST` | Create a new resource | Yes | No |
| `PUT` | Replace a resource entirely | Yes | Yes |
| `PATCH` | Update part of a resource | Yes | No |
| `DELETE` | Remove a resource | No | Yes |

**Idempotent** means calling it multiple times produces the same result. `DELETE /users/1` twice is the same as once (user is gone either way). `POST /users` twice creates two users.

---

## URLs and Endpoints

A well-designed REST URL describes a **resource**, not an action.

```
# Good — noun-based, hierarchical
GET    /users             → list all users
POST   /users             → create a user
GET    /users/42          → get user 42
PUT    /users/42          → replace user 42
PATCH  /users/42          → update fields of user 42
DELETE /users/42          → delete user 42

GET    /users/42/posts    → list posts belonging to user 42
GET    /users/42/posts/7  → get post 7 from user 42

# Bad — verb in URL (method already expresses the action)
POST   /createUser
GET    /getUser?id=42
POST   /deleteUser
```

**Query parameters** are for filtering, sorting, and pagination — not for identifying a resource:

```
GET /users?role=admin&sort=name&page=2&limit=20
GET /posts?tag=typescript&published=true
```

---

## HTTP Status Codes

The status code tells you whether the request succeeded — and why not if it failed.

### 2xx — Success

| Code | Meaning | When |
|------|---------|------|
| 200 OK | Request succeeded | GET, PUT, PATCH responses |
| 201 Created | Resource was created | POST that created something |
| 204 No Content | Succeeded, nothing to return | DELETE, sometimes PUT |

### 3xx — Redirect

| Code | Meaning | When |
|------|---------|------|
| 301 Moved Permanently | URL has permanently changed | |
| 302 Found | Temporary redirect | |
| 304 Not Modified | Cached version is still valid | Conditional GET |

### 4xx — Client Error (your fault)

| Code | Meaning | When |
|------|---------|------|
| 400 Bad Request | Invalid input | Missing field, bad JSON |
| 401 Unauthorized | Not authenticated | No token, expired token |
| 403 Forbidden | Authenticated but not allowed | Wrong role/permission |
| 404 Not Found | Resource doesn't exist | Wrong ID |
| 409 Conflict | Request conflicts with current state | Duplicate email |
| 422 Unprocessable Entity | Validation failed | Business rule violation |
| 429 Too Many Requests | Rate limit exceeded | |

### 5xx — Server Error (their fault)

| Code | Meaning | When |
|------|---------|------|
| 500 Internal Server Error | Something crashed | Bug in server code |
| 502 Bad Gateway | Upstream server failed | |
| 503 Service Unavailable | Server down or overloaded | |

**Key distinction:** 401 vs 403 — 401 means "I don't know who you are, please log in." 403 means "I know who you are, but you can't do this."

---

## HTTP Headers

Headers carry metadata — they're key-value pairs sent alongside the request or response.

### Common Request Headers

```
Content-Type: application/json       ← format of the request body
Accept: application/json             ← format you want in the response
Authorization: Bearer <token>        ← authentication
```

### Common Response Headers

```
Content-Type: application/json
Content-Length: 348
Cache-Control: max-age=3600
Location: /users/42                  ← sent with 201 to point to new resource
```

### Content-Type

```
application/json          → JSON body (most REST APIs)
application/x-www-form-urlencoded  → HTML form data
multipart/form-data       → file uploads
text/plain                → plain text
```

---

## JSON

REST APIs almost always exchange data as JSON.

```json
{
    "id": 42,
    "name": "Alec",
    "email": "alec@example.com",
    "role": "student",
    "tags": ["bscs", "wgu"],
    "address": {
        "city": "Denver",
        "state": "CO"
    }
}
```

Rules:
- Keys must be strings (in double quotes)
- Values can be: string, number, boolean, null, object, array
- No trailing commas
- No comments

---

## Making Requests with curl

`curl` is a command-line tool for sending HTTP requests. Useful for testing APIs without a browser.

```bash
# GET request
curl https://api.example.com/users

# GET with a header (authentication)
curl -H "Authorization: Bearer mytoken123" https://api.example.com/users/42

# POST with JSON body
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alec", "email": "alec@example.com"}'

# PUT (replace)
curl -X PUT https://api.example.com/users/42 \
  -H "Content-Type: application/json" \
  -d '{"name": "Alec Kelberry", "email": "alec@example.com"}'

# PATCH (partial update)
curl -X PATCH https://api.example.com/users/42 \
  -H "Content-Type: application/json" \
  -d '{"email": "new@example.com"}'

# DELETE
curl -X DELETE https://api.example.com/users/42

# Pretty-print JSON output (pipe to python)
curl https://api.example.com/users | python3 -m json.tool

# See response headers too
curl -i https://api.example.com/users

# Verbose (see request + response headers)
curl -v https://api.example.com/users
```

**Useful flags:**
| Flag | Meaning |
|------|---------|
| `-X METHOD` | Set HTTP method |
| `-H "key: val"` | Add a header |
| `-d 'body'` | Set request body |
| `-i` | Include response headers in output |
| `-v` | Verbose — show full request and response |
| `-o file` | Save response to a file |
| `-s` | Silent — suppress progress meter |

---

## Authentication

### API Keys

The simplest form. The server gives you a key; you send it with every request.

```bash
# In header (preferred)
curl -H "X-API-Key: abc123" https://api.example.com/data

# In query string (avoid — keys show up in server logs)
curl "https://api.example.com/data?api_key=abc123"
```

### Bearer Tokens (JWT)

Used with login-based APIs. You log in, get a token, include it as a `Bearer` token.

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR..." https://api.example.com/me
```

### Basic Auth

Base64-encode `username:password`. Not secure without HTTPS.

```bash
curl -u username:password https://api.example.com/me
# same as:
curl -H "Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=" https://api.example.com/me
```

---

## Request / Response Anatomy

### Full request example

```
POST /users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer abc123
Content-Length: 45

{"name": "Alec", "email": "alec@example.com"}
```

Breaking it down:
- Line 1: method + path + HTTP version
- Lines 2–5: headers
- Blank line: separates headers from body
- Last line: body

### Full response example

```
HTTP/1.1 201 Created
Content-Type: application/json
Location: /users/42
Content-Length: 72

{
    "id": 42,
    "name": "Alec",
    "email": "alec@example.com"
}
```

---

## REST Design Conventions

### Versioning

Include the API version in the URL so you can change the API without breaking existing clients:

```
/v1/users     ← current version
/v2/users     ← new version with breaking changes
```

### Pagination

Don't return all records at once. Standard approach:

```
GET /posts?page=2&limit=20

Response:
{
    "data": [...],
    "total": 143,
    "page": 2,
    "limit": 20,
    "next": "/posts?page=3&limit=20"
}
```

### Error responses

Always return a consistent error body:

```json
{
    "error": "ValidationError",
    "message": "Email is already in use",
    "field": "email"
}
```

### Naming conventions

- Use **plural nouns** for collections: `/users`, `/posts`, `/comments`
- Use **lowercase** with hyphens if needed: `/user-profiles` (not `/userProfiles`)
- Nest for ownership: `/users/42/posts` (posts belonging to user 42)
- Don't nest deeper than 2 levels — it gets unwieldy

---

## HTTP vs HTTPS

- **HTTP** — plaintext, visible to anyone on the network
- **HTTPS** — encrypted with TLS, safe for passwords, tokens, sensitive data

Always use HTTPS for anything with authentication. Never send API keys or tokens over HTTP.

---

## Common Pitfalls

**Using GET for mutations**
`GET /deleteUser?id=42` is wrong. GET requests may be cached, bookmarked, or prefetched by browsers. Use DELETE.

**Inconsistent status codes**
Returning `200 OK` for every response, even errors — then embedding the real status in the body. Don't do this. Use the actual HTTP status codes.

**Putting verbs in URLs**
`POST /createUser` should be `POST /users`. The HTTP method already expresses the action.

**Returning a 401 when you mean 403**
401 = not logged in. 403 = logged in but not permitted. They mean different things to the client.

**Not validating input**
Always validate on the server. A client sending bad data should get a 400 or 422 with a clear message — not a 500.

---

## Quick Reference

```
HTTP Methods
  GET     → read (no body)
  POST    → create (has body)
  PUT     → replace (has body, idempotent)
  PATCH   → partial update (has body)
  DELETE  → remove (no body, idempotent)

Status Codes
  200  OK               → success
  201  Created          → POST created something
  204  No Content       → success, no body (DELETE)
  400  Bad Request      → invalid input
  401  Unauthorized     → not logged in
  403  Forbidden        → logged in, but not allowed
  404  Not Found        → resource doesn't exist
  409  Conflict         → duplicate / state conflict
  422  Unprocessable    → validation failed
  500  Server Error     → bug on the server

URL Design
  GET    /users           → list
  POST   /users           → create
  GET    /users/42        → read one
  PUT    /users/42        → replace
  PATCH  /users/42        → partial update
  DELETE /users/42        → delete
  GET    /users/42/posts  → nested resource

curl cheat sheet
  curl URL                           → GET
  curl -X POST URL -d '{}' -H ...    → POST with JSON
  curl -H "Authorization: Bearer T"  → add auth header
  curl -i URL                        → include response headers
  curl -v URL                        → verbose (debug)
  curl URL | python3 -m json.tool    → pretty-print JSON

Headers
  Content-Type: application/json
  Authorization: Bearer <token>
  Accept: application/json
```
