package io.delario.pleiades.screenone.initialization;

import io.delario.pleiades.pages.IndexPage;

import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;
import io.delario.pleiades.screenone.AbstractScreenOneTest;
import static io.delario.pleiades.utils.BibleCanon.getOrderedChapterNumberStringsInBook;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import java.util.List;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import com.microsoft.playwright.Locator;

public class ScreenOneChapterInitializationTest extends AbstractScreenOneTest {

    @Test
    public void testChapterDropdownIsVisibleWhenDefaultsProvided() {
        IndexPage indexPage = super.goToIndexPage("Genesis", "1", "1", "1");
        Locator chapterDropdownLocator = indexPage.chapterDropdown;
        assertThat(chapterDropdownLocator).isVisible();
    }

    @Test
    public void testChapterDropdownIsVisibleWhenDefaultsNotProvided() {
        IndexPage indexPage = super.goToIndexPage();
        Locator chapterDropdownLocator = indexPage.chapterDropdown;
        assertThat(chapterDropdownLocator).isVisible();
    }

    @ParameterizedTest
    @CsvSource({
        "2 Chronicles, 18, 31, 3",
    })
    public void testCorrectChapterDropdownOptionListWhenDefaultsProvided(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        IndexPage indexPage = super.goToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);
        List<String> chapterOptions = indexPage.getChapterOptions();

        assertEquals(
            getOrderedChapterNumberStringsInBook(defaultBook),
            chapterOptions,
            "Chapter dropdown options are not correct."
        );
    }

    @Test
    public void testCorrectChapterDropdownOptionListWhenDefaultsNotProvided() {
        IndexPage indexPage = super.goToIndexPage();
        List<String> chapterOptions = indexPage.getChapterOptions();

        String defaultBookName = super.getBackendDefaultBookName();

        assertEquals(
            getOrderedChapterNumberStringsInBook(defaultBookName),
            chapterOptions,
            "Chapter dropdown options are not correct."
        );
    }

    @ParameterizedTest
    @CsvSource({
        "Genesis, 1, 1, 1",
        "Genesis, 50, 26, 3",
        "Matthew, 1, 25, 3",
        "Matthew, 28, 1, 1",
        "Revelation, 1, 1, 1",
        "Revelation, 22, 21, 3",
    })
    public void testCorrectDefaultChapterSelectedWhenDefaultsProvided(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        IndexPage indexPage = super.goToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);
        String selectedChapter = indexPage.getSelectedChapter();

        assertEquals(
            defaultChapter,
            selectedChapter,
            "The default selected chapter should be " + defaultChapter + "."
        );
    }

    @Test
    public void testCorrectDefaultChapterSelectedWhenDefaultsNotProvided() {
        IndexPage indexPage = super.goToIndexPage();
        String selectedChapter = indexPage.getSelectedChapter();

        String defaultChapterNumber = super.getBackendDefaultChapterNumber();

        assertEquals(
            defaultChapterNumber,
            selectedChapter,
            "The default selected chapter should be " + defaultChapterNumber + "."
        );
    }
}
