## ADDED Requirements

### Requirement: 基於 finger table 的搜尋路由
系統 SHALL 實作 Chord finger table lookup 演算法。從起始節點出發，利用 finger table 逐步路由至負責管理目標 key 的節點。每次路由跳轉計為一個 hop。

#### Scenario: 目標 key 在 successor 範圍內
- **WHEN** 從節點 `n` 搜尋 key `k`，且 `k` 落在 `(n, successor(n)]` 的區間內
- **THEN** 系統 MUST 回傳 `successor(n)` 為負責節點，hop 數為 1

#### Scenario: 目標 key 即為起始節點負責
- **WHEN** 從節點 `n` 搜尋 key `k`，且 `k` 由節點 `n` 自身負責
- **THEN** 系統 MUST 回傳節點 `n`，hop 數為 0

#### Scenario: 需要多次跳轉的搜尋
- **WHEN** 從節點 `n` 搜尋 key `k`，且 `k` 不在 successor 範圍內
- **THEN** 系統 MUST 從 finger table 中選擇不超過 `k` 的最大節點作為下一跳，重複路由直到找到負責節點

### Requirement: 執行 100 萬次搜尋並統計 hop 數分佈
系統 SHALL 讓每個節點各執行 100 次搜尋（共 10,000 × 100 = 1,000,000 次），每次搜尋一個隨機產生的 32-bit key 值。系統 MUST 記錄每次搜尋所需的 hop 數（0 ~ 31），並計算各 hop 數所佔的比例。

#### Scenario: 每個節點執行 100 次搜尋
- **WHEN** 搜尋模擬開始
- **THEN** 每個節點 MUST 各執行 100 次搜尋，搜尋目標為隨機產生的 32-bit key 值

#### Scenario: hop 數分佈統計
- **WHEN** 所有 1,000,000 次搜尋完成
- **THEN** 系統 MUST 輸出 hop 數 0 ~ 31 各自佔總搜尋次數的比例

#### Scenario: hop 數上限為 31
- **WHEN** 任何一次搜尋執行中
- **THEN** hop 數 MUST 不超過 31（32-bit ID 空間的理論上限）
