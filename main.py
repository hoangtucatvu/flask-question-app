from flask import Flask, render_template, request, redirect
import pandas as pd
import os

app = Flask(__name__)

FILE_PATH = "tong hop de thi.xlsx"

def load_records(path):
    if not os.path.exists(path):
        print("❗ File không tồn tại:", path)
        return []

    records = []
    try:
        xls = pd.ExcelFile(path)
        for sheet in xls.sheet_names:
            try:
                df = xls.parse(sheet)
                df.columns = [str(c).strip().upper() for c in df.columns]
                if "CÂU HỎI" in df.columns and "ĐÁP ÁN ĐÚNG" in df.columns:
                    for _, row in df.iterrows():
                        question = str(row.get("CÂU HỎI") or "").strip()
                        correct_key = str(row.get("ĐÁP ÁN ĐÚNG") or "").strip()
                        correct_answer = ""
                        if correct_key.isdigit():
                            correct_answer = str(row.get(f"ĐÁP ÁN {correct_key}", "")).strip()
                        if question and correct_answer:
                            records.append({
                                "cauhoi": question,
                                "dapan": correct_answer
                            })
            except Exception as e:
                print(f"Lỗi khi xử lý sheet '{sheet}':", e)
    except Exception as e:
        print("❗ Lỗi khi đọc file Excel:", e)
    return records

all_records = load_records(FILE_PATH)

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
