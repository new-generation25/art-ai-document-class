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
        # -> Scroll down to locate the evaluation criteria chart section and confirm the chart is rendered correctly with data points matching the predefined criteria.
        await page.mouse.wheel(0, 600)
        

        # -> Try interacting with the page elements that might trigger or reveal the evaluation criteria chart, such as buttons or tabs related to '심사' (evaluation) or '심사 전략' (evaluation strategy).
        frame = context.pages[-1]
        # Click on the '심사 전략' link to try to reveal the evaluation criteria chart section
        elem = frame.locator('xpath=html/body/nav/div/div[2]/a[3]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Resize the browser window to a smaller width to simulate a mobile viewport and verify the chart layout and labels adjust properly and remain fully visible and legible.
        await page.goto('http://localhost:3000/#analytics', timeout=10000)
        await asyncio.sleep(3)
        

        frame = context.pages[-1]
        # Click on the '심사 전략' tab to show the evaluation criteria chart again.
        elem = frame.locator('xpath=html/body/nav/div/div[2]/a[3]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        await page.mouse.wheel(0, 300)
        

        # -> Manually resize the browser window to smaller widths simulating mobile devices and visually confirm the chart layout and labels adjust properly and remain fully visible and legible. Then attempt to simulate a data update in the chart and verify dynamic update behavior.
        await page.mouse.wheel(0, -300)
        

        await page.mouse.wheel(0, 300)
        

        # -> Attempt to simulate a data update in the chart programmatically or by interacting with any available UI elements that might trigger a chart data refresh, then verify the chart updates dynamically without visual errors.
        frame = context.pages[-1]
        # Click the button ⚡ to trigger any possible chart data update or refresh.
        elem = frame.locator('xpath=html/body/section[3]/div[3]/div[2]/div/div[2]/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # --> Assertions to verify final state
        frame = context.pages[-1]
        await expect(frame.locator('text=심사 전략').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=압도적 맥락 파악').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=실시간 정보 검색').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=예술가형 행정 언어').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=4주 집중 커리큘럼').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=소수 인원 6명 모집').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=2026. 1. 7. ~ 1. 28. (매주 수)  |  ⏰ 10:00 ~ 12:00').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=회현동 소극장').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=AI라는 '똑똑한 비서'와 친해지기').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=나의 예술 철학을 담은 '한 줄 슬로건' 완성').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=AI 막내 비서 임명 및 원리 이해 (할루시네이션)').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=제미나이 3.0 Pro의 특징: 긴 문맥과 실시간 검색').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=[실습] 내 예술적 정체성 정의 및 키워드 분석').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=아이디어를 사업 테마로 번역하는 대화법').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=AI 예술가 언어 번역기').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=고령화 지역의 '생애사 기록'을 통한 세대 간 문화 공감대 형성 프로젝트 [번역 완료]').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=심사위원의').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=마음을 여는 전략').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=우수한 예술성(30%)도 중요하지만, 합격의 당락은 실현가능성(30%)과 사업수행역량(20%)에서 결정됩니다. 워크숍에서는 AI를 활용해 이 50%를 완벽하게 확보합니다.').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=데이터 기반의 구체적인 사업 필요성 도출').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=현실적인 주 단위 스케줄 및 리스크 관리').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=선정 확률을 높일 준비가 되셨나요?').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=지금 바로 워크숍 신청하기').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=⏳ 신청접수 마감: 2026. 1. 5.(월) 까지').first).to_be_visible(timeout=30000)
        await asyncio.sleep(5)
    
    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()
            
asyncio.run(run_test())
    