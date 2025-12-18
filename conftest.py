import pytest
from playwright.sync_api import sync_playwright, Page, Browser
import os
from pathlib import Path

# 测试结果目录
TEST_RESULTS_DIR = Path("./test-results")
TEST_RESULTS_DIR.mkdir(exist_ok=True)

# Auth 文件路径（用于已登录状态）
AUTH_FILE = "./fixtures/auth.json"


@pytest.fixture(scope="session")
def browser() -> Browser:
    """Session 级别的浏览器实例 - 在整个测试会话中共享"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture
def context(browser):
    """为每个测试创建新的浏览器上下文"""
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture
def page(context) -> Page:
    """为每个测试创建新的页面"""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def authenticated_page(browser):
    """返回已登录的页面（使用保存的认证状态）"""
    if not os.path.exists(AUTH_FILE):
        pytest.skip(f"Auth file not found: {AUTH_FILE}")
    
    context = browser.new_context(storage_state=AUTH_FILE)
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(autouse=True)
def test_setup_teardown():
    """测试前后的设置和清理"""
    # Setup
    print("\n=== Test Started ===")
    yield
    # Teardown
    print("=== Test Completed ===\n")


# Hook: 测试失败时自动截图
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