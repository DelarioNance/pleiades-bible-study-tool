package io.delario.pleiades.screenone.selection;

import io.delario.pleiades.screenone.AbstractScreenOneTest;
import static io.delario.pleiades.utils.BibleCanon.getOrderedVerseNumberStringsInChapter;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;


import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import java.util.List;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.options.SelectOption;


public class ScreenOneChapterSelectionTest extends AbstractScreenOneTest{
    @ParameterizedTest
    @CsvSource({
        "Genesis, 1, 1, 1",
        "Genesis, 50, 26, 5",
        "Matthew, 1, 25, 5",
        "Matthew, 28, 1, 1",
        "Revelation, 1, 1, 1",
        "Revelation, 22, 21, 5",
    }) // Pairwise + BVA + ECP
    public void testSameChapterSelectionDoesNotChangeUI(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        super.navigateToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);

        Locator preSelectBookDropdownLocator = super.page.getByLabel("Book");
        Locator preSelectChapterDropdownLocator = super.page.getByLabel("Chapter");
        Locator preSelectVerseDropdownLocator = super.page.getByLabel("Verse");
        Locator preSelectDepthDropdownLocator = super.page.getByLabel("Depth");

        List<String> preSelectBookOptions = preSelectBookDropdownLocator.locator("option").allInnerTexts();
        List<String> preSelectChapterOptions = preSelectChapterDropdownLocator.locator("option").allInnerTexts();
        List<String> preSelectVerseOptions = preSelectVerseDropdownLocator.locator("option").allInnerTexts();
        List<String> preSelectDepthOptions = preSelectDepthDropdownLocator.locator("option").allInnerTexts();

        String preSelectedBookText = preSelectBookDropdownLocator.locator("option:checked").innerText();
        String preSelectedChapterText = preSelectChapterDropdownLocator.locator("option:checked").innerText();
        String preSelectedVerseText = preSelectVerseDropdownLocator.locator("option:checked").innerText();
        String preSelectedDepthText = preSelectDepthDropdownLocator.locator("option:checked").innerText();

        super.page.getByLabel("Chapter:").selectOption(new SelectOption().setLabel(defaultChapter)); // select the option whose frontend text is the default book

        Locator postSelectBookDropdownLocator = super.page.getByLabel("Book");
        Locator postSelectChapterDropdownLocator = super.page.getByLabel("Chapter");
        Locator postSelectVerseDropdownLocator = super.page.getByLabel("Verse");
        Locator postSelectDepthDropdownLocator = super.page.getByLabel("Depth");

        List<String> postSelectBookOptions = postSelectBookDropdownLocator.locator("option").allInnerTexts();
        List<String> postSelectChapterOptions = postSelectChapterDropdownLocator.locator("option").allInnerTexts();
        List<String> postSelectVerseOptions = postSelectVerseDropdownLocator.locator("option").allInnerTexts();
        List<String> postSelectDepthOptions = postSelectDepthDropdownLocator.locator("option").allInnerTexts();
        
        String postSelectedBookText = postSelectBookDropdownLocator.locator("option:checked").innerText();
        String postSelectedChapterText = postSelectChapterDropdownLocator.locator("option:checked").innerText();
        String postSelectedVerseText = postSelectVerseDropdownLocator.locator("option:checked").innerText();
        String postSelectedDepthText = postSelectDepthDropdownLocator.locator("option:checked").innerText();

        assertEquals(postSelectBookOptions, preSelectBookOptions, "Chapter selection changed the book dropdown options.");
        assertEquals(postSelectChapterOptions, preSelectChapterOptions, "Chapter selection changed the chapter dropdown options.");
        assertEquals(postSelectVerseOptions, preSelectVerseOptions, "Chapter selection changed the verse dropdown options.");
        assertEquals(postSelectDepthOptions, preSelectDepthOptions, "Chapter selection changed the depth dropdown options.");

        assertEquals(postSelectedBookText, preSelectedBookText, "Chapter selection changed the selected book");
        assertEquals(postSelectedChapterText, preSelectedChapterText, "Chapter selection changed the selected chapter");
        assertEquals(postSelectedVerseText, preSelectedVerseText, "Chapter selection changed the selected verse");
        assertEquals(postSelectedDepthText, preSelectedDepthText, "Chapter selection changed the selected depth");
    }
}
