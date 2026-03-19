## ADDED Requirements

### Requirement: 隨機產生 key 值並映射至節點
系統 SHALL 隨機產生指定數量的 32-bit key 值，並將每個 key 映射到 Chord 環上負責管理該 key 的節點。負責節點為從該 key 值順時鐘方向遇到的第一個節點（即 ID 大於等於 key 的最小節點，若無則為環上 ID 最小的節點）。key 值不需要檢查是否重複產生過。

#### Scenario: key 正確映射至負責節點
- **WHEN** 產生一個 key 值 `k`
- **THEN** 系統 MUST 將 `k` 分配給 Chord 環上從 `k` 順時鐘方向遇到的第一個節點

#### Scenario: key 值跨越環形邊界
- **WHEN** key 值大於所有節點的 ID
- **THEN** 系統 MUST 將該 key 分配給 ID 最小的節點（環形 wrap-around）

### Requirement: 統計各節點負責的 key 數量
系統 SHALL 針對 numK = 10n, 20n, 30n, ..., 100n（其中 n = 10,000）分別執行 key 映射，並統計每個節點負責的 key 數量。對於每組 numK，系統 MUST 計算並輸出所有節點負責 key 數量的最小值、最大值及中位數（median）。

#### Scenario: 針對每組 numK 計算統計值
- **WHEN** numK 設定為 `i * n`（i = 10, 20, ..., 100）
- **THEN** 系統 MUST 產生 `i * n` 個隨機 key，映射至各節點，並輸出負責 key 數量的最小值、最大值及中位數

#### Scenario: 統計值涵蓋所有 10 組 numK
- **WHEN** key 映射流程執行完畢
- **THEN** 系統 MUST 產出 10 組統計結果（對應 numK = 100,000 到 1,000,000）
