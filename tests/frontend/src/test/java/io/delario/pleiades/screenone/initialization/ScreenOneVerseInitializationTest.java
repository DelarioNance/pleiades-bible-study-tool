package io.delario.pleiades.screenone.initialization;

import io.delario.pleiades.screenone.AbstractScreenOneTest;
import static io.delario.pleiades.utils.BibleCanon.getOrderedVerseNumberStringsInChapter;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import com.microsoft.playwright.Locator;

public class ScreenOneVerseInitializationTest extends AbstractScreenOneTest {

    // ------------------------------------------------------------
    // Visibility Tests
    // ------------------------------------------------------------

    @Test
    public void testVerseDropdownIsVisibleWhenDefaultsProvided() {
        super.navigateToIndexPage("Genesis", "1", "1", "1");
        Locator verseDropdownLocator = super.page.getByLabel("Verse:");
        assertTrue(verseDropdownLocator.isVisible(), 
            "The verse dropdown should be visible on the screen.");
    }

    @Test
    public void testVerseDropdownIsVisibleWhenDefaultsNotProvided() {
        super.navigateToIndexPage();
        Locator verseDropdownLocator = super.page.getByLabel("Verse:");
        assertTrue(verseDropdownLocator.isVisible(), 
            "The verse dropdown should be visible on the screen.");
    }

    // ------------------------------------------------------------
    // Option List Tests
    // ------------------------------------------------------------

    @ParameterizedTest
    @CsvSource({
        "2 Chronicles, 18, 31, 4",
    })
    public void testCorrectVerseDropdownOptionListWhenDefaultsProvided(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        super.navigateToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);

        Locator verseDropdownLocator = super.page.getByLabel("Verse");
        Locator optionsLocator = verseDropdownLocator.locator("option");

        assertEquals(
            getOrderedVerseNumberStringsInChapter(defaultBook, defaultChapter),
            optionsLocator.allInnerTexts(),
            "Verse dropdown options are not correct."
        );
    }

    @Test
    public void testCorrectVerseDropdownOptionListWhenDefaultsNotProvided() {
        super.navigateToIndexPage();

        Locator defaultBookNameLocator = super.page.getByPlaceholder("defaultBookNamePlaceholder");
        String defaultBookName = defaultBookNameLocator.inputValue();

        Locator defaultChapterNumberLocator = super.page.getByPlaceholder("defaultChapterNumberPlaceholder");
        String defaultChapterNumber = defaultChapterNumberLocator.inputValue();

        Locator verseDropdownLocator = super.page.getByLabel("Verse");
        Locator optionsLocator = verseDropdownLocator.locator("option");

        assertEquals(
            getOrderedVerseNumberStringsInChapter(defaultBookName, defaultChapterNumber),
            optionsLocator.allInnerTexts(),
            "Verse dropdown options are not correct."
        );
    }

    // ------------------------------------------------------------
    // Default Selection Tests
    // ------------------------------------------------------------

    @ParameterizedTest
    @CsvSource({
        "Genesis, 1, 1, 1",
        "Genesis, 50, 26, 5",
        "Matthew, 1, 25, 5",
        "Matthew, 28, 1, 1",
        "Revelation, 1, 1, 1",
        "Revelation, 22, 21, 5",
    }) // Pairwise + BVA + ECP
    public void testCorrectDefaultVerseSelectedWhenDefaultsProvided(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        super.navigateToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);

        Locator verseDropdownLocator = super.page.getByLabel("Verse:");
        Locator selectedOptionLocator = verseDropdownLocator.locator("option:checked");

        assertEquals(
            defaultVerse,
            selectedOptionLocator.innerText(),
            "The default selected verse should be " + defaultVerse + "."
        );
    }

    @Test
    public void testCorrectDefaultVerseSelectedWhenDefaultsNotProvided() {
        super.navigateToIndexPage();

        Locator defaultVerseNumberLocator = super.page.getByPlaceholder("defaultVerseNumberPlaceholder");
        String defaultVerseNumber = defaultVerseNumberLocator.inputValue();

        Locator verseDropdownLocator = super.page.getByLabel("Verse:");
        Locator selectedOptionLocator = verseDropdownLocator.locator("option:checked");

        assertEquals(
            defaultVerseNumber,
            selectedOptionLocator.innerText(),
            "The default selected verse should be " + defaultVerseNumber + "."
        );
    }
}
