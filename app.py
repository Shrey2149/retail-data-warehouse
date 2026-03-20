from flask import Flask, jsonify, render_template, request
from sqlalchemy import create_engine, text
import joblib
import pandas as pd

app = Flask(__name__)

username = "postgres"
password = "shreythegreat"
host = "localhost"
port = "5432"
database = "retail_dw"

model = joblib.load("churn_model.pkl")
scaler = joblib.load("scaler.pkl")
engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

@app.route("/predict-churn", methods=["GET"])
def predict_churn():

    query = """
        SELECT 
            customer_id,
            SUM(total_amount) AS total_spend,
            AVG(total_amount) AS avg_order_value,
            COUNT(transaction_id) AS purchase_frequency,
            MAX(transaction_date) AS last_purchase
        FROM fact_sales
        GROUP BY customer_id
    """

    df = pd.read_sql(query, engine)

    # Recency
    today = pd.to_datetime(df["last_purchase"]).max()
    df["recency"] = (today - pd.to_datetime(df["last_purchase"])).dt.days

    # Dummy customer_age (optional simple version)
    df["customer_age"] = 365

    features = df[[
        "total_spend",
        "avg_order_value",
        "purchase_frequency",
        "recency",
        "customer_age"
    ]]

    scaled = scaler.transform(features)

    df["churn_probability"] = model.predict_proba(scaled)[:, 1]

    # Risk categories
    def risk(p):
        if p > 0.7:
            return "High"
        elif p > 0.4:
            return "Medium"
        else:
            return "Low"

    df["risk"] = df["churn_probability"].apply(risk)

    return jsonify(df[[
        "customer_id",
        "churn_probability",
        "risk"
    ]].to_dict(orient="records"))

@app.route("/market-basket")
def market_basket():
    df = pd.read_csv("ml/frequent_itemsets.csv")

    data = df.to_dict(orient="records")

    return jsonify(data)


@app.route("/churn-metrics")
def churn_metrics():

    df = pd.read_json("http://127.0.0.1:5001/predict-churn")

    churn_rate = (df["risk"] == "High").mean()

    high_risk_count = (df["risk"] == "High").sum()

    return jsonify({
        "churn_rate": float(churn_rate),
        "high_risk_customers": int(high_risk_count)
    })

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

@app.route("/monthly-sales")
def monthly_sales():

    year = request.args.get("year")
    region = request.args.get("region")

    query = """
        SELECT 
            EXTRACT(YEAR FROM fs.transaction_date) AS year,
            EXTRACT(MONTH FROM fs.transaction_date) AS month,
            SUM(fs.total_amount) AS revenue
        FROM fact_sales fs
        JOIN dim_customer dc ON fs.customer_id = dc.customer_id
        WHERE 1=1
    """

    if year:
        query += f" AND EXTRACT(YEAR FROM fs.transaction_date) = {int(year)}"

    if region:
        query += f" AND dc.state = '{region}'"

    query += """
        GROUP BY year, month
        ORDER BY year, month;
    """

    with engine.connect() as connection:
        result = connection.execute(text(query))
        data = [
            {
                "year": int(row.year),
                "month": int(row.month),
                "revenue": float(row.revenue)
            }
            for row in result
        ]

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
        JOIN dim_customer dc ON fs.customer_id = dc.customer_id
        WHERE 1=1
    """

    # Year filter (using transaction_date)
    if year:
        query += f" AND EXTRACT(YEAR FROM fs.transaction_date) = {int(year)}"

    # Region filter
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
    app.run(host="0.0.0.0", port=10000)

