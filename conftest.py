import pytest
from playwright.sync_api import sync_playwright, Page, Browser
import os
from pathlib import Path

# 測試結果目錄
TEST_RESULTS_DIR = Path("./test-results")
TEST_RESULTS_DIR.mkdir(exist_ok=True)

# Auth 檔案路徑（用於已登入狀態）
AUTH_FILE = "./fixtures/user.json"  # 使用真實的用戶登入狀態


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
    """
    返回已登入的頁面（使用保存的認證狀態）
    
    如果驗證狀態檔案不存在，將跳過使用此 fixture 的測試
    """
    auth_path = Path(AUTH_FILE)
    
    # 如果驗證狀態不存在，則跳過測試
    if not auth_path.exists():
        pytest.skip(f"驗證狀態檔案不存在，無法進行需要認證的測試：{AUTH_FILE}")
    
    try:
        # 使用保存的驗證狀態建立新上下文
        context = browser.new_context(storage_state=str(auth_path))
        page = context.new_page()
        yield page
        page.close()
        context.close()
    except Exception as e:
        pytest.skip(f"無法載入驗證狀態：{str(e)}")


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