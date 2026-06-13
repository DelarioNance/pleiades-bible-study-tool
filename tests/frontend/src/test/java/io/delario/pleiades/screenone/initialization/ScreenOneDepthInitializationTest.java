package io.delario.pleiades.screenone.initialization;

import io.delario.pleiades.screenone.AbstractScreenOneTest;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import com.microsoft.playwright.Locator;

public class ScreenOneDepthInitializationTest extends AbstractScreenOneTest {
    @Test
    public void testDepthDropdownIsVisibleWhenDefaultsProvided() {
        super.navigateToIndexPage("Genesis", "1", "1", "1");
        Locator depthDropdownLocator = super.page.getByLabel("Depth:");
        assertTrue(depthDropdownLocator.isVisible(), 
            "The depth dropdown should be visible on the screen.");
    }

    @Test
    public void testDepthDropdownIsVisibleWhenDefaultsNotProvided() {
        super.navigateToIndexPage();
        Locator depthDropdownLocator = super.page.getByLabel("Depth:");
        assertTrue(depthDropdownLocator.isVisible(), 
            "The depth dropdown should be visible on the screen.");
    }

    @ParameterizedTest
    @CsvSource({
        "2 Chronicles, 18, 31, 4",
    }) // could have more cases, but it's not a big deal if the wrong depth is shown
    public void testCorrectDepthDropdownOptionListWhenDefaultsProvided(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        super.navigateToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);

        Locator depthDropdownLocator = super.page.getByLabel("Depth:");
        Locator optionsLocator = depthDropdownLocator.locator("option");

        assertEquals(
            List.of("1", "2", "3", "4", "5"),
            optionsLocator.allInnerTexts(),
            "Depth dropdown options are not correct."
        );
    }

    @Test
    public void testCorrectDepthDropdownOptionListWhenDefaultsNotProvided() {
        super.navigateToIndexPage();

        Locator depthDropdownLocator = super.page.getByLabel("Depth:");
        Locator optionsLocator = depthDropdownLocator.locator("option");

        assertEquals(
            List.of("1", "2", "3", "4", "5"),
            optionsLocator.allInnerTexts(),
            "Depth dropdown options are not correct."
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
    }) // Pairwise + BVA + ECP
    public void testCorrectDefaultDepthSelectedWhenDefaultsProvided(
        String defaultBook,
        String defaultChapter,
        String defaultVerse,
        String defaultDepth
    ) {
        super.navigateToIndexPage(defaultBook, defaultChapter, defaultVerse, defaultDepth);

        Locator depthDropdownLocator = super.page.getByLabel("Depth");
        Locator selectedOptionLocator = depthDropdownLocator.locator("option:checked");

        assertEquals(
            defaultDepth,
            selectedOptionLocator.innerText(),
            "The default selected depth should be " + defaultDepth + "."
        );
    }

    @Test
    public void testCorrectDefaultDepthSelectedWhenDefaultsNotProvided() {
        super.navigateToIndexPage();

        Locator defaultDepthLocator = super.page.getByPlaceholder("defaultDepthPlaceholder");
        String defaultDepth = defaultDepthLocator.inputValue();

        Locator depthDropdownLocator = super.page.getByLabel("Depth:");
        Locator selectedOptionLocator = depthDropdownLocator.locator("option:checked");

        assertEquals(
            defaultDepth,
            selectedOptionLocator.innerText(),
            "The default selected depth should be " + defaultDepth + "."
        );
    }
}
