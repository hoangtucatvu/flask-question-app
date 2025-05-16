from flask import Flask, render_template, request, redirect
import pandas as pd
import os

app = Flask(__name__)

# Đường dẫn tới file Excel
file_path = "tong hop de thi.xlsx"

# Hàm load toàn bộ dữ liệu từ file
def load_records(path):
    if not os.path.exists(path):
        print(f"❗ Không tìm thấy file: {path}")
        return []

    try:
        xls = pd.ExcelFile(path)
    except Exception as e:
        print(f"❌ Lỗi khi mở file Excel: {e}")
        return []

    records = []
    for sheet in xls.sheet_names:
        try:
            df = xls.parse(sheet)
            df.columns = [str(c).strip().upper() for c in df.columns]
            if "CÂU HỎI" in df.columns and "ĐÁP ÁN ĐÚNG" in df.columns:
                for _, row in df.iterrows():
                    q = str(row.get("CÂU HỎI") or "").strip()
                    correct_key = str(row.get("ĐÁP ÁN ĐÚNG") or "").strip()
                    correct_ans = ""
                    if correct_key.isdigit():
                        correct_ans = str(row.get(f"ĐÁP ÁN {correct_key}", "")).strip()
                    if q and correct_ans:
                        records.append({
                            "cauhoi": q,
                            "dapan": correct_ans
                        })
        except Exception as err:
            print(f"⚠️ Lỗi khi xử lý sheet {sheet}: {err}")
    return records

# Nạp dữ liệu ngay khi app khởi chạy
all_records = load_records(file_path)

@app.route("/", methods=["GET", "POST"])
def index():
    keyword = ""
    records = all_records
    if request.method == "POST":
        if "clear" in request.form:
            return redirect("/")
        keyword = request.form.get("keyword", "").strip().lower()
        if keyword:
            records = [
                r for r in all_records
                if keyword in r["cauhoi"].lower() or keyword in r["dapan"].lower()
            ]
    return render_template("index.html", records=records, keyword=keyword)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
