# Homework #1 — Chord DHT 模擬程式 總結報告

## 一、作業目標

本作業要求撰寫模擬程式，模擬 **Chord 分散式雜湊表（DHT）** 系統的運作，驗證兩個核心特性：

1. **Key 負載分佈**：觀察各節點負責管理的 key 數量是否均勻
2. **搜尋效率**：驗證 Chord 的路由機制是否能在 O(log N) 的 hop 數內完成搜尋

---

## 二、背景知識

### 2.1 什麼是 Chord？

Chord 是一種 **結構化的 P2P 覆疊網路協定**，由 MIT 於 2001 年提出。它解決的核心問題是：

> 在一個去中心化的網路中，如何有效率地找到某個檔案（key）存放在哪個節點上？

### 2.2 一致性雜湊（Consistent Hashing）

Chord 使用一致性雜湊將**節點**和**檔案 key** 映射到同一個環形 ID 空間：

- 本作業使用 **32-bit ID 空間**，範圍為 `0 ~ 2³²-1`（約 43 億）
- 節點和 key 都被雜湊到這個環上
- 每個 key 由**順時鐘方向遇到的第一個節點**負責保管

```
        ID 空間 (0 ~ 2³²-1)

             0
            /|\
           / | \
          /  |  \
    Node A   |   Node D
        \    |    /
         \   |   /
          \  |  /
           Node B

    Key k → 由順時鐘方向最近的節點負責
```

### 2.3 Finger Table

每個節點維護一個長度為 **m**（= 32）的 finger table，用來加速搜尋：

- `finger[i]` = 負責 key `(node_id + 2ⁱ) mod 2³²` 的節點
- 第 0 個 finger 指向最近的後繼節點，越後面的 finger 跨越越大的 ID 距離
- 這讓搜尋每一步都能**跳過約一半的剩餘距離**，實現 O(log N) 效率

### 2.4 搜尋路由流程

從節點 A 搜尋 key k 的流程：

1. 若 k 落在 (A, successor(A)] 之間 → successor 就是目標，完成
2. 否則，從 finger table 中找到**最接近但不超過 k 的節點**，跳轉過去
3. 重複直到找到負責節點

---

## 三、系統參數

| 參數 | 值 | 說明 |
|------|-----|------|
| m | 32 | ID 空間位元數（2³² 個可能的 ID） |
| n | 10,000 | 節點數量 |
| numK | 10n ~ 100n | 檔案 key 數量（100,000 ~ 1,000,000） |
| 搜尋次數 | 1,000,000 | 每個節點各 100 次 |

---

## 四、程式架構

所有邏輯集中在 `homework_1/homework_1_main.py`，約 170 行，結構如下：

```
main()
 ├── create_topology()        # 建立 Chord 環形拓撲
 │    ├── 產生 10,000 個不重複的 32-bit 隨機 ID
 │    ├── 排序後建立 predecessor / successor 環形關係
 │    └── 為每個節點建立 32 條 finger table
 │
 ├── map_keys_to_peers()      # Key 映射與統計
 │    ├── 對 numK = 10n, 20n, ..., 100n 分別執行
 │    ├── 隨機產生 key → 用 bisect 找到負責節點
 │    └── 統計各節點負責的 key 數量（min / max / median）
 │
 ├── compute_search_hops()    # 搜尋模擬
 │    ├── 每個節點執行 100 次隨機搜尋
 │    ├── 利用 finger table 逐步路由
 │    └── 統計 hop 0~31 各自的比例
 │
 └── plot_results()           # 輸出結果
      ├── save_results()  → data.txt（數據文字檔）
      ├── key_distribution.png（key 分佈圖）
      └── hop_distribution.png（hop 分佈圖）
```

### 輸出結構

每次執行會在 `homework_1/result/` 下建立時間戳資料夾，避免覆蓋：

```
homework_1/result/20260319_161423/
├── data.txt                # 原始數據
├── key_distribution.png    # Key 分佈圖
└── hop_distribution.png    # Hop 分佈圖
```

