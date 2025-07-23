import os

# 檔案路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "113學年度特殊教育學生課程領域分組及節數一覽表加上正式老師名字.xlsx")
OUTPUT_PATH = os.path.join(BASE_DIR, "output")

# 確保輸出資料夾存在
os.makedirs(OUTPUT_PATH, exist_ok=True)

# 教師名單
TEACHERS = ["A老師", "B老師", "C老師", "D老師", "E老師"]

# 課程類型
BASIC_SUBJECTS = ["社會", "動作", "學習"]
MAIN_SUBJECTS = ["國語", "數學"]