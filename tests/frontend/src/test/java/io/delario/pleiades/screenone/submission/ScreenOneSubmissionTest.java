package io.delario.pleiades.screenone.submission;

import io.delario.pleiades.pages.IndexPage;
import io.delario.pleiades.screenone.AbstractScreenOneTest;
import static io.delario.pleiades.utils.BibleCanon.getOrderedVerseNumberStringsInChapter;
import static io.delario.pleiades.utils.BibleCanon.getOrderedChapterNumberStringsInBook;
import static io.delario.pleiades.utils.BibleCanon.BOOKS_IN_NUMBER_ORDER;
import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;


import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import java.util.List;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.options.SelectOption;


public class ScreenOneSubmissionTest extends AbstractScreenOneTest{
    @Test
    public void testSubmissionDoesNotBreakUI() {
        IndexPage indexPage = super.goToIndexPage();

        String preSelectTitleHeaderText = indexPage.getTitleHeaderText();
        List<String> preSelectBookOptions = indexPage.getBookOptions();
        List<String> preSelectChapterOptions = indexPage.getChapterOptions();
        List<String> preSelectVerseOptions = indexPage.getVerseOptions();
        List<String> preSelectDepthOptions = indexPage.getDepthOptions();

        indexPage.submitScriptureSelection();

        String postSelectTitleHeaderText = indexPage.getTitleHeaderText();
        List<String> postSelectBookOptions = indexPage.getBookOptions();
        List<String> postSelectChapterOptions = indexPage.getChapterOptions();
        List<String> postSelectVerseOptions = indexPage.getVerseOptions();
        List<String> postSelectDepthOptions = indexPage.getDepthOptions();

        assertEquals(preSelectTitleHeaderText, postSelectTitleHeaderText);
        assertEquals(preSelectBookOptions, postSelectBookOptions);
        assertEquals(preSelectChapterOptions, postSelectChapterOptions);
        assertEquals(preSelectVerseOptions, postSelectVerseOptions);
        assertEquals(preSelectDepthOptions, postSelectDepthOptions);
    }
}
