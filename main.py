from flask import Flask, render_template, request, redirect
import pandas as pd
import os

app = Flask(__name__)

file_path = "tong hop de thi.xlsx"

def load_records(path):
    xls = pd.ExcelFile(path)
    records = []
    for sheet in xls.sheet_names:
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
    return records

all_records = load_records(file_path)

@app.route("/", methods=["GET", "POST"])
def index():
    keyword = ""
    records = all_records
    if request.method == "POST":
        if "clear" in request.form:
            return redirect("/")  # Reset từ khóa
        keyword = request.form.get("keyword", "").strip().lower()
        if keyword:
            records = [r for r in all_records if keyword in r["cauhoi"].lower() or keyword in r["dapan"].lower()]
    return render_template("index.html", records=records, keyword=keyword)

app.run(host="0.0.0.0", port=81)