import { getAllBooks, getChaptersFromBookID, getVersesFromChapterID } from "../apiHelpers.js";

export async function getIndexScreen() {
    const app = document.getElementById("app");

    app.innerHTML = `
        <h2>Select a Verse</h2>

        <label>Book:</label>
        <select id="bookSelect"></select>
        <br>
        <label>Chapter:</label>
        <select id="chapterSelect"></select>
        <br>
        <label>Verse:</label>
        <select id="verseSelect"></select>
    `;

    await initSelectors();
}


async function initSelectors() {
    await populateBookSelect();

    let selectedBookID = getSelectedBookID();

    await populateChapterSelect(selectedBookID);

    selectedBookID = getSelectedBookID();
    let selectedChapterID = getSelectedChapterID();

    await populateVerseSelect(selectedChapterID);

    const bookSelect = document.getElementById("bookSelect");
    const chapterSelect = document.getElementById("chapterSelect");
    const verseSelect = document.getElementById("verseSelect");

    bookSelect.addEventListener("change", populateBookChildrenSelects);
    chapterSelect.addEventListener("change", populateChapterChildrenSelects);
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
    const selectedBook = document.getElementById("bookSelect");
    return selectedBook.value; // ID for API, not the HTML ID
}


function getSelectedChapterID() {
    const selectedChapter = document.getElementById("chapterSelect");
    return selectedChapter.value;
}


async function populateBookChildrenSelects() {
    const selectedBookID = getSelectedBookID();
    await populateChapterSelect(selectedBookID);
    const selectedChapterID = getSelectedChapterID();
    await populateVerseSelect(selectedChapterID);
}


async function populateChapterChildrenSelects() {
    const selectedChapterID = getSelectedChapterID();
    await populateVerseSelect(selectedChapterID);
}