# 📘 Mocking & Patching

# 🧩 What Problem I Ran Into

The core issue was:

How do I properly unit test extract_books.py when it calls requests.get() and depends on external API data?

Challenges included:

- The function makes a real HTTP request

- Unit tests must not hit the network

- I needed to simulate the API response

- I wanted maintainable test data

- I didn’t want brittle tests tied to external systems

This led me to learn how to use mocking and patching to isolate the function and test only its logic.

---

# 🧪 Why Unit Tests Should NOT Be Tightly Coupled to API Data

### ✔ Unit tests should test *logic*, not *external systems*
A unit test verifies **my function**, not the API.

### ✔ API data can change
If the API adds fields, renames keys, or changes ordering, a tightly coupled test breaks even though my logic is correct.

### ✔ Unit tests must be stable and predictable
They should not fail because of:
- network issues  
- API downtime  
- API schema changes  

### ✔ Fake data should be minimal and representative
The goal is to test:
- “Does my function transform this shape into that shape?”

Not:
- “Does my function match the real Bible API exactly?”

---

# 🔧 Mocking vs. Patching (Clear Definitions)

## 🟦 **Mocking**
> Creating a fake object with fake behavior.

A `Mock()` can:
- have attributes  
- have methods  
- return fake values  
- simulate errors  

Example:
```python
fake_response = Mock()
fake_response.json.return_value = {"books": [...]}
```

This object behaves like a real `requests.Response`, but it’s fully controlled.

---

## 🟩 **Patching**
> Replacing a real object with a mock during the test.

Example:
```python
@patch("requests.get")
def test_extract_books(mock_get):
```

This means:
- Every call to `requests.get()` inside the test is replaced with `mock_get`
- No real HTTP requests happen
- I control what `requests.get()` returns

---

# 🔄 How Mocking + Patching Work Together

### 1. **Patch** replaces the function (`requests.get`)
### 2. **Mock** creates the fake response object
### 3. The patched function returns the mock

Flow:

```
requests.get()  →  mock_get()
mock_get()      →  fake_response
fake_response.json() → fake JSON
```

This isolates the function under test and removes external dependencies.

---

# 🧱 Illusrative Example

```python
from unittest.mock import patch, Mock
import pytest
from bible_ingestion.extract_books import extract_books

@pytest.fixture
def raw_book_data_fixture():
    return {
        'books': [
            {'id': 'GEN', 'commonName': 'Genesis', 'order': 1},
            {'id': 'EXO', 'commonName': 'Exodus', 'order': 2},
        ]
    }

@pytest.fixture
def extracted_book_data_fixture():
    return {
        'GEN': {'commonName': 'Genesis', 'order': 1},
        'EXO': {'commonName': 'Exodus', 'order': 2},
    }

@patch('requests.get')
def test_extract_books(
    mock_get, 
    raw_book_data_fixture, 
    extracted_book_data_fixture
):
    mock_response = Mock()
    mock_response.json.return_value = raw_book_data_fixture
    mock_get.return_value = mock_response

    result = extract_books('https://fake-url')

    assert result == extracted_book_data_fixture
```

This is clean, readable, and avoids brittle logic.

---

# 🧠 Key Takeaways

- **Mocking** = creating fake objects  
- **Patching** = replacing real objects with mocks  
- Unit tests should **not** depend on real API data  
- Use fixtures to keep test data clean and maintainable  
- Never re‑implement transformation logic inside the test  
- Test only the **behavior** of your function, not the API  
