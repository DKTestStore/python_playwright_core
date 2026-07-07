from playwright.sync_api import sync_playwright, expect

def test_maximize_chrome_browser():
    with sync_playwright() as page:
        chrome_browser=page.chromium.launch(headless=False,args=["--start-maximized"])
        chrome_context=chrome_browser.new_context(no_viewport=True)
        chrome_page=chrome_context.new_page()
        chrome_page.goto("https://www.google.com")
        print("Chrome Title:", chrome_page.title())
        expect(chrome_page).to_have_title("Google")
        chrome_page.wait_for_timeout(5000)
        chrome_browser.close()


def test_maximize_edge_browser():
    with sync_playwright() as page:
        edge_browser=page.chromium.launch(channel="msedge",headless=False,args=["--start-maximized"])
        edge_context=edge_browser.new_context(no_viewport=True)
        edge_page=edge_context.new_page()
        edge_page.goto("https://www.google.com")
        print("Edge Title:", edge_page.title())
        expect(edge_page).to_have_title("Google")
        edge_page.wait_for_timeout(5000)
        edge_browser.close()


def test_maximize_firefox_browser():
     with sync_playwright() as page:
         firefox_browser = page.firefox.launch(headless=False)
         firefox_context = firefox_browser.new_context(viewport={"width": 1920, "height": 1080})
         # firefox_context = firefox_browser.new_context(viewport={"width": 1366, "height": 768})
         # firefox_context = firefox_browser.new_context(viewport={"width": 1600, "height": 900})
         # firefox_context = firefox_browser.new_context(viewport={"width": 1280, "height": 720})
         # firefox_context = firefox_browser.new_context(viewport={"width": 1440, "height": 900})
         firefox_page = firefox_context.new_page()
         firefox_page.goto("https://www.google.com")
         firefox_page.wait_for_timeout(5000)
         firefox_browser.close()


def test_maximize_safari_browser():
    with sync_playwright() as page:
        safari_browser=page.webkit.launch(headless=False)
        safari_context=safari_browser.new_context(viewport={"width": 1920, "height": 1080})
        #safari_context = safari_browser.new_context(viewport={"width": 1366, "height": 768})
        #safari_context = safari_browser.new_context(viewport={"width": 1600, "height": 900})
        #safari_context = safari_browser.new_context(viewport={"width": 1280, "height": 720})
        #safari_context = safari_browser.new_context(viewport={"width": 1440, "height": 900})
        safari_page=safari_context.new_page()
        safari_page.goto("https://www.google.com")
        safari_page.wait_for_timeout(5000)
        safari_browser.close()



