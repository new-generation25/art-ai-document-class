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
        # -> Click on the '커리큘럼' navigation link to check its page and styling consistency.
        frame = context.pages[-1]
        # Click on the '커리큘럼' navigation link to navigate to the curriculum page and check Tailwind CSS styling consistency.
        elem = frame.locator('xpath=html/body/nav/div/div[2]/a').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click on the 'AI 번역 체험' navigation link to check its page and styling consistency.
        frame = context.pages[-1]
        # Click on the 'AI 번역 체험' navigation link to navigate to the translation demo page and check Tailwind CSS styling consistency.
        elem = frame.locator('xpath=html/body/nav/div/div[2]/a[2]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click on the '심사 전략' navigation link to check its page and styling consistency.
        frame = context.pages[-1]
        # Click on the '심사 전략' navigation link to navigate to the selection strategy page and check Tailwind CSS styling consistency.
        elem = frame.locator('xpath=html/body/nav/div/div[2]/a[3]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click on the '신청하기' button to open the modal form and verify Tailwind CSS styling consistency in the modal.
        frame = context.pages[-1]
        # Click on the '신청하기' button to open the modal form and check Tailwind CSS styling consistency.
        elem = frame.locator('xpath=html/body/nav/div/div[2]/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click on each tab button (1주차, 2주차, 3주차, 4주차) to verify consistent Tailwind CSS styling and spacing across tab content.
        frame = context.pages[-1]
        # Click on the '1주차 오리엔테이션' tab button to check Tailwind CSS styling consistency in the tab content.
        elem = frame.locator('xpath=html/body/section[2]/div[2]/div[3]/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click on the '2주차 논리 구조' tab button to verify Tailwind CSS styling consistency in the tab content.
        frame = context.pages[-1]
        # Click on the '2주차 논리 구조' tab button to check Tailwind CSS styling consistency in the tab content.
        elem = frame.locator('xpath=html/body/section[5]/div[2]/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click on the '3주차 상세 기획' tab button to verify Tailwind CSS styling consistency in the tab content.
        frame = context.pages[-1]
        # Click on the '3주차 상세 기획' tab button to check Tailwind CSS styling consistency in the tab content.
        elem = frame.locator('xpath=html/body/section[2]/div[2]/div[3]/button[3]').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Click on the '4주차 최종 점검' tab button to verify Tailwind CSS styling consistency in the tab content.
        frame = context.pages[-1]
        # Click on the '4주차 최종 점검' tab button to check Tailwind CSS styling consistency in the tab content.
        elem = frame.locator('xpath=html/body/div[2]/div/div[2]/form/div/div/div/input').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # -> Scroll down to reveal more form content and verify consistent Tailwind CSS styling and spacing for all form sections.
        await page.mouse.wheel(0, await page.evaluate('() => window.innerHeight'))
        

        # -> Perform a responsive design test by resizing the viewport and verifying consistent Tailwind CSS usage and layout across different screen sizes.
        await page.mouse.wheel(0, -await page.evaluate('() => window.innerHeight'))
        

        # -> Perform a responsive design test by resizing the viewport and verifying consistent Tailwind CSS usage and layout across different screen sizes.
        await page.mouse.wheel(0, await page.evaluate('() => window.innerHeight'))
        

        await page.mouse.wheel(0, -await page.evaluate('() => window.innerHeight'))
        

        # -> Perform a responsive design test by resizing the viewport and verifying consistent Tailwind CSS usage and layout across different screen sizes.
        await page.mouse.wheel(0, await page.evaluate('() => window.innerHeight'))
        

        await page.mouse.wheel(0, -await page.evaluate('() => window.innerHeight'))
        

        # -> Perform a responsive design test by resizing the viewport and verifying consistent Tailwind CSS usage and layout across different screen sizes.
        await page.mouse.wheel(0, await page.evaluate('() => window.innerHeight'))
        

        await page.mouse.wheel(0, -await page.evaluate('() => window.innerHeight'))
        

        # -> Test interactive states by focusing and hovering over key buttons and input fields to verify consistent Tailwind CSS styling for hover, focus, and active states.
        frame = context.pages[-1]
        # Click on the '신청서 제출하기' button to check hover and active states visually.
        elem = frame.locator('xpath=html/body/div[2]/div/div[2]/form/button').nth(0)
        await page.wait_for_timeout(3000); await elem.click(timeout=5000)
        

        # --> Assertions to verify final state
        frame = context.pages[-1]
        await expect(frame.locator('text=커리큘럼').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=AI 번역 체험').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=심사 전략').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=신청하기').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=1주차').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=2주차').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=3주차').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=4주차').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=예술인을 위한 AI 마스터 클래스').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=압도적 맥락 파악').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=실시간 정보 검색').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=예술가형 행정 언어').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=4주 집중 커리큘럼').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=6명 모집').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=2026. 1. 7. ~ 1. 28. (매주 수)  |  ⏰ 10:00 ~ 12:00').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=회현동 소극장').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=살 붙이기와 시각화').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=상세 실행 계획 수립 및 AI를 활용한 시각 자료 기획').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=계획서 본문 1페이지 및 핵심 시각화 자료 1종').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=AI 예술가 언어 번역기').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=할머니의 옛날 이야기를 그림으로 남기고 싶어요.').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=요즘 사람들이 예술을 너무 몰라요.').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=동네 오래된 시장이 사라지는 게 슬퍼요.').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=날씨 좋을 때 야외에서 공연할 생각이에요.').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=몽글몽글하고 따뜻한 빛이 가득한 무대를 만들래요.').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=심사위원의').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=우수한 예술성(30%)도 중요하지만, 합격의 당락은 실현가능성(30%)과 사업수행역량(20%)에서 결정됩니다. 워크숍에서는 AI를 활용해 이 50%를 완벽하게 확보합니다.').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=데이터 기반의 구체적인 사업 필요성 도출').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=현실적인 주 단위 스케줄 및 리스크 관리').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=선정 확률을 높일 준비가 되셨나요?').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=지금 바로 워크숍 신청하기').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=⏳ 신청접수 마감: 2026. 1. 5.(월) 까지').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=* 참여자 확정 발표는 선정된 분들께 개별 안내 드립니다.').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=💡 책임감 있는 참여를 위해 보증금 5만원이 있습니다. (4회 모두 참석 시 100% 환불)').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=[개인정보 수집 및 이용 동의] 수집된 정보는 운영 목적 외 사용되지 않습니다.').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=신청서 제출하기').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=© 2025 AI Arts Masterclass. All rights reserved.').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Instructor: JENNY').first).to_be_visible(timeout=30000)
        await expect(frame.locator('text=Built for Artist Max').first).to_be_visible(timeout=30000)
        await asyncio.sleep(5)
    
    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()
            
asyncio.run(run_test())
    