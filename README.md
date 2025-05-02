# UMedia API Documentation
<img src="um.png" alt="Unconsenting Media Logo" width="300">
This FastAPI-based API provides access to trigger-warning data for movies and TV shows sourced from UnconsentingMedia.org. It allows clients to fetch lists of titles, perform searches, and retrieve detailed trigger warnings and safety ratings for movies and TV shows.

---

### Base URL

- **Local Development:** `http://localhost:8000`
- **Production (example):** `https://your-deployed-url.com`

### Authentication

- **None required.** This is a public, read-only API.

---

## Endpoints

- GET `/`
- GET `/titles`
- GET `/titles/search`

### 1. GET `/`

**Description:** Health check endpoint. Confirms the API is running.

**Response:**

```json
{ "message": "UMedia API is running" }
```

---

### 2. GET `/titles`

**Description:** Returns a list of all movies and TV shows with their basic trigger-warning data and safety rating.

**Response Fields:**

| Field         | Type      | Description                                           |
|---------------|-----------|-------------------------------------------------------|
| `id`          | `int`     | Unique identifier from the source CSV                 |
| `name`        | `string`  | Title of the movie or TV show                         |
| `type`        | `string`  | Either `movie` or `TV Show`                           |
| `warnings`    | `string[]`| List of human-readable trigger warnings               |
| `safetyRating`| `string`  | Emoji: 🔴 red (high risk), 🟠 amber (moderate), 🟢 green (low) |

**Example Request:**

```bash
curl http://localhost:8000/titles
```

**Example Response:**

```json
[
  {
    "id": 973,
    "name": "The 100",
    "type": "TV Show",
    "warnings": ["Sexual harassment", "Adult-teen sexual relationship"],
    "safetyRating": "🟠"
  },
  {
    "id": 1202,
    "name": "Game of Thrones",
    "type": "TV Show",
    "warnings": ["Rape shown on-screen", "Sexual harassment"],
    "safetyRating": "🔴"
  }
]
```

---

### 3. GET `/titles/search`

**Description:** Search for a specific movie or TV show by title. Supports:
1. Case-insensitive match on the full title
2. match on a cleaned title (`cleanName`) if available
3. Fuzzy match (if exact fails)
4. Partial match fallback

**Query Parameters:**

| Parameter | Type     | Required | Description                                       |
|-----------|----------|----------|---------------------------------------------------|
| `q`(query)| `string` | yes      | Title to search for (enclose spaces with `%20`)   |

**Example Request:**

```bash
curl "http://localhost:8000/titles/search?q=The%20100"
```

**Example Response:**

```json
[
  {
    "id": 973,
    "name": "The 100",
    "type": "TV Show",
    "warnings": ["Sexual harassment", "Adult-teen sexual relationship"],
    "safetyRating": "🟠",
    "comment": [
      "An adult character has numerous sexual relationships with teenage girls.",
      "S1E6: sexual harassment (15:37-16:36).",
      "S1E9: it is revealed..."
    ]
  }
]
```

**Error Responses:**

- `404 Not Found` if no match:

```json
{ "error": "No matches found for 'Unknown Title'" }
```

---

### Error Handling

- **500 Internal Server Error:** Indicates a server-side problem (e.g., CSV missing or code bug).
- **404 or custom error JSON:** Returns `{ "error": "message" }` for not-found cases.

---

### Getting Started

1. **Clone the repo**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run locally**: `uvicorn main:app --reload`
4. **Open Swagger UI**: http://localhost:8000/docs

---

### License & Attribution

- Data source: [Unconsenting Media](https://www.unconsentingmedia.org)
  This code uses publicly available data from Unconsenting Media under their open data policy.
- API code: MIT License

---

Made by **Shaly** | GitHub: [@pandashaly](https://github.com/pandashaly)
<br>
<p align=center> <sub> Created with 🫀 and 🧠 by Shaly &nbsp;&nbsp;&nbsp; ©2024 </sub> </p>


