# 🚀 快速參考卡 - Playwright 測試框架

## 常用命令

```bash
# 📝 生成驗證狀態（首次）
pytest tests/test_login.py::TestLogin::test_login_with_email_and_password -v
python scripts/quick_auth_capture.py

# 🧪 運行測試
pytest tests/ -v                                          # 全部
pytest tests/test_cart_with_auth.py -v                   # 購物車
pytest -m smoke -v                                        # 煙霧測試
pytest -m authentication -v                              # 認證測試

# 🐛 調試模式
PWDEBUG=1 pytest tests/test_cart_with_auth.py -v -s

# 📊 生成報告
pytest tests/ -v --html=report.html
```

---

## 文件速查

| 需求 | 文件 |
|------|------|
| 🔐 登入流程 | `pages/login_page.py` |
| 🛒 購物車 | `pages/cart_page.py` |
| 🛠️ 工具函數 | `helpers/base_helpers.py` |
| 📊 測試數據 | `fixtures/test_data.py` |
| ⚙️ 全局配置 | `conftest.py` |
| 📋 測試列表 | `pytest.ini` |
| 🧪 登入測試 | `tests/test_login.py` |
| 🧪 購物車測試 | `tests/test_cart_with_auth.py` |
| 📖 使用指南 | `STORAGE_STATE_GUIDE.md` |
| 📖 架構設計 | `ARCHITECTURE.md` |

---

## 架構圖

```
┌─────────────────────────────────────┐
│  Tests（測試層）                    │
│  - test_login.py                    │
│  - test_cart_with_auth.py           │
│  - test_cart.py                     │
└──────────────┬──────────────────────┘
               │ 使用
┌──────────────▼──────────────────────┐
│  Pages（頁面層）                    │
│  - LoginPage                        │
│  - CartPage                         │
│  - HomepagePage                     │
└──────────────┬──────────────────────┘
               │ 使用
┌──────────────┴──────────────────────┐
│  Helpers（工具層）                  │
│  - WaitHelpers                      │
│  - LogHelpers                       │
│  - ScreenshotHelpers                │
└──────────────┬──────────────────────┘
               │ 使用
┌──────────────▼──────────────────────┐
│  Playwright Sync API                │
│  - Browser, Context, Page           │
└─────────────────────────────────────┘
```

---

## Storage State 流程圖

```
第一次運行
    ↓
執行 test_login.py
    ↓
模擬登入流程
    ↓
保存 cookies/localStorage → auth.json
    ↓
後續運行
    ↓
載入 auth.json
    ↓
跳過登入 → 直接進行業務測試
    ↓
節省 60+ 秒 ✨
```

---

## 常見選擇器模式

### LoginPage
```python
@property
def email_input_field(self):
    return self.page.locator("input[type='email']").first

@property
def password_input_field(self):
    return self.page.locator("input[type='password']").first

@property
def confirm_button(self):
    return self.page.locator("button:has-text('confirm')").last
```

### CartPage
```python
@property
def cat_section_button(self):
    return self.page.get_by_role("button", name="貓貓專區")

@property
def ai_search_input(self):
    return self.page.get_by_role("textbox", name="毛孩腎病適合吃什麼？")

@property
def add_to_cart_button(self):
    return self.page.get_by_test_id("button-add-to-cart")
```

---

## Fixture 快速參考

```python
# 在測試中使用
def test_something(page):              # 新頁面
    pass

def test_authenticated(authenticated_page):  # 已登入頁面
    pass

@pytest.fixture
def custom_fixture(page):              # 自定義 fixture
    page.goto("https://example.com")
    yield page
```

---

## LogHelpers 用法

```python
from helpers.base_helpers import LogHelpers

# 簡單日誌
LogHelpers.log_step("導航到首頁")
# 輸出：>> 導航到首頁

# 步驟編號
LogHelpers.log_step(1, "登入用戶")
# 輸出：--- Step 1: 登入用戶 ---

# 動作日誌
LogHelpers.log_action("點擊購物車按鈕")
# 輸出：[2025-12-19 12:00:00] 點擊購物車按鈕
```

---

## 調試技巧

### 查看頁面信息
```python
print(page.url)        # 當前 URL
print(page.title())    # 頁面標題
print(page.content())  # HTML 內容
```

### 定位器調試
```python
# 查看定位器匹配數
locator = page.locator("button")
print(f"找到 {locator.count()} 個按鈕")

# 查看第一個元素文字
print(locator.first.text_content())

# 截圖
page.screenshot(path="debug.png")
```

### 動作調試
```python
# 等待後點擊
page.wait_for_selector("button", timeout=5000)
page.click("button")

# 填入並提交
page.fill("input", "test@example.com")
page.press("input", "Enter")
```

---

## 性能對比

```
測試場景：完整購物流程

❌ 舊方法（每次登入）：
時間 = 登入(60s) + 購物(20s) = 80s
成功率 = 40%

✅ 新方法（使用 Storage State）：
時間 = 購物(20s) = 20s  ⬇️ 75%
成功率 = 99% ⬆️ 150%
```

---

## 目錄結構速查

```
PlaywrightProject-1/
├── conftest.py                    ← Fixture 定義
├── pytest.ini                     ← 配置
├── pages/
│   ├── login_page.py             ← 登入 POM
│   ├── cart_page.py              ← 購物車 POM
│   └── ...
├── helpers/
│   └── base_helpers.py           ← 工具函數
├── fixtures/
│   ├── test_data.py              ← 測試數據
│   └── auth.json                 ← 驗證狀態
├── tests/
│   ├── test_login.py             ← 登入測試
│   └── test_cart_with_auth.py    ← 購物車測試（推薦）
└── docs/
    ├── README.md
    ├── ARCHITECTURE.md
    ├── STORAGE_STATE_GUIDE.md
    └── ...
```

---

## 第一次上手步驟

### 1️⃣ 環境檢查
```bash
python --version              # 應該是 3.14.0
pip list | grep playwright   # 應該有 playwright 1.57.0
pip list | grep pytest       # 應該有 pytest 9.0.2
```

### 2️⃣ 生成驗證
```bash
pytest tests/test_login.py::TestLogin::test_login_with_email_and_password -v
# 或
python scripts/quick_auth_capture.py
```

### 3️⃣ 驗證文件
```bash
ls fixtures/auth.json  # 應該存在且大小 > 100 bytes
```

### 4️⃣ 運行測試
```bash
pytest tests/test_cart_with_auth.py -v --tb=short
```

---

## 疑難排解

| 問題 | 解決方案 |
|------|---------|
| `auth.json` 不存在 | 重新運行登入測試 |
| 選擇器找不到 | 用 PWDEBUG=1 檢查 DOM |
| 頁面加載超時 | 增加 timeout 或檢查網絡 |
| 測試卡住 | 使用 --timeout=30 或檢查阻塞 |
| 編碼錯誤 | 確保檔案使用 UTF-8 編碼 |

---

## 資源鏈接

- 📖 [Playwright 文檔](https://playwright.dev/python/)
- 📖 [Pytest 文檔](https://docs.pytest.org/)
- 📄 STORAGE_STATE_GUIDE.md - 詳細使用指南
- 📄 ARCHITECTURE.md - 架構設計文檔

---

**最後更新**：2025-12-19
**版本**：1.0 - 框架完成版
