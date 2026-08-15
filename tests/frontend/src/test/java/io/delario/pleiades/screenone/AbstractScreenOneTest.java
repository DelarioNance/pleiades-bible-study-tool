package io.delario.pleiades.screenone;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;

import io.delario.pleiades.pages.IndexPage;
import com.microsoft.playwright.Browser;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import com.microsoft.playwright.options.WaitForSelectorState;

public abstract class AbstractScreenOneTest {
    protected static Playwright playwright;
    protected static Browser browser;
    protected Page page; 
    protected final String baseURL = "http://127.0.0.1:8000";

    /**
     * One-time Playwright + Browser initialization. We use BeforeAll because
     * creating Playwright and Browser instances is expensive.
     */
    @BeforeAll
    public static void initializeTestClass() {
        playwright = Playwright.create();
        browser = playwright.chromium().launch(
            new com.microsoft.playwright.BrowserType.LaunchOptions()
        );
    }

    /**
     * Every test receives a fresh Page instance. The IndexPage object
     * is not created here because each test must decide whether to
     * navigate to the IndexPage with or without default values.
     */
    @BeforeEach
    public void initializeTestCase() {
        this.page = browser.newPage();
    }

    /**
     * Navigate to the Index page WITHOUT defaults, waiting until
     * page is in a state ready for testing.
     */
    protected IndexPage goToIndexPage() {
        page.navigate(this.baseURL);
        waitForTestReadyState();
        return new IndexPage(page);
    }

    /**
     * Navigate to the Index page WITH defaults, waiting until
     * page is in a state ready for testing.
     */
    protected IndexPage goToIndexPage(String initialBook, String initialChapter, String initialVerse, String initialDepth) {
        page.navigate(
            baseURL 
            + "?default_book_name=" + initialBook
            + "&default_chapter_number=" + initialChapter
            + "&default_verse_number=" + initialVerse
            + "&default_depth=" + initialDepth
        );
        waitForTestReadyState();
        return new IndexPage(page);
    }
    
    /**
     * Synchronizes the DOM so tests never interact with partially-loaded dropdowns.
     *
     * Playwright auto-waits for visibility and attachment of the dropdown element,
     * but it does NOT wait for <option> children to be populated.
     *
     * The Index page loads dropdown options asynchronously based on:
     *  - default book
     *  - default chapter
     *  - default verse
     *  - default depth
     *
     * Without this method, tests would be flaky.
     * With this method, tests are deterministic and stable.
     */
    protected void waitForTestReadyState() {
        // The Playwright with Java docs are incomplete, so you must inspect the definition
        // of the waitFor method, WaitForOptions class, setState method, and WaitForSelectorState enum 
        // to understand how this works
        this.page.getByLabel("Book").locator("option").first().waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.ATTACHED));
        this.page.getByLabel("Chapter").locator("option").first().waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.ATTACHED));
        this.page.getByLabel("Verse").locator("option").first().waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.ATTACHED));
        this.page.getByLabel("Depth").locator("option").first().waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.ATTACHED));
    }

    /**
     * Test-only helper for retrieving the backend-provided default book name.
     * This reads the hidden placeholder input that the backend exposes solely
     * for verification purposes.
     */
    protected String getBackendDefaultBookName() {
        Locator defaultBookNameLocator = page.getByPlaceholder("defaultBookNamePlaceholder");
        return defaultBookNameLocator.inputValue();
    }

    protected String getBackendDefaultChapterNumber() {
        Locator defaultChapterNumberLocator = page.getByPlaceholder("defaultChapterNumberPlaceholder");
        return defaultChapterNumberLocator.inputValue();
    }

    protected String getBackendDefaultVerseNumber() {
        Locator defaultVerseNumberLocator = page.getByPlaceholder("defaultVerseNumberPlaceholder");
        return defaultVerseNumberLocator.inputValue();
    }

    protected String getBackendDefaultDepth() {
        Locator defaultDepthLocator = page.getByPlaceholder("defaultDepthPlaceholder");
        return defaultDepthLocator.inputValue();
    }
}
