# Update feed for EasyBrailleEdit

需要更新的檔案清單與版本資訊是寫在 `_updates.txt` 檔案裡。

> 閱讀 GEMINI.md 以了解如何生成此專案需要的 Python 腳本。

## Step 1: 複製新版檔案

把 text-to-braille 專案的 `\deploy\InnoSetup\Files\app\` 目錄下的檔案複製到此專案的 `Files` 目錄（子目錄不用複製）。

## Step 2: 更新檔案列表

執行腳本 upd_file_versions.py 來更新檔案列表。

### 1-1: 安裝依賴

如果還沒有在本機安裝依賴套件，請先執行以下命令：

```bash
pip install pefile
```

### 1-2: 執行腳本

```bash
python upd_file_versions.py
```

## Step 3: 提交更新

```bash
git add .
git commit -m "Deploy new versions of files."
```
