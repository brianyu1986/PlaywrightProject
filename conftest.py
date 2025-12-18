import pytest
from playwright.sync_api import sync_playwright, Page, Browser
import os
from pathlib import Path

# 測試結果目錄
TEST_RESULTS_DIR = Path("./test-results")
TEST_RESULTS_DIR.mkdir(exist_ok=True)

# Auth 檔案路徑（用於已登入狀態）
AUTH_FILE = "./fixtures/auth.json"


@pytest.fixture(scope="session")
def browser() -> Browser:
    """Session 層級的瀏覽器實例 - 在整個測試會話中共享"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture
def context(browser):
    """為每個測試建立新的瀏覽器上下文"""
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture
def page(context) -> Page:
    """為每個測試建立新的頁面"""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def authenticated_page(browser):
    """返回已登入的頁面（使用保存的認證狀態）"""
    if not os.path.exists(AUTH_FILE):
        pytest.skip(f"Auth file not found: {AUTH_FILE}")
    
    context = browser.new_context(storage_state=AUTH_FILE)
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(autouse=True)
def test_setup_teardown():
    """測試前後的設定和清理"""
    # 設定
    print("\n=== Test Started ===")
    yield
    # 清理
    print("=== Test Completed ===\n")


# 鈎子：測試失敗時自動截圖
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.failed and "page" in item.fixturenames:
        page = item.funcargs.get("page")
        if page:
            screenshot_path = f"./test-results/{item.name}_failure.png"
            page.screenshot(path=screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")