package io.delario.pleiades.pages;

import com.microsoft.playwright.Page;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.options.SelectOption;

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
    // Locators (private helpers)
    // =========================================================

    private Locator bookDropdown() {
        return page.getByLabel("Book");
    }

    private Locator bookSelection() {
        return bookDropdown().locator("option:checked");
    }

    private Locator bookOptions() {
        return bookDropdown().locator("option");
    }

    // =========================================================
    // Actions (user interactions)
    // =========================================================

    public void selectBook(String bookName) {
        bookDropdown().selectOption(
            new SelectOption().setLabel(bookName)
        );
    }

    // =========================================================
    // Getters (state reads)
    // =========================================================

    public String getSelectedBook() {
        return bookSelection().innerText();
    }

    public List<String> getBookOptions() {
        return bookOptions().allInnerTexts();
    }
}