from playwright.sync_api import Page


class LoginPage:
    """登入頁面 - Page Object Model"""

    def __init__(self, page: Page):
        self.page = page
        self.page.goto("https://www.dogcatstar.com/my-account/")
    
    # 定位器 - 使用更穩健的策略
    @property
    def email_login_button(self):
        """使用 Email 登入按鈕"""
        return self.page.get_by_role("button", name="使用 Email 登入")
    
    @property
    def email_input_field(self):
        """電郵輸入框 - 使用特定的選擇器"""
        # 嘗試使用 get_by_placeholder 先找到具體的郵件輸入框
        email_field = self.page.locator("input[type='email'], input[placeholder*='郵']").first
        if email_field.count() > 0:
            return email_field
        # 備選方案：使用 get_by_role 但加上更多過濾
        return self.page.get_by_role("textbox").locator("visible=true").first
    
    @property
    def email_confirm_button(self):
        """電郵確認按鈕 - 查找所有確認按鈕的第一個"""
        buttons = self.page.get_by_role("button", name="確認")
        return buttons.first if buttons.count() > 0 else None
    
    @property
    def password_login_button(self):
        """密碼登入按鈕"""
        return self.page.get_by_role("button", name="密碼登入")
    
    @property
    def password_input_field(self):
        """密碼輸入框 - 使用特定的選擇器"""
        # 嘗試使用 get_by_type 選擇密碼輸入框
        password_field = self.page.locator("input[type='password']").first
        if password_field.count() > 0:
            return password_field
        # 備選方案
        return self.page.get_by_role("textbox").nth(1)
    
    @property
    def password_confirm_button(self):
        """密碼確認按鈕 - 查找所有確認按鈕的最後一個"""
        buttons = self.page.get_by_role("button", name="確認")
        if buttons.count() > 1:
            return buttons.nth(1)
        elif buttons.count() > 0:
            return buttons.last
        return None
    
    # 操作方法
    def login_with_email_and_password(self, email: str, password: str):
        """使用電郵和密碼登入 - 分步驟操作"""
        try:
            # 步驟 1: 點擊使用 Email 登入
            email_btn = self.email_login_button
            if email_btn:
                email_btn.click()
                self.page.wait_for_timeout(500)
            
            # 步驟 2: 輸入電郵
            email_field = self.email_input_field
            if email_field:
                email_field.click()
                self.page.wait_for_timeout(200)
                email_field.fill(email)
                self.page.wait_for_timeout(300)
            
            # 步驟 3: 點擊電郵確認按鈕
            email_confirm = self.email_confirm_button
            if email_confirm:
                email_confirm.click()
                self.page.wait_for_timeout(1500)  # 等待頁面轉換到密碼步驟
            
            # 步驟 4: 檢查密碼登入按鈕是否出現
            password_btn = self.password_login_button
            if password_btn:
                # 確保按鈕可見且可點擊
                password_btn.scroll_into_view_if_needed()
                self.page.wait_for_timeout(300)
                password_btn.click()
                self.page.wait_for_timeout(500)
            
            # 步驟 5: 輸入密碼
            password_field = self.password_input_field
            if password_field:
                password_field.click()
                self.page.wait_for_timeout(200)
                password_field.fill(password)
                self.page.wait_for_timeout(300)
            
            # 步驟 6: 點擊密碼確認按鈕
            password_confirm = self.password_confirm_button
            if password_confirm:
                password_confirm.click()
                # 等待登入完成
                self.page.wait_for_url("**/my-account/**", timeout=15000)
            
        except Exception as e:
            print(f"❌ 登入過程中出錯: {str(e)}")
            raise
    
    def login_by_email(self):
        """點擊電郵登入"""
        email_btn = self.email_login_button
        if email_btn:
            email_btn.click()
    
    def enter_email(self, email: str):
        """輸入電郵"""
        email_field = self.email_input_field
        if email_field:
            email_field.fill(email)
    
    def confirm_email(self):
        """確認電郵"""
        email_confirm = self.email_confirm_button
        if email_confirm:
            email_confirm.click()
    
    def login_with_password(self):
        """點擊密碼登入"""
        password_btn = self.password_login_button
        if password_btn:
            password_btn.click()
    
    def enter_password(self, password: str):
        """輸入密碼"""
        password_field = self.password_input_field
        if password_field:
            password_field.fill(password)
    
    def confirm_password(self):
        """確認密碼"""
        password_confirm = self.password_confirm_button
        if password_confirm:
            password_confirm.click()
            # 等待登入完成
            self.page.wait_for_url("**/my-account/**", timeout=15000)