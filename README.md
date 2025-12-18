# PlaywrightProject

Playwright執行相關指令：
playwright運行模式       --headed 
                        --headless

瀏覽器選擇 --browser=Chromium (Chrome and edge) 
          --browser=firefox
          --browser=webkit   (Safari engine)

截圖熒幕     --screenshot=on
            --screen=only-on-failure
錄影       --video=on
           --video=retain-on-failure
HTML報告    --html=xxx.html (需要額外的pytest-html套件)
Trace Viewer  pytest --traceing on

架構說明：
/pages  （POM/Screenplay）
/fixtures（Auth/測資）
/helpers （API/資料工廠/等待）
/tests（以功能域分組）
使用這樣的架構用於重複利用Class且易於維護
如果說某一個頁面做出改動，只需要針對pages中的特定頁面做出屬性上的修正，再調試測試用例即可。
目前只是基於本次要求的頁面部分功能做出實作，往後擴充，應該將每個頁面上的屬性都加上，以便於自動化測試進行已經排除錯誤。
如果測試足夠完整，也能夠保證每次上線前需要預先做的準備越完善，減少線上問題的發生率。