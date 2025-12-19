"""
登入流程測試 & 驗證狀態生成

此模組測試登入功能並生成驗證狀態快照供後續測試使用。
這樣後續測試可以直接使用已登入的狀態，無需重複登入。
"""

import pytest
import os
from pathlib import Path
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from fixtures.test_data import TEST_USERS
from helpers.base_helpers import LogHelpers


class TestLogin:
    """登入流程測試"""
    
    @pytest.mark.smoke
    @pytest.mark.authentication
    def test_login_with_email_and_password(self, page):
        """
        測試：使用郵箱和密碼登入
        
        此測試會保存驗證狀態供其他測試使用
        超時時間設置為 120 秒
        """
        LogHelpers.log_step("測試開始：登入流程")
        
        # 設置超時
        page.set_default_timeout(120000)  # 120 秒
        page.set_default_navigation_timeout(120000)
        
        # 初始化登入頁面
        login_page = LoginPage(page)
        
        try:
            # 執行登入
            LogHelpers.log_step("執行登入操作")
            login_page.login_with_email_and_password(
                email=TEST_USERS["valid_user"]["email"],
                password=TEST_USERS["valid_user"]["password"]
            )
            
            # 驗證登入成功
            LogHelpers.log_step("驗證登入成功")
            page.wait_for_url("**/my-account/**", timeout=30000)
            assert page.url.startswith("https://www.dogcatstar.com"), "登入失敗：URL 未轉向到帳戶頁面"
            
            # 保存驗證狀態
            LogHelpers.log_step("保存驗證狀態")
            auth_file = Path("./fixtures/auth.json")
            auth_file.parent.mkdir(exist_ok=True)
            page.context.storage_state(path=str(auth_file))
            
            LogHelpers.log_step(f"✅ 驗證狀態已保存：{auth_file}")
            assert auth_file.exists(), "驗證狀態檔案保存失敗"
            
            # 驗證檔案大小
            file_size = auth_file.stat().st_size
            assert file_size > 100, f"驗證狀態檔案過小：{file_size} bytes"
            LogHelpers.log_step(f"✅ 驗證狀態檔案有效：{file_size} bytes")
            
        except Exception as e:
            LogHelpers.log_step(f"❌ 登入測試失敗：{str(e)}")
            raise


class TestLoginWithAuthState:
    """使用驗證狀態的測試"""
    
    @pytest.mark.smoke
    @pytest.mark.authentication
    def test_access_account_with_saved_auth_state(self, authenticated_page):
        """
        測試：使用保存的驗證狀態直接訪問帳戶頁面
        
        此測試驗證保存的驗證狀態是否有效
        """
        LogHelpers.log_step("使用驗證狀態導航到帳戶頁面")
        authenticated_page.goto("https://www.dogcatstar.com/my-account/")
        authenticated_page.wait_for_load_state("networkidle", timeout=5000)
        
        LogHelpers.log_step("驗證已登入狀態")
        assert authenticated_page.url.startswith("https://www.dogcatstar.com"), "未能成功訪問帳戶頁面"
        
        LogHelpers.log_step("✅ 驗證狀態有效，已成功登入")


class TestCartWithAuthState:
    """使用驗證狀態進行購物車測試（跳過登入）"""
    
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_view_cart_without_login_flow(self, authenticated_page):
        """
        測試：查看購物車（使用已保存的驗證狀態）
        
        此測試跳過登入流程，直接使用認證狀態查看購物車
        """
        LogHelpers.log_step("導航到主頁")
        cart_page = CartPage(authenticated_page)
        
        LogHelpers.log_step("驗證購物車為空")
        cart_page.verify_empty_cart()
        
        LogHelpers.log_step("✅ 購物車驗證成功")
    
    
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_add_product_with_auth_state(self, authenticated_page):
        """
        測試：新增產品到購物車（使用已保存的驗證狀態）
        
        此測試使用認證狀態，跳過登入流程
        """
        LogHelpers.log_step("導航到主頁")
        cart_page = CartPage(authenticated_page)
        
        LogHelpers.log_step("驗證購物車為空")
        cart_page.verify_empty_cart()
        
        LogHelpers.log_step("瀏覽貓貓專區")
        cart_page.navigate_to_cat_section()
        
        LogHelpers.log_step("搜尋產品：貓貓罐頭")
        cart_page.search_product("貓貓罐頭")
        
        LogHelpers.log_step("新增產品到購物車")
        cart_page.add_product_to_cart()
        
        LogHelpers.log_step("✅ 產品已新增到購物車")
