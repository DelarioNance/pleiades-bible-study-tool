export async function getBooks() {
  const response = await fetch("/v1/books");
  return await response.json();
}

export async function getChaptersFromBookID(bookID) {
  const response = await fetch(`/v1/books/${bookID}/chapters`);
  return await response.json();
}

export async function getVersesFromChapterID(chapterID) {
  const response = await fetch(`/v1/chapters/${chapterID}/verses`);
  return await response.json();
}

export async function runVerseTraversal(verseID) {
  const response = await fetch(`/v1/verses/${verseID}/traversal_results`);
  return await response.json();
}
