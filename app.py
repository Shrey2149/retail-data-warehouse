from flask import Flask, jsonify, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__)

username = "postgres"
password = "shreythegreat"
host = "localhost"
port = "5432"
database = "retail_dw"

engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/total-revenue",methods = ["GET"])
def total_revenue():
    connection = engine.connect()
    result = connection.execute(
        text("SELECT SUM(total_amount) FROM fact_sales;")
    )
    revenue = result.scalar()
    connection.close()
    return jsonify({"total_revenue": float(revenue) if revenue else 0})

@app.route("/monthly-sales", methods=["GET"])
def monthly_sales():
    year = request.args.get("year")
    region = request.args.get("region")

    connection = engine.connect()
    query = """
        SELECT dt.year,
               dt.month,
               SUM(fs.total_amount) AS revenue
        FROM fact_sales fs
        JOIN dim_time dt ON fs.date_id = dt.date_id
        JOIN dim_customer dc ON fs.customer_id = dc.customer_id
        WHERE 1=1
    """
    if year:
        query += f" AND dt.year = {int(year)}"
    if region:
        query += f" AND dc.state = '{region}'"

    query += """ 
            GROUP BY dt.year, dt.month 
            ORDER BY dt.year, dt.month;
    """
    
    result = connection.execute(text(query))    
    data = [
        {
            "year": row[0],
            "month": row[1],
            "revenue": float(row[2])
        }
        for row in result
    ]
    connection.close()

    return jsonify(data)

@app.route("/total-orders", methods=["GET"])
def total_orders():
    connection = engine.connect()

    result = connection.execute(
        text("SELECT COUNT(*) FROM fact_sales;")
    )

    count = result.scalar()

    connection.close()

    return jsonify({"total_orders": int(count)})

@app.route("/total-customers", methods=["GET"])
def total_customers():
    connection = engine.connect()

    result = connection.execute(
        text("SELECT COUNT(DISTINCT customer_id) FROM fact_sales;")
    )

    count = result.scalar()

    connection.close()

    return jsonify({"total_customers": int(count)})

@app.route("/avg-order-value", methods=["GET"])
def avg_order_value():
    connection = engine.connect()

    result = connection.execute(
        text("SELECT AVG(total_amount) FROM fact_sales;")
    )

    avg = result.scalar()

    connection.close()

    return jsonify({"avg_order_value": float(avg) if avg else 0})


@app.route("/revenue-by-region",methods = ["GET"])
def revenue_by_region():
    connection = engine.connect()
    query = """
        SELECT dc.state AS region,
                SUM(fs.total_amount) AS revenue
        FROM fact_sales fs
        JOIN dim_customer dc
        ON fs.customer_id = dc.customer_id
        GROUP BY dc.state
        ORDER BY revenue DESC;
    """
    result = connection.execute(text(query))

    data = [
        {
            "region" : row[0],
            "revenue" : float(row[1])
        }
        for row in result
    ]
    connection.close()

    return jsonify(data)

@app.route("/top-products", methods=["GET"])
def top_products():

    year = request.args.get("year")
    region = request.args.get("region")

    connection = engine.connect()

    query = """
        SELECT dp.name,
               SUM(fs.total_amount) AS revenue
        FROM fact_sales fs
        JOIN dim_product dp ON fs.product_id = dp.product_id
        JOIN dim_time dt ON fs.date_id = dt.date_id
        JOIN dim_customer dc ON fs.customer_id = dc.customer_id
        WHERE 1=1
    """

    if year:
        query += f" AND dt.year = {int(year)}"

    if region:
        query += f" AND dc.state = '{region}'"

    query += """
        GROUP BY dp.name
        ORDER BY revenue DESC
        LIMIT 10;
    """

    result = connection.execute(text(query))

    data = [
        {
            "product": row[0],
            "revenue": float(row[1])
        }
        for row in result
    ]

    connection.close()

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

