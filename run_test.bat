@echo off
cd c:\Users\USER\Documents\PlaywrightProject-1
echo 開始執行 test_cart.py ...
echo.
.venv\Scripts\python.exe -m pytest tests\test_cart.py -v --tb=short
echo.
echo 測試完成!
pause
