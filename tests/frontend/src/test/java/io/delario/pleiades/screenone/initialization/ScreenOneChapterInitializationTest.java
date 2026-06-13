package io.delario.pleiades.screenone.initialization;

import io.delario.pleiades.screenone.AbstractScreenOneTest;
import static io.delario.pleiades.utils.BibleCanon.getOrderedChapterNumberStringsInBook;
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
        assertTrue(chapterDropdownLocator.isVisible(),
            "The chapter dropdown should be visible on the screen.");
    }

    @Test
    public void testChapterDropdownIsVisibleWhenDefaultsNotProvided() {
        super.navigateToIndexPage();
        Locator chapterDropdownLocator = super.page.getByLabel("Chapter:");
        assertTrue(chapterDropdownLocator.isVisible(),
            "The chapter dropdown should be visible on the screen.");
    }

    @ParameterizedTest
    @CsvSource({
        "2 Chronicles, 18, 31, 4",
    })
    public void testCorrectChapterDropdownOptionListWhenDefaultsProvided(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        super.navigateToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);
        Locator chapterDropdownLocator = super.page.getByLabel("Chapter");
        Locator optionsLocator = chapterDropdownLocator.locator("option");

        assertEquals(
            getOrderedChapterNumberStringsInBook(defaultBook),
            optionsLocator.allInnerTexts(),
            "Chapter dropdown options are not correct."
        );
    }

    @Test
    public void testCorrectChapterDropdownOptionListWhenDefaultsNotProvided() {
        super.navigateToIndexPage();

        Locator defaultBookNameLocator = super.page.getByPlaceholder("defaultBookNamePlaceholder");
        String defaultBookName = defaultBookNameLocator.inputValue();

        Locator chapterDropdownLocator = super.page.getByLabel("Chapter");
        Locator optionsLocator = chapterDropdownLocator.locator("option");

        assertEquals(
            getOrderedChapterNumberStringsInBook(defaultBookName),
            optionsLocator.allInnerTexts(),
            "Chapter dropdown options are not correct."
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
    public void testCorrectDefaultChapterSelectedWhenDefaultsProvided(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        super.navigateToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);

        Locator chapterDropdownLocator = super.page.getByLabel("Chapter:");
        Locator selectedOptionLocator = chapterDropdownLocator.locator("option:checked");

        assertEquals(
            defaultChapter,
            selectedOptionLocator.innerText(),
            "The default selected chapter should be " + defaultChapter + "."
        );
    }

    @Test
    public void testCorrectDefaultChapterSelectedWhenDefaultsNotProvided() {
        super.navigateToIndexPage();

        Locator defaultChapterNumberLocator = super.page.getByPlaceholder("defaultChapterNumberPlaceholder");
        String defaultChapterNumber = defaultChapterNumberLocator.inputValue();

        Locator chapterDropdownLocator = super.page.getByLabel("Chapter:");
        Locator selectedOptionLocator = chapterDropdownLocator.locator("option:checked");

        assertEquals(
            defaultChapterNumber,
            selectedOptionLocator.innerText(),
            "The default selected chapter should be " + defaultChapterNumber + "."
        );
    }
}
