package io.delario.pleiades.pages;

import com.microsoft.playwright.Page;

import java.util.List;

/**
 * Page Object representing the Index page of the application.
 *
 * <h2>Usage</h2>
 * This class must be created using the {@link #navigateTo(Page)} factory method.
 * Direct instantiation is intentionally restricted to ensure the page is always
 * on the correct URL before interactions occur.
 *
 * <pre>
 * IndexPage index = IndexPage.navigateTo(page);
 * index.selectBook("Genesis");
 * String selected = index.getSelectedBook();
 * </pre>
 */
public class IndexPage {

    // =========================================================
    // Fields
    // =========================================================

    private final Page page;

    private static final String URL = "/";
    private static final String BOOK_DROPDOWN_LABEL = "Book";
    private static final String CHAPTER_DROPDOWN_LABEL = "Chapter";
    private static final String VERSE_DROPDOWN_LABEL = "Verse";
    private static final String DEPTH_DROPDOWN_LABEL = "Depth";

    // =========================================================
    // Construction / Navigation
    // =========================================================

    private IndexPage(Page page) {
        this.page = page;
    }

    /**
     * Navigates to the Index page and returns a ready-to-use Page Object.
     */
    public static IndexPage navigateTo(Page page) {
        page.navigate(URL);
        return new IndexPage(page);
    }

    // =========================================================
    // Dropdowns
    // =========================================================

    private Dropdown getBookDropdown() {
        return new Dropdown(this.page.getByLabel(BOOK_DROPDOWN_LABEL));
    }

    private Dropdown getChapterDropdown() {
        return new Dropdown(this.page.getByLabel(CHAPTER_DROPDOWN_LABEL));
    }

    private Dropdown getVerseDropdown() {
        return new Dropdown(this.page.getByLabel(VERSE_DROPDOWN_LABEL));
    }

    private Dropdown getDepthDropdown() {
        return new Dropdown(this.page.getByLabel(DEPTH_DROPDOWN_LABEL));
    }

    // =========================================================
    // Selection Getters
    // =========================================================

    public String getSelectedBook() {
        return this.getBookDropdown().getSelectedOptionText();
    }

    public String getSelectedChapter() {
        return this.getChapterDropdown().getSelectedOptionText();
    }

    public String getSelectedVerse() {
        return this.getVerseDropdown().getSelectedOptionText();
    }

    public String getSelectedDepth() {
        return this.getDepthDropdown().getSelectedOptionText();
    }

    // =========================================================
    // Options Getters
    // =========================================================

    public List<String> getBookOptions() {
        return this.getBookDropdown().getOptionTexts();
    }

    public List<String> getChapterOptions() {
        return this.getChapterDropdown().getOptionTexts();
    }

    public List<String> getVerseOptions() {
        return this.getVerseDropdown().getOptionTexts();
    }

    public List<String> getDepthOptions() {
        return this.getDepthDropdown().getOptionTexts();
    }

    // =========================================================
    // Option Selectors
    // =========================================================

    public void selectBook(String book) {
        this.getBookDropdown().selectOptionByLabel(book);
    }

    public void selectChapter(String chapter) {
        this.getChapterDropdown().selectOptionByLabel(chapter);
    }

    public void selectVerse(String verse) {
        this.getVerseDropdown().selectOptionByLabel(verse);
    }

    public void selectDepth(String depth) {
        this.getDepthDropdown().selectOptionByLabel(depth);
    }
}