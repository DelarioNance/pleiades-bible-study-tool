import { getAllBooks, getChaptersFromBookID, getVersesFromChapterID, runVerseTraversal } from "../apiHelpers.js";

const currentSelections = {
    book:   { value: null, name: null },
    chapter:{ value: null, name: null },
    verse:  { value: null, name: null },
    depth:  { value: null, name: null }
};

const degreeNames = [
    "Selected Verse", 
    "1st-Degree", 
    "2nd-Degree"
];


export async function getIndexScreen() {
    const app = document.getElementById("app");

    app.innerHTML = `
        <h2>Find Related Scriptures</h2>

        <div id="scriptureSelection">
            <label for="bookSelect">Book:</label>
            <select id="bookSelect"></select>
            <label for="chapterSelect">Chapter:</label>
            <select id="chapterSelect"></select>
            <label for="verseSelect">Verse:</label>
            <select id="verseSelect"></select>
            <label hidden for="depthSelect" >Depth:</label>
            <select hidden id="depthSelect">
                <option value=1>1</option>
                <option value=2>2</option>
                <option value=3>3</option>
            </select>
        </div>

        <button id="submitButton" data-testid="submit-button">Search</button>
        <p>
            <!--
                Commed out until app supports verse preview
                <span id="selectedVerseDisplay"/>Click Below!</span>
            -->
        </p>
        <div id="traversalResults" data-testid="traversal-results">
        </div>
    `;
    
    await initializeSelections();
    // await displaySelectedVerse();
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
    document.getElementById("depthSelect")
        .addEventListener("change", handleDepthSelectChange);
    document.getElementById("submitButton")
        .addEventListener("click", handleSubmitButtonClick);
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

function getSelectionCounterElement() {
    return document.getElementById("selectionCounter");
}

function getSubmissionCounterElement() {
    return document.getElementById("submissionCounter");
}

function getTraversalResultsElement() {
    return document.getElementById("traversalResults");
}


function bumpCounter(counterElement) {
    const currentCounter = parseInt(counterElement.dataset.counter);
    const newCounter = (currentCounter + 1).toString();
    counterElement.dataset.counter = newCounter;
}


// NOTE: If UI testing automation is shifted away from Playwright, then
// +1 may no longer function correctly. Even though manual UI selections
// for the same option do not trigger a "change," the Playwright code
// to do so does trigger a "change" event. This is why the counter 
// increments by +1 for both same and new selections.
function bumpSelectionCounter() {
    const selectionCounterElement = getSelectionCounterElement();
    bumpCounter(selectionCounterElement);
}

function bumpSubmissionCounter() {
    const submissionCounterElement = getSubmissionCounterElement();
    bumpCounter(submissionCounterElement);
}

async function handleBookSelectChange(event) {
    const bookSelect = event.target;
    const newValue = bookSelect.value;

    if (newValue !== currentSelections.book.value) {
        selectBookByValue(newValue, bookSelect);
        await populateChapterSelect(newValue);

        const chapterSelect = getChapterSelectElement();
        selectChapterByValue(chapterSelect.value, chapterSelect);

        await populateVerseSelect(chapterSelect.value);

        const verseSelect = getVerseSelectElement();
        selectVerseByValue(verseSelect.value, verseSelect);
    }

    bumpSelectionCounter();
}


async function handleChapterSelectChange(event) {
    const chapterSelect = event.target;
    const newValue = chapterSelect.value;

    if (newValue !== currentSelections.chapter.value) {
        selectChapterByValue(newValue, chapterSelect);

        await populateVerseSelect(newValue);

        const verseSelect = getVerseSelectElement();
        selectVerseByValue(verseSelect.value, verseSelect);
    }

    bumpSelectionCounter();
}


async function handleVerseSelectChange(event) {
    const verseSelect = event.target;
    const newValue = verseSelect.value;

    if (newValue !== currentSelections.verse.value) {
        selectVerseByValue(newValue, verseSelect);
    }

    bumpSelectionCounter();
}

async function handleDepthSelectChange(event) {
    const depthSelect = event.target;
    const newValue = depthSelect.value;

    if (newValue !== currentSelections.depth.value) {
        selectDepthByValue(newValue, depthSelect);
    }

    bumpSelectionCounter();
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


async function handleSubmitButtonClick() {
    const selectedVerseValue = getSelectedVerseValue();
    const verseTraversalResults = await runVerseTraversal(selectedVerseValue);

    const traversalResultsElement = getTraversalResultsElement();
    traversalResultsElement.replaceChildren();

    const numLayers = Object.keys(verseTraversalResults).length;

    for (let layer = 0; layer < numLayers; layer++) {
        // Layer container
        const layerDiv = document.createElement("div");
        layerDiv.classList.add("traversal-layer")

        // All verses in this layer
        const verses = verseTraversalResults[layer];
        
        const layerSpan = document.createElement("span");
        layerSpan.classList.add("traversal-layer-number")
        layerSpan.textContent = getDegreeLabel(layer, verses.length);

        layerDiv.appendChild(layerSpan);

        for (const verse of verses) {
            const verseDiv = document.createElement("div");
            verseDiv.classList.add("traversal-verse");

            const referenceElement = document.createElement("span");
            referenceElement.classList.add("traversal-verse-identifier");
            referenceElement.textContent =
                `${verse.book_name} ${verse.chapter_number}:${verse.verse_number} KJV`;

            const textElement = document.createElement("span");
            textElement.classList.add("traversal-verse-text");
            textElement.textContent = verse.verse_text;

            verseDiv.appendChild(referenceElement);
            verseDiv.appendChild(document.createElement("br"));
            verseDiv.appendChild(textElement);
    
            layerDiv.appendChild(verseDiv);
        }

        traversalResultsElement.appendChild(layerDiv);
    }

    bumpSubmissionCounter();
}

function getDegreeLabel(layer, verseCount) {
    if (layer === 0) {
        return "Selected Scripture";
    }

    const noun = verseCount === 1 ? "Connection" : "Connections";
    const degree = degreeNames[layer] || `Degree ${layer}`;
    return `${degree} ${noun}`;
}