import asyncio
from playwright import async_api
from playwright.async_api import expect

async def run_test():
    pw = None
    browser = None
    context = None
    
    try:
        # Start a Playwright session in asynchronous mode
        pw = await async_api.async_playwright().start()
        
        # Launch a Chromium browser in headless mode with custom arguments
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--window-size=1280,720",         # Set the browser window size
                "--disable-dev-shm-usage",        # Avoid using /dev/shm which can cause issues in containers
                "--ipc=host",                     # Use host-level IPC for better stability
                "--single-process"                # Run the browser in a single process mode
            ],
        )
        
        # Create a new browser context (like an incognito window)
        context = await browser.new_context()
        context.set_default_timeout(5000)
        
        # Open a new page in the browser context
        page = await context.new_page()
        
        # Navigate to your target URL and wait until the network request is committed
        await page.goto("http://localhost:3000", wait_until="commit", timeout=10000)
        
        # Wait for the main page to reach DOMContentLoaded state (optional for stability)
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=3000)
        except async_api.Error:
            pass
        
        # Iterate through all iframes and wait for them to load as well
        for frame in page.frames:
            try:
                await frame.wait_for_load_state("domcontentloaded", timeout=3000)
            except async_api.Error:
                pass
        
        # Interact with the page elements to simulate user flow
        # -> Scroll down the page to check if the navigation bar remains sticky and visible.
        await page.mouse.wheel(0, 600)
        

        # -> Click each navigation link in the navigation bar to verify correct routing to their sections.
        frame = context.pages[-1]
        # Click the '커리큘럼' navigation link to verify routing.
        elem = frame.locator('xpath=html/body/nav/div/div[2]/a').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click the 'AI 번역 체험' navigation link to verify correct routing to its section.
        frame = context.pages[-1]
        # Click the 'AI 번역 체험' navigation link to verify routing.
        elem = frame.locator('xpath=html/body/nav/div/div[2]/a[2]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click the '심사 전략' navigation link to verify correct routing to its section.
        frame = context.pages[-1]
        # Click the '심사 전략' navigation link to verify routing.
        elem = frame.locator('xpath=html/body/nav/div/div[2]/a[3]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click the '신청하기' button to verify correct routing or scrolling to the application section.
        frame = context.pages[-1]
        # Click the '신청하기' button to verify routing.
        elem = frame.locator('xpath=html/body/nav/div/div[2]/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # --> Assertions to verify final state
        frame = context.pages[-1]
        await expect(frame.locator('text=커리큘럼').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=AI 번역 체험').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=심사 전략').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=신청하기').first).to_be_visible(timeout=30000)
        # Check that the navigation bar is visible and fixed at the top on initial load
        await expect(frame.locator('text=🎨').first).to_be_visible(timeout=30000)
        # Scroll down the page and confirm the navigation bar remains sticky and visible
        await page.mouse.wheel(0, 600)
        await expect(frame.locator('text=🎨').first).to_be_visible(timeout=30000)
        # Click each navigation link and validate navigation to corresponding sections
        await frame.locator('text=커리큘럼').first.click()
        await expect(frame.locator('text=4주 집중 커리큘럼').first).to_be_visible(timeout=30000)
        await frame.locator('text=AI 번역 체험').first.click()
        await expect(frame.locator('text=압도적 맥락 파악').first).to_be_visible(timeout=30000)
        await frame.locator('text=심사 전략').first.click()
        await expect(frame.locator('text=심사위원의').first).to_be_visible(timeout=30000)
        await frame.locator('text=신청하기').first.click()
        await expect(frame.locator('text=AI 활용 워크숍 신청서').first).to_be_visible(timeout=30000)
        await asyncio.sleep(5)
    
    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()
            
asyncio.run(run_test())
    