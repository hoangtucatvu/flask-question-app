from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
file_path = "tong hop de thi.xlsx"

# Load toàn bộ dữ liệu từ Excel
xls = pd.ExcelFile(file_path)
all_data = []

for sheet in xls.sheet_names:
    df = xls.parse(sheet)
    if "Câu hỏi" in df.columns and "Đáp án đúng" in df.columns:
        df = df[["Câu hỏi", "Đáp án đúng"]].dropna()
        all_data.append(df)

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
            filtered = df_all[df_all["Câu hỏi"].str.lower().str.contains(keyword, na=False)]
            records = filtered.to_dict(orient="records")

    # ⚠️ KHÔNG gọi .to_dict nếu records là list!
    return render_template("index.html", records=records, keyword=keyword)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
