# Playwright 測試專案架構

## 📁 專案結構

```
PlaywrightProject-1/
│
├── pages/                      # Page Object Model (POM)
│   ├── __init__.py
│   ├── login_page.py          # 登入頁面物件
│   ├── cart_page.py           # 購物車頁面物件
│   ├── homepage.py            # 首頁物件
│   └── myaccount_page.py      # 帳戶頁面物件
│
├── fixtures/                   # 測試資料和 Fixtures
│   ├── __init__.py
│   ├── test_data.py           # 測試使用者、產品資料
│   └── auth.json              # 已登入使用者認證狀態（自動產生）
│
├── helpers/                    # 公共輔助函式
│   ├── __init__.py
│   └── base_helpers.py        # 等待、截圖、日誌、重試等工具
│
├── tests/                      # 測試案例（按功能模組分組）
│   ├── __init__.py
│   ├── test_cart.py           # 購物車功能測試
│   ├── test_login.py          # 登入功能測試
│   └── test_search.py         # 搜尋功能測試
│
├── conftest.py                # Pytest 全域設定和 Fixtures
├── pytest.ini                 # Pytest 設定檔
├── requirements.txt           # Python 相依性
└── test-results/             # 測試結果（截圖、報告等）
```

## 🎯 架構優勢

1. **Page Object Model (POM)**
   - 將頁面元素定位和操作封裝到單獨的類別中
   - 降低測試程式碼和頁面程式碼的耦合性
   - 提高程式碼複用率和可維護性

2. **分層測試結構**
   - `pages/` - UI 物件層
   - `helpers/` - 工具層
   - `fixtures/` - 測試資料層
   - `tests/` - 測試案例層

3. **可複用的 Fixtures**
   - 集中管理測試資料
   - 支援已登入狀態
   - 自動截圖失敗案例

4. **輔助工具庫**
   - 等待工具
   - 截圖工具
   - 日誌工具
   - 重試機制

## 🚀 執行測試

### 安裝相依性
```bash
# 啟用虛擬環境
.\.venv\Scripts\Activate.ps1

# 安裝必需套件
pip install pytest pytest-playwright playwright
```

### 執行所有測試
```bash
pytest tests/
```

### 執行特定測試檔案
```bash
pytest tests/test_cart.py
```

### 執行特定測試類或方法
```bash
pytest tests/test_cart.py::TestCart::test_add_product_to_cart
```

### 執行並產生 HTML 報告
```bash
pytest tests/ --html=test-results/report.html
```

### 執行帶有標記的測試
```bash
pytest tests/ -m smoke
```

### 顯示詳简輸出
```bash
pytest tests/ -v -s
```

## 📝 撰寫測試的步驟

### 1. 建立新的 Page Object

在 `pages/` 中建立新檔案：

```python
from playwright.sync_api import Page

class NewPage:
    def __init__(self, page: Page):
        self.page = page
    
    @property
    def element_name(self):
        return self.page.get_by_role(...)
    
    def perform_action(self):
        self.element_name.click()
```

### 2. 在測試中使用 Page Object

```python
from pages.new_page import NewPage

def test_something(page):
    new_page = NewPage(page)
    new_page.perform_action()
```

### 3. 使用辅助工具

```python
from helpers.base_helpers import LogHelpers, WaitHelpers

LogHelpers.log_step(1, "描述步骤")
WaitHelpers.wait_and_click(page, ".selector")
```

## 🔑 最佳实践

1. ✅ 每个页面一个单独的 Page Object 类
2. ✅ 使用 @property 装饰器定义元素定位器
3. ✅ 为每个操作创建清晰的方法名
4. ✅ 集中管理测试数据在 fixtures/
5. ✅ 使用日志记录测试步骤
6. ✅ 在 conftest.py 中集中管理 Fixtures
7. ✅ 为测试类添加清晰的文档字符串
8. ✅ 使用 pytest 标记（@pytest.mark）区分测试类型

## 🛠️ 常用命令

```bash
# 显示虚拟环境信息
pip list

# 检查代码格式
python -m black tests/

# 录制新的测试
playwright codegen https://www.dogcatstar.com/ --target python

# 查看 Playwright 调试器
playwright codegen --debug-on https://www.dogcatstar.com/
```

## 📚 相关文档

- [Playwright 官方文档](https://playwright.dev/python/)
- [Pytest 官方文档](https://docs.pytest.org/)
- [Page Object Model 最佳实践](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
