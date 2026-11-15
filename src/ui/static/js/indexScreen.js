import {
  populateBookSelect,
  populateChapterSelect,
  populateVerseSelect,
} from "./populators.js";

import {
  getAppElement,
  getBookSelectElement,
  getChapterSelectElement,
  getVerseSelectElement,
  getDepthSelectElement,
} from "./getters.js";

import {
  selectBookByValue,
  selectChapterByValue,
  selectVerseByValue,
  selectDepthByValue,
} from "./selectors.js";

import {
  handleBookSelectChange,
  handleChapterSelectChange,
  handleVerseSelectChange,
  handleDepthSelectChange,
  handleSubmitButtonClick,
} from "./eventHandlers.js";

export async function getIndexScreen() {
  const app = getAppElement();

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
                Commented out until app supports verse preview
                <span id="selectedVerseDisplay"/>Click Below!</span>
            -->
        </p>
        <div id="traversalResults" data-testid="traversal-results">
        </div>
    `;

  await initializeSelections();
  attachEventListeners();
}

async function initializeSelections() {
  await populateBookSelect();

  const bookSelect = getBookSelectElement();
  const defaultBookID = document.getElementById("defaultBookID").value;
  selectBookByValue(defaultBookID, bookSelect);

  await populateChapterSelect(bookSelect.value);

  const chapterSelect = getChapterSelectElement();
  const defaultChapterID = document.getElementById("defaultChapterID").value;
  selectChapterByValue(defaultChapterID, chapterSelect);

  await populateVerseSelect(chapterSelect.value);

  const verseSelect = getVerseSelectElement();
  const defaultVerseID = document.getElementById("defaultVerseID").value;
  selectVerseByValue(defaultVerseID, verseSelect);

  const depthSelect = getDepthSelectElement();
  const defaultDepth = document.getElementById("defaultDepth").value;
  selectDepthByValue(defaultDepth, depthSelect);
}

async function attachEventListeners() {
  document
    .getElementById("bookSelect")
    .addEventListener("change", handleBookSelectChange);
  document
    .getElementById("chapterSelect")
    .addEventListener("change", handleChapterSelectChange);
  document
    .getElementById("verseSelect")
    .addEventListener("change", handleVerseSelectChange);
  document
    .getElementById("depthSelect")
    .addEventListener("change", handleDepthSelectChange);
  document
    .getElementById("submitButton")
    .addEventListener("click", handleSubmitButtonClick);
}
