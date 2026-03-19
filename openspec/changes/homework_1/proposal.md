## Why

本專案為「點對點與區塊鏈系統」課程的 Homework #1，需要實作一個 Chord DHT（分散式雜湊表）模擬程式。目標是透過模擬來觀察 Chord 系統中每個節點負責的 key 數量分佈，以及搜尋時所需的 hop 數分佈，以驗證 Chord 協定的理論特性。作業繳交期限為 2026-04-29。

## What Changes

- 實作完整的 Chord DHT 模擬系統，包含 10,000 個節點，每個節點使用 32-bit ID
- 建立 Chord 拓撲結構：隨機產生節點 ID、建立 predecessor/successor 關係、產生 finger table
- 實作 key 對映功能：將隨機產生的 key 分配到對應的節點，統計每個節點負責的 key 數量
- 實作搜尋模擬：利用 finger table 進行 routing，執行 100 萬次搜尋並統計 hop 數分佈
- 繪製兩張圖表：
  - 圖一：每個節點負責 key 數量的最小值、最大值、中位數 vs. numK（10n ~ 100n）
  - 圖二：搜尋所需 hop 數的比例分佈圖（hop 0 ~ 31）

## Capabilities

### New Capabilities
- `chord-topology`: Chord 環形拓撲建立，包含節點 ID 產生、predecessor/successor 設定、finger table 建構
- `key-mapping`: 將隨機 key 值對映至 Chord 節點，統計各節點負責的 key 數量（最小值、最大值、中位數）
- `search-simulation`: 基於 finger table 的搜尋路由模擬，統計 hop 數分佈
- `result-visualization`: 繪製統計結果圖表（key 分佈圖與 hop 分佈圖）

### Modified Capabilities
（無，本專案為全新實作）

## Impact

- 新增主程式邏輯於 `main.py`（目前僅有 placeholder）
- 可能需要引入 `matplotlib` 等繪圖套件作為依賴
- 使用 single thread 即可，不需要 multi-thread
- 最終產出為程式碼及兩張數據圖，需整合至 Word 文件繳交
