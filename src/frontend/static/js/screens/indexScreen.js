import { getAllBooks, getChaptersFromBookID, getVersesFromChapterID } from "../apiHelpers.js";

export async function getIndexScreen() {
    const app = document.getElementById("app");

    app.innerHTML = `
        <h2>Select a Verse and Connection Depth</h2>

        <label for="bookSelect">Book:</label>
        <select id="bookSelect"></select>
        <br>
        <label for="chapterSelect">Chapter:</label>
        <select id="chapterSelect"></select>
        <br>
        <label for="verseSelect">Verse:</label>
        <select id="verseSelect"></select>
        <br>
        <label for="depthSelect">Depth:</label>
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
    await displaySelectedVerse();
    attachEventListeners();
}


async function initializeSelections() {
    await populateBookSelect();

    const bookSelect = getBookSelectElement();
    bookSelect.value = document.getElementById("defaultBookID").value;

    await populateChapterSelect(bookSelect.value);

    const chapterSelect = getChapterSelectElement();
    chapterSelect.value = document.getElementById("defaultChapterID").value;

    await populateVerseSelect(chapterSelect.value); 

    const verseSelect = getVerseSelectElement();
    verseSelect.value = document.getElementById("defaultVerseID").value;
}   


async function populateBookSelect() {    
    const books = await getAllBooks();
    const bookSelect = getBookSelectElement();
    
    bookSelect.innerHTML = ""; // prevents accidentally appending to the list instead of replacing it
    books.forEach(book => {
        const option = document.createElement("option");
        option.value = book.id;
        option.textContent = book.name;
        bookSelect.appendChild(option);
    })
}
;


async function populateChapterSelect(bookOptionValue) {
    const chapters = await getChaptersFromBookID(bookOptionValue);
    const chapterSelect = getChapterSelectElement();

    chapterSelect.innerHTML = "";
    chapters.forEach(chapter => {
        const option = document.createElement("option");
        option.value = chapter.id;
        option.textContent = chapter.number;
        chapterSelect.appendChild(option);
    })
}
;


async function populateVerseSelect(chapterOptionValue) {
    const verses = await getVersesFromChapterID(chapterOptionValue);
    const verseSelect = getVerseSelectElement();

    verseSelect.innerHTML = "";
    verses.forEach(verse => {
        const option = document.createElement("option");
        option.value = verse.id;
        option.textContent = verse.number;
        option.dataset.text = verse.text; // Store verse text for later display
        verseSelect.appendChild(option);
    })
}
;


function displaySelectedVerse() {
    const verseSelect = getVerseSelectElement();
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



function getBookSelectElement() {
    return document.getElementById("bookSelect");
}


function getSelectedBookValue() {
    return getBookSelectElement().value;
}


function getChapterSelectElement() {
    return document.getElementById("chapterSelect");
}


function getSelectedChapterValue() {
    return getChapterSelectElement().value;
}


function getVerseSelectElement() {
    return document.getElementById("verseSelect");
}

function getSelectedVerseValue() {
    return getVerseSelectElement().value;
}


async function handleBookSelectChange() {
    const selectedBookValue = getSelectedBookValue();
    await populateChapterSelect(selectedBookValue);

    await handleChapterSelectChange();
}


async function handleChapterSelectChange() {
    const selectedChapterValue = getSelectedChapterValue();
    await populateVerseSelect(selectedChapterValue);

    handleVerseSelectChange();
}


function handleVerseSelectChange() {
    displaySelectedVerse();
}
