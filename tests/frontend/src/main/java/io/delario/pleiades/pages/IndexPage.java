package io.delario.pleiades.pages;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import com.microsoft.playwright.options.SelectOption;
import com.microsoft.playwright.options.WaitForSelectorState;

import java.util.List;

/**
 * <p><strong>Page Object representing the Index page of the Pleiades application.</strong></p>
 *
 * <p>This class encapsulates the structure and behavior of the four dropdowns
 * (Book, Chapter, Verse, Depth) that define the initial state of Screen One.
 * It provides a clean, semantic API for retrieving dropdown contents and
 * selected values, while exposing Playwright Locator objects for direct UI
 * assertions.</p>
 *
 * <h3>Design Principles</h3>
 *
 * <ol>
 *   <li><strong>Locators are intentionally public.</strong><br>
 *       Playwright’s assertion API operates directly on Locator objects.
 *       Exposing them allows tests to use Playwright’s fluent assertion style
 *       without duplicating locator queries or requiring excessive wrapper
 *       methods.</li>
 *
 *   <li><strong>Semantic getter methods hide DOM structure.</strong><br>
 *       Although locators are public, tests should not query <code>&lt;option&gt;</code>
 *       elements or <code>option:checked</code> selectors directly. Getter methods
 *       provide stable, intention‑revealing access to dropdown options and selected
 *       values, keeping DOM details out of the test suite.</li>
 *
 *   <li><strong>The Page Object is pure.</strong><br>
 *       It does not navigate, wait, or manage page lifecycle. Navigation and
 *       ready‑state synchronization are handled by the test harness. This keeps
 *       the Page Object environment‑agnostic and focused solely on representing
 *       the Index page’s UI.</li>
 * </ol>
 *
 * <h3>Usage</h3>
 *
 * <pre>
 * IndexPage index = goToIndexPage();   // navigation handled by test harness
 * List&lt;String&gt; books = index.getBookOptions();
 * String selectedBook = index.getSelectedBook();
 * </pre>
 */
public class IndexPage {
    // Locators are intentionally public.
    //
    // Playwright’s assertion API operates directly on Locator objects. 
    // If these locators were private, tests would either:
    //
    //   (1) need to recreate the same locator queries themselves, leaking DOM structure into
    //       the test suite, or
    //   (2) require this Page Object to expose dozens of wrapper methods just to support
    //       Playwright’s fluent assertion style.
    //
    // Exposing locators keeps tests expressive and aligned with Playwright’s design, while
    // still allowing this Page Object to provide higher‑level, semantic methods (such as
    // option getters and selected‑value getters). Those methods prevent tests from depending
    // on internal DOM details, but public locators give tests the flexibility to assert UI
    // state without unnecessary abstraction.

    public Locator bookDropdown;
    public Locator chapterDropdown;
    public Locator verseDropdown;
    public Locator depthDropdown;

   /**
     * <p><strong>Constructs an IndexPage by binding Playwright locators to the
     * dropdown elements on the Index route.</strong></p>
     *
     * <p>Tests (or the test harness) are responsible for navigating to the correct
     * URL <em>before</em> creating this Page Object. This ensures that:</p>
     *
     * <ul>
     *   <li>The DOM is fully loaded and stable.</li>
     *   <li>Locators bind to the correct page structure.</li>
     *   <li>The Page Object never represents an uninitialized or incorrect route.</li>
     * </ul>
     *
     * <h3>Why navigation is not handled here</h3>
     *
     * <p>Navigation is intentionally kept out of this class to preserve Page Object
     * purity. If this constructor performed navigation or route selection, the
     * IndexPage would take on multiple responsibilities (navigation <em>and</em>
     * structure), making it inflexible and harder to maintain.</p>
     *
     * <p>By keeping navigation in the test layer, this class remains focused solely
     * on describing and interacting with the Index page’s UI.</p>
     */
    public IndexPage(Page page) {
        this.bookDropdown = page.getByLabel("Book");
        this.chapterDropdown = page.getByLabel("Chapter");
        this.verseDropdown = page.getByLabel("Verse");
        this.depthDropdown = page.getByLabel("Depth");
    }


