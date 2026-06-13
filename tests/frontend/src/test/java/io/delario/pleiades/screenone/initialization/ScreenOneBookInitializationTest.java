package io.delario.pleiades.screenone.initialization;

import io.delario.pleiades.screenone.AbstractScreenOneTest;
import static io.delario.pleiades.utils.BibleCanon.BOOKS_IN_NUMBER_ORDER;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import com.microsoft.playwright.Locator;

public class ScreenOneBookInitializationTest extends AbstractScreenOneTest {

    @Test
    public void testBookDrowndownIsVisibleWhenDefaultsProvided() {
        super.navigateToIndexPage("Genesis", "1", "1", "1");
        Locator bookDropdownLocator = super.page.getByLabel("Book:");
        assertTrue(bookDropdownLocator.isVisible(),
            "The book dropdown should be visible on the screen.");
    }

    @Test
    public void testBookDrowndownIsVisibleWhenDefaultsNotProvided() {
        super.navigateToIndexPage();
        Locator bookDropdownLocator = super.page.getByLabel("Book:");
        assertTrue(bookDropdownLocator.isVisible(),
            "The book dropdown should be visible on the screen.");
    }

    @Test
    public void testCorrectBookDropdownOptionListWhenDefaultsProvided() {
        super.navigateToIndexPage("Genesis", "1", "1", "1");
        Locator bookDropdownLocator = super.page.getByLabel("Book:");
        Locator optionsLocator = bookDropdownLocator.locator("option");

        assertEquals(
            BOOKS_IN_NUMBER_ORDER,
            optionsLocator.allInnerTexts(),
            "The book dropdown should contain the correct list of books in the correct order."
        );
    }

    @Test
    public void testCorrectBookDropdownOptionListWhenDefaultsNotProvided() {
        super.navigateToIndexPage();
        Locator bookDropdownLocator = super.page.getByLabel("Book:");
        Locator optionsLocator = bookDropdownLocator.locator("option");

        assertEquals(
            BOOKS_IN_NUMBER_ORDER,
            optionsLocator.allInnerTexts(),
            "The book dropdown should contain the correct list of books in the correct order."
        );
    }

    @ParameterizedTest
    @CsvSource({
        "Genesis, 1, 1, 1",
        "Genesis, 50, 26, 5",
        "Matthew, 1, 25, 5",
        "Matthew, 28, 1, 1",
        "Revelation, 1, 1, 1",
        "Revelation, 22, 21, 5",
    })
    public void testCorrectDefaultBookSelectedWhenDefaultsProvided(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        super.navigateToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);

        Locator bookDropdownLocator = super.page.getByLabel("Book:");
        Locator selectedOptionLocator = bookDropdownLocator.locator("option:checked");

        assertEquals(
            defaultBook,
            selectedOptionLocator.innerText(),
            "The default selected book should be " + defaultBook + "."
        );
    }

    @Test
    public void testCorrectDefaultBookSelectedWhenDefaultsNotProvided() {
        super.navigateToIndexPage();

        Locator defaultBookNameLocator = super.page.getByPlaceholder("defaultBookNamePlaceholder");
        String defaultBookName = defaultBookNameLocator.inputValue();

        Locator bookDropdownLocator = super.page.getByLabel("Book:");
        Locator selectedOptionLocator = bookDropdownLocator.locator("option:checked");

        assertEquals(
            defaultBookName,
            selectedOptionLocator.innerText(),
            "The default selected book should be " + defaultBookName + "."
        );
    }
}