---

## 五、關鍵實作細節

### 5.1 環形區間判斷 `in_range(x, a, b)`

Chord 環上的區間 `(a, b]` 可能跨越 0 點（wrap-around），需要特殊處理：

```python
def in_range(x, a, b):
    if a < b:
        return a < x <= b     # 一般情況
    return x > a or x <= b    # 跨越 0 點
```

這是整個程式中最容易出錯的地方，一旦寫錯會導致搜尋路由無限迴圈或結果偏差。

### 5.2 使用 bisect 加速查找

Python 的 `bisect.bisect_left` 對排序後的節點 ID 列表進行二分搜尋，將「找到 key 的負責節點」從 O(n) 降為 O(log n)：

```python
idx = bisect.bisect_left(ids, target)
responsible_node = ids[idx % N]  # % N 處理 wrap-around
```

### 5.3 Finger Table 建構

對每個節點，計算 32 個 finger 條目：

```python
for i in range(32):
    target = (node_id + 2**i) % 2**32
    finger[i] = find_successor(target)
```

---

## 六、實驗結果與分析

### 6.1 Key 分佈（圖一）

| numK | Min | Median | Max |
|------|-----|--------|-----|
| 100,000 | 0 | 7.0 | ~90 |
| 500,000 | 0 | 34.0 | ~450 |
| 1,000,000 | 0 | 68.0 | ~900 |

**觀察：**
- **中位數**隨 numK 線性成長，符合預期（平均每個節點負責 numK/n 個 key）
- **最大值**遠大於中位數，呈現明顯的**長尾分佈**
- **最小值**始終為 0，代表總有節點完全沒分配到 key

**知識點：** 這展示了一致性雜湊的**負載不均勻問題**。在實際系統中，會使用**虛擬節點（virtual nodes）** 來改善負載平衡，讓每個實體節點對應多個虛擬 ID。

### 6.2 Hop 分佈（圖二）

| Hops | 比例 |
|------|------|
| 1~3 | ~1% |
| 4~6 | ~27% |
| **7~8** | **~43%（峰值）** |
| 9~11 | ~28% |
| 12+ | ~1% |

**觀察：**
- 分佈呈**鐘形曲線**，峰值在 7~8 hops
- 理論期望值 ≈ ½ log₂(10000) ≈ **6.6 hops**，實測結果吻合
- 幾乎所有搜尋在 14 hops 內完成，遠低於上限 32

**知識點：** 這驗證了 Chord 的核心理論——finger table 讓搜尋複雜度為 **O(log N)**。每一步跳躍都將剩餘距離縮小約一半，所以 10,000 個節點只需約 log₂(10000) ≈ 13 步以內就能找到任意 key。

---

## 七、涵蓋的知識點總整理

| 知識領域 | 具體內容 |
|----------|----------|
| **P2P 架構** | 結構化覆疊網路 vs. 非結構化覆疊網路的差異 |
| **一致性雜湊** | 將節點與 key 映射到同一環形空間，實現去中心化的資料定位 |
| **Chord 協定** | 環形拓撲、predecessor/successor 關係、finger table 結構 |
| **路由效率** | Finger table 實現 O(log N) 跳數的搜尋，每步跨越約一半距離 |
| **負載分佈** | 一致性雜湊下的負載不均勻現象，以及虛擬節點的改善思路 |
| **環形空間處理** | Wrap-around 區間判斷，modular arithmetic 的正確實作 |
| **模擬方法** | 使用隨機抽樣模擬大規模分散式系統行為 |
| **資料視覺化** | 誤差棒圖（error bar）、機率密度分佈圖（PDF） |

---

## 八、執行方式

```bash
# 安裝依賴
pip install matplotlib

# 執行模擬
python homework_1/homework_1_main.py
```

執行時間約 2~3 分鐘，主要花費在 100 萬次搜尋模擬上。
