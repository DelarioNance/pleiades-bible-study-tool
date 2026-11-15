import { 
  getBooks, 
  getChaptersFromBookID, 
  getVersesFromChapterID 
} from "./api.js";

import {
  getBookSelectElement,
  getChapterSelectElement,
  getVerseSelectElement,
} from "./getters.js";

export async function populateBookSelect() {
  const books = await getBooks();
  const bookSelect = getBookSelectElement();

  bookSelect.innerHTML = ""; // prevents accidentally appending to the list instead of replacing it
  books.forEach((book) => {
    const option = document.createElement("option");
    option.value = book.book_id;
    option.textContent = book.book_name;
    bookSelect.appendChild(option);
  });
}

export async function populateChapterSelect(bookOptionValue) {
  const chapters = await getChaptersFromBookID(bookOptionValue);
  const chapterSelect = getChapterSelectElement();

  chapterSelect.innerHTML = "";
  chapters.forEach((chapter) => {
    const option = document.createElement("option");
    option.value = chapter.chapter_id;
    option.textContent = chapter.chapter_number;
    chapterSelect.appendChild(option);
  });
}

export async function populateVerseSelect(chapterOptionValue) {
  const verses = await getVersesFromChapterID(chapterOptionValue);
  const verseSelect = getVerseSelectElement();

  verseSelect.innerHTML = "";
  verses.forEach((verse) => {
    const option = document.createElement("option");
    option.value = verse.verse_id;
    option.textContent = verse.verse_number;
    option.dataset.text = verse.verse_text; // Store verse text for later display
    verseSelect.appendChild(option);
  });
}
