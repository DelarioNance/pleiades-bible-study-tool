# 📘 **Pleiades Bible Study Tool — MVP Summary**

## **Who — User(s)**
- Individuals who want to the ability to reference a given Bible verse's related verses

---

## **Why — Motivation**
- Traditional Bible apps show related verses, but not **layered connections** or **graph‑based relationships**.  
    - This causes exploration of related verses at various depths to be manual, slow, and error-prone

---

## **What — Primary Requirement**
- **Allow a user to select a verse and its related verses at every depth.**

---

## **End-to-End Flow**

1. User can choose a KJV verse
2. After choosing a KJV verse, the user can copy and paste that verse's related verses at every depth (in canonical order, not depth order)



## **UI Screens**

### **1. Traversal Screen**
- Three dropdowns, from which the user can respectively select the following:
  - Book  
  - Chapter  
  - Verse  
- “Run Traversal” button  

### **2. Results Screen**
- Displays text of the related verses in the following example format:

```
Genesis 1:1
In the beginning God created the heaven and the earth.

John 3:16
For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.

Revelation 22:21
The grace of our Lord Jesus Christ be with you all. Amen.
```
- The user can copy the text.