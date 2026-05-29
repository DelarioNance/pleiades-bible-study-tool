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
            <option value=1>1</option>
            <option value=2>2</option>
            <option value=3>3</option>
            <option value=4>4</option>
            <option value=5>5</option>
        </select>
        <p>"<span id="selectedVerseDisplay"/></span>"</p>
        <button id="submitButton">Submit</button>
    `;

    
    await initializeSelections();
    attachEventListeners();
    await displaySelectedVerse();
}


async function initializeSelections() {
    await populateSelections(); 
    selectDefaultOptions();
}


async function populateSelections() {
    await populateBookSelect();

    const selectedBookID = getSelectedBookID();
    await populateChapterSelect(selectedBookID);

    const selectedChapterID = getSelectedChapterID();
    await populateVerseSelect(selectedChapterID); 
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
        option.dataset.text = verse.text; // Store verse text for later displa
        verseSelect.appendChild(option);
    })
}
;


function selectDefaultOptions() {
    const defaultSelections = window.defaultSelections;
    
    const defaultBookName = defaultSelections["bookName"];
    const defaultChapterNumber = defaultSelections["chapterNumber"];
    const defaultVerseNumber = defaultSelections["verseNumber"];
    const defaultDepth = defaultSelections["depth"];

    const bookSelect = document.getElementById("bookSelect");
    const chapterSelect = document.getElementById("chapterSelect");
    const verseSelect = document.getElementById("verseSelect");
    const depthSelect = document.getElementById("depthSelect");

    const defaultBookOption = Array.from(bookSelect.options).find(option => option.textContent === defaultBookName);
    const defaultChapterOption = Array.from(chapterSelect.options).find(option => Number(option.textContent) === defaultChapterNumber);
    const defaultVerseOption = Array.from(verseSelect.options).find(option => Number(option.textContent) === defaultVerseNumber);
    const defaultDepthOption = Array.from(depthSelect.options).find(option => Number(option.textContent) === defaultDepth);

    defaultBookOption.selected = true;
    defaultChapterOption.selected = true;
    defaultVerseOption.selected = true;
    defaultDepthOption.selected = true;
}


function displaySelectedVerse() {
    const verseSelect = document.getElementById("verseSelect");
    console.log(verseSelect)
    const selectedVerseText = verseSelect.options[verseSelect.selectedIndex].dataset.text;
    console.log(selectedVerseText)
    const selectedVerseDisplay = document.getElementById("selectedVerseDisplay");
    console.log(selectedVerseDisplay);
    selectedVerseDisplay.textContent = selectedVerseText;
}


async function attachEventListeners() {
    document.getElementById("bookSelect")
        .addEventListener("change", handleBookSelectChange);   
    document.getElementById("chapterSelect")
        .addEventListener("change", handleChapterSelectChange);
    document.getElementById("verseSelect")
        .addEventListener("change", handleVerseSelectChange);
}


function getSelectedBookID() {
    return document.getElementById("bookSelect").value; // ID for API, not the HTML ID
}


function getSelectedChapterID() {
    return document.getElementById("chapterSelect").value;
}


async function handleBookSelectChange() {
    const bookID = getSelectedBookID();
    await populateChapterSelect(bookID);

    await handleChapterSelectChange();
}


async function handleChapterSelectChange() {
    const chapterID = getSelectedChapterID();
    await populateVerseSelect(chapterID);

    handleVerseSelectChange();
}


function handleVerseSelectChange() {
    displaySelectedVerse();
}
