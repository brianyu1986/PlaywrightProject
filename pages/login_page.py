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
        return self.page.get_by_role("textbox", name="請輸入").nth(1)
    
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
        self.login_button.click()