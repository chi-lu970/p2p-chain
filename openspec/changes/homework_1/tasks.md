## 1. 專案設定

- [x] 1.1 安裝 matplotlib 依賴套件，更新 requirements.txt
- [x] 1.2 建立模組檔案結構：`chord.py`、`simulation.py`、`visualization.py`

## 2. Chord 拓撲建立（chord.py）

- [x] 2.1 實作 Node 類別，包含 id、predecessor、successor、finger_table 屬性
- [x] 2.2 實作 `create_topology()` 函式：隨機產生 n=10,000 個不重複的 32-bit 節點 ID
- [x] 2.3 將節點依 ID 排序，建立 Chord 環形結構，設定每個節點的 predecessor 與 successor
- [x] 2.4 實作 `find_successor(key)` 輔助函式：給定 key 值，找到 Chord 環上負責該 key 的節點（使用 bisect 二分搜尋）
- [x] 2.5 實作 finger table 建構：為每個節點計算 32 個 finger table 條目，finger[i] = find_successor((node_id + 2^i) mod 2^32)

## 3. Key 映射與統計（simulation.py）

- [x] 3.1 實作 `map_keys_to_peers()` 函式：針對 numK = 10n, 20n, ..., 100n，隨機產生 key 並映射至負責節點
- [x] 3.2 統計每組 numK 下各節點負責的 key 數量，計算最小值、最大值及中位數
- [x] 3.3 儲存統計結果供繪圖使用

## 4. 搜尋模擬（simulation.py）

- [x] 4.1 實作 `chord_lookup(start_node, key)` 函式：從起始節點出發，利用 finger table 路由至負責節點，回傳 hop 數
- [x] 4.2 正確處理環形 ID 空間的邊界情況（wrap-around）
- [x] 4.3 實作 `compute_search_hops()` 函式：每個節點執行 100 次隨機搜尋，共 1,000,000 次，統計 hop 數分佈（0 ~ 31）

## 5. 結果視覺化（visualization.py）

- [x] 5.1 實作 key 分佈圖繪製：X 軸為 numK，Y 軸為 key 數量，顯示最小值、最大值、中位數（含誤差棒）
- [x] 5.2 實作 hop 數分佈圖繪製：X 軸為 hop 數（0~31），Y 軸為比例（PDF），折線圖呈現
- [x] 5.3 將兩張圖表儲存為 PNG 圖片檔案

## 6. 主程式整合與驗證（main.py）

- [x] 6.1 整合所有模組，在 main.py 中依序呼叫 createTopology → mapKeysToPeers → computeSearchHops → 繪圖
- [x] 6.2 驗證程式輸出結果是否與作業提供的參考圖表趨勢一致
