# 🧵 **Python Async/Await — The Mental Model**

## 🟦 1. What async *is*
- Async is **cooperative multitasking**.
- Coroutines run on **one thread**, but they **yield** when waiting on I/O.
- The event loop switches between coroutines whenever one hits an `await`.

Async ≠ parallelism.  
Async = “don’t sit idle while waiting.”

---

## 🟩 2. Coroutines: how they’re created and run

### **Defining** an async function:
```python
async def count():
    ...
```
This defines a *coroutine factory*, not a coroutine.

### **Calling** an async function:
```python
c = count()
```
This creates a **coroutine object**.  
It does *not* run yet.

### **Running** a coroutine:
```python
await c
```
This schedules it and runs it until it hits an `await`.

---

## 🟧 3. What `await` actually does
`await` means:

> “Pause this coroutine here and give control back to the event loop.”

- If other coroutines are scheduled → event loop runs them.
- If none are scheduled → event loop waits.

`await` **always** yields.  
Concurrency only happens if something else is ready to run.

---

## 🟨 4. What `asyncio.gather()` does
`gather()`:

- Takes multiple coroutine objects
- Schedules them all at once
- Returns a single coroutine that completes when all are done

```python
await asyncio.gather(c1, c2, c3)
```

This is why concurrency happens — the event loop now has multiple tasks to switch between.

Without `gather()` (or `create_task()`), async functions run **sequentially**.

---

## 🟪 5. Event loop behavior (the real flow)
1. A coroutine runs until it hits `await`.
2. It yields to the event loop.
3. The event loop picks another scheduled coroutine.
4. When the awaited operation completes, the coroutine is resumed.
5. This continues until all coroutines finish.

Coroutines never “return control to their caller.”  
They always yield to the **event loop**.

---

## 🟫 6. `asyncio.run()` — starting the async world
```python
asyncio.run(main())
```

- Creates an event loop
- Schedules `main()`
- Runs until all awaited tasks finish
- Cleans up the loop

You can only call it once per program.

---

## 🟦 7. `asyncio.sleep()` — the canonical example
```python
await asyncio.sleep(1)
```

This:
- sets a timer
- yields control immediately
- lets other coroutines run
- resumes after the timer fires

It’s the simplest demonstration of async concurrency.

---

## 🟩 8. Concurrency vs sequential async

### Sequential:
```python
await count()
await count()
await count()
```
Runs one at a time → **no concurrency**.

### Concurrent:
```python
await asyncio.gather(count(), count(), count())
```
Runs all three together → **concurrency**.

---

## 🟧 9. When to use async
Async is ideal when your code spends time **waiting**:

- HTTP requests  
- Database queries  
- File/network I/O  
- Timers  
- Websocket events  

Async is *not* helpful for CPU‑bound work.

---

## 🟨 10. The one‑sentence mental model

> **Async lets you overlap waiting.  
> It doesn’t make Python faster — it stops Python from being idle.**