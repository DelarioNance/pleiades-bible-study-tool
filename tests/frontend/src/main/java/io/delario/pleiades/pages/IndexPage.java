package io.delario.pleiades.pages;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import com.microsoft.playwright.options.AriaRole;
import com.microsoft.playwright.options.SelectOption;
import com.microsoft.playwright.options.WaitForSelectorState;
import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;

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
    public Locator titleHeader;
    public Locator bookLabel;
    public Locator bookDropdown;
    public Locator chapterDropdown;
    public Locator verseDropdown;
    public Locator depthDropdown;
    public Locator submitButton;
    public Locator resultsDisplay;

    private Locator selectionCounter;
    private Locator submissionCounter;
    
    private final String SELECTION_COUNTER_ATTRIBUTE_NAME = "data-counter";
    private final String SUBMISSION_COUNTER_ATTRIBUTE_NAME = "data-counter";

    // NOTE: If UI testing automation is shifted away from Playwright, then
    // +1 may no longer function correctly. Even though manual UI selections
    // for the same option do not trigger a "change," the Playwright code
    // to do so does trigger a "change" event. This is why the counter 
    // increments by +1 for both same and new selections.
    private final int SELECTION_COUNTER_INCREMENT = 1;
    private final int SUBMISSION_COUNTER_INCREMENT = 1;

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
        this.titleHeader = page.getByTestId("title");
        this.bookDropdown = page.getByLabel("Book");
        this.chapterDropdown = page.getByLabel("Chapter");
        this.verseDropdown = page.getByLabel("Verse");
        this.depthDropdown = page.getByLabel("Depth");
        this.submitButton = page.getByTestId("submit-buton");
        this.selectionCounter = page.getByPlaceholder("selectionCounter");
        this.submissionCounter = page.getByPlaceholder("submissionCounter");
        this.resultsDisplay = page.getByTestId("traversal-results");
    }

    ///////////////////////////////////////
    /// RETRIEVAL METHODS //
    ///////////////////////////////////////
    
    // Even though locators are public, tests should NOT query <option> elements
    // directly. Doing so would leak DOM structure into the test suite and create
    // brittle tests if the underlying HTML ever changes.
    //
    // These “option getter” methods provide a stable, semantic API for retrieving
    // dropdown contents. They abstract away the fact that options are represented
    // as <option> elements, so tests interact with meaningful data (book names,
    // chapter numbers, etc.) instead of raw DOM queries.

    public String getTitleHeaderText() {
        return this.titleHeader.innerText();
    }

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

    public List<Map<String, Object>> getDisplayedVerses() {
        List<Map<String, Object>> results = new ArrayList<>();

        List<Locator> layers = this.resultsDisplay.locator(".traversal-layer").all(); // note: all() is not lazy

        for (int degree = 0; degree < layers.size(); degree++) {
            Locator layer = layers.get(degree);

            for (Locator verse : layer.locator(".traversal-verse").all()) {
                results.add(Map.of(
                    "degree_connection", degree,
                    "scripture_identifier", verse.locator(".traversal-verse-identifier").innerText().trim(),
                    "scripture_text", verse.locator(".traversal-verse-text").innerText().trim()
                ));
            }
    }

    return results;
}

    private int getSelectionCount() {
        return getCount(this.selectionCounter, SELECTION_COUNTER_ATTRIBUTE_NAME);
    }

    private int getSubmissionCount() {
        return getCount(this.submissionCounter, SUBMISSION_COUNTER_ATTRIBUTE_NAME);
    }

    private int getCount(Locator counterLocator, String attributeName) {
        return Integer.parseInt(
            counterLocator.getAttribute(attributeName)
        );
    }

    ///////////////////////////////////////
    /// ACTION METHODS //
    ///////////////////////////////////////

    public void selectBook(String book) {
        makeSelection(this.bookDropdown, book);
    }

    public void selectChapter(String chapter) {
        makeSelection(this.chapterDropdown, chapter);
    }

    public void selectVerse(String verse) {
        makeSelection(this.verseDropdown, verse);
    }

    public void selectDepth(String depth) {
        makeSelection(this.depthDropdown, depth);
    }

    private void makeSelection(Locator dropdown, String value) {
        int preSelectionCounter = getSelectionCount();
        // System.out.println("Current counter: " + preSelectionCounter + ", current dropdown value: " + currentDropdownValue + ", new value: " + value);

        dropdown.selectOption(new SelectOption().setLabel(value));

        // try {
        //     Thread.sleep(10000);
        // } catch (InterruptedException e) {
        // } // Allow time for the selection cascade to complete and the counter to increment.

        // System.out.println("New counter: " + getSelectionCounter() + ", new dropdown value: " + dropdown.locator("option:checked").innerText());

        // We wait until the selection counter increments to the expected value as a synchronization point.
        // Without the monotonic incrementing counter, UI tests could proceed before the selection cascade
        // has completed. The definition of "completed" is the action of the corresponding event listener
        // in the frontend code.
        assertThat(this.selectionCounter)
            .hasAttribute(
                SELECTION_COUNTER_ATTRIBUTE_NAME, 
                Integer.toString(preSelectionCounter + SELECTION_COUNTER_INCREMENT)
            );
    }

    public void submitScriptureSelection() {
        int preSubmissionCounter = getSubmissionCount();

        this.submitButton.click();

        assertThat(this.submissionCounter)
            .hasAttribute(
                SUBMISSION_COUNTER_ATTRIBUTE_NAME, 
                Integer.toString(preSubmissionCounter + SUBMISSION_COUNTER_INCREMENT)
            );
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
        System.out.println();

        System.out.println("Pre-submission Counter: " + indexPage.getSubmissionCount());
        System.out.println();
        System.out.println("Pre-submission Results: " + indexPage.resultsDisplay.innerHTML());
        System.out.println();
        System.out.println("Pre-submission Verses: " + indexPage.getDisplayedVerses());
        System.out.println();

        indexPage.submitScriptureSelection();

        System.out.println("Post-Submission Counter: " + indexPage.getSubmissionCount());
        System.out.println();
        System.out.println("Post-submission Results: " + indexPage.resultsDisplay.innerHTML());
        System.out.println();
        System.out.println("Post-submission Verses: " + indexPage.getDisplayedVerses());
        System.out.println();
    }
}