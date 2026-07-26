from playwright.sync_api import sync_playwright
import pandas as pd

URL = "https://example.com"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set True for background execution
    page = browser.new_page()

    # Open webpage
    page.goto(URL, wait_until="networkidle")

    # Wait until table is visible
    page.wait_for_selector("table")

    # Get the first table
    table = page.locator("table").first

    # Extract headers
    headers = table.locator("thead tr th").all_inner_texts()

    # Extract rows
    rows = []
    for row in table.locator("tbody tr").all():
        rows.append(row.locator("td").all_inner_texts())

    browser.close()

# Convert to DataFrame
df = pd.DataFrame(rows, columns=headers)

print(df)

# Save to CSV
df.to_csv("table_data.csv", index=False)
