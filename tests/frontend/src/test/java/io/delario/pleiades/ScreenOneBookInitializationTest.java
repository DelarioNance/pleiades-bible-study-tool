package io.delario.pleiades;
import static io.delario.pleiades.BibleCanon.BOOKS_IN_NUMBER_ORDER;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

import com.microsoft.playwright.Locator;

/**
 * Unit test for simple App.
 */
public class ScreenOneBookInitializationTest extends AbstractScreenOneInitializationTest{

    @Test
    public void testBookDrowndownExists() {
        Locator bookDropdownLocator = page.getByLabel("Book:"); // similar to SQL views in the sense that it lets us get the real-time element on the page that has the label "Book:".
        assertTrue(bookDropdownLocator.isVisible(), "The book dropdown should be visible on the screen."); // this will eventually fail if the dropdown does not correspond to the specified label
    }

    @Test
    public void testCorrectBookDropdownOptionList() {
        Locator bookDropdownLocator = page.getByLabel("Book:"); // similar to SQL views in the sense that it lets us get the real-time element on the page that has the label "Book:".
        Locator optionsLocator = bookDropdownLocator.locator("option"); // this will get all the option elements within the dropdown
        assertTrue(optionsLocator.allInnerTexts().equals(BOOKS_IN_NUMBER_ORDER), "The book dropdown should contain the correct list of books in the correct order.");
    }
}
