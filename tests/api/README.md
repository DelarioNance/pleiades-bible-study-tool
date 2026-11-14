# API Test Suite

## Purpose
Automated tests for the Pleiades API layer. They check that the API returns correctly structured data, returns the right data for known inputs, and responds sensibly when something goes wrong on either the client or the server side.

## Running the Tests

Run from the project root:

```bash
source venv/bin/activate
pytest tests/api
```

## Organization

The tests are divided into four categories, each answering a different question about the API.

### Contract Tests
Validate that responses have the expected structure: the right fields, data types, and overall shape.

### Integration Tests
Validate responses for known, expected occurrences. These tests request real data, such as a specific book, chapter, or verse.

### Client Error Tests
Check what happens when the client does something wrong, such as requesting a book, chapter, or verse that does not exist or sending invalid input.

### Server Error Tests
Check what happens when something fails on the server side, such as a database problem.

## Notable Areas for Improvement

### URL Management

- **Current Approach:** API endpoint URLs are written directly in the tests, so a change to a route means updating every test that uses it.
- **Planned Enhancement:** Introduce a structure similar to page objects, such as a small API client layer that owns the endpoint URLs and request logic. Tests would call methods like "get chapters for a book" instead of building URLs themselves, so a URL change only needs to be fixed in one place.