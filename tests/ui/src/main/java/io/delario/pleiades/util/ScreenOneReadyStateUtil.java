package io.delario.pleiades.util;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.options.WaitForSelectorState;

public final class ScreenOneReadyStateUtil {

    /**
     * Synchronizes the DOM so tests never interact with partially-loaded dropdowns.
     *
     * Playwright auto-waits for visibility and attachment of the dropdown element,
     * but it does NOT wait for <option> children to be populated.
     *
     * The Index page loads dropdown options asynchronously based on:
     *  - default book
     *  - default chapter
     *  - default verse
     *  - default depth
     *
     * Without this method, tests would be flaky.
     * With this method, tests are deterministic and stable.
     */
    public static void waitForReadyState(Page page) {
        // The Playwright with Java docs are incomplete, so you must inspect the definition
        // of the waitFor method, WaitForOptions class, setState method, and WaitForSelectorState enum 
        // to understand how this works
        page.getByLabel("Book").locator("option").first().waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.ATTACHED));
        page.getByLabel("Chapter").locator("option").first().waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.ATTACHED));
        page.getByLabel("Verse").locator("option").first().waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.ATTACHED));
        page.getByLabel("Depth").locator("option").first().waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.ATTACHED));
    }
}
