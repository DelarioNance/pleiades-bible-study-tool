import { currentSelections } from "./state.js";

export function selectBookByValue(newValue, selectElement) {
  selectElement.value = newValue;
  const newName =
    selectElement.options[selectElement.selectedIndex].textContent;

  currentSelections.book.value = newValue;
  currentSelections.book.name = newName;
}

export function selectChapterByValue(newValue, selectElement) {
  selectElement.value = newValue;
  const newName =
    selectElement.options[selectElement.selectedIndex].textContent;

  currentSelections.chapter.value = newValue;
  currentSelections.chapter.name = newName;
}

export function selectVerseByValue(newValue, selectElement) {
  selectElement.value = newValue;
  const newName =
    selectElement.options[selectElement.selectedIndex].textContent;

  currentSelections.verse.value = newValue;
  currentSelections.verse.name = newName;
}

export function selectDepthByValue(newValue, selectElement) {
  selectElement.value = newValue;
  const newName =
    selectElement.options[selectElement.selectedIndex].textContent;

  currentSelections.depth.value = newValue;
  currentSelections.depth.name = newName;
}