# Playwright 测试项目架构

## 📁 项目结构

```
PlaywrightProject-1/
│
├── pages/                      # Page Object Model (POM)
│   ├── __init__.py
│   ├── login_page.py          # 登录页面对象
│   ├── cart_page.py           # 购物车页面对象
│   ├── homepage.py            # 首页对象
│   └── myaccount_page.py      # 账户页面对象
│
├── fixtures/                   # 测试数据和 Fixtures
│   ├── __init__.py
│   ├── test_data.py           # 测试用户、产品数据
│   └── auth.json              # 已登录用户认证状态（自动生成）
│
├── helpers/                    # 公共辅助函数
│   ├── __init__.py
│   └── base_helpers.py        # 等待、截图、日志、重试等工具
│
├── tests/                      # 测试用例（按功能模块分组）
│   ├── __init__.py
│   ├── test_cart.py           # 购物车功能测试
│   ├── test_login.py          # 登录功能测试
│   └── test_search.py         # 搜索功能测试
│
├── conftest.py                # Pytest 全局配置和 Fixtures
├── pytest.ini                 # Pytest 配置文件
├── requirements.txt           # Python 依赖
└── test-results/             # 测试结果（截图、报告等）
```

## 🎯 架构优势

1. **Page Object Model (POM)**
   - 将页面元素定位和操作封装到单独的类中
   - 降低测试代码和页面代码的耦合性
   - 提高代码复用率和可维护性

2. **分层测试结构**
   - `pages/` - UI 对象层
   - `helpers/` - 工具层
   - `fixtures/` - 测试数据层
   - `tests/` - 测试用例层

3. **可复用的 Fixtures**
   - 集中管理测试数据
   - 支持已登录状态
   - 自动截图失败用例

4. **辅助工具库**
   - 等待工具
   - 截图工具
   - 日志工具
   - 重试机制

## 🚀 运行测试

### 安装依赖
```bash
# 激活虚拟环境
.\.venv\Scripts\Activate.ps1

# 安装必需包
pip install pytest pytest-playwright playwright
```

### 运行所有测试
```bash
pytest tests/
```

### 运行特定测试文件
```bash
pytest tests/test_cart.py
```

### 运行特定测试类或方法
```bash
pytest tests/test_cart.py::TestCart::test_add_product_to_cart
```

### 运行并生成 HTML 报告
```bash
pytest tests/ --html=test-results/report.html
```

### 运行带有标记的测试
```bash
pytest tests/ -m smoke
```

### 显示详细输出
```bash
pytest tests/ -v -s
```

## 📝 写测试的步骤

### 1. 创建新的 Page Object

在 `pages/` 中创建新文件：

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

### 2. 在测试中使用 Page Object

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
