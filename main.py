from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
file_path = "tong hop de thi.xlsx"

# Tải toàn bộ dữ liệu từ Excel, chuẩn hóa tên cột
xls = pd.ExcelFile(file_path)
all_data = []

for sheet in xls.sheet_names:
    df = xls.parse(sheet)
    df.columns = [str(c).strip().upper() for c in df.columns]
    if "CÂU HỎI" in df.columns and "ĐÁP ÁN ĐÚNG" in df.columns:
        df["SHEET"] = sheet
        all_data.append(df[["CÂU HỎI", "ĐÁP ÁN ĐÚNG"]])

df_all = pd.concat(all_data, ignore_index=True)

@app.route("/", methods=["GET", "POST"])
def index():
    keyword = ""
    records = []

    if request.method == "POST":
        if "clear" in request.form:
            keyword = ""
        else:
            keyword = request.form["keyword"].strip().lower()
            records = df_all[df_all["CÂU HỎI"].str.lower().str.contains(keyword, na=False)]

    return render_template("index.html", records=records.to_dict(orient="records"), keyword=keyword)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
