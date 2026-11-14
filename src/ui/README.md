# User Interface (UI) Layer

## Purpose
The browser-based front end for Pleiades. It lets users pick a book, chapter, and verse, then displays the results returned by the API layer. The UI is a Single Page Application (SPA): one HTML page is loaded, and JavaScript swaps content in and out from there.

## Organization

Other than the `index.html` page, everything in browser lives in a single static folder.

### CSS
A stylesheet folder holds the CSS. The styling was originally generated with AI by directing the AI to match the theme of the Pleiades logo.

### Images
An image folder holds the Pleiades logo, generated with AI.

### JavaScript
A JavaScript folder holds the user-facing functionality, split into a few small files with distinct jobs:

- **The app entry file** is the script the index page loads. Start here to see how the app boots.
- **The router file** handles switching between screens. There is currently only one screen, but additional screens would be handled by the router.
- **The index screen file** contains most of the user functionality: building the dropdowns, responding to selections, and rendering results.
- **The counters file** holds monotonic counters. These give tests a reliable signal that an update has finished, mitigating flaky tests.
- **The state file** holds shared state, such as the current book, chapter, verse, and depth selections, so the different JavaScript functions stay synchronized. Dropdown elements can't report their previous selection on their own, so this is where that is tracked.

## Design Decisions

### Why a Single Page Instead of Multiple Pages
Pleiades uses one page rather than several server-rendered pages to keep the UI decoupled from the API layer. The UI only needs to know how to request data and display it, so if the API layer moves from FastAPI to a different tool in the future, the UI should require less changes.