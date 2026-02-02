from playwright.sync_api import sync_playwright, expect
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Navigating to home...")
        try:
            page.goto("http://localhost:3000")
        except Exception as e:
            print(f"Failed to load page: {e}")
            return

        # Check title
        print("Checking title...")
        expect(page.get_by_role("heading", name="Zero-Scout")).to_be_visible()

        # Type "Google" in input
        print("Typing query...")
        page.get_by_placeholder("Search tickers").fill("Google")

        # Click Scout
        print("Clicking Scout...")
        page.get_by_role("button", name="Scout").click()

        # Wait for "Google" result
        print("Waiting for results...")
        # Since MOCK_SEARCH is on, it should be fast, but we have 2s throttle if multiple tickers.
        # Here just one ticker.
        # Check for headline
        expect(page.get_by_text("Mock News for Google news")).to_be_visible(timeout=10000)

        # Take screenshot
        print("Taking screenshot...")
        page.screenshot(path="verification.png", full_page=True)

        browser.close()
        print("Done.")

if __name__ == "__main__":
    run()
