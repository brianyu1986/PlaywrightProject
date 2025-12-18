from playwright.sync_api import Page


class LoginPage:
    """登入頁面 - Page Object Model"""

    def __init__(self, page: Page):
        self.page = page
        self.page.goto("https://www.dogcatstar.com/my-account/")
    
    # 定位器
    @property
    def email_login_button(self):
        return self.page.get_by_role("button", name="使用 Email 登入")
    
    @property
    def email_input_field(self):
        return self.page.get_by_role("textbox", name="請輸入").first
    
    @property
    def email_confirm_button(self):
        return self.page.get_by_role("button", name="確認").first
    
    @property
    def password_login_button(self):
        return self.page.get_by_role("button", name="密碼登入")
    
    @property
    def password_input_field(self):
        # 使用更穩健的定位策略 - 查找所有文本框後過濾
        all_inputs = self.page.locator('input[type="password"], input[type="text"]')
        # 嘗試通過 placeholder 找到密碼輸入框
        password_input = self.page.locator('input[placeholder*="密碼"], input[placeholder*="輸入"]')
        if password_input.count() > 0:
            return password_input.first
        # 備選方案：使用 nth
        return all_inputs.nth(1) if all_inputs.count() > 1 else all_inputs.first
    
    @property
    def password_confirm_button(self):
        return self.page.get_by_role("button", name="確認").nth(1)
    
    # 操作
    def login_with_email_and_password(self, email: str, password: str):
        """使用電郵和密碼登入"""
        self.email_login_button.click()
        self.email_input_field.fill(email)
        self.email_confirm_button.click()
        
        self.password_login_button.click()
        self.password_input_field.fill(password)
        self.password_confirm_button.click()
    
    def login_by_email(self):
        """點擊電郵登入"""
        self.email_login_button.click()
    
    def enter_email(self, email: str):
        """輸入電郵"""
        self.email_input_field.fill(email)
    
    def confirm_email(self):
        """確認電郵"""
        self.email_confirm_button.click()
    
    def login_with_password(self):
        """點擊密碼登入"""
        self.password_login_button.click()
    
    def enter_password(self, password: str):
        """輸入密碼"""
        self.password_input_field.fill(password)
    
    def confirm_password(self):
        """確認密碼"""
        self.password_confirm_button.click()
        # 等待登入完成
        self.page.wait_for_url("**/my-account/**", timeout=10000)