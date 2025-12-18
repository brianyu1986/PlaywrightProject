"""
购物车功能测试

测试场景：
1. 用户登录
2. 搜索产品
3. 添加产品到购物车
4. 验证购物车中的产品
"""

import pytest
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from fixtures.test_data import TEST_USERS, SEARCH_KEYWORDS, PRODUCT_VARIANTS
from helpers.base_helpers import LogHelpers


class TestCart:
    """购物车测试类"""
    
    @pytest.mark.smoke
    def test_add_product_to_cart(self, page):
        """
        测试：添加产品到购物车
        
        步骤：
        1. 登录用户
        2. 浏览猫猫专区
        3. 使用AI搜索功能搜索产品
        4. 添加产品到购物车
        5. 验证产品已添加到购物车
        """
        LogHelpers.log_step(1, "初始化页面")
        cart_page = CartPage(page)
        
        LogHelpers.log_step(2, "进入购物车并点击用户")
        cart_page.go_to_cart()
        cart_page.go_to_user()
        
        LogHelpers.log_step(3, "使用邮箱和密码登录")
        login_page = LoginPage(page)
        user_data = TEST_USERS["valid_user"]
        login_page.login_with_email_and_password(user_data["email"], user_data["password"])
        
        LogHelpers.log_step(4, "验证购物车为空")
        cart_page.verify_empty_cart()
        
        LogHelpers.log_step(5, "点击猫猫专区")
        cart_page.click_cat_section()
        
        LogHelpers.log_step(6, "使用AI搜索功能")
        cart_page.click_ai_search()
        search_keyword = SEARCH_KEYWORDS["cat_food"]
        cart_page.search_product(search_keyword)
        
        LogHelpers.log_step(7, "点击第一个产品")
        cart_page.click_first_product()
        
        LogHelpers.log_step(8, f"选择产品变体: {PRODUCT_VARIANTS['format_1']}")
        cart_page.select_product_variant(PRODUCT_VARIANTS["format_1"])
        
        LogHelpers.log_step(9, "添加产品到购物车")
        cart_page.add_product_to_cart()
        
        LogHelpers.log_step(10, "关闭弹出窗口")
        cart_page.close_popup()
        
        LogHelpers.log_step(11, "进入购物车")
        cart_page.go_to_cart()
        
        LogHelpers.log_step(12, "验证产品已添加到购物车")
        expected_product = "迪士尼貓狗系列 COZY 四季被"
        cart_page.verify_item_in_cart(expected_product)
        
        print("\n✅ 测试通过：产品已成功添加到购物车")
    
    @pytest.mark.smoke
    def test_empty_cart_initially(self, page):
        """
        测试：验证初始购物车为空
        """
        LogHelpers.log_step(1, "初始化页面")
        cart_page = CartPage(page)
        
        LogHelpers.log_step(2, "进入购物车")
        cart_page.go_to_cart()
        
        LogHelpers.log_step(3, "验证购物车为空")
        cart_page.verify_empty_cart()
        
        print("\n✅ 测试通过：购物车初始状态为空")
