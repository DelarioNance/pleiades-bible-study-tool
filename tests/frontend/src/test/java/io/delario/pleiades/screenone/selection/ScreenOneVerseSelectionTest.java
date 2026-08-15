package io.delario.pleiades.screenone.selection;

import io.delario.pleiades.pages.IndexPage;
import io.delario.pleiades.screenone.AbstractScreenOneTest;
import static io.delario.pleiades.utils.BibleCanon.getOrderedVerseNumberStringsInChapter;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import java.util.List;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.options.SelectOption;


public class ScreenOneVerseSelectionTest extends AbstractScreenOneTest{
    @ParameterizedTest
    @CsvSource({
        "Genesis, 1, 1, 1",
        "Genesis, 50, 26, 5",
        "Matthew, 1, 25, 5",
        "Matthew, 28, 1, 1",
        "Revelation, 1, 1, 1",
        "Revelation, 22, 21, 5",
    }) // Pairwise + BVA + ECP
    public void testSameVerseSelectionDoesNotChangeUI(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        IndexPage indexPage = super.goToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);

        List<String> preSelectBookOptions = indexPage.getBookOptions();
        List<String> preSelectChapterOptions = indexPage.getChapterOptions();
        List<String> preSelectVerseOptions = indexPage.getVerseOptions();
        List<String> preSelectDepthOptions = indexPage.getDepthOptions();

        String preSelectBookSelection = indexPage.getSelectedBook();
        String preSelectChapterSelection = indexPage.getSelectedChapter();
        String preSelectVerseSelection = indexPage.getSelectedVerse();
        String preSelectDepthSelection = indexPage.getSelectedDepth();

        indexPage.selectVerse(defaultVerse);

        Locator postSelectBookDropdownLocator = super.page.getByLabel("Book");
        Locator postSelectChapterDropdownLocator = super.page.getByLabel("Chapter");
        Locator postSelectVerseDropdownLocator = super.page.getByLabel("Verse");
        Locator postSelectDepthDropdownLocator = super.page.getByLabel("Depth");

        List<String> postSelectBookOptions = indexPage.getBookOptions();
        List<String> postSelectChapterOptions = indexPage.getChapterOptions();
        List<String> postSelectVerseOptions = indexPage.getVerseOptions();
        List<String> postSelectDepthOptions = indexPage.getDepthOptions();

        String postSelectBookSelection = indexPage.getSelectedBook();
        String postSelectChapterSelection = indexPage.getSelectedChapter();
        String postSelectVerseSelection = indexPage.getSelectedVerse();
        String postSelectDepthSelection = indexPage.getSelectedDepth();

        assertEquals(preSelectBookOptions, postSelectBookOptions);
        assertEquals(preSelectChapterOptions, postSelectChapterOptions);
        assertEquals(preSelectVerseOptions, postSelectVerseOptions);
        assertEquals(preSelectDepthOptions, postSelectDepthOptions);

        assertEquals(preSelectBookSelection, postSelectBookSelection);
        assertEquals(preSelectChapterSelection, postSelectChapterSelection);
        assertEquals(preSelectVerseSelection, postSelectVerseSelection);
        assertEquals(preSelectDepthSelection, postSelectDepthSelection);
    }


    @ParameterizedTest()
    @CsvSource({
        "Genesis, 1, 1, 1, 31",
        "Genesis, 1, 10, 1, 2",
        "Obadiah, 1, 1, 1, 15",
        "Revelation, 9, 4, 1, 11",
        "Revelation, 9, 21, 1, 1",
        "Genesis, 22, 1, 1, 1",
        "Revelation, 22, 21, 1, 1"
    }) // ECP (first, middle, last book) + Pairwise ({first,middle,last} x {first,middle,last}) + testing going from a non-1 chapter to a book with only 1 chapter
    public void testDifferentVerseSelectionChangesUICorrectly(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth,
        String newVerse
    ) {
        IndexPage indexPage = super.goToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);

        List<String> preSelectBookOptions = indexPage.getBookOptions();
        List<String> preSelectChapterOptions = indexPage.getChapterOptions();
        List<String> preSelectVerseOptions = indexPage.getVerseOptions();
        List<String> preSelectDepthOptions = indexPage.getDepthOptions();

        String preSelectBookSelection = indexPage.getSelectedBook();
        String preSelectChapterSelection = indexPage.getSelectedChapter();
        String preSelectVerseSelection = indexPage.getSelectedVerse();
        String preSelectDepthSelection = indexPage.getSelectedDepth();

        indexPage.selectVerse(newVerse);
        
        List<String> postSelectBookOptions = indexPage.getBookOptions();
        List<String> postSelectChapterOptions = indexPage.getChapterOptions();
        List<String> postSelectVerseOptions = indexPage.getVerseOptions();
        List<String> postSelectDepthOptions = indexPage.getDepthOptions();

        String postSelectBookSelection = indexPage.getSelectedBook();
        String postSelectChapterSelection = indexPage.getSelectedChapter();
        String postSelectVerseSelection = indexPage.getSelectedVerse();
        String postSelectDepthSelection = indexPage.getSelectedDepth();

        assertEquals(preSelectBookOptions, postSelectBookOptions);
        assertEquals(preSelectChapterOptions, postSelectChapterOptions);
        assertEquals(preSelectVerseOptions, postSelectVerseOptions);
        assertEquals(preSelectDepthOptions, postSelectDepthOptions);

        assertEquals(preSelectBookSelection, postSelectBookSelection);
        assertEquals(preSelectChapterSelection, postSelectChapterSelection);
        assertEquals(newVerse, postSelectVerseSelection);
        assertEquals(preSelectDepthSelection, postSelectDepthSelection);
    }
}
