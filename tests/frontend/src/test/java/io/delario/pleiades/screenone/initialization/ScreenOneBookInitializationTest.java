package io.delario.pleiades.screenone.initialization;

import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;
import io.delario.pleiades.pages.IndexPage;
import io.delario.pleiades.screenone.AbstractScreenOneTest;
import static io.delario.pleiades.utils.BibleCanon.BOOKS_IN_NUMBER_ORDER;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import java.util.List;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import com.microsoft.playwright.Locator;

public class ScreenOneBookInitializationTest extends AbstractScreenOneTest {
    @Test
    public void testBookDrowndownIsVisibleWhenDefaultsNotProvided() {
        IndexPage indexPage = super.goToIndexPage();
        Locator bookDropdown = indexPage.bookDropdown;
        assertThat(bookDropdown).isVisible();
    }

    @Test
    public void testBookDrowndownIsVisibleWhenDefaultsProvided() {
        IndexPage indexPage = super.goToIndexPage("Genesis", "1", "1", "1");
        Locator bookDropdown = indexPage.bookDropdown;
        assertThat(bookDropdown).isVisible();
    }

    @Test
    public void testCorrectBookDropdownOptionListWhenDefaultsNotProvided() {
        IndexPage indexPage = super.goToIndexPage();
        List<String> bookOptions = indexPage.getBookOptions();

        assertEquals(
            BOOKS_IN_NUMBER_ORDER,
            bookOptions,
            "The book dropdown should contain the correct list of books in the correct order."
        );
    }

    @Test
    public void testCorrectBookDropdownOptionListWhenDefaultsProvided() {
        IndexPage indexPage = super.goToIndexPage("Genesis", "1", "1", "1");
        List<String> bookOptions = indexPage.getBookOptions();

        assertEquals(
            BOOKS_IN_NUMBER_ORDER,
            bookOptions,
            "The book dropdown should contain the correct list of books in the correct order."
        );
    }

    @Test
    public void testCorrectDefaultBookSelectedWhenDefaultsNotProvided() {
        IndexPage indexPage = super.goToIndexPage();
        String selectedBook = indexPage.getSelectedBook();

        String defaultBookName = super.getBackendDefaultBookName();

        assertEquals(
            defaultBookName,
            selectedBook,
            "The default selected book should be " + defaultBookName + "."
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
    public void testCorrectDefaultBookSelectedWhenDefaultsProvided(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        IndexPage indexPage = super.goToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);
        String selectedBook = indexPage.getSelectedBook();

        assertEquals(
            defaultBook,
            selectedBook,
            "The default selected book should be " + defaultBook + "."
        );
    }
}
