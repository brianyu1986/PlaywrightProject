"""
驗證登入狀態診斷

此測試用於檢查 user.json 中保存的登入狀態是否仍然有效
如果無法在 my-account 頁面看到登入標記，表示 user.json 已過期
"""

import pytest
from helpers.base_helpers import LogHelpers


class TestAuthStatus:
    """檢查登入狀態"""
    
    @pytest.mark.smoke
    def test_check_login_status(self, authenticated_page):
        """
        診斷測試：驗證登入狀態
        
        步驟：
        1. 打開 my-account 頁面
        2. 檢查是否顯示已登入用戶信息
        3. 驗證登入狀態是否有效
        """
        page = authenticated_page
        
        LogHelpers.log_step("1️⃣ 導航到 my-account 頁面")
        page.goto("https://www.dogcatstar.com/my-account/")
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        
        LogHelpers.log_step("2️⃣ 驗證頁面 URL")
        current_url = page.url
        LogHelpers.log_step(f"當前 URL: {current_url}")
        assert "my-account" in current_url, f"未進入 my-account 頁面，URL: {current_url}"
        
        LogHelpers.log_step("3️⃣ 檢查頁面標題")
        title = page.title()
        LogHelpers.log_step(f"頁面標題: {title}")
        
        LogHelpers.log_step("4️⃣ 檢查是否顯示用戶名或登出按鈕")
        page_content = page.content()
        
        # 檢查多種登出/用戶相關的指標
        login_indicators = [
            "登出",
            "logout",
            "我的帳戶",
            "my account",
            "user_id",
            "374296",  # user.json 中的用戶 ID
        ]
        
        found_indicators = []
        for indicator in login_indicators:
            if indicator.lower() in page_content.lower():
                found_indicators.append(indicator)
        
        LogHelpers.log_step(f"找到的登入指標: {found_indicators}")
        
        if found_indicators:
            LogHelpers.log_step("✅ 確認已成功登入！")
            print(f"\n✅ 登入狀態確認：找到以下登入標記 {found_indicators}")
        else:
            LogHelpers.log_step("❌ 未發現登入標記 - 可能 user.json 已過期")
            print("\n❌ 警告：未發現登入標記！")
            print("可能原因：")
            print("  1. user.json 中的 token 已過期")
            print("  2. Cookie 已失效")
            print("  3. 需要重新登入並更新 user.json")
            
            # 拍攝截圖以便診斷
            page.screenshot(path="./test-results/login_status_check_failure.png")
            assert False, "登入狀態無效 - user.json 可能已過期，需要重新更新"
        
        LogHelpers.log_step("✅ 測試通過：登入狀態有效")
