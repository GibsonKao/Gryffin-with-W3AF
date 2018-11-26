# Gryffin-with-W3AF
Gryffin with W3AF
![Imgur](https://i.imgur.com/4kyexpl.png)

## Usage
1. 將測試網址寫入: target.txt
2. 執行 PT (整合 W3AF + Gryffin)
   執行方式 : $ python collection.py
3. 輸出測試結果在 result/audit資料夾，包含 text, html, csv 和xml檔案

## PT Flow
開始執行的script: collect.py => 執行步驟 (由collect.py 自動執行)
1. 執行 W3AF crawler (collect.py – console())
   輸出結果url在 (url)_W3afAnalyze.txt當中
2. 執行 runGryffin.py 的 GryffinRunner()
   利用1的結果當entry list，執行 Gruffin
   輸出結果url在 (url)_urls.txt當中
3. 執行 runGryffin2.py 的 GryffinRunner2()
   利用2的結果當entry list，再執行Gryffin
   輸出的結果 url在 (url)_urls.txt當中
4. 執行 AfterGryffin.py 的looper()
   透過W3AF的audit功能，對(url)_urls.txt中的網址進行測試
   輸出audit結果在 result/audit資料夾中，包含xml, html, text, csv格式

## 程式碼說明
### collect.py
程式的進入點
實做呼叫W3AF crawler 的 function
### runGryffin.py
利用 Gryffin 取得的網頁html做 regex parsing
### runGryffin2.py
利用 Gryffin 會自動開啟每個連結的特性，parsing取得的http response header內所包含的網址
### AfterGryffin.py
呼叫 W3AF的PT test 
### target.txt
紀錄要測試的網址
