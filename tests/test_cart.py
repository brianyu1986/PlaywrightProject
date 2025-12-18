"""
購物車功能測試

測試場景：
1. 使用者登入
2. 搜尋產品
3. 新增產品到購物車
4. 驗證購物車中的產品
"""

import pytest
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from fixtures.test_data import TEST_USERS, SEARCH_KEYWORDS, PRODUCT_VARIANTS
from helpers.base_helpers import LogHelpers


class TestCart:
    """購物車測試類"""
    
    @pytest.mark.smoke
    def test_add_product_to_cart(self, page):
        """
        測試：新增產品到購物車
        
        步驟：
        1. 登入使用者
        2. 瀏覽貓貓專區
        3. 使用AI搜尋功能搜尋產品
        4. 新增產品到購物車
        5. 驗證產品已新增到購物車
        """
        LogHelpers.log_step(1, "初始化頁面")
        cart_page = CartPage(page)
        
        LogHelpers.log_step(2, "進入購物車並點擊使用者")
        cart_page.go_to_cart()
        cart_page.go_to_user()
        
        LogHelpers.log_step(3, "使用電郵和密碼登入")
        login_page = LoginPage(page)
        user_data = TEST_USERS["valid_user"]
        login_page.login_with_email_and_password(user_data["email"], user_data["password"])
        
        LogHelpers.log_step(4, "驗證購物車為空")
        cart_page.verify_empty_cart()
        
        LogHelpers.log_step(5, "點擊貓貓專區")
        cart_page.click_cat_section()
        
        LogHelpers.log_step(6, "使用AI搜尋功能")
        cart_page.click_ai_search()
        search_keyword = SEARCH_KEYWORDS["cat_food"]
        cart_page.search_product(search_keyword)
        
        LogHelpers.log_step(7, "點擊第一個產品")
        cart_page.click_first_product()
        
        LogHelpers.log_step(8, f"選擇產品變體: {PRODUCT_VARIANTS['format_1']}")
        cart_page.select_product_variant(PRODUCT_VARIANTS["format_1"])
        
        LogHelpers.log_step(9, "新增產品到購物車")
        cart_page.add_product_to_cart()
        
        LogHelpers.log_step(10, "關閉彈出視窗")
        cart_page.close_popup()
        
        LogHelpers.log_step(11, "進入購物車")
        cart_page.go_to_cart()
        
        LogHelpers.log_step(12, "驗證產品已新增到購物車")
        expected_product = "迪士尼貓狗系列 COZY 四季被"
        cart_page.verify_item_in_cart(expected_product)
        
        print("\n✅ 測試通過：產品已成功新增到購物車")
    
    @pytest.mark.smoke
    def test_empty_cart_initially(self, page):
        """
        測試：驗證初始購物車為空
        """
        LogHelpers.log_step(1, "初始化頁面")
        cart_page = CartPage(page)
        
        LogHelpers.log_step(2, "進入購物車")
        cart_page.go_to_cart()
        
        LogHelpers.log_step(3, "驗證購物車為空")
        cart_page.verify_empty_cart()
        
        print("\n✅ 測試通過：購物車初始狀態為空")
