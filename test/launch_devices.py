from playwright.sync_api import sync_playwright, expect

def test_maximize_chrome_browser():
    with sync_playwright() as page:
        iphone = page.devices['iPhone 16']
        chrome_browser=page.chromium.launch(headless=False)
        chrome_context=chrome_browser.new_context(**iphone)
        chrome_page=chrome_context.new_page()
        chrome_page.goto("https://www.google.com")
        print("Chrome Title:", chrome_page.title())
        expect(chrome_page).to_have_title("Google")
        chrome_page.wait_for_timeout(5000)
        chrome_browser.close()