## ADDED Requirements

### Requirement: 繪製 key 分佈圖
系統 SHALL 繪製一張點線圖，X 軸為 numK（以萬為單位，即 10, 20, ..., 100 × 10,000），Y 軸為每個節點負責的 key 數量。圖中 MUST 同時顯示最小值、最大值及中位數三條線/點，並以誤差棒（error bar）或類似方式呈現範圍。

#### Scenario: 圖表包含完整的統計資料
- **WHEN** key 分佈圖被繪製
- **THEN** 圖表 MUST 包含 10 個資料點（對應 numK = 10n ~ 100n），每個資料點顯示最小值、最大值及中位數

#### Scenario: 圖表格式正確
- **WHEN** key 分佈圖被繪製
- **THEN** X 軸標籤 MUST 為 "Total number of keys"，Y 軸標籤 MUST 為 "Number of keys per node"，並包含適當的標題

### Requirement: 繪製 hop 數分佈圖
系統 SHALL 繪製一張圖表，X 軸為 hop 數（0 ~ 31），Y 軸為該 hop 數所佔的比例（PDF）。圖形呈現方式為折線圖或類似的分佈圖。

#### Scenario: hop 分佈圖包含完整資料
- **WHEN** hop 分佈圖被繪製
- **THEN** 圖表 MUST 包含 hop 數 0 ~ 31 的比例值，所有比例值加總 MUST 等於 1.0

#### Scenario: hop 分佈圖格式正確
- **WHEN** hop 分佈圖被繪製
- **THEN** X 軸標籤 MUST 為 "Path length" 或 "Number of hops"，Y 軸標籤 MUST 為 "PDF" 或 "Proportion"

### Requirement: 圖表輸出為圖片檔案
系統 SHALL 將兩張圖表分別儲存為圖片檔案（PNG 格式），以便插入 Word 文件繳交。

#### Scenario: 圖表成功儲存
- **WHEN** 模擬完成且圖表繪製完畢
- **THEN** 系統 MUST 在指定目錄產出兩張 PNG 圖片檔案
