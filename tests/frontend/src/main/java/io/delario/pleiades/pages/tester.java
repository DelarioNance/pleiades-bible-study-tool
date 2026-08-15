package io.delario.pleiades.pages;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;

public class tester {
    public static void main(String[] args) {
        Playwright playwright;
        Browser browser;
        Page page; 
    
        playwright = Playwright.create();
        browser = playwright.chromium().launch(
            new com.microsoft.playwright.BrowserType.LaunchOptions()
        );
        page = browser.newPage();

        IndexPage index = IndexPage.navigateTo(page);

        System.out.println("Navigated to Index Page");
        System.out.println(index.getSelectedBook());
        System.out.println(index.getSelectedChapter());
        System.out.println(index.getSelectedVerse());
        System.out.println(index.getSelectedDepth());
        
        System.out.println(index.getBookOptions());
        System.out.println(index.getChapterOptions());
        System.out.println(index.getVerseOptions());
        System.out.println(index.getDepthOptions());

        System.out.println("Selecting Book, Chapter, Verse, and Depth...");
        index.selectBook("2 Chronicles");
        index.selectChapter("18");
        index.selectVerse("31");
        index.selectDepth("1");

        System.out.println("Selections made:");
        System.out.println(index.getSelectedBook());
        System.out.println(index.getSelectedChapter());
        System.out.println(index.getSelectedVerse());
        System.out.println(index.getSelectedDepth());

        System.out.println(index.getBookOptions());
        System.out.println(index.getChapterOptions());
        System.out.println(index.getVerseOptions());
        System.out.println(index.getDepthOptions());
    }
    
}
