"""公共輔助函數 - 等待、日誌、重試等"""

import time
from playwright.sync_api import Page
from typing import Callable


class WaitHelpers:
    """等待相關的輔助函數"""
    
    @staticmethod
    def wait_for_element(page: Page, locator, timeout: int = 5000):
        """等待元素出現"""
        try:
            page.wait_for_selector(locator, timeout=timeout)
            return True
        except Exception:
            return False
    
    @staticmethod
    def wait_and_click(page: Page, selector: str, timeout: int = 5000):
        """等待元素出現後點擊"""
        page.wait_for_selector(selector, timeout=timeout)
        page.click(selector)
    
    @staticmethod
    def wait_for_navigation(page: Page, callback: Callable, timeout: int = 5000):
        """等待頁面導航"""
        with page.expect_navigation(timeout=timeout):
            callback()


class ScreenshotHelpers:
    """截圖相關的輔助函數"""
    
    @staticmethod
    def take_screenshot(page: Page, filename: str):
        """截圖"""
        page.screenshot(path=f"./test-results/{filename}.png")


class LogHelpers:
    """日誌相關的輔助函數"""
    
    @staticmethod
    def log_action(action: str):
        """記錄操作"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {action}")
    
    @staticmethod
    def log_step(step_info, description: str = None):
        """
        記錄測試步驟
        
        支援兩種用法：
        1. log_step("描述文字") - 簡單描述
        2. log_step(1, "描述文字") - 包含步驟號
        """
        if isinstance(step_info, int):
            # 格式：log_step(1, "描述")
            print(f"\n--- Step {step_info}: {description} ---")
        else:
            # 格式：log_step("描述")
            print(f"\n>> {step_info}")


class RetryHelpers:
    """重試相關的輔助函數"""
    
    @staticmethod
    def retry_action(func: Callable, retries: int = 3, delay: float = 0.5):
        """重試執行函數"""
        for attempt in range(retries):
            try:
                return func()
            except Exception as e:
                if attempt == retries - 1:
                    raise
                time.sleep(delay)
                continue
