import { currentSelections } from "./state.js";
import {
  getSelectedVerseValue,
  getTraversalResultsElement,
  getChapterSelectElement,
  getVerseSelectElement,
} from "./getters.js";
import { runVerseTraversal } from "./api.js";
import {
  populateChapterSelect,
  populateVerseSelect,
} from "./populators.js";
import {
  selectBookByValue,
  selectChapterByValue,
  selectVerseByValue,
  selectDepthByValue,
} from "./selectors.js";
import { bumpSelectionCounter, bumpSubmissionCounter } from "./counters.js";

const degreeNames = ["Selected Verse", "1st-Degree", "2nd-Degree"];

export async function handleBookSelectChange(event) {
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

export async function handleChapterSelectChange(event) {
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

export async function handleVerseSelectChange(event) {
  const verseSelect = event.target;
  const newValue = verseSelect.value;

  if (newValue !== currentSelections.verse.value) {
    selectVerseByValue(newValue, verseSelect);
  }

  bumpSelectionCounter();
}

export async function handleDepthSelectChange(event) {
  const depthSelect = event.target;
  const newValue = depthSelect.value;

  if (newValue !== currentSelections.depth.value) {
    selectDepthByValue(newValue, depthSelect);
  }

  bumpSelectionCounter();
}

export async function handleSubmitButtonClick() {
  const selectedVerseValue = getSelectedVerseValue();
  const verseTraversalResults = await runVerseTraversal(selectedVerseValue);

  const traversalResultsElement = getTraversalResultsElement();
  traversalResultsElement.replaceChildren();

  const numLayers = Object.keys(verseTraversalResults).length;

  for (let layer = 0; layer < numLayers; layer++) {
    // Layer container
    const layerDiv = document.createElement("div");
    layerDiv.classList.add("traversal-layer");

    // All verses in this layer
    const verses = verseTraversalResults[layer];

    const layerSpan = document.createElement("span");
    layerSpan.classList.add("traversal-layer-number");
    layerSpan.textContent = getDegreeLabel(layer, verses.length);

    layerDiv.appendChild(layerSpan);

    for (const verse of verses) {
      const verseDiv = document.createElement("div");
      verseDiv.classList.add("traversal-verse");

      const referenceElement = document.createElement("span");
      referenceElement.classList.add("traversal-verse-identifier");
      referenceElement.textContent = `${verse.book_name} ${verse.chapter_number}:${verse.verse_number} KJV`;

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

export function getDegreeLabel(layer, verseCount) {
  if (layer === 0) {
    return "Selected Scripture";
  }

  const noun = verseCount === 1 ? "Connection" : "Connections";
  const degree = degreeNames[layer] || `Degree ${layer}`;
  return `${degree} ${noun}`;
}