    // Even though locators are public, tests should NOT query <option> elements
    // directly. Doing so would leak DOM structure into the test suite and create
    // brittle tests if the underlying HTML ever changes.
    //
    // These “option getter” methods provide a stable, semantic API for retrieving
    // dropdown contents. They abstract away the fact that options are represented
    // as <option> elements, so tests interact with meaningful data (book names,
    // chapter numbers, etc.) instead of raw DOM queries.

    public List<String> getBookOptions() {
        return this.bookDropdown.locator("option").allInnerTexts();
    }

    public List<String> getChapterOptions() {
        return this.chapterDropdown.locator("option").allInnerTexts();
    }

    public List<String> getVerseOptions() {
        return this.verseDropdown.locator("option").allInnerTexts();
    }

    public List<String> getDepthOptions() {
        return this.depthDropdown.locator("option").allInnerTexts();
    }

    // These “selected value” getter methods abstract away how the Index page
    // represents the currently selected item in each dropdown.
    //
    // Even though locators are public, tests should NOT query "option:checked"
    // directly. Doing so would leak DOM structure into the test suite and tightly
    // couple tests to the specific HTML implementation.    

    public String getSelectedBook() {
        return this.bookDropdown.locator("option:checked").innerText();
    }

    public String getSelectedChapter() {
        return this.chapterDropdown.locator("option:checked").innerText();
    }

    public String getSelectedVerse() {
        return this.verseDropdown.locator("option:checked").innerText();
    }

    public String getSelectedDepth() {
        return this.depthDropdown.locator("option:checked").innerText();
    }

    public void selectBook(String book) {
        this.bookDropdown.selectOption(new SelectOption().setLabel(book));
    }

    public void selectChapter(String chapter) {
        this.chapterDropdown.selectOption(new SelectOption().setLabel(chapter));
    }

    public void selectVerse(String verse) {
        this.verseDropdown.selectOption(new SelectOption().setLabel(verse));
    }

    public void selectDepth(String depth) {
        this.depthDropdown.selectOption(new SelectOption().setLabel(depth));
    }

    public static void main(String[] args) {
        Playwright playwright = Playwright.create();
        Browser browser = playwright.chromium().launch(
            new com.microsoft.playwright.BrowserType.LaunchOptions()
        );

        // The caller (not the Page Object) is responsible for navigating
        // to the correct route before constructing IndexPage.
        Page page = browser.newPage();
        page.navigate("http://127.0.0.1:8000");

        // Wait for the page to reach a ready state.
        page.getByLabel("Book").locator("option").first().waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.ATTACHED));
        page.getByLabel("Chapter").locator("option").first().waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.ATTACHED));
        page.getByLabel("Verse").locator("option").first().waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.ATTACHED));
        page.getByLabel("Depth").locator("option").first().waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.ATTACHED));

        // Now that the DOM is stable, construct the Page Object.
        IndexPage indexPage = new IndexPage(page);

        // Example usage: retrieve options and selected values
        System.out.println();
        System.out.println("Books (" + indexPage.getBookOptions().size() + "): " + indexPage.getBookOptions());
        System.out.println();

        System.out.println("Chapters (" + indexPage.getChapterOptions().size() + "): " + indexPage.getChapterOptions());
        System.out.println();

        System.out.println("Verses (" + indexPage.getVerseOptions().size() + "): " + indexPage.getVerseOptions());
        System.out.println();

        System.out.println("Depth Options (" + indexPage.getDepthOptions().size() + "): " + indexPage.getDepthOptions());
        System.out.println();

        System.out.println("Selected Book: " + indexPage.getSelectedBook());
        System.out.println();

        System.out.println("Selected Chapter: " + indexPage.getSelectedChapter());
        System.out.println();

        System.out.println("Selected Verse: " + indexPage.getSelectedVerse());
        System.out.println();

        System.out.println("Selected Depth: " + indexPage.getSelectedDepth());
    }
}