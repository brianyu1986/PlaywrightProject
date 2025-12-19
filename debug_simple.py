#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
簡化調試腳本：測試商品選擇和定制化流程
"""
from playwright.sync_api import sync_playwright
from pages.cart_page import CartPage
from helpers.base_helpers import LogHelpers

def debug_product_selection():
    """調試商品選擇流程"""
    with sync_playwright() as p:
        # 使用瀏覽器
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        
        # 直接加載保存的狀態到 context
        import json
        try:
            with open('fixtures/user.json', 'r', encoding='utf-8') as f:
                storage_state = json.load(f)
            context.add_cookies(storage_state.get('cookies', []))
        except Exception as e:
            LogHelpers.log_step(f"WARNING: 無法加載狀態: {e}")
        
        page = context.new_page()
        
        try:
            LogHelpers.log_step("=" * 60)
            LogHelpers.log_step("PRODUCT SELECTION DEBUG")
            LogHelpers.log_step("=" * 60)
            
            # Step 1: Verify login
            LogHelpers.log_step("\n[STEP 1] Checking login...")
            page.goto("https://www.dogcatstar.com/my-account/")
            page.wait_for_load_state("domcontentloaded", timeout=10000)
            if "my-account" in page.url:
                LogHelpers.log_step("OK: Login verified")
            else:
                LogHelpers.log_step("ERROR: Not logged in")
                return
            
            page.wait_for_timeout(2000)
            
            # Step 2: Navigate to cat category
            LogHelpers.log_step("\n[STEP 2] Navigating to cat category...")
            page.goto("https://www.dogcatstar.com/product-category/cat/")
            page.wait_for_load_state("domcontentloaded", timeout=10000)
            LogHelpers.log_step("OK: Cat category loaded")
            
            page.wait_for_timeout(2000)
            
            # Step 3: Find product information
            LogHelpers.log_step("\n[STEP 3] Getting product info...")
            cart_page = CartPage(page)
            
            # Get all products
            products = page.locator('[class*="product-item"], [class*="woocommerce-loop-product"], li.product').all()
            LogHelpers.log_step(f"Found {len(products)} products on page")
            
            if len(products) > 0:
                # Scroll to first product
                products[0].scroll_into_view_if_needed()
                page.wait_for_timeout(1000)
                
                product_info = cart_page.get_first_product_info()
                LogHelpers.log_step(f"Product name: {product_info['name']}")
                LogHelpers.log_step(f"Product price: {product_info['price']}")
            
            # Step 4: Find and click add to cart
            LogHelpers.log_step("\n[STEP 4] Looking for add to cart button...")
            add_buttons = page.locator('button:has-text("加入購物車")').all()
            LogHelpers.log_step(f"Found {len(add_buttons)} add to cart buttons")
            
            if len(add_buttons) > 0:
                # Click the first button
                LogHelpers.log_step("Scrolling to first button...")
                add_buttons[0].scroll_into_view_if_needed()
                page.wait_for_timeout(1000)
                
                LogHelpers.log_step("Clicking add to cart button...")
                add_buttons[0].click(force=True)
                LogHelpers.log_step("OK: Button clicked")
                
                page.wait_for_timeout(3000)
                
                # Step 5: Check for customization options
                LogHelpers.log_step("\n[STEP 5] Checking for options dialog...")
                
                # Check for different dialog elements
                dialogs = page.locator('[role="dialog"], [class*="modal"], [class*="popup"]').all()
                LogHelpers.log_step(f"Found {len(dialogs)} dialog elements")
                
                # Check for buttons in dialog
                all_buttons = page.locator('button').all()
                LogHelpers.log_step(f"Total buttons on page: {len(all_buttons)}")
                
                button_texts = set()
                for btn in all_buttons[:20]:  # Check first 20 buttons
                    text = btn.text_content().strip()
                    if text and len(text) < 50:
                        button_texts.add(text)
                
                LogHelpers.log_step("Button texts found:")
                for text in sorted(button_texts):
                    LogHelpers.log_step(f"  - {text}")
                
                # Step 6: Try customization
                LogHelpers.log_step("\n[STEP 6] Handling customization...")
                cart_page._handle_product_customization()
                
                page.wait_for_timeout(2000)
                
                # Step 7: Look for confirm button
                LogHelpers.log_step("\n[STEP 7] Looking for confirm button...")
                confirm_buttons = page.locator('button:has-text("確定"), button:has-text("確認"), button:has-text("確定加入")').all()
                LogHelpers.log_step(f"Found {len(confirm_buttons)} confirm buttons")
                
                if len(confirm_buttons) > 0:
                    LogHelpers.log_step("Clicking confirm button...")
                    confirm_buttons[0].click(force=True)
                    LogHelpers.log_step("OK: Confirm button clicked")
                    page.wait_for_timeout(3000)
                
                # Step 8: Check cart
                LogHelpers.log_step("\n[STEP 8] Checking cart...")
                page.goto("https://www.dogcatstar.com/cart/")
                page.wait_for_load_state("domcontentloaded", timeout=10000)
                
                items_count = cart_page.get_cart_items_count()
                LogHelpers.log_step(f"Items in cart: {items_count}")
                
                if items_count > 0:
                    LogHelpers.log_step("SUCCESS: Product added to cart!")
                else:
                    LogHelpers.log_step("INFO: No items in cart")
                
        except Exception as e:
            LogHelpers.log_step(f"ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            LogHelpers.log_step("\n" + "=" * 60)
            LogHelpers.log_step("DEBUG COMPLETE")
            LogHelpers.log_step("=" * 60)
            page.close()
            context.close()
            browser.close()

if __name__ == "__main__":
    debug_product_selection()
