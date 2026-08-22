# **GET /v1/books**

## **Summary**
Retrieve metadata for all KJV books

---

## **HTTP Method**
`GET`

## **Endpoint**
`/v1/books`

## **Query Parameters**
None.

---

## **Successful Response**

### **Status Code**
`200 OK`

### **Response Body**
```
{
    "books": [
        {
            "id": 1,
            "name": "Genesis",
            "order": 1
        },
        {
            "id": 2,
            "name": "Exodus",
            "order": 2
        }
    ]
}
```

### **Field Definitions**

- **id** (integer)  
  - **Definition:** Database primary key for the book  
  - **Use:** Stable identifier for efficient chapter and verse lookups

- **name** (string)  
  - **Definition:** Human‑readable name of the book  
  - **Use:** Displayed in the UI for user selection

- **order** (integer)  
  - **Definition:** Canonical order of the book in the Bible
  - **Use:** Allows for predictable ordering in the UI

---

## **Error Responses**

### **500 Internal Server Error**
Returned when the server cannot load book metadata (e.g., database unavailable, ETL failure).

```
{
    "error": "Failed to load books."
}
```