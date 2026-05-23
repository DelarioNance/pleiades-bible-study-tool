import { getAllBooks, getChaptersFromBookID, getVersesFromChapterID } from "../apiHelpers.js";

export async function getIndexScreen() {
    const app = document.getElementById("app");

    app.innerHTML = `
        <h2>Select a Verse and Connection Depth</h2>

        <label>Book:</label>
        <select id="bookSelect"></select>
        <br>
        <label>Chapter:</label>
        <select id="chapterSelect"></select>
        <br>
        <label>Verse:</label>
        <select id="verseSelect"></select>
        <br>
        <label>Depth:</label>
        <select id="depthSelect">
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
        </select>
        <br>
        <br>
        <button id="submitButton">Submit</button>
    `;

    await initSelects();
    attachEventListeners();
}


async function initSelects() {
    await populateBookSelect();

    const selectedBookID = getSelectedBookID();
    await populateChapterSelect(selectedBookID);

    const selectedChapterID = getSelectedChapterID();
    await populateVerseSelect(selectedChapterID); 
}   


async function attachEventListeners() {
    document.getElementById("bookSelect")
        .addEventListener("change", handleBookSelectChange);   
    document.getElementById("chapterSelect")
        .addEventListener("change", handleChapterSelectChange);
    document.getElementById("submitButton")
        .addEventListener("click", submitSelections);
}


async function populateBookSelect() {    
    const books = await getAllBooks();
    const bookSelect = document.getElementById("bookSelect");
    
    bookSelect.innerHTML = ""; // prevents accidentally appending to the list instead of replacing it
    books.forEach(book => {
        const option = document.createElement("option");
        option.value = book.id;
        option.textContent = book.name;
        bookSelect.appendChild(option);
    })
}
;


async function populateChapterSelect(selectedBookID) {
    const chapters = await getChaptersFromBookID(selectedBookID);
    const chapterSelect = document.getElementById("chapterSelect");

    chapterSelect.innerHTML = "";
    chapters.forEach(chapter => {
        const option = document.createElement("option");
        option.value = chapter.id;
        option.textContent = chapter.number;
        chapterSelect.appendChild(option);
    })

}
;


async function populateVerseSelect(selectedChapterID) {
    const verses = await getVersesFromChapterID(selectedChapterID);
    const verseSelect = document.getElementById("verseSelect");

    verseSelect.innerHTML = "";
    verses.forEach(verse => {
        const option = document.createElement("option");
        option.value = verse.id;
        option.textContent = verse.number;
        verseSelect.appendChild(option);
    })
}
;


function getSelectedBookID() {
    return document.getElementById("bookSelect").value; // ID for API, not the HTML ID
}


function getSelectedChapterID() {
    return document.getElementById("chapterSelect").value;
}


async function handleBookSelectChange() {
    const bookID = getSelectedBookID();
    await populateChapterSelect(bookID);

    const chapterID = getSelectedChapterID();
    await populateVerseSelect(chapterID);
}


async function handleChapterSelectChange() {
    const chapterID = getSelectedChapterID();
    await populateVerseSelect(chapterID);
}


async function submitSelections() {
    const verseID = document.getElementById("verseSelect").value;  
    const depth = document.getElementById("depthSelect").value;
    
    const response = await fetch("/v1/submit-selections", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            verse_id: verseID,
            depth: depth
        })
    });

    const result = await response.json();
    console.log(result);
}