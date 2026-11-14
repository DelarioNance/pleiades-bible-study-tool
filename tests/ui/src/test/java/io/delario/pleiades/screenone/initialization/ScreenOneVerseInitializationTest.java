package io.delario.pleiades.screenone.initialization;

import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;
import io.delario.pleiades.pages.IndexPage;
import io.delario.pleiades.screenone.AbstractScreenOneTest;
import static io.delario.pleiades.utils.BibleCanon.getOrderedVerseNumberStringsInChapter;
import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import java.util.List;

import com.microsoft.playwright.Locator;

public class ScreenOneVerseInitializationTest extends AbstractScreenOneTest {

    // ------------------------------------------------------------
    // Visibility Tests
    // ------------------------------------------------------------

    @Test
    public void testVerseDropdownIsVisibleWhenDefaultsProvided() {
        IndexPage indexPage = super.goToIndexPage("Genesis", "1", "1", "1");
        Locator verseDropdown = indexPage.verseDropdown;

        assertThat(verseDropdown).isVisible();
    }

    @Test
    public void testVerseDropdownIsVisibleWhenDefaultsNotProvided() {
        IndexPage indexPage = super.goToIndexPage();
        Locator verseDropdown = indexPage.verseDropdown;

        assertThat(verseDropdown).isVisible();
    }

    // ------------------------------------------------------------
    // Option List Tests
    // ------------------------------------------------------------

    @ParameterizedTest
    @CsvSource({
        "2 Chronicles, 18, 31, 3",
    })
    public void testCorrectVerseDropdownOptionListWhenDefaultsProvided(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        IndexPage indexPage = super.goToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);
        List<String> verseOptions = indexPage.getVerseOptions();

        assertEquals(
            getOrderedVerseNumberStringsInChapter(defaultBook, defaultChapter),
            verseOptions,
            "Verse dropdown options are not correct."
        );
    }

    @Test
    public void testCorrectVerseDropdownOptionListWhenDefaultsNotProvided() {
        IndexPage indexPage = super.goToIndexPage();
        List<String> verseOptions = indexPage.getVerseOptions();

        String defaultBookName = super.getBackendDefaultBookName();
        String defaultChapterNumber = super.getBackendDefaultChapterNumber();

        assertEquals(
            getOrderedVerseNumberStringsInChapter(defaultBookName, defaultChapterNumber),
            verseOptions,
            "Verse dropdown options are not correct."
        );
    }

    // ------------------------------------------------------------
    // Default Selection Tests
    // ------------------------------------------------------------

    @ParameterizedTest
    @CsvSource({
        "Genesis, 1, 1, 1",
        "Genesis, 50, 26, 3",
        "Matthew, 1, 25, 3",
        "Matthew, 28, 1, 1",
        "Revelation, 1, 1, 1",
        "Revelation, 22, 21, 3",
    })
    public void testCorrectDefaultVerseSelectedWhenDefaultsProvided(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        IndexPage indexPage = super.goToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);
        String selectedVerse = indexPage.getSelectedVerse();

        assertEquals(
            defaultVerse,
            selectedVerse,
            "The default selected verse should be " + defaultVerse + "."
        );
    }

    @Test
    public void testCorrectDefaultVerseSelectedWhenDefaultsNotProvided() {
        IndexPage indexPage = super.goToIndexPage();
        String selectedVerse = indexPage.getSelectedVerse();

        String defaultVerseNumber = super.getBackendDefaultVerseNumber();

        assertEquals(
            defaultVerseNumber,
            selectedVerse,
            "The default selected verse should be " + defaultVerseNumber + "."
        );
    }
}
