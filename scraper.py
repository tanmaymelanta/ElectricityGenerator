from playwright.sync_api import sync_playwright
import pandas as pd

URL = "https://grid-india.in/en/reports/daily-psp-report"
print(URL)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    print(f"browser {browser}")
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    print(f"page {page}")
    page.goto(URL, wait_until="networkidle")
    print("page goto url")
    # Wait until page loads
    page.wait_for_selector("table")

    # Click Financial Year dropdown
    page.locator("div[role='button']").first.click()

    # Select 2013-14
    page.get_by_text("2013-14", exact=True).click()

    # Wait for table refresh
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    table = page.locator("table")

    headers = table.locator("thead th").all_inner_texts()

    rows = []

    for row in table.locator("tbody tr").all():
        rows.append(row.locator("td").all_inner_texts())

    browser.close()

df = pd.DataFrame(rows, columns=headers)

print(df)

df.to_csv("daily_psp_2013_14.csv", index=False)
