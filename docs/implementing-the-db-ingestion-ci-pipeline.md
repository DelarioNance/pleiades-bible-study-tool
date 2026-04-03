# 📘 What I Learned Today: CI Pipelines, Docker, Python Packages, JUnit XML, and Database Testing

This document captures the key insights, mental models, and practical steps I learned while building a real CI pipeline using Bitbucket Pipelines, Docker service containers, pytest, and JUnit XML reporting.  

This document serves as future reference.

---

## 🧱 1. CI Pipelines: What They Actually Are

### **Core Idea**
A CI pipeline is an automated system that:

- Spins up a fresh, isolated environment  
- Clones the repository  
- Installs dependencies  
- Runs tests  
- Reports results  

### **Mental Model**
A CI pipeline is like:

> A brand‑new Linux machine created for a temporary time, runs my code, and disappears.

### **Key Takeaways**
- Nothing from my local machine matters unless it’s committed to Git.  
- Every run starts from zero.  

---

## 🐳 2. Docker Images vs Containers

### **Image**
A blueprint (like a class).

### **Container**
A running instance of that blueprint (like an object).

### **Key Insight**
Bitbucket automatically orchestrates containers.  
I don’t manually run Docker commands — the pipeline does it for me.

---

## 🗄️ 3. Postgres Service Container: How It Works

When I define:

```yaml
services:
  - test-db
```

Bitbucket:

1. Pulls the Postgres image  
2. Creates a container  
3. Injects environment variables  
4. Starts Postgres  

---

## 🔐 4. Environment Variables in Bitbucket

### **Rules I Learned**
- Repo variables are injected into the container at runtime.  

### **Dynamic DB URL**
Instead of storing full URLs, I let the source code dynamically generate the different parts of the URLs:

```python
return f"postgresql+psycopg2://{user}:{password}@localhost:5432/{name}"
```

---

## 🧪 5. pytest + JUnit XML: Making CI Understand Tests

### **pytest does NOT generate XML by default**
I must explicitly tell it:

```bash
pytest --junitxml=test-results/results.xml
```

### **Bitbucket does NOT scan the entire filesystem**
It only looks in folders meeting a specific naming convention for test results.

### **The folder must exist**
If `test-results/` doesn’t exist inside the container:

---

## 🏗️ 7. The Final Working Pipeline (Mental Model)

My pipeline now:

1. Spins up a Python container  
2. Spins up a Postgres container  
3. Injects environment variables  
4. Installs dependencies  
5. Runs pytest  
6. Generates JUnit XML  

This is a production‑grade CI workflow.

---

## 🧩 8. What Actually “Clicked” Today

- CI is a fresh machine every run  
- Docker images vs containers finally made sense  
- Bitbucket orchestrates containers automatically  
- Postgres service containers behave like real DB servers  
- pytest needs explicit XML output for CI systems   

---

## 🌟 9. The Big Picture

Today I learned:

- CI/CD fundamentals  
- Docker container orchestration  
- Python dependency installation in CI  
- Dynamic DB URL generation  
- JUnit XML reporting  
- Bitbucket test discovery  

This wasn’t just “getting tests to run.”  
It was building a **real, reproducible, professional CI pipeline** from scratch.
