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
        # -> Open the workshop application modal using keyboard navigation (Tab and Enter keys) on the '워크숍 신청하기' button.
        frame = context.pages[-1]
        # Click the '워크숍 신청하기' button to open the workshop application modal.
        elem = frame.locator('xpath=html/body/header/div/div/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # --> Assertions to verify final state
        frame = context.pages[-1]
        await expect(frame.locator('text=워크숍 신청하기').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=AI 활용 워크숍 신청서').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=기본 정보 (성함, 연락처, 이메일, 활동 지역, 예술 분야, 세부 예술활동)').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=AI 활용 경험 (생성형 AI 사용 경험, 구글 계정 사용 여부)').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=공모사업 도전 경험 (최근 2년 내 경험, 목표 공모사업, 어려운 점 선택)').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=워크숍 기대 사항 (얻고 싶은 결과물, AI에게 묻고 싶은 질문)').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=장비 준비 (노트북/태블릿 지참 가능 여부)').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=개인정보 수집 및 이용 동의 필요, 운영 목적 외 사용 안 함').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=신청서 제출하기').first).to_be_visible(timeout=30000)
        await asyncio.sleep(5)
    
    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()
            
asyncio.run(run_test())
    