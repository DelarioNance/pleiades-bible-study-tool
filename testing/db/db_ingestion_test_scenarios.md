<!--
Database KJV Bible Ingestion Test Scenarios
Author: Delario

This document defines the complete set of test scenarios used to validate the
correctness, integrity, and stability of the KJV Bible ingestion pipeline for
the Pleiades application. These scenarios ensure that the ingested database
matches the canonical structure of the King James Version, satisfies all schema
constraints, and maintains high-quality content formatting. The ingestion
pipeline must consistently pass these scenarios regardless of changes to data
sources, schema evolution, or implementation details.
-->

# 📘 **Database KJV Bible Ingestion Test Scenarios**

Note: The test scenarios below assume the KJV version.

## 🌿 Domain Requirement Test Scenarios

- Used to guarantee that the concept of the Bible is maintained

| **ID** | **Title** | **Purpose** | **Expected Result** |
|-------|-----------|-------------|----------------------|
| **DB‑01** | Canonical Book Count | Validate correct number of books | 66 books exist |
| **DB‑02** | Canonical Chapter Count | Validate correct number of chapters | 1,189 chapters exist |
| **DB‑03** | Canonical Verse Count | Validate correct number of verses | 31,102 verses exist |
| **DB‑04** | Canonical Book List | Validate canonical book names + order | Ordered canonical book list matches ordered DB book list |
| **DB‑06** | Chapter Count Per Book | Validate chapter counts per book | All books have correct chapter counts |
| **DB‑07** | Verse Count Per Chapter | Validate verse counts per chapter | All chapters have correct verse counts |
| **DB‑08** | Chapter Number Contiguity | Ensure no gaps in chapter numbering | All books have chapter numbers which start at 1 and increase without gaps |
| **DB‑09** | Verse Number Contiguity | Ensure no gaps in verse numbering | All chapters have verse numbers which start at 1 and increase without gaps |

## 🌿 Schema Integrity Test Scenarios

- Used to guarantee that the database tables and their relationships satisfy conditions assumed by other layers for those layers to function correctly (e.g., API layer, UI layer)

| **ID** | **Title** | **Purpose** | **Expected Result** |
|-------|-----------|-------------|----------------------|
| **DB‑10** | Chapter Has Valid Book | Ensure every chapter belongs to an existing book | All chapters reference a valid `book_id` in `books` |
| **DB‑11** | Verse Has Valid Chapter | Ensure every verse belongs to an existing chapter | All verses reference a valid `chapter_id` in `chapters` |
| **DB‑12** | Unique Book Names | Prevent duplicate book names | All book names are unique |
| **DB‑13** | Unique Chapter Numbers Per Book | Prevent duplicate chapter numbers within a book | Each book has unique chapter numbers (no duplicates) |
| **DB‑14** | Unique Verse Numbers Per Chapter | Prevent duplicate verse numbers within a chapter | Each chapter has unique verse numbers (no duplicates) |
| **DB‑15** | Non‑Null Book Names | Ensure book names are not missing | All book names are non‑null |
| **DB‑16** | Non‑Null Chapter Numbers | Ensure chapter numbers are not missing | All chapter numbers are non‑null |
| **DB‑17** | Non‑Null Verse Text | Ensure verse text is not missing | All verse text fields are non‑null |

## 🌿 Content Integrity Test Scenarios

- Used to guarantee a certain level of quality of the displayed text

| **ID** | **Title** | **Purpose** | **Expected Result** |
|-------|-----------|-------------|----------------------|
| **DB‑18** | Non‑Whitespace Book Names | Ensure book names are not blank | All book names are not whitespace |
| **DB‑19** | Integer Chapter Numbers | Ensure chapter numbers are numeric | All chapter numbers are  integers |
| **DB‑20** | Non‑Whitespace Verse Text | Ensure verse text is not blank | All verse text fields are not whitespace |
