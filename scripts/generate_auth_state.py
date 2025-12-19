"""
生成驗證狀態快照 (Authentication State Snapshot)

此腳本執行登入流程並保存認證狀態，供後續測試使用。
這樣可以避免每個測試都重新登入，大幅加速測試執行。
"""

import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from fixtures.test_data import TEST_USERS
from helpers.base_helpers import WaitHelpers, LogHelpers


def generate_auth_state():
    """
    生成並保存驗證狀態
    """
    auth_file = Path("auth.json")
    user = TEST_USERS["valid_user"]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            LogHelpers.log_step("導航到登入頁面")
            page.goto("https://www.dogcatstar.com/my-account/", wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle", timeout=5000)
            
            LogHelpers.log_step("點擊郵箱登入按鈕")
            email_button = page.locator("button:has-text('use a mailbox')")
            if email_button.is_visible():
                email_button.click()
            
            page.wait_for_timeout(500)
            
            LogHelpers.log_step("輸入郵箱")
            email_input = page.locator("input[type='email']")
            if email_input.count() > 0:
                email_input.first.fill(user["email"])
                email_input.first.press("Enter")
            
            page.wait_for_timeout(500)
            
            LogHelpers.log_step("點擊郵箱確認按鈕")
            email_confirm = page.locator("button:has-text('confirm')")
            if email_confirm.count() > 0:
                email_confirm.last.click()
            
            page.wait_for_timeout(1000)
            
            LogHelpers.log_step("點擊密碼登入按鈕")
            password_button = page.locator("button:has-text('use password')")
            if password_button.is_visible():
                password_button.click()
            
            page.wait_for_timeout(500)
            
            LogHelpers.log_step("輸入密碼")
            password_input = page.locator("input[type='password']")
            if password_input.count() > 0:
                password_input.first.fill(user["password"])
                password_input.first.press("Enter")
            
            page.wait_for_timeout(500)
            
            LogHelpers.log_step("點擊密碼確認按鈕")
            password_confirm = page.locator("button:has-text('confirm')")
            if password_confirm.count() > 0:
                password_confirm.last.click()
            
            LogHelpers.log_step("等待登入完成")
            page.wait_for_url("**/my-account/**", timeout=10000)
            page.wait_for_load_state("networkidle", timeout=5000)
            
            LogHelpers.log_step("保存驗證狀態")
            context.storage_state(path=str(auth_file))
            
            LogHelpers.log_step(f"✅ 驗證狀態已保存至 {auth_file}")
            
        except Exception as e:
            LogHelpers.log_step(f"❌ 生成驗證狀態失敗: {str(e)}")
            raise
        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    generate_auth_state()
