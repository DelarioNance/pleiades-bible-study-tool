package io.delario.pleiades;
import static io.delario.pleiades.BibleCanon.getOrderedChapterNumberStringsInBook;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import com.microsoft.playwright.Locator;


public class ScreenOneChapterInitializationTest extends AbstractScreenOneTest {
    @Test
    public void testChapterDropdownIsVisibleWhenDefaultsProvided() {
        super.navigateToIndexPage("Genesis", "1", "1", "1");
        Locator chapterDropdownLocator = super.page.getByLabel("Chapter:");
        assertTrue(chapterDropdownLocator.isVisible(), "The chapter dropdown should be visible on the screen.");
    }

    @Test
    public void testChapterDropdownIsVisibleWhenDefaultsNotProvided() {
        super.navigateToIndexPage();
        Locator chapterDropdownLocator = super.page.getByLabel("Chapter:");
        assertTrue(chapterDropdownLocator.isVisible(), "The chapter dropdown should be visible on the screen.");
    }

    @ParameterizedTest
    @CsvSource({
        "2 Chronicles, 18, 31, 4",
    }) // even though there's only 1 test case, using test parameterization since defaultBook is referenced twice
    public void testCorrectChapterDropdownOptionListWhenDefaultsProvided(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        super.navigateToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);
        Locator chapterDropdownLocator = super.page.getByLabel("Chapter");
        Locator optionsLocator = chapterDropdownLocator.locator("option");
        assertEquals(getOrderedChapterNumberStringsInBook(defaultBook), optionsLocator.allInnerTexts(), "Chapter dropdown options are not correct.");
    }

    @Test
    public void testCorrectChapterDropdownOptionListWhenDefaultsNotProvided() {
        super.navigateToIndexPage();
        Locator defaultBookNameLocator = super.page.getByPlaceholder("defaultBookNamePlaceholder");
        String defaultBookName = defaultBookNameLocator.inputValue();
        Locator chapterDropdownLocator = super.page.getByLabel("Chapter");
        Locator optionsLocator = chapterDropdownLocator.locator("option");
        assertEquals(getOrderedChapterNumberStringsInBook(defaultBookName), optionsLocator.allInnerTexts(), "Chapter dropdown options are not correct.");
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
    public void testCorrectDefaultChapterSelectedWhenDefaultsProvided(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {    
        super.navigateToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);
        Locator chapterDropdownLocator = super.page.getByLabel("Chapter:");
        Locator selectedOptionLocator = chapterDropdownLocator.locator("option:checked"); // CSS pseudo-class to get the currently selected option in the dropdown
        assertTrue(selectedOptionLocator.innerText().equals(defaultChapter), "The default selected chapter should be " + defaultChapter + ".");
    }

    @Test
    public void testCorrectDefaultChapterSelectedWhenDefaultsNotProvided() {
        super.navigateToIndexPage();
        Locator defaultChapterNumberLocator = super.page.getByPlaceholder("defaultChapterNumberPlaceholder");
        String defaultChapterNumber = defaultChapterNumberLocator.inputValue();
        Locator chapterDropdownLocator = super.page.getByLabel("Chapter:");
        Locator selectedOptionLocator = chapterDropdownLocator.locator("option:checked"); // CSS pseudo-class to get the currently selected option in the dropdown
        assertTrue(selectedOptionLocator.innerText().equals(defaultChapterNumber), "The default selected chapter should be " + defaultChapterNumber + ".");
    }
    
}
