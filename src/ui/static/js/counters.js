import { getSelectionCounterElement, getSubmissionCounterElement } from "./getters.js";

// NOTE: If UI testing automation is shifted away from Playwright, then
// +1 may no longer function correctly. Even though manual UI selections
// for the same option do not trigger a "change," the Playwright code
// to do so does trigger a "change" event. This is why the counter
// increments by +1 for both same and new selections.
export function bumpSelectionCounter() {
  const selectionCounterElement = getSelectionCounterElement();
  bumpCounter(selectionCounterElement);
}

export function bumpSubmissionCounter() {
  const submissionCounterElement = getSubmissionCounterElement();
  bumpCounter(submissionCounterElement);
}

export function bumpCounter(counterElement) {
  const currentCounter = parseInt(counterElement.dataset.counter);
  const newCounter = (currentCounter + 1).toString();
  counterElement.dataset.counter = newCounter;
}