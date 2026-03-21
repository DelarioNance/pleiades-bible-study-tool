<!--
Database KJV Bible Ingestion Requirements
Author: Delario Nance, Jr.

This document defines the correctness contract 
for the KJV Bible ingestion pipeline used in 
the Pleiades application. All ingestion logic 
must produce a database that satisfies these 
requirements.
-->

# 📘 **Database KJV Bible Ingestion Requirements**

This document defines the requirements for the Bible ingestion pipeline used in the Pleiades application.

The ingestion pipeline must always produce a database that satisfies these requirements, regardless of changes to the data source, schema, or ingestion logic.

---

# 🌿 **1. Domain Requirements**  
These requirements come directly from the structure and rules of the Bible itself. They define what a “correct Bible dataset” is.

### **1.1 Canonical Structure**
- The Bible contains **66 books**.  
- The Bible contains **1,189 chapters**.
- The Bible contains **31,102 verses**.
- Books appear in a fixed **canonical order**.  
- Books have a **canonical name**.
- Each book contains a known number of chapters.  
- Each chapter contains a known number of verses.

### **1.2 Contiguous Numbering**
- Chapter numbers must start at 1 and increase without gaps.  
- Verse numbers must start at 1 and increase without gaps.

### **1.3 Content Requirements**
- Every verse must contain non‑empty text.  
- Text must be normalized (no stray characters, no formatting artifacts).  
- No duplicate verses or chapters.

These rules are non‑negotiable because they reflect the domain itself.

---

# 🌱 **2. Schema Requirements**  
These requirements come from the structure of the database tables and relationships.

### **2.1 Relational Integrity**
- Every chapter must reference a valid `book_id`.  
- Every verse must reference a valid `chapter_id`.  

### **2.2 Data Validity**
- Book IDs must be unique.
- Chapter IDs must be unique.
- Verse IDs must be unique.  
- Foreign keys must be valid.  
- Books have required names
- Chapters have required numbers
- Verses have required numbers
- Verses have required verbiage

These requirements ensure the ingestion pipeline produces data that matches the schema’s constraints.

---

# **Summary**

The ingestion pipeline must always produce a database that:

- matches the domain structure of the Bible  
- satisfies the schema’s relational rules  
- supports future features  
- avoids high‑risk failure modes  
- remains stable and idempotent  
- passes the full correctness contract  

If all these requirements are met, the database is considered valid and safe for API and UI development.
