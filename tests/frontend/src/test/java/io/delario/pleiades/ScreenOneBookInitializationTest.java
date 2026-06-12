package io.delario.pleiades;
import static io.delario.pleiades.BibleCanon.BOOKS_IN_NUMBER_ORDER;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import com.microsoft.playwright.Locator;

/**
 * Unit test for simple App.
 */
public class ScreenOneBookInitializationTest extends AbstractScreenOneInitializationTest{
    @Test
    public void testBookDrowndownIsVisibleWhenDefaultsProvided() {
        super.navigateToIndexPage("Genesis", "1", "1", "1");
        Locator bookDropdownLocator = super.page.getByLabel("Book:"); // similar to SQL views in the sense that it lets us get the real-time element on the page that has the label "Book:".
        assertTrue(bookDropdownLocator.isVisible(), "The book dropdown should be visible on the screen."); // this will eventually fail if the dropdown does not correspond to the specified label
    }

    @Test
    public void testBookDrowndownIsVisibleWhenDefaultsNotProvided() {
        super.navigateToIndexPage();
        Locator bookDropdownLocator = super.page.getByLabel("Book:"); // similar to SQL views in the sense that it lets us get the real-time element on the page that has the label "Book:".
        assertTrue(bookDropdownLocator.isVisible(), "The book dropdown should be visible on the screen."); // this will eventually fail if the dropdown does not correspond to the specified label
    }

    @Test
    public void testCorrectBookDropdownOptionListWhenDefaultsProvided() {
        super.navigateToIndexPage("Genesis", "1", "1", "1");
        Locator bookDropdownLocator = super.page.getByLabel("Book:"); // similar to SQL views in the sense that it lets us get the real-time element on the page that has the label "Book:".
        Locator optionsLocator = bookDropdownLocator.locator("option"); // this will get all the option elements within the dropdown
        assertTrue(optionsLocator.allInnerTexts().equals(BOOKS_IN_NUMBER_ORDER), "The book dropdown should contain the correct list of books in the correct order.");
    }

    @Test
    public void testCorrectBookDropdownOptionListWhenDefaultsNotProvided() {
        super.navigateToIndexPage();
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
    public void testCorrectDefaultBookSelectedWhenDefaultsProvided(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        super.navigateToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);
        Locator bookDropdownLocator = super.page.getByLabel("Book:");
        Locator selectedOptionLocator = bookDropdownLocator.locator("option:checked"); // CSS pseudo-class to get the currently selected option in the dropdown
        assertTrue(selectedOptionLocator.innerText().equals(defaultBook), "The default selected book should be " + defaultBook + ".");
    }

    // maybe have a test to ensure that the book id is correct when given a book name

    // need to retrieve default
    @Test
    public void testCorrectDefaultBookSelectedWhenDefaultsNotProvided() {
        super.navigateToIndexPage();
        String fallbackBookID = (String) page.evaluate("() => window.defaultSelections.bookID");
        Locator bookDropdownLocator = super.page.getByLabel("Book:");
        Locator selectedOptionLocator = bookDropdownLocator.locator("option:checked"); // CSS pseudo-class to get the currently selected option in the dropdown
        assertTrue(selectedOptionLocator.getAttribute("value").equals(fallbackBookID), "The default selected book should be " + fallbackBookID + ".");
    }

    // maybe have a test to ensure that the book name is correct when given a book name
}