package io.delario.pleiades.pages;
import java.util.List;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.options.SelectOption;

public class Dropdown {
    private final Locator locator;

    public Dropdown(Locator locator) {
        this.locator = locator;
    }

    public String getSelectedOptionText() {
        return this.locator.locator("option:checked").innerText();
    }

    public List<String> getOptionTexts() {
        return this.locator.locator("option").allInnerTexts();
    }

    public void selectOptionByLabel(String label) {
        this.locator.selectOption(new SelectOption().setLabel(label));
    }}
