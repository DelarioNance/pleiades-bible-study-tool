package io.delario.pleiades;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import com.microsoft.playwright.options.WaitForSelectorState;

public abstract class AbstractScreenOneInitializationTest {
    protected static Playwright playwright;
    protected static Browser browser;
    protected Page page; 
    protected String baseURL;

    @BeforeAll
    public static void initializeTestClass() {
        playwright = Playwright.create();
        browser = playwright.chromium().launch(
            new com.microsoft.playwright.BrowserType.LaunchOptions()
        );
    }

    @BeforeEach
    public void initializeTestCase() {
        this.page = browser.newPage();
        this.baseURL = "http://127.0.0.1:8000";
    }

    protected void navigateToIndexPage() {
        this.page.navigate(this.baseURL);
        waitForTestReadyState();
    }

    protected void navigateToIndexPage(String book, String chapter, String verse, String depth) {
        String url = this.baseURL
            + "?default_book_name=" + book
            + "&default_chapter_number=" + chapter
            + "&default_verse_number=" + verse
            + "&default_depth=" + depth;

        this.page.navigate(url);
        waitForTestReadyState();
    }

    protected void waitForTestReadyState() {
        // The Playwright with Java docs are incomplete, so you must inspect the definition
        // of the waitFor method, WaitForOptions class, setState method, and WaitForSelectorState enum 
        // to understand how this works
        this.page.getByLabel("Book").locator("option").first().waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.ATTACHED));
        this.page.getByLabel("Chapter").locator("option").first().waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.ATTACHED));
        this.page.getByLabel("Verse").locator("option").first().waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.ATTACHED));
        this.page.getByLabel("Depth").locator("option").first().waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.ATTACHED));
    }

}
