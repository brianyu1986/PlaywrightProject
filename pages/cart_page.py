from playwright.sync_api import Page, expect


class CartPage:
    """购物车页面 - Page Object Model"""

    def __init__(self, page: Page):
        self.page = page
        self.page.goto("https://www.dogcatstar.com/")
    
    # Locators
    @property
    def cart_link(self):
        return self.page.get_by_role("link", name="Cart")
    
    @property
    def user_link(self):
        return self.page.get_by_role("link", name="User")
    
    @property
    def empty_cart_heading(self):
        return self.page.get_by_test_id("paper-cart-empty").get_by_role("heading")
    
    @property
    def cat_section_button(self):
        return self.page.get_by_role("button", name="貓貓專區")
    
    @property
    def ai_search_button(self):
        return self.page.get_by_role("button", name="AI搜尋")
    
    @property
    def ai_search_input(self):
        return self.page.get_by_role("textbox", name="毛孩腎病適合吃什麼？")
    
    @property
    def product_links(self):
        return self.page.get_by_role("link", name="product")
    
    @property
    def add_to_cart_button(self):
        return self.page.get_by_test_id("button-add-to-cart")
    
    @property
    def popup_close_button(self):
        return self.page.get_by_test_id("popup-close-button")
    
    @property
    def cart_item_heading(self):
        return self.page.get_by_test_id("paper-card-main-normal").locator("h6")
    
    @property
    def remove_button(self):
        return self.page.get_by_test_id("paper-card-main-normal").get_by_role("button")
    
    # Actions
    def go_to_cart(self):
        """点击购物车链接"""
        self.cart_link.click()
    
    def go_to_user(self):
        """点击用户链接"""
        self.user_link.click()
    
    def verify_empty_cart(self):
        """验证购物车为空"""
        expect(self.empty_cart_heading).to_contain_text("購物車中沒有商品")
    
    def click_cat_section(self):
        """点击猫猫专区"""
        self.cat_section_button.click()
    
    def click_ai_search(self):
        """点击AI搜索"""
        self.ai_search_button.click()
    
    def search_product(self, keyword: str):
        """搜索产品"""
        self.ai_search_input.click()
        self.ai_search_input.fill(keyword)
    
    def click_first_product(self):
        """点击第一个产品"""
        self.product_links.first.click()
    
    def select_product_variant(self, variant_name: str):
        """选择产品变体（如款式）"""
        self.page.get_by_role("button", name=variant_name).click()
    
    def add_product_to_cart(self):
        """添加产品到购物车"""
        self.add_to_cart_button.click()
    
    def close_popup(self):
        """关闭弹出窗口"""
        self.popup_close_button.click()
    
    def verify_item_in_cart(self, item_name: str):
        """验证购物车中有特定商品"""
        expect(self.cart_item_heading).to_contain_text(item_name)
    
    def remove_item_from_cart(self, index: int = 0):
        """从购物车删除商品"""
        self.remove_button.filter(has_text="").nth(index).click()
