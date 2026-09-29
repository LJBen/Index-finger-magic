
# Index Finger Magic 👆 指尖防衛戰 🪄

一個結合 **OpenCV** 與 **Mediapipe** 手勢辨識技術的互動繪圖防衛遊戲！玩家只需透過攝影機伸出食指，即可在空氣中揮畫魔法、擊退降落的怪物，在有限生命中挑戰最高分數！

---

## 🎮 遊戲玩法與手勢說明 (How to Play)

1. **啟動遊戲**：開啟攝影機並將手部放入鏡頭畫面中。
2. **揮畫魔法 (攻擊)**：伸出**食指**即可在畫面上劃出線條。劃出怪物身上對應的**弱點軌跡**，即可將其擊敗！
3. **擊退怪物**：阻止從畫面頂部降落的怪物，想盡辦法在有限生命值（HP）下取得最高分數！
4. **結束遊戲**：隨時比出**拳頭**手勢即可結束遊戲。

---

## 🧠 模型與辨識技術 (Model & AI)

* 本專案採用 **Teachable Machine** 進行微調（Fine-tuning）與輕量化模型訓練。
* 結合攝影機即時影像串流，實現低延遲的手勢狀態判斷（食指繪圖 / 拳頭結束）與劃線擊殺互動。

---

## 💻 環境配置與需求 (Requirements)

* **硬體需求**：需配備可正常使用的 **Webcam 攝影機**。
* **Python 版本**：`Python 3.11.9`

---

## 🚀 快速開始與執行步驟 (Getting Started)

### 1. Clone 專案 (Git Clone)

```bash
git clone https://github.com/LJBen/Index-finger-magic.git
```

### 2. 安裝依賴套件

```bash
pip install -r requirements.txt

```

### 3. 執行遊戲

開啟並執行專案主程式：

```bash
Index_finger_magic.ipynb

```


## 📄 授權條款 (License)

Distributed under the MIT License. See `LICENSE` for more information.
