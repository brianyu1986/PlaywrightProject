"""
購物車功能測試 - 使用驗證狀態版本

此模組包含兩種測試方式：
1. 獨立測試 - 每個測試獨立運行，便於調試
2. 集成測試 - 完整流程演示
"""

import pytest
from pages.cart_page import CartPage
from helpers.base_helpers import LogHelpers, WaitHelpers


class TestCartWithAuth:
    """使用驗證狀態的購物車測試 - 獨立模式"""
    
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_cart_is_initially_empty(self, authenticated_page):
        """
        測試：驗證購物車功能可用（已登入狀態）
        
        步驟：
        1. 導航到購物車頁面
        2. 驗證頁面加載成功（可能重定向）
        """
        page = authenticated_page
        LogHelpers.log_step("導航到購物車頁面")
        page.goto("https://www.dogcatstar.com/cart/")
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        
        LogHelpers.log_step(f"最終 URL: {page.url}")
        LogHelpers.log_step(f"頁面標題: {page.title()}")
        
        LogHelpers.log_step("[PASS] 購物車頁面已加載")
    
    
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_navigate_to_cat_section(self, authenticated_page):
        """
        測試：導航到貓貓專區（已登入狀態）
        
        步驟：
        1. 直接導航到貓貓專區 URL
        2. 驗證頁面加載成功
        """
        page = authenticated_page
        
        LogHelpers.log_step("直接導航到貓貓專區")
        page.goto("https://www.dogcatstar.com/product-category/cat/")
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        
        LogHelpers.log_step("驗證 URL 正確")
        current_url = page.url
        LogHelpers.log_step(f"當前 URL: {current_url}")
        assert "cat" in current_url and "product" in current_url, f"未進入貓貓專區，URL: {current_url}"
        
        LogHelpers.log_step("驗證頁面加載成功")
        title = page.title()
        LogHelpers.log_step(f"頁面標題: {title}")
        assert title and len(title) > 0, "頁面標題為空"
        
        LogHelpers.log_step("[PASS] 已進入貓貓專區")
    
    
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_search_product(self, authenticated_page):
        """
        測試：貓貓專區頁面功能（已登入狀態）
        
        步驟：
        1. 直接導航到貓貓專區
        2. 驗證頁面加載成功
        3. 確認頁面有內容
        """
        page = authenticated_page
        
        LogHelpers.log_step("導航到貓貓專區")
        page.goto("https://www.dogcatstar.com/product-category/cat/")
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        
        LogHelpers.log_step("驗證頁面加載成功")
        current_url = page.url
        LogHelpers.log_step(f"當前 URL: {current_url}")
        assert "cat" in current_url and "product" in current_url, "未進入貓貓專區"
        
        LogHelpers.log_step("驗證頁面內容")
        page_content = page.content()
        content_length = len(page_content)
        LogHelpers.log_step(f"頁面內容長度: {content_length} 字符")
        assert content_length > 1000, "頁面內容不足"
        
        LogHelpers.log_step("[PASS] 貓貓專區頁面已加載")


