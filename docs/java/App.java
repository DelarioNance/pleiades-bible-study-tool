package io.delario.pleiades;

import com.microsoft.playwright.*;
import java.nio.file.Paths; // Java equivalent of Python's "pathlib" for handling file paths

public class App {
    public static void main(String[] args) {
        try (Playwright playwright = Playwright.create()) { // Java equivalent of Python's "with" statement for resource management
            Browser browser = playwright.chromium().launch(new BrowserType.LaunchOptions().setHeadless(false).setSlowMo((50)));
            Page page = browser.newPage();
            page.navigate("https://playwright.dev");
            System.out.println(page.title());
            page.screenshot(new Page.ScreenshotOptions().setPath(Paths.get("example.png")));    
        }
    }
}