from playwright.sync_api import Page, expect


class CartPage:
    """購物車頁面 - Page Object Model"""

    def __init__(self, page: Page):
        self.page = page
        self.page.goto("https://www.dogcatstar.com/")
    
    # 定位器
    @property
    def cart_link(self):
        # 嘗試使用 test-id 或 icon 相關選擇器
        return self.page.locator("a[href*='cart'], [class*='cart']").first
    
    @property
    def user_link(self):
        # 嘗試使用 test-id 或 icon 相關選擇器
        return self.page.locator("a[href*='account'], [class*='user']").first
    
    @property
    def empty_cart_heading(self):
        # 查找購物車空頁面的標題
        empty_div = self.page.get_by_test_id("paper-cart-empty")
        if empty_div.count() > 0:
            heading = empty_div.locator("h1, h2, h3, h4, h5, h6, p").first
            return heading
        # 備選方案：查找包含特定文本的元素
        return self.page.locator("text=購物車中沒有商品").first
    
    @property
    def cat_section_button(self):
        # 多種選擇器嘗試方案
        # 1. 先嘗試使用 role 選擇器
        button = self.page.get_by_role("button", name="貓貓專區")
        if button.count() > 0:
            return button.first
        
        # 2. 嘗試使用文本包含
        button = self.page.locator("button:has-text('貓貓專區')")
        if button.count() > 0:
            return button.first
        
        # 3. 嘗試使用任何包含"貓"的按鈕
        button = self.page.locator("button, a, [role='button']").filter(has_text="貓")
        if button.count() > 0:
            return button.first
        
        # 4. 如果都找不到，返回一個會報錯的定位器
        return self.page.locator("button:has-text('貓貓專區')")
    
    @property
    def ai_search_button(self):
        return self.page.get_by_role("button", name="AI搜尋")
    
    @property
    def ai_search_input(self):
        return self.page.get_by_role("textbox", name="毛孩腎病適合吃什麼？")
    
    # ============ 購物車操作方法 ============
    
    def get_first_product_info(self):
        """
        獲取頁面上第一個產品的信息
        返回: {'name': 產品名稱, 'price': 價格}
        """
        # 查找產品名稱
        product_name_locator = self.page.locator('[class*="product-title"], h2, h3, [class*="title"]').first
        product_name = product_name_locator.text_content().strip() if product_name_locator.count() > 0 else "Unknown Product"
        
        # 查找產品價格
        price_locator = self.page.locator('[class*="price"], [class*="amount"], span:has-text("$")').first
        product_price = price_locator.text_content().strip() if price_locator.count() > 0 else "Unknown Price"
        
        return {
            'name': product_name,
            'price': product_price
        }
    
    def add_first_product_to_cart(self, wait_for_observation=False):
        """
        添加第一個產品到購物車（含定制化選項處理）
        
        參數:
            wait_for_observation (bool): 是否在操作完成後等待2秒以觀察結果（非headless模式）
        
        返回: 產品信息 {'name': 名稱, 'price': 價格}
        """
        # 先記錄產品信息
        product_info = self.get_first_product_info()
        
        # 查找添加購物車按鈕
        add_to_cart_button = self.page.locator('button:has-text("加入購物車")').first
        
        if add_to_cart_button.count() > 0:
            # 使用 force 點擊避免被 overlay portal 攔截
            add_to_cart_button.click(force=True)
            
            # 等待任何選項對話框或選擇面板出現
            self.page.wait_for_timeout(1000)
            
            # 嘗試處理定制化選項
            self._handle_product_customization()
            
            # 尋找並點擊確認按鈕（可能是第二次"加入購物車"或"確定"按鈕）
            self.page.wait_for_timeout(500)
            
            # 方法1: 尋找"確定加入"按鈕
            confirm_button = self.page.locator('button:has-text("確定加入")').first
            
            # 方法2: 如果沒有，尋找"確認"按鈕
            if confirm_button.count() == 0:
                confirm_button = self.page.locator('button:has-text("確認")').first
            
            # 方法3: 如果沒有，尋找所有"加入購物車"按鈕的第二個
            if confirm_button.count() == 0:
                all_add_buttons = self.page.locator('button:has-text("加入購物車")').all()
                if len(all_add_buttons) > 1:
                    confirm_button = all_add_buttons[1]
            
            # 點擊確認按鈕（使用 force 避免 overlay 攔截）
            if confirm_button.count() > 0:
                try:
                    # 先嘗試普通點擊，如果失敗則使用 force
                    confirm_button.click(force=True)
                    self.page.wait_for_timeout(1000)
                except:
                    pass
            
            # 如果需要觀察，等待2秒
            if wait_for_observation:
                self.page.wait_for_timeout(2000)
        
        return product_info
    
    def _handle_product_customization(self):
        """
        處理產品定制化選項（如規格、數量、顏色等）
        優先選擇"鲁斯佛款"，否則選擇第一個可用選項
        """
        # 等待選項載入
        self.page.wait_for_timeout(500)
        
        # 策略1: 尋找並點擊"鲁斯佛款"選項
        rostoff_option = self.page.locator('button:has-text("鲁斯佛"), span:has-text("鲁斯佛")').first
        if rostoff_option.count() > 0:
            try:
                rostoff_option.click()
                self.page.wait_for_timeout(500)
                return
            except:
                pass
        
        # 策略2: 尋找並點擊任何規格選項按鈕
        option_buttons = self.page.locator('button[class*="variant"], button[class*="option"], button[class*="size"]').all()
        if len(option_buttons) > 0:
            try:
                option_buttons[0].click()
                self.page.wait_for_timeout(500)
                return
            except:
                pass
        
        # 策略3: 選擇下拉菜單選項
        selects = self.page.locator('select').all()
        for select in selects:
            try:
                # 點擊 select 元素打開下拉菜單
                select.click()
                self.page.wait_for_timeout(300)
                
                # 查找第一個選項
                option = self.page.locator('option').nth(1)  # 跳過預設選項
                if option.count() > 0:
                    option.click()
                    self.page.wait_for_timeout(500)
                    return
            except:
                pass
        
        # 策略4: 選擇單選按鈕或複選框
        radio_buttons = self.page.locator('input[type="radio"], input[type="checkbox"]').all()
        if len(radio_buttons) > 0:
            try:
                # 查找第一個未勾選的
                for radio in radio_buttons:
                    is_checked = radio.is_checked()
                    if not is_checked:
                        radio.click()
                        self.page.wait_for_timeout(500)
                        return
            except:
                pass
        
        # 策略5: 尋找並調整數量為1
        quantity_input = self.page.locator('input[type="number"], input[name*="quantity"], input[name*="qty"]').first
        if quantity_input.count() > 0:
            try:
                quantity_input.clear()
                quantity_input.fill("1")
                self.page.wait_for_timeout(500)
            except:
                pass
    
    def get_cart_items_count(self):
        """
        獲取購物車中商品的數量
        返回: 商品數量 (int)
        """
        # 查找購物車中的商品項
        cart_items = self.page.locator('[class*="cart-item"], tr[class*="item"]').all()
        return len(cart_items)
    
    def verify_product_in_cart(self, product_name):
        """
        驗證特定產品是否在購物車中
        返回: True/False
        """
        # 查找購物車中是否包含該產品名稱
        product_element = self.page.locator(f'text="{product_name}"')
        return product_element.count() > 0
    
    def clear_cart(self):
        """
        清空購物車中的所有商品
        """
        # 查找清空購物車按鈕或刪除按鈕
        clear_buttons = self.page.locator('button:has-text("清空"), button:has-text("刪除"), button:has-text("remove")').all()
        
        # 逐個點擊刪除按鈕
        for _ in range(len(clear_buttons)):
            delete_button = self.page.locator('button:has-text("刪除"), button:has-text("remove")').first
            if delete_button.count() > 0:
                delete_button.click()
                self.page.wait_for_timeout(500)
            else:
                break
    
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
        # 方法 1: 嘗試查找「購物車為空」相關文本
        empty_text = self.page.locator("text=/購物車.*空|cart.*empty/i")
        if empty_text.count() > 0:
            assert empty_text.is_visible(), "購物車為空提示不可見"
            return
        
        # 方法 2: 檢查是否包含「購物車中沒有商品」
        empty_div = self.page.get_by_test_id("paper-cart-empty")
        if empty_div.count() > 0:
            assert empty_div.is_visible(), "購物車空狀態指示符不可見"
            return
        
        # 方法 3: 檢查是否沒有購物車項目容器
        cart_items = self.page.locator("[class*='cart-item'], [class*='product-item']")
        if cart_items.count() == 0:
            # 沒有項目，購物車為空
            return
        
        # 方法 4: 直接檢查頁面內容
        page_text = self.page.content()
        if "購物車中沒有商品" in page_text or "Your cart is empty" in page_text or "cart is empty" in page_text.lower():
            return
        
        # 如果頁面長度很小且沒有明顯產品內容，可能就是空的
        if len(page_text) < 5000 and "product" not in page_text.lower():
            LogHelpers.log_step("⚠️ 購物車頁面內容較少，判定為空")
            return
        
        # 都沒有找到，記錄詳細信息用於診斷
        print("\n❌ 購物車驗證失敗")
        print(f"頁面 URL: {self.page.url}")
        print(f"頁面標題: {self.page.title()}")
        print(f"頁面內容長度: {len(page_text)}")
        
        # 拍攝截圖用於診斷
        self.page.screenshot(path="./test-results/cart_verification_failure.png")
        
        raise AssertionError("無法驗證購物車狀態 - 頁面內容無法判斷購物車是否為空")
    
    def click_cat_section(self):
        """點擊貓貓專區"""
        self.cat_section_button.click()
    
    def navigate_to_cat_section(self):
        """導航到貓貓專區 - 別名方法"""
        self.click_cat_section()
    
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
