"""公共辅助函数 - 等待、日志、重试等"""

import time
from playwright.sync_api import Page
from typing import Callable


class WaitHelpers:
    """等待相关的辅助函数"""
    
    @staticmethod
    def wait_for_element(page: Page, locator, timeout: int = 5000):
        """等待元素出现"""
        try:
            page.wait_for_selector(locator, timeout=timeout)
            return True
        except Exception:
            return False
    
    @staticmethod
    def wait_and_click(page: Page, selector: str, timeout: int = 5000):
        """等待元素出现后点击"""
        page.wait_for_selector(selector, timeout=timeout)
        page.click(selector)
    
    @staticmethod
    def wait_for_navigation(page: Page, callback: Callable, timeout: int = 5000):
        """等待页面导航"""
        with page.expect_navigation(timeout=timeout):
            callback()


class ScreenshotHelpers:
    """截图相关的辅助函数"""
    
    @staticmethod
    def take_screenshot(page: Page, filename: str):
        """截图"""
        page.screenshot(path=f"./test-results/{filename}.png")


class LogHelpers:
    """日志相关的辅助函数"""
    
    @staticmethod
    def log_action(action: str):
        """记录操作"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {action}")
    
    @staticmethod
    def log_step(step_number: int, description: str):
        """记录测试步骤"""
        print(f"\n--- Step {step_number}: {description} ---")


class RetryHelpers:
    """重试相关的辅助函数"""
    
    @staticmethod
    def retry_action(func: Callable, retries: int = 3, delay: float = 0.5):
        """重试执行函数"""
        for attempt in range(retries):
            try:
                return func()
            except Exception as e:
                if attempt == retries - 1:
                    raise
                time.sleep(delay)
                continue
