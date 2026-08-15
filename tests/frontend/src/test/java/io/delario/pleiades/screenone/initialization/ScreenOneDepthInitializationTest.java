package io.delario.pleiades.screenone.initialization;

import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;
import io.delario.pleiades.pages.IndexPage;
import io.delario.pleiades.screenone.AbstractScreenOneTest;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import com.microsoft.playwright.Locator;

public class ScreenOneDepthInitializationTest extends AbstractScreenOneTest {

    // ------------------------------------------------------------
    // Visibility Tests
    // ------------------------------------------------------------

    @Test
    public void testDepthDropdownIsVisibleWhenDefaultsProvided() {
        IndexPage indexPage = super.goToIndexPage("Genesis", "1", "1", "1");
        Locator depthDropdown = indexPage.depthDropdown;

        assertThat(depthDropdown).isVisible();
    }

    @Test
    public void testDepthDropdownIsVisibleWhenDefaultsNotProvided() {
        IndexPage indexPage = super.goToIndexPage();
        Locator depthDropdown = indexPage.depthDropdown;

        assertThat(depthDropdown).isVisible();
    }

    // ------------------------------------------------------------
    // Option List Tests
    // ------------------------------------------------------------

    @ParameterizedTest
    @CsvSource({
        "2 Chronicles, 18, 31, 4",
    })
    public void testCorrectDepthDropdownOptionListWhenDefaultsProvided(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        IndexPage indexPage = super.goToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);
        List<String> depthOptions = indexPage.getDepthOptions();

        assertEquals(
            List.of("1", "2", "3", "4", "5"),
            depthOptions,
            "Depth dropdown options are not correct."
        );
    }

    @Test
    public void testCorrectDepthDropdownOptionListWhenDefaultsNotProvided() {
        IndexPage indexPage = super.goToIndexPage();
        List<String> depthOptions = indexPage.getDepthOptions();

        assertEquals(
            List.of("1", "2", "3", "4", "5"),
            depthOptions,
            "Depth dropdown options are not correct."
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
    })
    public void testCorrectDefaultDepthSelectedWhenDefaultsProvided(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        IndexPage indexPage = super.goToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);
        String selectedDepth = indexPage.getSelectedDepth();

        assertEquals(
            defaultDepth,
            selectedDepth,
            "The default selected depth should be " + defaultDepth + "."
        );
    }

    @Test
    public void testCorrectDefaultDepthSelectedWhenDefaultsNotProvided() {
        IndexPage indexPage = super.goToIndexPage();
        String selectedDepth = indexPage.getSelectedDepth();

        String defaultDepth = super.getBackendDefaultDepth();

        assertEquals(
            defaultDepth,
            selectedDepth,
            "The default selected depth should be " + defaultDepth + "."
        );
    }
}
