package io.delario.pleiades.screenone.selection;

import io.delario.pleiades.pages.IndexPage;
import io.delario.pleiades.screenone.AbstractScreenOneTest;
import static io.delario.pleiades.utils.BibleCanon.getOrderedVerseNumberStringsInChapter;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;

import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import java.util.List;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.options.SelectOption;

@Disabled("Depth dropdown is hidden")
public class ScreenOneDepthSelectionTest extends AbstractScreenOneTest{
    @ParameterizedTest
    @CsvSource({
        "Genesis, 1, 1, 1",
        "Genesis, 50, 26, 3",
        "Matthew, 1, 25, 3",
        "Matthew, 28, 1, 1",
        "Revelation, 1, 1, 1",
        "Revelation, 22, 21, 3",
    }) // Pairwise + BVA + ECP
    public void testSameDepthSelectionDoesNotChangeUI(
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

        indexPage.selectDepth(defaultDepth);

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
        "Genesis, 1, 1, 1, 2",
        "Genesis, 1, 10, 1, 3",
        "Obadiah, 1, 1, 3, 1",
        "Revelation, 9, 4, 3, 1",
        "Revelation, 9, 21, 2, 3",
        "Genesis, 22, 1, 2, 1",
    })
    public void testDifferentDepthSelectionChangesUICorrectly(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth,
        String newDepth
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

        indexPage.selectDepth(newDepth);

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
        assertEquals(newDepth, postSelectDepthSelection);
    }
}
