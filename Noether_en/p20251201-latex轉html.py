import re
from pathlib import Path

# ================= 設定區域 =================
# 請修改這裡的檔案路徑
TARGET_FILE = "/Users/bacon/Library/Mobile Documents/com~apple~CloudDocs/Macbook-iDownload/Web/Pro-Pure Perspective/20251126-1/Noether_en/Cx.html"
# ===========================================

def convert_latex_format(file_path):
    path = Path(file_path)
    
    if not path.exists():
        print(f"❌ 找不到檔案: {path}")
        return

    try:
        content = path.read_text(encoding='utf-8')
        print(f"📂 正在處理檔案: {path.name}")
        
        # 1. 處理行內公式：將 $...$ 換成 \(...\)
        pattern_inline = r'(?<![\$\\])\$(?![\$])(.*?)(?<![\$\\])\$(?![\$])'
        content, count_inline = re.subn(pattern_inline, r'\\(\1\\)', content)
        
        # 1. 處理 align 和 align* 環境：將其包裹在 \[ ... \] 中
        # 正則解釋：
        # \\begin\{align(\*?)\} : 匹配 \begin{align} 或 \begin{align*}，並捕捉星號（如果有）為群組 2
        # .*?                   : 非貪婪匹配內容
        # \\end\{align\2\}      : 匹配對應的結束標籤（\2 確保星號有無是一致的）
        # flags=re.DOTALL       : 讓 . (點號) 可以匹配換行符，因為 align 通常跨多行
        pattern_align = r'(\\begin\{align\*?\}.*?\\end\{align\*?\})'
        content, count_align = re.subn(pattern_align, r'\\[\1\\]', content, flags=re.DOTALL)

        # 2. 處理行內公式：將 $...$ 換成 \(...\)
        pattern_inline = r'(?<![\$\\])\$(?![\$])(.*?)(?<![\$\\])\$(?![\$])'
        content, count_inline = re.subn(pattern_inline, r'\\(\1\\)', content)

        count_display_start=0
        count_display_end=0


        # 4. 移除 \noindent (新增功能)
        count_noindent = content.count(r'\noindent')
        content = content.replace(r'\noindent', '')

        # 存檔
        if all(c == 0 for c in [count_inline, count_display_start, count_noindent]):
            print("⚠️ 未發現任何需要修改的符號。")
        else:
            new_path = path.parent / (path.stem + "_converted" + path.suffix)
            new_path.write_text(content, encoding='utf-8')
            
            print("✅ 處理完成！統計如下：")
            print(f"   - $...$ 置換: {count_inline}")
            print(f"   - \[    置換: {count_display_start}")
            print(f"   - \]    置換: {count_display_end}")
            print(f"   - \\noindent 移除: {count_noindent}")
            print(f"📄 新檔案已儲存至: {new_path}")

    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

if __name__ == "__main__":
    convert_latex_format(TARGET_FILE)