## Context

本專案需實作 Chord DHT 模擬程式，作為「點對點與區塊鏈系統」課程 Homework #1。目前專案僅有一個空的 `main.py` placeholder。需要從零建構完整的 Chord 模擬系統，包含拓撲建立、key 分配、搜尋模擬及結果視覺化。

Chord 是一種結構化的 P2P 覆疊網路協定，使用一致性雜湊（consistent hashing）將節點和 key 映射到同一個環形 ID 空間（本作業為 32-bit，即 0 ~ 2^32-1）。每個節點維護一個 finger table 以實現 O(log N) 的路由效率。

## Goals / Non-Goals

**Goals:**
- 正確實作 Chord 環形拓撲結構（10,000 個節點，32-bit ID 空間）
- 正確建立每個節點的 predecessor、successor 及 finger table
- 正確將 key 映射到負責的節點，並統計 key 分佈
- 正確模擬基於 finger table 的搜尋路由，統計 hop 數分佈
- 繪製符合作業要求的兩張圖表
- 程式碼結構清晰，方便理解與繳交

**Non-Goals:**
- 不需要實作節點的加入（join）或離開（leave）協定
- 不需要 multi-thread 或並行處理
- 不需要實際的網路通訊，純模擬即可
- 不需要處理節點失效（failure）的情況
- 不需要實作 stabilization 協定

## Decisions

### 決策 1：使用 Python 作為實作語言

**選擇**：Python + matplotlib

**理由**：
- 專案已初始化為 Python 專案（有 `main.py` 和 `.venv`）
- Python 的 `random` 模組可方便產生隨機 ID
- `matplotlib` 提供強大的繪圖能力，可直接產出圖表
- 開發效率高，適合模擬程式

**替代方案**：Java（作業虛擬碼偏向 Java 風格），但 Python 更簡潔

### 決策 2：資料結構設計

**選擇**：使用 sorted list 儲存所有節點 ID，每個節點用 dict 或 class 儲存其 predecessor、successor 及 finger table

**理由**：
- 排序後的節點列表可用二分搜尋快速找到 key 的負責節點（用於驗證及 key 映射）
- Finger table 為長度 32 的陣列（對應 32-bit ID 空間），`finger[i]` 指向負責 `(node_id + 2^i) mod 2^32` 的節點

### 決策 3：搜尋路由實作

**選擇**：實作標準 Chord finger table lookup

**流程**：
1. 從起始節點出發，檢查目標 key 是否在 (node_id, successor_id] 之間
2. 若是，則 successor 即為目標，回傳 hop 數
3. 若否，從 finger table 中找到最接近但不超過 key 的節點，跳轉過去
4. 重複直到找到負責節點

### 決策 4：模組劃分

**選擇**：將程式碼組織為以下模組結構：
- `chord.py`：核心 Chord 邏輯（Node 類別、拓撲建立、finger table）
- `simulation.py`：模擬邏輯（key 映射、搜尋模擬）
- `visualization.py`：繪圖邏輯
- `main.py`：主程式入口，串接所有模組

**理由**：職責分離，程式碼清晰易懂

## Risks / Trade-offs

- **[效能風險] 10,000 節點 × 32 個 finger table 條目需要大量計算** → 使用排序陣列 + 二分搜尋（`bisect` 模組）加速查找，整體建構時間應在合理範圍內
- **[正確性風險] 環形 ID 空間的邊界處理（wrap-around）容易出錯** → 仔細實作區間判斷函式，處理 ID 跨越 0 點的情況
- **[記憶體風險] 100 萬次搜尋的資料量** → 僅統計 hop 數計數，不儲存每次搜尋的完整路徑
- **[ID 碰撞風險] 隨機產生 32-bit ID 可能重複** → 使用 set 確保不重複（10,000 個節點在 2^32 空間中碰撞機率極低，但仍需處理）
