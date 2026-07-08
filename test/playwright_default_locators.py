# Default locators for Playwright automation

from playwright.sync_api import sync_playwright,expect

def launch_chromium():
    """Launch Chromium browser using Playwright sync API"""
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=False,  # Set to False to see the browser
        args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    #page.set_viewport_size({"width": 0, "height": 0})  # Maximize window
    
    return playwright, browser, context, page

def close_browser(playwright, browser, context, page):
    """Close the browser and context"""
    context.close()
    browser.close()
    playwright.stop()


def test_getByRole_Locator():
    """Test launching Chromium browser"""
    playwright, browser, context, page = launch_chromium()
    page.goto("https://testautomationpractice.blogspot.com/p/playwrightpractice.html")
    title = page.title()
    assert title is not None
    print(f"Page title: {title}")
    try:
        page.wait_for_timeout(3000)
        primary_action_button=page.get_by_role("button",name="Primary Action")
        primary_action_button.click()
        primary_action_button.click()
        primary_action_button.click()
        page.wait_for_timeout(3000)

    except Exception as e:
        print(f"Error occurred: {e}")
        raise  # Re-raise to make test fail

    try:
        page.wait_for_timeout(3000)
        secondary_action_button=page.get_by_role("button",name="Toggle Button")
        secondary_action_button.click()
        secondary_action_button.click()
        secondary_action_button.click()
        secondary_action_button.click()
        page.wait_for_timeout(3000)

    except Exception as e:
        print(f"Error occurred: {e}")
        raise  # Re-raise to make test fail

    try:
        page.wait_for_timeout(3000)
        div_with_button=page.get_by_role("button",name="Div with button role")
        div_with_button.click()
        div_with_button.click()
        div_with_button.click()
        div_with_button.click()
        page.wait_for_timeout(3000)

    except Exception as e:
        print(f"Error occurred: {e}")
        raise  # Re-raise to make test fail

    try:
        page.wait_for_timeout(3000)
        # Click div element with role="button" using get_by_role()
        # HTML: <div role="button" tabindex="0" class="card">Div with button role</div>
        div_button = page.get_by_role("button", name="Div with button role")
        div_button.click()
        print("Div button clicked successfully")
        page.wait_for_timeout(3000)

    except Exception as e:
        print(f"Error occurred: {e}")
        raise  # Re-raise to make test fail

    try:
        page.wait_for_timeout(3000)

        # Method 2: Get by role with name (if input has label or aria-label)
        username_input = page.get_by_role("textbox", name="username")
        username_input.fill("Automation Test")

        page.wait_for_timeout(3000)
        # Method 3: Get by role and filter by id
        username_input = page.locator("input[role='textbox']#username")
        username_input.fill("Manual Test")
        username_input.clear()
        username_input.type("Test")
        page.wait_for_timeout(3000)

    except Exception as e:
        print(f"Error occurred: {e}")
        raise  # Re-raise to make test fail

    try:
        page.get_by_role("checkbox", name="Accept Terms").click()
        page.wait_for_timeout(3000)

    except Exception as e:
        print(f"Error occurred: {e}")
        raise  # Re-raise to make test fail

    try:
        page.get_by_role("menuitem",name="Home").click()
        page.wait_for_timeout(3000)
        page.get_by_role("menuitem",name="Products").click()
        page.wait_for_timeout(3000)
        page.get_by_role("menuitem",name="Contact").click()
        page.wait_for_timeout(3000)

    except Exception as e:
        print(f"Error occurred: {e}")
        raise  # Re-raise to make test fail


    try:
        expect(page.get_by_role("alert",name="This is an important alert message!")).not_to_be_visible()

    except Exception as e:
        print(f"Error occurred: {e}")
        raise  # Re-raise to make test fail

    finally:
        close_browser(playwright, browser, context, page)

