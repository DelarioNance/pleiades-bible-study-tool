export function getAppElement() {
  return document.getElementById("app");
}

export function getBookSelectElement() {
  return document.getElementById("bookSelect");
}


export function getChapterSelectElement() {
  return document.getElementById("chapterSelect");
}


export function getVerseSelectElement() {
  return document.getElementById("verseSelect");
}

export function getDepthSelectElement() {
  return document.getElementById("depthSelect");
}

export function getSelectedVerseValue() {
  return getVerseSelectElement().value;
}

export function getSelectionCounterElement() {
  return document.getElementById("selectionCounter");
}

export function getSubmissionCounterElement() {
  return document.getElementById("submissionCounter");
}

export function getTraversalResultsElement() {
  return document.getElementById("traversalResults");
}
