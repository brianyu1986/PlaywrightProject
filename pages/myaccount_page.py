from playwright.sync_api import Page

class MyAccountPage:

    def __init__(self, page:Page):
        self.page = page
        self.page.goto("https://www.dogcatstar.com/my-account/")
        self.email_login = page.get_by_role("button", name="使用 Email 登入")
        self.email_input = page.get_by_role("textbox", name="請輸入")
        self.email_confirm = page.get_by_role("button", name="確認")
        self.usePassword_button = page.get_by_role("button", name="密碼登入")
        self.password_input = page.get_by_role("textbox", name="請輸入")
        self.login_button = page.get_by_role("button", name="確認")
