package io.delario.pleiades;
import static io.delario.pleiades.BibleCanon.BOOKS_IN_NUMBER_ORDER;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Map;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import com.microsoft.playwright.Locator;

/**
 * Unit test for simple App.
 */
public class ScreenOneBookInitializationTest extends AbstractScreenOneInitializationTest{
    private void navigateToIndexPage() {
        navigateToPage(buildUrl(baseURL, Map.of()));
    }

    private void navigateToIndexPage(
        String book,
        String chapter,
        String verse,
        String depth
    ) {
        navigateToPageNoWait(buildUrl(
            baseURL,
            Map.of(
                "default_book_name", book,
                "default_chapter_number", chapter,
                "default_verse_number", verse,
                "default_depth", depth
            )
        ));
        // wait for the page to load by waiting for the book dropdown to be visible
    }

    private String buildUrl(String baseUrl, Map<String, String> params) {
        if (params.isEmpty()) {
            return baseUrl;
        }

        StringBuilder sb = new StringBuilder(baseUrl).append("?");
        params.forEach((k, v) -> sb.append(k).append("=").append(v).append("&"));
        sb.setLength(sb.length() - 1); // remove trailing &

        return sb.toString();
    }

    private void navigateToPageNoWait(String url) {
        page.navigate(url);
    }

    @Test
    public void testBookDrowndownExists() {
        navigateToIndexPage();
        Locator bookDropdownLocator = super.page.getByLabel("Book:"); // similar to SQL views in the sense that it lets us get the real-time element on the page that has the label "Book:".
        assertTrue(bookDropdownLocator.isVisible(), "The book dropdown should be visible on the screen."); // this will eventually fail if the dropdown does not correspond to the specified label
    }

    @Test
    public void testCorrectBookDropdownOptionList() {
        navigateToIndexPage();
        Locator bookDropdownLocator = super.page.getByLabel("Book:"); // similar to SQL views in the sense that it lets us get the real-time element on the page that has the label "Book:".
        Locator optionsLocator = bookDropdownLocator.locator("option"); // this will get all the option elements within the dropdown
        assertTrue(optionsLocator.allInnerTexts().equals(BOOKS_IN_NUMBER_ORDER), "The book dropdown should contain the correct list of books in the correct order.");
    }

    @ParameterizedTest
    @CsvSource({
        "Genesis, 1, 1, 1",
        "Genesis, 50, 26, 5",
        "Matthew, 1, 25, 5",
        "Matthew, 28, 1, 1",
        "Revelation, 1, 1, 1",
        "Revelation, 22, 21, 5",
    }) // Pairwise Testing + Boundary Value Analysis + Equivalence Class Partitioning
    public void testCorrectDefaultBookSelected(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        navigateToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);
        Locator bookDropdownLocator = super.page.getByLabel("Book:");
        Locator selectedOptionLocator = bookDropdownLocator.locator("option:checked"); // CSS pseudo-class to get the currently selected option in the dropdown
        assertTrue(selectedOptionLocator.innerText().equals(defaultBook), "The default selected book should be " + defaultBook + ".");
    }
}
// info from previous page
// going to page from start
// ensuring that dropdown has populated
