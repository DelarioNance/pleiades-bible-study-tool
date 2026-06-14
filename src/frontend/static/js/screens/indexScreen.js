import { getAllBooks, getChaptersFromBookID, getVersesFromChapterID } from "../apiHelpers.js";

let currentSelections = {
    book:   { value: null, name: null },
    chapter:{ value: null, name: null },
    verse:  { value: null, name: null },
    depth:  { value: null, name: null }
};


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
    const defaultBookID = document.getElementById("defaultBookID").value
    selectBookByValue(defaultBookID, bookSelect);

    await populateChapterSelect(bookSelect.value);

    const chapterSelect = getChapterSelectElement();
    const defaultChapterID = document.getElementById("defaultChapterID").value
    selectChapterByValue(defaultChapterID, chapterSelect);

    await populateVerseSelect(chapterSelect.value); 

    const verseSelect = getVerseSelectElement();
    const defaultVerseID = document.getElementById("defaultVerseID").value
    selectVerseByValue(defaultVerseID, verseSelect);

    const depthSelect = getDepthSelectElement();
    const defaultDepth = document.getElementById("defaultDepth").value
    selectDepthByValue(defaultDepth, depthSelect);
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
    const selectedVerseText = verseSelect.options[verseSelect.selectedIndex].dataset.text;
    const selectedVerseDisplay = document.getElementById("selectedVerseDisplay");
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

function getDepthSelectElement() {
    return document.getElementById("depthSelect");
}

function getSelectedVerseValue() {
    return getVerseSelectElement().value;
}


async function handleBookSelectChange(event) {
    const bookSelect = event.target;
    const newValue = bookSelect.value;

    if (newValue === currentSelections.book.value) {
        return;
    }

    selectBookByValue(newValue, bookSelect);

    await populateChapterSelect(newValue);

    const chapterSelect = getChapterSelectElement();
    selectChapterByValue(chapterSelect.value, chapterSelect);

    await populateVerseSelect(chapterSelect.value);

    const verseSelect = getVerseSelectElement();
    selectVerseByValue(verseSelect.value, verseSelect);
    console.log(currentSelections);
}


async function handleChapterSelectChange(event) {
    const chapterSelect = event.target;
    const newValue = chapterSelect.value;

    if (newValue === currentSelections.chapter.value) {
        return;
    }

    selectChapterByValue(chapterSelect.value, chapterSelect);

    await populateVerseSelect(chapterSelect.value);

    const verseSelect = getVerseSelectElement();
    selectVerseByValue(verseSelect.value, verseSelect);
    console.log(currentSelections);
}


function handleVerseSelectChange(event) {
    const verseSelect = event.target;
    const newValue = verseSelect.value;

    if (newValue === currentSelections.verse.value) {
        return;
    }
    
    selectVerseByValue(verseSelect.value, verseSelect);
    console.log(currentSelections);
}

function selectBookByValue(newValue, selectElement) {
    selectElement.value = newValue;
    const newName = selectElement.options[selectElement.selectedIndex].textContent;

    currentSelections.book.value = newValue;
    currentSelections.book.name = newName;
}

function selectChapterByValue(newValue, selectElement) {
    selectElement.value = newValue;
    const newName = selectElement.options[selectElement.selectedIndex].textContent;

    currentSelections.chapter.value = newValue;
    currentSelections.chapter.name = newName;
}

function selectVerseByValue(newValue, selectElement) {
    selectElement.value = newValue;
    const newName = selectElement.options[selectElement.selectedIndex].textContent;

    currentSelections.verse.value = newValue;
    currentSelections.verse.name = newName;
}

function selectDepthByValue(newValue, selectElement) {
    selectElement.value = newValue;
    const newName = selectElement.options[selectElement.selectedIndex].textContent;

    currentSelections.depth.value = newValue;
    currentSelections.depth.name = newName;
}
