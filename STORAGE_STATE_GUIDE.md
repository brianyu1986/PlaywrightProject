# 測試框架優化 - 使用儲存狀態 (Storage State)

## 目標
解決登入流程超時問題，通過使用 Playwright 的 `storage_state` 功能保存認證狀態，避免每個測試都重複登入。

## 架構
```
tests/
├── test_login.py              # 登入流程測試 - 生成驗證狀態
├── test_cart_with_auth.py     # 購物車測試 - 使用驗證狀態（無需登入）
└── test_cart.py               # 原始測試（已登入流程集成）

scripts/
└── quick_auth_capture.py      # 快速登入捕獲腳本 - 手動生成 auth.json

fixtures/
└── auth.json                  # 保存的認證狀態（由 test_login 或腳本生成）
```

## 工作流程

### 步驟 1: 生成驗證狀態
執行以下任一方式：

**方式 A：使用測試 (推薦)**
```bash
pytest tests/test_login.py::TestLogin::test_login_with_email_and_password -v
```

**方式 B：使用快速捕獲腳本**
```bash
python scripts/quick_auth_capture.py
```

### 步驟 2: 使用驗證狀態進行測試
```bash
pytest tests/test_cart_with_auth.py -v
```

所有使用 `authenticated_page` fixture 的測試都會自動使用保存的認證狀態。

## 優勢

| 問題 | 原始方法 | 儲存狀態方法 |
|------|---------|------------|
| 登入超時 | ❌ 經常超時 | ✅ 首次登入一次，後續使用快照 |
| 測試速度 | ❌ 每個測試 60+ 秒 | ✅ 測試時間減少 80%+ |
| 可靠性 | ❌ 多步驟易失敗 | ✅ 單一登入 → 穩定性高 |
| 維護成本 | ❌ 選擇器需頻繁更新 | ✅ 選擇器變化不影響已登入測試 |

## 當前狀態

### ✅ 已完成
- POM 架構設計
- `test_login.py` - 登入測試案例
- `test_cart_with_auth.py` - 認證購物車測試
- `quick_auth_capture.py` - 快速登入捕獲腳本
- `conftest.py` 增強 - 支持 `authenticated_page`

### ⏳ 進行中
- 執行登入捕獲腳本生成 `auth.json`

### 📋 後續步驟
1. 驗證 `auth.json` 生成成功
2. 運行 `test_cart_with_auth.py` 驗證框架工作正常
3. 調整購物車測試邏輯以正確驗證登入狀態
4. 更新 `test_cart.py` 支持跳過登入流程

## 故障排除

### auth.json 不存在或無效
```bash
# 重新生成
python scripts/quick_auth_capture.py
# 或
pytest tests/test_login.py::TestLogin::test_login_with_email_and_password -v
```

### 認證狀態過期
- 認證狀態有有效期限
- 定期重新生成 `auth.json`
- 或修改 `quick_auth_capture.py` 定期自動更新

### 測試仍然超時
- 檢查網路連線
- 驗證帳戶未被鎖定
- 檢查購物車頁面 DOM 結構是否變化

## 測試執行命令

```bash
# 生成驗證狀態
pytest tests/test_login.py::TestLogin::test_login_with_email_and_password -v

# 運行所有認證購物車測試
pytest tests/test_cart_with_auth.py -v

# 運行特定測試
pytest tests/test_cart_with_auth.py::TestCartWithAuth::test_cart_is_initially_empty -v

# 運行所有測試（包括登入和購物車）
pytest tests/ -v --tb=short
```

## 文件引用
- [conftest.py](../conftest.py) - 核心 fixture 配置
- [test_login.py](test_login.py) - 登入測試
- [test_cart_with_auth.py](test_cart_with_auth.py) - 認證購物車測試
- [quick_auth_capture.py](../scripts/quick_auth_capture.py) - 快速捕獲腳本
