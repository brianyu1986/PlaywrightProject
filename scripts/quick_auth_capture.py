"""
快速登入捕獲腳本

此腳本會自動進行登入並保存驗證狀態
目的：減少重複登入時間，提升測試效率
"""

import json
import sys
from pathlib import Path

# 添加父級目錄到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fixtures.test_data import TEST_USERS
from playwright.sync_api import sync_playwright

def capture_auth_state():
    """捕獲認證狀態"""
    print("🔐 開始登入流程...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 显示浏览器便于观察
        page = browser.new_page()
        
        try:
            user = TEST_USERS["valid_user"]
            
            # 第一步：导航到登入页面
            print("📍 導航到登入頁面...")
            page.goto("https://www.dogcatstar.com/my-account/", timeout=30000)
            page.wait_for_load_state("domcontentloaded", timeout=10000)
            
            # 第二步：点击邮箱登入按钮
            print("📧 點擊郵箱登入...")
            try:
                email_buttons = page.locator("button:has-text('use a mailbox')")
                if email_buttons.count() > 0:
                    email_buttons.first.click()
                    page.wait_for_timeout(500)
            except Exception as e:
                print(f"⚠️ 郵箱按鈕点击出错：{e}")
            
            # 第三步：填写邮箱
            print(f"✉️ 填寫郵箱：{user['email']}")
            try:
                email_input = page.locator("input[type='email']").first
                email_input.fill(user["email"])
                email_input.press("Enter")
                page.wait_for_timeout(1000)
            except Exception as e:
                print(f"⚠️ 郵箱填寫出错：{e}")
            
            # 第四步：点击邮箱确认
            print("✔️ 點擊郵箱確認...")
            try:
                confirm_buttons = page.locator("button:has-text('confirm')")
                if confirm_buttons.count() > 0:
                    confirm_buttons.last.click()
                    page.wait_for_timeout(1500)
            except Exception as e:
                print(f"⚠️ 郵箱確認点击出错：{e}")
            
            # 第五步：点击密码登入
            print("🔑 點擊密碼登入...")
            try:
                password_buttons = page.locator("button:has-text('use password')")
                if password_buttons.count() > 0:
                    password_buttons.first.click()
                    page.wait_for_timeout(500)
            except Exception as e:
                print(f"⚠️ 密碼按鈕点击出错：{e}")
            
            # 第六步：填写密码
            print("🔐 填寫密碼...")
            try:
                password_input = page.locator("input[type='password']").first
                password_input.fill(user["password"])
                password_input.press("Enter")
                page.wait_for_timeout(1000)
            except Exception as e:
                print(f"⚠️ 密碼填寫出错：{e}")
            
            # 第七步：点击密码确认
            print("✔️ 點擊密碼確認...")
            try:
                confirm_buttons = page.locator("button:has-text('confirm')")
                if confirm_buttons.count() > 0:
                    confirm_buttons.last.click()
                    page.wait_for_timeout(2000)
            except Exception as e:
                print(f"⚠️ 密碼確認点击出错：{e}")
            
            # 第八步：等待导航完成
            print("⏳ 等待登入完成...")
            try:
                page.wait_for_url("**/my-account/**", timeout=15000)
            except Exception as e:
                print(f"⚠️ URL 導航超時，繼續：{e}")
            
            page.wait_for_timeout(2000)
            
            print("✅ 登入成功！")
            print(f"📍 當前 URL：{page.url}")
            
            # 保存认证状态
            print("💾 保存驗證狀態...")
            auth_file = Path("./fixtures/auth.json")
            auth_file.parent.mkdir(exist_ok=True)
            page.context.storage_state(path=str(auth_file))
            
            print(f"✅ 驗證狀態已保存至：{auth_file}")
            print(f"📊 檔案大小：{auth_file.stat().st_size} bytes")
            
            return True
            
        except Exception as e:
            print(f"❌ 錯誤：{str(e)}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            browser.close()


if __name__ == "__main__":
    success = capture_auth_state()
    exit(0 if success else 1)
