#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
診斷腳本：檢查頁面結構
"""
from playwright.sync_api import sync_playwright
from helpers.base_helpers import LogHelpers
import json

def diagnose_page_structure():
    """診斷頁面結構"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        
        # 加載登錄狀態
        try:
            with open('fixtures/user.json', 'r', encoding='utf-8') as f:
                storage_state = json.load(f)
            context.add_cookies(storage_state.get('cookies', []))
        except Exception as e:
            LogHelpers.log_step(f"WARNING: 無法加載狀態: {e}")
        
        page = context.new_page()
        
        try:
            LogHelpers.log_step("=" * 80)
            LogHelpers.log_step("PAGE STRUCTURE DIAGNOSIS")
            LogHelpers.log_step("=" * 80)
            
            # 進入貓貓專區
            LogHelpers.log_step("\n[1] Going to cat category...")
            page.goto("https://www.dogcatstar.com/product-category/cat/")
            page.wait_for_load_state("domcontentloaded", timeout=10000)
            
            LogHelpers.log_step("[2] Checking product elements...")
            
            # 檢查各種可能的選擇器
            selectors = {
                'article.product': page.locator('article.product').all(),
                'li.product': page.locator('li.product').all(),
                '.product-item': page.locator('.product-item').all(),
                '.woocommerce-loop-product': page.locator('.woocommerce-loop-product').all(),
                '[class*="product"]': page.locator('[class*="product"]').all(),
                'a.woocommerce-loop-product__link': page.locator('a.woocommerce-loop-product__link').all(),
            }
            
            for selector_name, elements in selectors.items():
                LogHelpers.log_step(f"  {selector_name}: {len(elements)} elements")
            
            # 嘗試找到第一個真實商品
            LogHelpers.log_step("\n[3] Trying to find first real product...")
            
            # 獲取頁面中所有包含商品文本的鏈接
            all_links = page.locator('a').all()
            LogHelpers.log_step(f"Total links: {len(all_links)}")
            
            # 查找 href 包含 product 的鏈接
            product_links = page.locator('a[href*="product"]').all()
            LogHelpers.log_step(f"Product links (with /product/): {len(product_links)}")
            
            if len(product_links) > 0:
                for i, link in enumerate(product_links[:5]):  # 只看前 5 個
                    href = link.get_attribute('href')
                    text = link.text_content().strip()[:50]
                    if text:
                        LogHelpers.log_step(f"  {i+1}. {text}")
                        LogHelpers.log_step(f"     URL: {href}")
            
            # 查看頁面的 H2/H3 元素
            LogHelpers.log_step("\n[4] Product titles (H2/H3)...")
            product_titles = page.locator('h2, h3').all()
            LogHelpers.log_step(f"Total H2/H3: {len(product_titles)}")
            
            for i, title in enumerate(product_titles[:10]):
                text = title.text_content().strip()[:50]
                if text and len(text) > 3:
                    LogHelpers.log_step(f"  {i+1}. {text}")
            
            # 查看購物車頁面結構
            LogHelpers.log_step("\n[5] Checking cart page structure...")
            page.goto("https://www.dogcatstar.com/cart/")
            page.wait_for_load_state("domcontentloaded", timeout=10000)
            
            # 查找購物車商品
            cart_items = page.locator('[class*="cart-item"], tr[class*="item"], .woocommerce-cart-form__cart-item').all()
            LogHelpers.log_step(f"Cart items found: {len(cart_items)}")
            
            for i, item in enumerate(cart_items):
                text = item.text_content().strip()[:100]
                LogHelpers.log_step(f"  Item {i+1}: {text}")
            
            # 查找刪除按鈕
            delete_buttons = page.locator('button:has-text("刪除"), button:has-text("移除"), .remove').all()
            LogHelpers.log_step(f"Delete buttons found: {len(delete_buttons)}")
            
        except Exception as e:
            LogHelpers.log_step(f"ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            LogHelpers.log_step("\n" + "=" * 80)
            LogHelpers.log_step("DIAGNOSIS COMPLETE")
            LogHelpers.log_step("=" * 80)
            page.close()
            context.close()
            browser.close()

if __name__ == "__main__":
    diagnose_page_structure()
