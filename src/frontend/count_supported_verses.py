from playwright.sync_api import expect, sync_playwright
import pandas as pd


PLEIADES_URL = "https://pleiades-bible-study-tool.fastapicloud.dev/"
HEADLESS = True  # Set to False to see the browser in action
TOTAL_VERSES = 31102

def main():
    data_list = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        page.goto(PLEIADES_URL)

        book_dropdown = page.get_by_label("Book:")
        chapter_dropdown = page.get_by_label("Chapter:")
        verse_dropdown = page.get_by_label("Verse:")
        selection_counter = page.get_by_placeholder("selectionCounter")
        results = page.get_by_test_id("traversal-results")
        submit_button = page.get_by_test_id("submit-button")
        submission_counter = page.get_by_placeholder("submissionCounter")

        verse_cnt = 0

        book_options = book_dropdown.all_inner_texts()[0].split("\n")
        for book in book_options:
            select_option(book_dropdown, book, selection_counter)

            chapter_options = chapter_dropdown.all_inner_texts()[0].split("\n")
            for chapter in chapter_options:
                select_option(chapter_dropdown, chapter, selection_counter)

                verse_options = verse_dropdown.all_inner_texts()[0].split("\n")
                for verse in verse_options:
                    verse_cnt += 1
                    select_option(verse_dropdown, verse, selection_counter)
                    submit(submit_button, submission_counter)

                    layer_2_count = count_verses(results, "1st-Degree Connections")
                    layer_3_count = count_verses(results, "2nd-Degree Connections")

                    data_list.append({
                        "Book": book,
                        "Chapter": chapter,
                        "Verse": verse,
                        "Layer 2 Count": layer_2_count,
                        "Layer 3 Count": layer_3_count
                    })

                    print(f"Processed {book} {chapter}:{verse}")

        browser.close()

        df = pd.DataFrame(data_list)
        df.to_csv("supported_verses.csv")


def select_option(dropdown, label, selection_counter):
    pre_selection_counter = selection_counter.get_attribute("data-counter")
    dropdown.select_option(label=label)
    expect(selection_counter).to_have_attribute("data-counter", str(int(pre_selection_counter) + 1))


def submit(submit_button, submission_counter):
    pre_submission_counter = int(submission_counter.get_attribute("data-counter"))
    submit_button.click()
    expect(submission_counter).to_have_attribute("data-counter", str(pre_submission_counter + 1))


def count_verses(results, degree_text):
    layer = results.locator(".traversal-layer").filter(
        has=results.locator("span", has_text=degree_text)
    )
    return layer.locator("div.traversal-verse").count()


if __name__ == "__main__":
    main()