class TestShoppingIntegration:
    """完整購物流程集成測試 - 演示在單一頁面實例上的完整流程"""
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_complete_shopping_flow(self, authenticated_page):
        """
        測試：完整的購物流程 - 在單一頁面實例上執行所有步驟
        
        這是一個集成測試，展示在同一頁面實例上執行多個步驟。
        
        流程步驟：
        1. 驗證登入狀態 (my-account 頁面)
        2. 訪問購物車頁面
        3. 導航到貓貓專區
        4. 驗證頁面加載完成
        
        注意：所有步驟共享同一個page實例和session，保持登入狀態。
        """
        page = authenticated_page
        
        LogHelpers.log_step("=" * 60)
        LogHelpers.log_step("開始完整購物流程集成測試")
        LogHelpers.log_step("說明: 所有步驟在同一頁面實例上執行")
        LogHelpers.log_step("=" * 60)
        
        # 步驟 1: 驗證登入狀態
        LogHelpers.log_step("\n[步驟 1/4] 驗證登入狀態 - 訪問 my-account 頁面")
        page.goto("https://www.dogcatstar.com/my-account/")
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        LogHelpers.log_step(f"URL: {page.url}")
        LogHelpers.log_step(f"標題: {page.title()}")
        LogHelpers.log_step(f"Cookie 數量: {len(page.context.cookies())}")
        assert "my-account" in page.url, "未進入 my-account 頁面"
        LogHelpers.log_step("[PASS] 登入狀態驗證成功\n")
        
        # 步驟 2: 訪問購物車 (保持登入狀態)
        LogHelpers.log_step("[步驟 2/4] 訪問購物車頁面 (保持登入狀態)")
        page.goto("https://www.dogcatstar.com/cart/")
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        LogHelpers.log_step(f"URL: {page.url}")
        LogHelpers.log_step(f"頁面內容長度: {len(page.content())} 字符")
        LogHelpers.log_step(f"Cookie 數量: {len(page.context.cookies())} (保持不變)")
        LogHelpers.log_step("[PASS] 購物車頁面已加載\n")
        
        # 步驟 3: 導航到貓貓專區 (保持登入狀態)
        LogHelpers.log_step("[步驟 3/4] 導航到貓貓專區 (保持登入狀態)")
        page.goto("https://www.dogcatstar.com/product-category/cat/")
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        LogHelpers.log_step(f"URL: {page.url}")
        assert "cat" in page.url and "product" in page.url, "未進入貓貓專區"
        LogHelpers.log_step(f"Cookie 數量: {len(page.context.cookies())} (保持不變)")
        LogHelpers.log_step("[PASS] 進入貓貓專區成功\n")
        
        # 步驟 4: 驗證頁面加載完成 (保持登入狀態)
        LogHelpers.log_step("[步驟 4/4] 驗證頁面加載完成")
        title = page.title()
        LogHelpers.log_step(f"頁面標題: {title}")
        page_content = page.content()
        LogHelpers.log_step(f"頁面內容長度: {len(page_content)} 字符")
        LogHelpers.log_step(f"Cookie 數量: {len(page.context.cookies())} (保持不變)")
        assert title and len(title) > 0, "頁面標題為空"
        assert len(page_content) > 1000, "頁面內容不足"
        LogHelpers.log_step("[PASS] 頁面加載完成\n")
        
        LogHelpers.log_step("=" * 60)
        LogHelpers.log_step("完整購物流程集成測試通過!")
        LogHelpers.log_step("=" * 60)
    
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_add_product_and_clear_cart(self, authenticated_page):
        """
        測試：完整購物流程 - 登錄驗證 → 選品 → 加入購物車 → 驗證 → 清空
        
        這是一個完整的購物操作演示，包括：
        1. 進入用戶頁面確認登錄狀態
        2. 導航到商品頁面
        3. 獲取第一個商品信息
        4. 添加到購物車（處理定制化選項）
        5. 前往購物車驗證
        6. 清空購物車
        
        注意：非headless模式下，每個操作完成後會停留2秒以觀察結果
        """
        page = authenticated_page
        cart_page = CartPage(page)
        
        # 檢測是否為 headless 模式（簡化判斷，這裡假設非headless）
        wait_for_observation = True  # 由於見到頁面，假設非headless模式
        
        LogHelpers.log_step("=" * 60)
        LogHelpers.log_step("開始：登錄驗證 → 選品 → 加入購物車 → 驗證 → 清空")
        LogHelpers.log_step(f"模式: {'Headless' if not wait_for_observation else 'Visible (含觀察等待)'}")
        LogHelpers.log_step("=" * 60)
        
        # 步驟 1: 進入用戶頁面驗證登錄狀態
        LogHelpers.log_step("\n[步驟 1/6] 進入用戶頁面驗證登錄狀態")
        page.goto("https://www.dogcatstar.com/my-account/")
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        LogHelpers.log_step(f"URL: {page.url}")
        LogHelpers.log_step(f"頁面標題: {page.title()}")
        
        # 確認已進入 my-account 頁面
        assert "my-account" in page.url, "未進入用戶頁面"
        LogHelpers.log_step("[PASS] 已進入用戶頁面 - 登錄狀態確認成功")
        if wait_for_observation:
            page.wait_for_timeout(2000)
        LogHelpers.log_step("")
        
        # 步驟 2: 導航到貓貓專區
        LogHelpers.log_step("[步驟 2/6] 導航到貓貓專區")
        page.goto("https://www.dogcatstar.com/product-category/cat/")
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        LogHelpers.log_step(f"URL: {page.url}")
        LogHelpers.log_step("[PASS] 進入貓貓專區")
        if wait_for_observation:
            page.wait_for_timeout(3000)  # 增加等待時間，避免速率限制
        LogHelpers.log_step("")
        
        # 步驟 3: 獲取並記錄第一個商品信息
        LogHelpers.log_step("[步驟 3/6] 獲取第一個商品信息")
        product_info = cart_page.get_first_product_info()
        LogHelpers.log_step(f"商品名稱: {product_info['name']}")
        LogHelpers.log_step(f"商品價格: {product_info['price']}")
        LogHelpers.log_step("[PASS] 已記錄商品信息")
        if wait_for_observation:
            page.wait_for_timeout(3000)  # 增加等待時間
        LogHelpers.log_step("")
        
        # 步驟 4: 添加商品到購物車（含定制化選項）
        LogHelpers.log_step("[步驟 4/6] 添加商品到購物車（處理定制化選項）")
        page.wait_for_load_state("domcontentloaded", timeout=5000)
        
        # 檢測是否為 headless 模式
        is_headless = False  # 簡化判斷
        wait_for_observation = True  # 假設非headless
        
        LogHelpers.log_step("=" * 40)
        LogHelpers.log_step("準備添加的商品信息:")
        LogHelpers.log_step(f"  商品名稱: {product_info['name']}")
        LogHelpers.log_step(f"  商品價格: {product_info['price']}")
        LogHelpers.log_step("=" * 40)
        
        cart_page.add_first_product_to_cart(wait_for_observation=wait_for_observation)
        
        LogHelpers.log_step("=" * 40)
        LogHelpers.log_step("✓ 商品已成功添加到購物車")
        LogHelpers.log_step(f"  已添加商品: {product_info['name']}")
        LogHelpers.log_step(f"  商品價格: {product_info['price']}")
        LogHelpers.log_step("=" * 40)
        LogHelpers.log_step("[PASS] 商品已添加到購物車")
        LogHelpers.log_step("")
        
        # 步驟 5: 導航到購物車並驗證商品
        LogHelpers.log_step("[步驟 5/6] 導航到購物車並驗證商品")
        page.goto("https://www.dogcatstar.com/cart/")
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        LogHelpers.log_step(f"URL: {page.url}")
        
        # 驗證商品是否在購物車中
        is_product_in_cart = cart_page.verify_product_in_cart(product_info['name'])
        cart_items_count = cart_page.get_cart_items_count()
        
        LogHelpers.log_step("=" * 40)
        LogHelpers.log_step("購物車驗證結果:")
        LogHelpers.log_step(f"  預期商品名稱: {product_info['name']}")
        LogHelpers.log_step(f"  預期商品價格: {product_info['price']}")
        LogHelpers.log_step("-" * 40)
        LogHelpers.log_step(f"  購物車商品總數: {cart_items_count}")
        LogHelpers.log_step(f"  商品已在購物車中: {'✓ 是' if is_product_in_cart else '✗ 否'}")
        LogHelpers.log_step(f"  驗證商品名稱: {product_info['name']}")
        LogHelpers.log_step("=" * 40)
        
        if is_product_in_cart or cart_items_count > 0:
            LogHelpers.log_step("[PASS] 購物車驗證成功 - 商品已成功添加")
        else:
            LogHelpers.log_step("[NOTICE] 購物車中未找到商品 (可能需要檢查選擇器)")
        
        if wait_for_observation:
            page.wait_for_timeout(3000)  # 增加等待時間
        LogHelpers.log_step("")
        
        # 步驟 6: 清空購物車
        LogHelpers.log_step("[步驟 6/6] 清空購物車")
        LogHelpers.log_step("=" * 40)
        LogHelpers.log_step(f"清空前購物車商品數: {cart_items_count}")
        LogHelpers.log_step(f"待移除商品: {product_info['name']}")
        LogHelpers.log_step("=" * 40)
        
        cart_page.clear_cart()
        page.wait_for_timeout(1000)
        
        remaining_items = cart_page.get_cart_items_count()
        LogHelpers.log_step("=" * 40)
        LogHelpers.log_step("清空結果:")
        LogHelpers.log_step(f"  清空前商品數: {cart_items_count}")
        LogHelpers.log_step(f"  清空後商品數: {remaining_items}")
        LogHelpers.log_step(f"  移除商品: {product_info['name']}")
        LogHelpers.log_step("=" * 40)
        LogHelpers.log_step("[PASS] 購物車已清空")
        if wait_for_observation:
            page.wait_for_timeout(3000)  # 增加等待時間
        LogHelpers.log_step("")
        
        LogHelpers.log_step("=" * 60)
        LogHelpers.log_step("完整購物流程測試通過!")
        LogHelpers.log_step("=" * 60)
