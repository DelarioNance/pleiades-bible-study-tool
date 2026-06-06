package io.delario.pleiades;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;

public abstract class AbstractScreenOneInitializationTest {
    protected Playwright playwright;
    protected Browser browser;
    protected Page page; 

    @BeforeEach
    public void init() {
        playwright = Playwright.create();
        browser = playwright.chromium().launch(new com.microsoft.playwright.BrowserType.LaunchOptions().setSlowMo(50));
        page = browser.newPage();
        page.navigate("http://127.0.0.1:8000");
    }

    @AfterEach
    public void teardown() {
        // possibly close the browser and playwright instances to free up resources
    }
}
