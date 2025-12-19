#!/usr/bin/env python
"""
調試腳本：測試商品選擇和定制化流程
"""
import sys
from playwright.sync_api import sync_playwright
from pages.cart_page import CartPage
from helpers.base_helpers import LogHelpers

def debug_product_selection():
    """調試商品選擇流程"""
    with sync_playwright() as p:
        # 使用瀏覽器
        context = p.chromium.launch_persistent_context(
            user_data_dir=None,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        # 從 fixtures/user.json 加載儲存的登錄狀態
        try:
            import json
            with open('fixtures/user.json', 'r') as f:
                storage_state = json.load(f)
            page = context.new_page()
            page.context.add_cookies(storage_state.get('cookies', []))
            # 設置 localStorage
            page.evaluate(f"() => {{ window.localStorage.clear(); }}")
            for item in storage_state.get('origins', []):
                for storage_item in item.get('localStorage', []):
                    page.evaluate(f"() => {{ window.localStorage.setItem('{storage_item['name']}', '{storage_item['value']}'); }}")
        except Exception as e:
            print(f"⚠️ 無法加載存儲狀態: {e}")
            page = context.new_page()
        
        try:
            LogHelpers.log_step("=" * 60)
            LogHelpers.log_step("商品選擇流程調試")
            LogHelpers.log_step("=" * 60)
            
            # 第一步：進入用戶頁面驗證登錄
            LogHelpers.log_step("\n[步驟 1] 驗證登錄狀態...")
            page.goto("https://www.dogcatstar.com/my-account/")
            page.wait_for_load_state("domcontentloaded", timeout=10000)
            LogHelpers.log_step(f"URL: {page.url}")
            LogHelpers.log_step(f"頁面標題: {page.title()}")
            
            if "my-account" not in page.url:
                LogHelpers.log_step("❌ 未進入用戶頁面，可能未登錄")
                return
            
            LogHelpers.log_step("✓ 已進入用戶頁面 - 登錄成功")
            page.wait_for_timeout(2000)
            
            # 第二步：進入貓貓專區
            LogHelpers.log_step("\n[步驟 2] 進入貓貓專區...")
            page.goto("https://www.dogcatstar.com/product-category/cat/")
            page.wait_for_load_state("domcontentloaded", timeout=10000)
            LogHelpers.log_step(f"URL: {page.url}")
            
            # 第三步：獲取商品信息
            LogHelpers.log_step("\n[步驟 3] 獲取第一個商品信息...")
            
            # 首先滾動到頁面底部以確保商品加載
            page.wait_for_timeout(1000)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            page.wait_for_timeout(1000)
            
            # 查找商品卡片而不是按鈕
            product_cards = page.locator('[class*="product"], [class*="item"], article').all()
            LogHelpers.log_step(f"找到 {len(product_cards)} 個潛在商品卡片")
            
            # 滾動到第一個商品
            if len(product_cards) > 0:
                product_cards[0].scroll_into_view_if_needed()
                page.wait_for_timeout(1000)
            
            cart_page = CartPage(page)
            product_info = cart_page.get_first_product_info()
            LogHelpers.log_step(f"商品名稱: {product_info['name']}")
            LogHelpers.log_step(f"商品價格: {product_info['price']}")
            page.wait_for_timeout(2000)
            
            # 第四步：點擊添加購物車按鈕
            LogHelpers.log_step("\n[步驟 4] 點擊 '加入購物車' 按鈕...")
            
            # 滾動到按鈕確保在視口內
            add_to_cart_button = page.locator('button:has-text("加入購物車")').first
            
            if add_to_cart_button.count() > 0:
                LogHelpers.log_step("✓ 找到 '加入購物車' 按鈕")
                LogHelpers.log_step("滾動到按鈕位置...")
                add_to_cart_button.scroll_into_view_if_needed()
                page.wait_for_timeout(1000)
                
                LogHelpers.log_step("正在點擊...")
                add_to_cart_button.click(force=True)
                LogHelpers.log_step("✓ 已點擊")
                page.wait_for_timeout(2000)
                
                # 第五步：檢查頁面上的所有選項元素
                LogHelpers.log_step("\n[步驟 5] 檢查頁面上的選項元素...")
                
                # 檢查按鈕
                all_buttons = page.locator('button').all()
                LogHelpers.log_step(f"找到 {len(all_buttons)} 個按鈕")
                for i, btn in enumerate(all_buttons[:10]):  # 只檢查前 10 個
                    btn_text = btn.text_content().strip()
                    if btn_text:
                        LogHelpers.log_step(f"  按鈕 {i+1}: {btn_text}")
                
                # 檢查 select 下拉菜單
                selects = page.locator('select').all()
                LogHelpers.log_step(f"找到 {len(selects)} 個下拉菜單")
                
                # 檢查單選/複選框
                radios = page.locator('input[type="radio"], input[type="checkbox"]').all()
                LogHelpers.log_step(f"找到 {len(radios)} 個單選/複選框")
                
                # 第六步：嘗試處理定制化選項
                LogHelpers.log_step("\n[步驟 6] 執行定制化選項處理...")
                cart_page._handle_product_customization()
                page.wait_for_timeout(2000)
                
                # 第七步：尋找確認按鈕
                LogHelpers.log_step("\n[步驟 7] 尋找確認按鈕...")
                
                confirm_buttons = [
                    page.locator('button:has-text("確定加入")').first,
                    page.locator('button:has-text("確認")').first,
                ]
                
                for i, btn in enumerate(confirm_buttons):
                    if btn.count() > 0:
                        LogHelpers.log_step(f"✓ 找到確認按鈕 {i+1}: '{btn.text_content().strip()}'")
                        LogHelpers.log_step("正在點擊...")
                        btn.click(force=True)
                        LogHelpers.log_step("✓ 已點擊")
                        page.wait_for_timeout(2000)
                        break
                else:
                    LogHelpers.log_step("⚠️ 未找到任何確認按鈕")
                
                # 第八步：檢查是否進入購物車
                LogHelpers.log_step("\n[步驟 8] 檢查購物車...")
                page.goto("https://www.dogcatstar.com/cart/")
                page.wait_for_load_state("domcontentloaded", timeout=10000)
                
                items_count = cart_page.get_cart_items_count()
                is_in_cart = cart_page.verify_product_in_cart(product_info['name'])
                
                LogHelpers.log_step(f"購物車商品數: {items_count}")
                LogHelpers.log_step(f"商品在購物車中: {is_in_cart}")
                
                if is_in_cart or items_count > 0:
                    LogHelpers.log_step("✓ 商品成功添加到購物車！")
                else:
                    LogHelpers.log_step("❌ 商品未成功添加到購物車")
            else:
                LogHelpers.log_step("❌ 未找到 '加入購物車' 按鈕")
                
        except Exception as e:
            LogHelpers.log_step(f"❌ 調試過程出錯: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            LogHelpers.log_step("\n" + "=" * 60)
            LogHelpers.log_step("調試完成")
            LogHelpers.log_step("=" * 60)
            page.close()
            context.close()

if __name__ == "__main__":
    debug_product_selection()
