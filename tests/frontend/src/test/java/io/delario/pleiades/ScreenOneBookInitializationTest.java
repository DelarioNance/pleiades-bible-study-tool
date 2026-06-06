package io.delario.pleiades;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

import com.microsoft.playwright.Locator;

/**
 * Unit test for simple App.
 */
public class ScreenOneBookInitializationTest extends AbstractScreenOneInitializationTest{

    @Test
    public void testCorrectBookLabelExists() {
        Locator bookLabel = page.getByLabel("Book:"); // similar to SQL views in the sense that it lets us get the real-time element on the page that has the label "Book:".
        assertTrue(bookLabel.isVisible(), "The book label should be visible on the screen."); // this will fail if the label isn't attached to a select element
    }
}
