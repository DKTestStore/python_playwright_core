from webbrowser import Chrome

from playwright.sync_api import sync_playwright

def test_resize_chrome_browser():
    with sync_playwright()as page:
        chrome_browser=page.chromium.launch(headless=False,args=["--start-maximized"])
        #chrome_browser = page.chromium.launch(headless=False, args=["--start-maximized", "--force-device-scale-factor=0.5"])
        chrome_context = chrome_browser.new_context(no_viewport=True)
        chrome_page = chrome_context.new_page()
        chrome_page.goto("https://www.google.com")
        chrome_page.evaluate("document.body.style.transform = 'scale(0.7)'")
        #chrome_page.evaluate("document.body.style.transformOrigin = '0 0'")
        chrome_page.wait_for_timeout(9000)
        chrome_context.close()

def test_resize_firefox_browser():
    with sync_playwright() as page:
        firefox_browser=page.firefox.launch(headless=False,args=["--start-maximized"])
        firefox_context = firefox_browser.new_context(viewport={"width": 1920, "height": 1080})
        firefox_page = firefox_context.new_page()
        firefox_page.goto("https://www.google.com")
        firefox_page.evaluate("document.body.style.transform = 'scale(0.7)'")
        #firefox_page.evaluate("document.body.style.transformOrigin = '0 0'")
        firefox_page.wait_for_timeout(10000)
        firefox_browser.close()