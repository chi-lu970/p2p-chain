## ADDED Requirements

### Requirement: 產生不重複的 32-bit 節點 ID
系統 SHALL 為每個節點隨機產生一個 32-bit 無號整數作為 ID（範圍 0 ~ 2^32-1），且所有節點 ID 不得重複。系統 SHALL 支援 n = 10,000 個節點。

#### Scenario: 成功產生 10,000 個不重複的節點 ID
- **WHEN** 系統初始化 10,000 個節點
- **THEN** 每個節點 MUST 擁有一個唯一的 32-bit ID，且所有 ID 值皆在 [0, 2^32-1] 範圍內

#### Scenario: 確認無重複 ID
- **WHEN** 所有節點 ID 產生完成
- **THEN** 任意兩個節點的 ID MUST 不相同

### Requirement: 建立 Chord 環形結構的 predecessor 與 successor
系統 SHALL 將所有節點依 ID 值排序，形成 Chord 環形結構。每個節點 MUST 記錄其 predecessor（前一個節點）及 successor（下一個節點），環形結構中 ID 最大的節點的 successor 為 ID 最小的節點，反之亦然。

#### Scenario: 正確設定 predecessor 與 successor
- **WHEN** 所有節點 ID 產生完成並排序
- **THEN** 每個節點的 successor MUST 是環上順時鐘方向的下一個節點，predecessor MUST 是逆時鐘方向的前一個節點

#### Scenario: 環形結構的邊界正確性
- **WHEN** 存取 ID 最大的節點
- **THEN** 該節點的 successor MUST 為 ID 最小的節點；ID 最小節點的 predecessor MUST 為 ID 最大的節點

### Requirement: 建立每個節點的 finger table
系統 SHALL 為每個節點建立一個長度為 32 的 finger table。對於節點 ID 為 `n` 的節點，finger table 的第 `i` 個條目（i = 0 ~ 31）MUST 指向負責管理 key 值 `(n + 2^i) mod 2^32` 的節點，即在 Chord 環上從 `(n + 2^i) mod 2^32` 順時鐘方向遇到的第一個節點。

#### Scenario: finger table 條目正確指向
- **WHEN** 節點 `n` 的 finger table 第 `i` 條目被查詢
- **THEN** 該條目 MUST 回傳負責 key 值 `(n + 2^i) mod 2^32` 的節點（即從該 key 值順時鐘方向遇到的第一個存活節點）

#### Scenario: finger table 長度為 32
- **WHEN** 任意節點的 finger table 被檢視
- **THEN** finger table 長度 MUST 為 32（對應 32-bit ID 空間）
