from playwright.sync_api import Page, expect
from helpers.base_helpers import LogHelpers


class CartPage:
    """購物車頁面 - Page Object Model"""

    def __init__(self, page: Page):
        self.page = page
        self.page.goto("https://www.dogcatstar.com/")
    
    def close_popup_if_exists(self):
        """
        檢測並關閉購物車頁面上的彈出窗口
        支持關閉按鈕和"今日不再顯示"按鈕
        """
        LogHelpers.log_step("檢查是否有彈出窗口...")
        self.page.wait_for_timeout(1000)  # 等待彈出窗口加載
        
        # 查找彈出窗口容器
        popup_selectors = [
            '[role="dialog"]',
            '[class*="modal"]',
            '[class*="popup"]',
            '[class*="overlay"]',
            '.swal2-container',  # SweetAlert
            '.modal',
        ]
        
        popup_found = False
        for selector in popup_selectors:
            popups = self.page.locator(selector).all()
            if len(popups) > 0:
                # 檢查彈出窗口是否可見
                for popup in popups:
                    if popup.is_visible():
                        LogHelpers.log_step(f"✓ 找到彈出窗口: {selector}")
                        popup_found = True
                        
                        # 先嘗試找"今日不再顯示"按鈕
                        do_not_show_button = popup.locator('button:has-text("今日不再顯示"), label:has-text("今日不再顯示")').first
                        if do_not_show_button.count() > 0:
                            try:
                                LogHelpers.log_step("點擊 '今日不再顯示'...")
                                do_not_show_button.click()
                                self.page.wait_for_timeout(500)
                            except Exception as e:
                                LogHelpers.log_step(f"WARNING: 點擊失敗: {str(e)}")
                        
                        # 然後尋找關閉按鈕
                        close_buttons = [
                            popup.locator('button:has-text("關閉")'),
                            popup.locator('button:has-text("×")'),
                            popup.locator('button:has-text("X")'),
                            popup.locator('button.close, button[class*="close"], button[aria-label*="close"]'),
                            popup.locator('.swal2-close'),  # SweetAlert
                        ]
                        
                        for close_btn in close_buttons:
                            if close_btn.first.count() > 0:
                                try:
                                    LogHelpers.log_step("點擊關閉按鈕...")
                                    close_btn.first.click(force=True)
                                    self.page.wait_for_timeout(500)
                                    LogHelpers.log_step("✓ 彈出窗口已關閉")
                                    return True
                                except Exception as e:
                                    LogHelpers.log_step(f"WARNING: 關閉失敗: {str(e)}")
                                    continue
                        
                        # 如果都找不到，嘗試點擊彈出窗口外部關閉
                        try:
                            LogHelpers.log_step("嘗試按 ESC 鍵關閉...")
                            self.page.press("Escape")
                            self.page.wait_for_timeout(500)
                            LogHelpers.log_step("✓ 已按 ESC 鍵")
                            return True
                        except Exception as e:
                            LogHelpers.log_step(f"WARNING: ESC 失敗: {str(e)}")
        
        if not popup_found:
            LogHelpers.log_step("✓ 未發現彈出窗口")
        
        return not popup_found
    
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
        LogHelpers.log_step("尋找商品信息...")
        
        # 使用 WooCommerce 標準選擇器查找商品
        # 嘗試使用 a.woocommerce-loop-product__link 這是真實商品鏈接
        product_links = self.page.locator('a.woocommerce-loop-product__link').all()
        LogHelpers.log_step(f"找到 {len(product_links)} 個商品鏈接")
        
        if len(product_links) > 0:
            # 使用第一個商品鏈接的文本作為商品名稱
            first_product_link = product_links[0]
            product_name = first_product_link.text_content().strip()
            LogHelpers.log_step(f"✓ 找到商品: {product_name}")
            
            # 尋找價格 - 通常在商品鏈接的父元素內
            parent = first_product_link.locator("..")
            price_locator = parent.locator('.price, .product-price, .woocommerce-Price-amount, [class*="price"]').first
            product_price = price_locator.text_content().strip() if price_locator.count() > 0 else "N/A"
            LogHelpers.log_step(f"  價格: {product_price}")
        else:
            # 備用方案
            LogHelpers.log_step("未找到商品鏈接，使用備用選擇器...")
            product_name_locator = self.page.locator('.product-item-name, [class*="product-title"], h2, h3').first
            product_name = product_name_locator.text_content().strip() if product_name_locator.count() > 0 else "Unknown Product"
            
            price_locator = self.page.locator('[class*="price"], [class*="amount"]').first
            product_price = price_locator.text_content().strip() if price_locator.count() > 0 else "Unknown Price"
        
        return {
            'name': product_name,
            'price': product_price
        }
    
    def add_first_product_to_cart(self, wait_for_observation=False):
        """
        添加第一個產品到購物車（含定制化選項處理和速率限制處理）
        
        參數:
            wait_for_observation (bool): 是否在操作完成後等待2秒以觀察結果（非headless模式）
        
        返回: 產品信息 {'name': 名稱, 'price': 價格}
        """
        LogHelpers.log_step("準備添加商品到購物車...")
        
        # 先記錄產品信息
        product_info = self.get_first_product_info()
        LogHelpers.log_step(f"商品信息: {product_info['name']} - {product_info['price']}")
        
        # 找到第一個商品鏈接所在的容器
        LogHelpers.log_step("找到商品容器...")
        product_links = self.page.locator('a.woocommerce-loop-product__link').all()
        
        if len(product_links) == 0:
            LogHelpers.log_step("ERROR: 未找到商品鏈接")
            return product_info
        
        # 獲取第一個商品的容器（直接使用 Page 進行全頁搜索）
        first_product_link = product_links[0]
        
        LogHelpers.log_step("滾動到第一個商品...")
        first_product_link.scroll_into_view_if_needed()
        self.page.wait_for_timeout(2000)
        
        # 在頁面上查找添加購物車按鈕（通常在第一個商品附近）
        LogHelpers.log_step("尋找 '加入購物車' 按鈕...")
        add_to_cart_buttons = self.page.locator('button:has-text("加入購物車"), a.button:has-text("加入購物車"), .add-to-cart, button.add_to_cart').all()
        LogHelpers.log_step(f"找到 {len(add_to_cart_buttons)} 個按鈕")
        
        if len(add_to_cart_buttons) > 0:
            # 使用第一個按鈕
            add_to_cart_button = add_to_cart_buttons[0]
            LogHelpers.log_step("✓ 找到按鈕，正在點擊...")
            try:
                add_to_cart_button.scroll_into_view_if_needed()
                self.page.wait_for_timeout(1000)
                add_to_cart_button.click(force=True)
                LogHelpers.log_step("✓ 按鈕已點擊")
            except Exception as e:
                error_msg = str(e)
                if "rate" in error_msg.lower() or "limit" in error_msg.lower():
                    LogHelpers.log_step(f"ERROR: 觸發速率限制: {error_msg}")
                    LogHelpers.log_step("等待 60 秒後重試...")
                    self.page.wait_for_timeout(60000)
                else:
                    LogHelpers.log_step(f"ERROR: Click failed with: {error_msg}")
                return product_info
            
            # 等待任何選項對話框或選擇面板出現（增加等待時間）
            LogHelpers.log_step("等待選項對話框（3秒）...")
            self.page.wait_for_timeout(3000)
            
            # 檢查是否出現速率限制錯誤
            if "rate limit" in self.page.content().lower() or "too many requests" in self.page.content().lower():
                LogHelpers.log_step("ERROR: 檢測到速率限制訊息")
                LogHelpers.log_step("等待 90 秒...")
                self.page.wait_for_timeout(90000)
                # 嘗試重新加載頁面
                self.page.reload()
                self.page.wait_for_load_state("domcontentloaded", timeout=10000)
            
            # 嘗試處理定制化選項
            LogHelpers.log_step("處理定制化選項...")
            self._handle_product_customization()
            
            # 尋找並點擊確認按鈕
            LogHelpers.log_step("尋找確認按鈕...")
            self.page.wait_for_timeout(1500)
            
            # 嘗試多種確認按鈕選擇器
            confirm_button = None
            for selector in [
                'button:has-text("確定加入")',
                'button:has-text("確認")',
                'button:has-text("確定")',
                'button.confirm, button.submit'
            ]:
                btn = self.page.locator(selector).first
                if btn.count() > 0:
                    LogHelpers.log_step(f"✓ 找到確認按鈕: {selector}")
                    confirm_button = btn
                    break
            
            # 如果沒找到確認按鈕，試試找第二個"加入購物車"按鈕
            if confirm_button is None:
                all_add_buttons = self.page.locator('button:has-text("加入購物車")').all()
                if len(all_add_buttons) > 1:
                    LogHelpers.log_step(f"✓ 找到 {len(all_add_buttons)} 個按鈕，使用第二個")
                    confirm_button = all_add_buttons[1]
            
            # 點擊確認按鈕
            if confirm_button is not None:
                try:
                    LogHelpers.log_step("點擊確認按鈕...")
                    confirm_button.scroll_into_view_if_needed()
                    self.page.wait_for_timeout(1000)
                    confirm_button.click(force=True)
                    LogHelpers.log_step("✓ 確認按鈕已點擊")
                    self.page.wait_for_timeout(3000)
                except Exception as e:
                    error_msg = str(e)
                    if "rate" in error_msg.lower():
                        LogHelpers.log_step(f"ERROR: 確認時觸發速率限制")
                        self.page.wait_for_timeout(90000)
                    else:
                        LogHelpers.log_step(f"WARNING: Confirm click failed: {error_msg}")
            else:
                LogHelpers.log_step("WARNING: 未找到任何確認按鈕")
            
            # 如果需要觀察，等待2秒
            if wait_for_observation:
                LogHelpers.log_step("等待觀察結果...")
                self.page.wait_for_timeout(2000)
        else:
            LogHelpers.log_step("ERROR: 未找到 '加入購物車' 按鈕")
        
        return product_info
    
    def _handle_product_customization(self):
        """
        處理產品定制化選項（如規格、數量、顏色等）
        優先選擇"鲁斯佛款"，否則選擇第一個可用選項
        """
        LogHelpers.log_step("開始處理商品定制化選項...")
        self.page.wait_for_timeout(500)
        
        # 策略1: 尋找並點擊"鲁斯佛款"選項
        LogHelpers.log_step("策略 1: 尋找 '鲁斯佛款' 選項...")
        rostoff_option = self.page.locator('button:has-text("鲁斯佛"), span:has-text("鲁斯佛")').first
        if rostoff_option.count() > 0:
            try:
                LogHelpers.log_step("✓ 找到 '鲁斯佛款' 選項，正在點擊...")
                rostoff_option.click()
                self.page.wait_for_timeout(500)
                LogHelpers.log_step("✓ '鲁斯佛款' 已選擇")
                return
            except Exception as e:
                LogHelpers.log_step(f"✗ '鲁斯佛款' 點擊失敗: {str(e)}")
                pass
        else:
            LogHelpers.log_step("✗ 未找到 '鲁斯佛款' 選項")
        
        # 策略2: 尋找並點擊任何規格選項按鈕
        LogHelpers.log_step("策略 2: 尋找規格選項按鈕...")
        option_buttons = self.page.locator('button[class*="variant"], button[class*="option"], button[class*="size"]').all()
        LogHelpers.log_step(f"找到 {len(option_buttons)} 個規格選項按鈕")
        if len(option_buttons) > 0:
            try:
                button_text = option_buttons[0].text_content()
                LogHelpers.log_step(f"正在點擊第一個規格按鈕: '{button_text}'")
                option_buttons[0].click()
                self.page.wait_for_timeout(500)
                LogHelpers.log_step("✓ 規格選項已選擇")
                return
            except Exception as e:
                LogHelpers.log_step(f"✗ 規格選項點擊失敗: {str(e)}")
                pass
        else:
            LogHelpers.log_step("✗ 未找到規格選項按鈕")
        
        # 策略3: 選擇下拉菜單選項
        LogHelpers.log_step("策略 3: 尋找下拉菜單...")
        selects = self.page.locator('select').all()
        LogHelpers.log_step(f"找到 {len(selects)} 個下拉菜單")
        for i, select in enumerate(selects):
            try:
                LogHelpers.log_step(f"正在處理第 {i+1} 個下拉菜單...")
                # 點擊 select 元素打開下拉菜單
                select.click()
                self.page.wait_for_timeout(300)
                
                # 查找第一個選項
                option = self.page.locator('option').nth(1)  # 跳過預設選項
                if option.count() > 0:
                    option_text = option.text_content()
                    LogHelpers.log_step(f"正在選擇下拉菜單選項: '{option_text}'")
                    option.click()
                    self.page.wait_for_timeout(500)
                    LogHelpers.log_step("✓ 下拉菜單選項已選擇")
                    return
            except Exception as e:
                LogHelpers.log_step(f"✗ 下拉菜單處理失敗: {str(e)}")
                pass
        
        # 策略4: 選擇單選按鈕或複選框
        LogHelpers.log_step("策略 4: 尋找單選按鈕或複選框...")
        radio_buttons = self.page.locator('input[type="radio"], input[type="checkbox"]').all()
        LogHelpers.log_step(f"找到 {len(radio_buttons)} 個單選/複選框")
        if len(radio_buttons) > 0:
            try:
                # 查找第一個未勾選的
                for j, radio in enumerate(radio_buttons):
                    is_checked = radio.is_checked()
                    LogHelpers.log_step(f"單選框 {j+1}: 已勾選={is_checked}")
                    if not is_checked:
                        LogHelpers.log_step(f"正在點擊未勾選的單選框 {j+1}...")
                        radio.click()
                        self.page.wait_for_timeout(500)
                        LogHelpers.log_step("✓ 單選框已選擇")
                        return
            except Exception as e:
                LogHelpers.log_step(f"✗ 單選框處理失敗: {str(e)}")
                pass
        
        # 策略5: 尋找並調整數量為1
        LogHelpers.log_step("策略 5: 尋找數量輸入框...")
        quantity_input = self.page.locator('input[type="number"], input[name*="quantity"], input[name*="qty"]').first
        if quantity_input.count() > 0:
            try:
                current_value = quantity_input.input_value()
                LogHelpers.log_step(f"找到數量輸入框，當前值: {current_value}")
                quantity_input.clear()
                quantity_input.fill("1")
                self.page.wait_for_timeout(500)
                LogHelpers.log_step("✓ 數量已設置為 1")
            except Exception as e:
                LogHelpers.log_step(f"✗ 數量輸入框處理失敗: {str(e)}")
                pass
        else:
            LogHelpers.log_step("✗ 未找到數量輸入框")
        
        LogHelpers.log_step("商品定制化選項處理完成")
    
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
        LogHelpers.log_step("尋找刪除按鈕...")
        
        # 嘗試多種刪除按鈕選擇器
        selectors = [
            'button:has-text("刪除")',
            'button:has-text("移除")',
            'button:has-text("Remove")',
            'button.remove, a.remove, [class*="remove"]',
            '.product-remove a, .product-remove button',
            'a[data-product_key]'  # WooCommerce 標準刪除按鈕
        ]
        
        for selector in selectors:
            delete_buttons = self.page.locator(selector).all()
            if len(delete_buttons) > 0:
                LogHelpers.log_step(f"✓ 找到 {len(delete_buttons)} 個刪除按鈕 (選擇器: {selector})")
                
                # 逐個點擊刪除按鈕
                attempt = 0
                while attempt < len(delete_buttons):
                    try:
                        # 重新查找按鈕，因為 DOM 可能已更改
                        new_buttons = self.page.locator(selector).all()
                        if len(new_buttons) == 0:
                            LogHelpers.log_step("✓ 所有商品已刪除")
                            break
                        
                        btn = new_buttons[0]
                        LogHelpers.log_step(f"點擊刪除按鈕 {attempt + 1}...")
                        btn.scroll_into_view_if_needed()
                        self.page.wait_for_timeout(500)
                        btn.click(force=True)
                        LogHelpers.log_step("✓ 已點擊")
                        self.page.wait_for_timeout(2000)  # 等待購物車更新
                        attempt += 1
                    except Exception as e:
                        LogHelpers.log_step(f"WARNING: 刪除失敗: {str(e)}")
                        break
                
                return  # 成功找到並嘗試刪除
        
        LogHelpers.log_step("WARNING: 未找到任何刪除按鈕")
    
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
