from playwright.sync_api import sync_playwright

def test_native_options():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1. Initial Navigation
        print("Going to Playwright website...")
        page.goto("https://playwright.dev/")
        page.wait_for_timeout(5000)

        # 2. Second Navigation
        print("Going to GitHub...")
        page.goto("https://github.com/")
        page.wait_for_timeout(5000)

        # 3. NAVIGATE BACK (Mimics the 'Back' arrow)
        print("Navigating Back...")
        page.go_back()
        print(f"Current URL: {page.url}")  # Will be playwright.dev
        page.wait_for_timeout(5000)

        # 4. NAVIGATE FORWARD (Mimics the 'Forward' arrow)
        print("Navigating Forward...")
        page.go_forward()

        print(f"Current URL: {page.url}")  # Will be github.com again
        page.wait_for_timeout(5000)

        # 5. REFRESH (Mimics 'F5' or the Reload button)
        print("Refreshing the page...")
        page.reload()

        # Alternative JavaScript using browser history
        page.evaluate("history.go(0)")
        page.wait_for_timeout(5000)

        browser.close()

def test_renavigate_to_current_url():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.google.com")
        page.wait_for_timeout(5000)
        current_url=page.url
        page.goto(current_url)
        page.wait_for_timeout(5000)
        browser.close()

def test_refresh_page_using_function_key():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.google.com")
        page.wait_for_timeout(5000)
        page.keyboard.press("F5")
        page.wait_for_load_state()
        page.wait_for_timeout(5000)
        browser.close()

def test_refresh_page_keyboard_commands():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page  = browser.new_page()
        page.goto("https://www.google.com")
        page.wait_for_timeout(5000)
        page.keyboard.press("Control+R")  # For Windows/Linux
        # page.keyboard.press("Command+R")  # For macOS
        page.wait_for_load_state()
        page.wait_for_timeout(5000)
        browser.close()


def test_refesh():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.google.com")
        page.wait_for_timeout(5000)
        page.evaluate("location.reload()")

# Standard JavaScript reload
#page.evaluate("location.reload()")

# Alternative JavaScript using browser history
#page.evaluate("history.go(0)")

# Alternative JavaScript using href reassignment
#page.evaluate("location.href = location.href")