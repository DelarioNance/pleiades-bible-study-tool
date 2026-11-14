# Application Programming Interface (API) Layer

## Purpose
Serves the Pleiades UI and exposes a API for retrieving book data, chapter data, and verse data and for traversing verse cross-references. Only one HTML template is served, per Pleiades's identity as a Single Page Application (SPA). Routers handle HTTP requests, and query modules run the SQL against the Pleiades database.

## Entry Point

Run from the project root. Interactive API docs are served at `/docs`.

```bash
source venv/bin/activate
fastapi dev src/api/main.py
```


## Notable Areas for Improvment

### User-Facing Error Handling

- **Current Approach:** Errors cause the user to see a generic message or a raw JSON error body when a request fails.
- **Planned Enhancement:** Serve user-friendly messages to the UI in response to errors.