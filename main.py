# f1 file buffer
# f2 file buffer
import pandas as pd
from flask import Flask, request, render_template, make_response
import io


def read_file_csv(file):
    df = pd.read_csv(file, encoding='utf-16', sep='\t')

    return df


def merge(f1, f2):
    # f1 and f2 are files recieved in Flask request.files
    # check the file type

    print('Check 0')
    print(f1.filename.split(".")[-1])
    print(f2.filename.split(".")[-1])

    if f1.filename.split(".")[-1] == "csv":
        df1 = read_file_csv(f1)

    print('Check 0.5')
    if f2.filename.split(".")[-1] == "csv":
        df2 = read_file_csv(f2)

    print('Check 1')

    # check for excel
    if f1.filename.split(".")[-1] == "xlsx" or f1.filename.split(".")[-1] == "xls":
        df1 = pd.read_excel(f1)
    if f2.filename.split(".")[-1] == "xlsx" or f2.filename.split(".")[-1] == "xls":
        df2 = pd.read_excel(f2)

    # merge the files
    df = pd.concat([df1, df2], axis=0, ignore_index=True)

    print(df1.columns)
    print(df2.columns)

    buffer = io.BytesIO()
    wtiter = pd.ExcelWriter(buffer)
    df.to_excel(wtiter, index=False)
    wtiter.close()

    buffer.seek(0)

    return buffer


# make a flask endpoint
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        f1 = request.files["f1"]
        f2 = request.files["f2"]
        # call the merge function
        merged_buffer = merge(f1, f2)

        response = make_response(merged_buffer)
        response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        response.headers["Content-Disposition"] = "attachment; filename=merged.xlsx"

        return response

    return render_template("index.html")

# @app.route("/merge", methods=["POST"])
# def merge_files():
#     f1 = request.files["f1"]
#     f2 = request.files["f2"]
#     # call the merge function
#     merged_buffer = merge(f1, f2)

#     response = make_response(merged_buffer)
#     response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     response.headers["Content-Disposition"] = "attachment; filename=merged.xlsx"

#     return response


if __name__ == "__main__":
    app.run(debug=True)
