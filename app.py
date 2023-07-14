# An API using Flask to communicate with bulkybookwebtesting.azurewebsites.net

from flask import Flask, request, jsonify
import pyodbc
from datetime import datetime

app = Flask(__name__)


@app.route("/get-category/<category_id>")
def get_category(category_id):
    conn = pyodbc.connect(
        r"Driver={FreeTDS};"
        "Server=tcp:bulkyserver.database.windows.net, 1433;"
        "Database=bulky_db;"
        "Uid=admin-sql;"
        "Pwd=Pass123?!;"
        "Encrypt=yes;"
        "Trusted_Connection=no;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    sql_string = f"""
        select * from bulky_db.dbo.Categories
        where Id={category_id}
    """

    cursor = conn.execute(sql_string)

    category_info = {}
    for row in cursor:
        print(row[0])
        category_info["category_id"] = row[0]
        category_info["category_name"] = row[1]
        category_info["display_order"] = row[2]
        category_info["created_date"] = row[3]

    # In url, this is represented as ?=. Not exactly sure how to use it.
    # extra = request.args.get("extra")
    # if extra:
    #     user_data["extra"] = extra

    conn.close()

    return jsonify(category_info), 200


@app.route("/create-category", methods=["POST"])
def create_category():
    conn = pyodbc.connect(
        "Driver={FreeTDS};"
        "Server=tcp:bulkyserver.database.windows.net, 1433;"
        "Database=bulky_db;"
        "Uid=admin-sql;"
        "Pwd=Pass123?!;"
        "Encrypt=yes;"
        "Trusted_Connection=no;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    current_datetime = str(datetime.now())

    data = request.get_json()
    data_values = list(data.values())
    data_values.append(current_datetime)

    for i, value in enumerate(data_values):
        data_values[i] = f"'{value}'"

    insert_values = ",".join(data_values)

    insert_builder = "("
    insert_builder += insert_values
    insert_builder += ")"

    sql_string = f"""
        insert into bulky_db.dbo.Categories(Name, DisplayOrder,CreatedDateTime)
        values {insert_builder};
    """
    print(sql_string)
    cursor = conn.execute(sql_string)
    conn.commit()
    conn.close()
    return jsonify(data), 201


# @app.route("/edit-category/<category-id>", methods=["PUT"])
# def edit_category(category_id):
#     conn = pyodbc.connect(
#         "Driver={FreeTDS};"
#         "Server=tcp:bulkyserver.database.windows.net, 1433;"
#         "Database=bulky_db;"
#         "Uid=admin-sql;"
#         "Pwd=Pass123?!;"
#         "Encrypt=yes;"
#         "Trusted_Connection=no;"
#         "TrustServerCertificate=no;"
#         "Connection Timeout=30;"
#     )
#     conn.close()


@app.route("/delete-category/<category_id>", methods=["DELETE"])
def delete_category(category_id):
    conn = pyodbc.connect(
        "Driver={FreeTDS};"
        "Server=tcp:bulkyserver.database.windows.net, 1433;"
        "Database=bulky_db;"
        "Uid=admin-sql;"
        "Pwd=Pass123?!;"
        "Encrypt=yes;"
        "Trusted_Connection=no;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    sql_string = f"""
        delete from bulky_db.dbo.Categories
        where Id='{category_id}'
    """

    cursor = conn.execute(sql_string)
    conn.commit()

    conn.close()
    return f"Category {category_id}", 200


if __name__ == "__main__":
    app.run(debug=True)
