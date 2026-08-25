package io.delario.pleiades.screenone;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;

import io.delario.pleiades.pages.IndexPage;
import com.microsoft.playwright.Browser;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import io.delario.pleiades.util.ScreenOneReadyStateUtil;

public abstract class AbstractScreenOneTest {
    protected static Playwright playwright;
    protected static Browser browser;
    protected Page page; 
    protected final String baseURL = getBaseURL();

    private String getBaseURL() {
        // Local tests and CI tests are expected
        // to default since neither make Java
        // aware of environment variables.
        String env = System.getenv("PLEIADES_ENV");
        if (env == null || env.isBlank()) {
            env = "sandbox";
        }
        System.out.println("Running tests against environment: " + env);

        String url = switch (env) {
            case "sandbox", "test" -> "http://127.0.0.1:8000";
            case "staging" -> System.getenv("URL_STAGING");
            case "prod" -> System.getenv("URL_PROD");
            default -> null;
        };

        if (url == null || url.isBlank()) {
            throw new IllegalStateException(
                "Invalid baseURL: environment variable not set or empty for PLEIADES_ENV=" + env
            );
        }

        System.out.println("Using base URL: " + url);

        return url;
    }

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
        ScreenOneReadyStateUtil.waitForReadyState(this.page);
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
        ScreenOneReadyStateUtil.waitForReadyState(this.page);
        return new IndexPage(page);
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
