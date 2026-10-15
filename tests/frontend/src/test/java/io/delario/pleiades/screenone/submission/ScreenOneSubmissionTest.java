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

import java.io.File;
import java.io.IOException;
import java.nio.file.FileSystems;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.fasterxml.jackson.core.exc.StreamReadException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.DatabindException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Route;
import com.microsoft.playwright.options.SelectOption;


public class ScreenOneSubmissionTest extends AbstractScreenOneTest{
    @Test
    public void testSubmissionDoesNotBreakUI() {
        IndexPage indexPage = super.goToIndexPage();

        String preSubmitTitleHeaderText = indexPage.getTitleHeaderText();
        List<String> preSubmitBookOptions = indexPage.getBookOptions();
        List<String> preSubmitChapterOptions = indexPage.getChapterOptions();
        List<String> preSubmitVerseOptions = indexPage.getVerseOptions();
        List<String> preSubmitDepthOptions = indexPage.getDepthOptions();

        indexPage.submitScriptureSelection();

        String postSubmitTitleHeaderText = indexPage.getTitleHeaderText();
        List<String> postSubmitBookOptions = indexPage.getBookOptions();
        List<String> postSubmitChapterOptions = indexPage.getChapterOptions();
        List<String> postSubmitVerseOptions = indexPage.getVerseOptions();
        List<String> postSubmitDepthOptions = indexPage.getDepthOptions();

        assertEquals(preSubmitTitleHeaderText, postSubmitTitleHeaderText);
        assertEquals(preSubmitBookOptions, postSubmitBookOptions);
        assertEquals(preSubmitChapterOptions, postSubmitChapterOptions);
        assertEquals(preSubmitVerseOptions, postSubmitVerseOptions);
        assertEquals(preSubmitDepthOptions, postSubmitDepthOptions);
    }

    @ParameterizedTest
    @CsvSource({
        "src/test/java/io/delario/pleiades/mocks/traversal_api_response/single_layer_mock.json, src/test/java/io/delario/pleiades/mocks/traversal_api_response/single_layer_expected.json",
        "src/test/java/io/delario/pleiades/mocks/traversal_api_response/dense_tree_mock.json, src/test/java/io/delario/pleiades/mocks/traversal_api_response/dense_tree_expected.json",
        "src/test/java/io/delario/pleiades/mocks/traversal_api_response/no_tree_mock.json, src/test/java/io/delario/pleiades/mocks/traversal_api_response/no_tree_expected.json",
    })
    public void testSubmissionDisplaysCorrectResults(String mockDataPathStr, String expectedDataPathStr) throws StreamReadException, DatabindException, IOException {
        Path mockDataPath = FileSystems.getDefault().getPath(mockDataPathStr);

        super.page.route("**/traversal_results", route -> {
            route.fulfill(new Route.FulfillOptions().setPath(mockDataPath));
        });
        
        IndexPage indexPage = super.goToIndexPage();
        indexPage.submitScriptureSelection();

        List<Map<String, String>> displayedVerses = indexPage.getDisplayedVerses();

        List<Map<String, String>> expected = new ObjectMapper().readValue(
            new File(expectedDataPathStr),
            new TypeReference<List<Map<String, String>>>() {}
        );

        assertEquals(expected, displayedVerses);
    }
}
