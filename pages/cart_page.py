from playwright.sync_api import Page, expect


class CartPage:
    """購物車頁面 - Page Object Model"""

    def __init__(self, page: Page):
        self.page = page
        self.page.goto("https://www.dogcatstar.com/")
    
    # 定位器
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
    
    # 操作
    def go_to_cart(self):
        """點擊購物車連結"""
        self.cart_link.click()
    
    def go_to_user(self):
        """點擊使用者連結"""
        self.user_link.click()
    
    def verify_empty_cart(self):
        """驗證購物車為空"""
        expect(self.empty_cart_heading).to_contain_text("購物車中沒有商品")
    
    def click_cat_section(self):
        """點擊貓貓專區"""
        self.cat_section_button.click()
    
    def click_ai_search(self):
        """點擊AI搜尋"""
        self.ai_search_button.click()
    
    def search_product(self, keyword: str):
        """搜尋產品"""
        self.ai_search_input.click()
        self.ai_search_input.fill(keyword)
    
    def click_first_product(self):
        """點擊第一個產品"""
        self.product_links.first.click()
    
    def select_product_variant(self, variant_name: str):
        """選擇產品變體（如款式）"""
        self.page.get_by_role("button", name=variant_name).click()
    
    def add_product_to_cart(self):
        """新增產品到購物車"""
        self.add_to_cart_button.click()
    
    def close_popup(self):
        """關閉彈出視窗"""
        self.popup_close_button.click()
    
    def verify_item_in_cart(self, item_name: str):
        """驗證購物車中有特定商品"""
        expect(self.cart_item_heading).to_contain_text(item_name)
    
    def remove_item_from_cart(self, index: int = 0):
        """從購物車刪除商品"""
        self.remove_button.filter(has_text="").nth(index).click()
