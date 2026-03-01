# -*- coding: utf-8 -*-
import asyncio
from pathlib import Path

async def main():
    from patchright.async_api import async_playwright
    
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(headless=True)
    page = await browser.new_page()
    
    html_path = Path("D:/面試/英文履歷.html").resolve()
    await page.goto(f"file:///{html_path}", wait_until="networkidle", timeout=30000)
    await page.wait_for_timeout(2000)
    
    await page.pdf(
        path="D:/面試/Danny_Wang_Resume_EN.pdf",
        format="A4",
        print_background=True,
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
    )
    print("PDF generated successfully")
    
    await browser.close()
    await pw.stop()

asyncio.run(main())
