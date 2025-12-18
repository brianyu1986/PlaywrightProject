# PlaywrightProject

> 一個基於 **Playwright** 和 **Pytest** 的專業端對端（E2E）測試自動化框架，採用 **Page Object Model (POM)** 架構設計，專為可維護性和可擴展性而構建。

## 🎯 專案概述

本專案是用於 [dogcatstar.com](https://www.dogcatstar.com/) 寵物用品購物平台的自動化測試框架。透過系統性的測試設計，確保功能穩定性和品質保證。

## 📋 設計理由

### 為什麼選擇 Playwright？

- **跨瀏覽器支援**：原生支援 Chromium、Firefox、WebKit，無需額外配置
- **快速可靠**：自動等待機制，減少 flaky 測試
- **開發者友善**：豐富的 API 和調試工具（Playwright Inspector）
- **多語言支援**：支援 Python、JavaScript、Java、C# 等
- **現代 Web 應用**：完美支援 SPA、動態內容和複雜互動

### 為什麼採用 Page Object Model (POM)？

**傳統做法的問題：**
```python
# ❌ 不好的做法 - 緊耦合測試和頁面
def test_purchase():
    page.get_by_text("購物車").click()
    page.fill("input[name='email']", "test@example.com")
    page.fill("input[name='password']", "password")
    # ... 頁面元素到處散佈
```

**POM 的優勢：**
```python
# ✅ 好的做法 - 分離關注點
def test_purchase(page):
    cart_page = CartPage(page)
    login_page = LoginPage(page)
    
    cart_page.go_to_cart()
    login_page.login_with_credentials("test@example.com", "password")
    # ... 邏輯清晰，易於維護
```

**具體好處：**

1. **維護性高**
   - 修改頁面元素只需更新 POM 類別
   - 不影響測試用例邏輯
   - 減少重複代碼

2. **可讀性強**
   - 測試代碼如同業務需求文件
   - 非技術人員也能理解測試意圖
   - 便於知識傳遞

3. **可復用性好**
   - 相同的頁面操作可被多個測試重用
   - 減少代碼重複
   - 提高開發效率

### 分層架構設計

```
📁 PlaywrightProject/
├── 📂 pages/              ← UI 頁面物件層
│   ├── login_page.py       # 登入邏輯封裝
│   ├── cart_page.py        # 購物車邏輯封裝
│   └── ...
├── 📂 fixtures/           ← 測試資料層
│   ├── test_data.py        # 測試用戶、資料集
│   └── auth.json           # 認證狀態快照
├── 📂 helpers/            ← 工具層
│   └── base_helpers.py     # 等待、截圖、重試等
├── 📂 tests/              ← 測試案例層
│   ├── test_cart.py        # 購物車測試
│   ├── test_login.py       # 登入測試
│   └── ...
└── conftest.py            ← Pytest 配置層
```

**各層職責：**

| 層級 | 職責 | 優勢 |
|------|------|------|
| **頁面層** | 封裝 UI 元素和操作 | 集中管理頁面變化 |
| **測試層** | 定義業務邏輯和驗證 | 關注測試意圖 |
| **資料層** | 管理測試資料 | 便於切換測試資料集 |
| **工具層** | 提供通用功能 | 減少程式碼重複 |
| **配置層** | 管理全域 Fixtures | 統一環境設置 |

## 🚀 快速開始

### 環境準備

```bash
# 1. 激活虛擬環境
.\.venv\Scripts\Activate.ps1

# 2. 安裝依賴
pip install pytest pytest-playwright playwright

# 3. 安裝瀏覽器驅動
playwright install

# 4. 執行測試
pytest tests/ -v
```

### 常用命令

```bash
# 執行所有測試
pytest tests/

# 執行特定測試
pytest tests/test_cart.py

# 執行特定測試方法
pytest tests/test_cart.py::TestCart::test_add_product_to_cart

# 執行帶有標記的測試
pytest tests/ -m smoke

# 生成 HTML 報告
pytest tests/ --html=test-results/report.html

# 顯示詳細輸出
pytest tests/ -v -s

# 錄製新的測試腳本
playwright codegen https://www.dogcatstar.com/
```

## 📊 Playwright 常用選項

```bash
# 執行模式
--headed                # 頭部模式（顯示瀏覽器窗口）
--headless              # 無頭模式（背景執行）

# 瀏覽器選擇
--browser=chromium      # Chromium 內核（Chrome、Edge）
--browser=firefox       # Firefox 瀏覽器
--browser=webkit        # WebKit 內核（Safari）

# 截圖和錄影
--screenshot=on         # 始終截圖
--screenshot=only-on-failure  # 僅失敗時截圖
--video=on              # 錄製所有測試
--video=retain-on-failure     # 僅失敗時保留錄影

# 報告
--html=report.html      # 生成 HTML 報告（需要 pytest-html）
--tracing=on            # 啟用 Trace Viewer
```

## 🔄 未來擴充計畫

### 第一階段：核心功能完善

#### 1.1 頁面物件擴展
```python
# ✅ 完成度 30%
# 目標：涵蓋所有關鍵業務流程

目前完成：
- LoginPage 基礎功能
- CartPage 核心操作

待完成：
- ProductDetailPage（產品詳情頁）
- CheckoutPage（結帳流程）
- UserAccountPage（用戶帳戶）
- SearchPage（搜尋結果）
```

#### 1.2 測試用例補充
```python
# ✅ 完成度 20%

優先級高：
- 登入/登出流程
- 購物車管理
- 產品搜尋和篩選
- 訂單下單流程

優先級中：
- 用戶帳戶管理
- 地址簿管理
- 收藏清單
- 優惠券應用

優先級低：
- 評論和評分
- 推薦系統
- 社交分享
```

### 第二階段：高級功能集成

#### 2.1 API 測試層
```python
# 目標：集成 API 自動化測試
# 使用 requests 或 httpx 庫

from helpers.api_helpers import APIClient

class ProductAPI:
    def __init__(self, base_url):
        self.client = APIClient(base_url)
    
    def get_products(self, category):
        return self.client.get(f"/api/products?category={category}")
    
    def search_products(self, keyword):
        return self.client.get(f"/api/search", params={"q": keyword})
```

#### 2.2 數據驅動測試
```python
# 目標：支持 CSV/JSON 資料驅動測試

@pytest.mark.parametrize("test_data", read_test_data("test_cases.json"))
def test_with_multiple_datasets(page, test_data):
    login_page = LoginPage(page)
    login_page.login(test_data["email"], test_data["password"])
    # ... 驗證邏輯
```

#### 2.3 跨瀏覽器並行執行
```python
# 目標：使用 pytest-xdist 進行並行測試
# 安裝：pip install pytest-xdist

# 執行：pytest tests/ -n auto  # 自動檢測 CPU 核心
# 或：pytest tests/ -n 4       # 指定 4 個工作進程
```

### 第三階段：企業級功能

#### 3.1 持續集成 (CI/CD)
```yaml
# GitHub Actions 配置
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest tests/ --html=report.html
      - uses: actions/upload-artifact@v2
        if: always()
        with:
          name: test-report
          path: test-results/
```

#### 3.2 測試報告和分析
```python
# 目標：集成進階報告工具
# 支持的工具：
# - pytest-html（HTML 報告）
# - allure（漂亮的測試報告）
# - pytest-cov（代碼覆蓋率）

# 使用 Allure：
# pip install allure-pytest
# pytest tests/ --alluredir=allure-results
# allure serve allure-results
```

#### 3.3 性能和負載測試
```python
# 目標：整合 Locust 進行性能測試
from locust import HttpUser, task

class E2ELoadTest(HttpUser):
    @task
    def browse_products(self):
        # 模擬用戶行為進行負載測試
        pass
```

### 第四階段：智能化測試

#### 4.1 AI 驅動的測試生成
```python
# 目標：使用 AI 自動生成測試用例
# 工具：Testim、Applitools 等

# 預期功能：
# - 自動選擇關鍵場景
# - 智能定位元素（抵抗 UI 變化）
# - 自動生成測試代碼
```

#### 4.2 視覺回歸測試
```python
# 目標：使用 Applitools Eyes 進行視覺測試
# 安裝：pip install applitools

from applitools.playwright import Eyes

def test_visual_regression(page):
    eyes = Eyes()
    eyes.open(page, "App", "Visual Test")
    # ... 操作頁面
    eyes.check_window("Full Page")
    eyes.close()
```

## 📈 期望效果

### 短期（3 個月）
- ✅ 核心業務流程 80% 測試覆蓋率
- ✅ 所有測試自動化執行
- ✅ 減少 50% 的手動測試時間

### 中期（6 個月）
- ✅ 完整的業務流程覆蓋
- ✅ CI/CD 流程整合
- ✅ 測試團隊能自主編寫測試

### 長期（12 個月）
- ✅ 企業級測試框架
- ✅ 代碼覆蓋率 > 80%
- ✅ 零人工干預的自動化流程

## 📚 最佳實踐

1. **編寫可維護的測試**
   - 使用描述性的測試名稱
   - 遵循 AAA 模式（Arrange-Act-Assert）
   - 避免測試間依賴

2. **頁面物件設計**
   - 一個類別對應一個頁面
   - 只暴露必要的業務方法
   - 隱藏技術細節

3. **資料管理**
   - 測試資料獨立於代碼
   - 使用 fixtures 進行數據隔離
   - 避免測試污染

4. **錯誤處理**
   - 充分的日誌記錄
   - 失敗時自動截圖
   - 詳細的錯誤信息

## 🔗 相關資源

- [Playwright 官方文檔](https://playwright.dev/python/)
- [Pytest 官方文檔](https://docs.pytest.org/)
- [Page Object Model 模式](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
- [dogcatstar.com](https://www.dogcatstar.com/)

## 📝 貢獻指南

1. 為新功能建立特性分支
2. 遵循既有的架構和命名規則
3. 提交前執行所有測試
4. 編寫清晰的提交信息

## 📄 授權

MIT License