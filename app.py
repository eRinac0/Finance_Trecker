import os
from datetime import date

from flask import Flask, flash, redirect, render_template, request, url_for

from database import (
    add_transaction, create_connection, create_table, delete_transaction,
    get_balance, get_expense_report, get_transactions,
)
from validators import validate_date, validate_transaction


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "local-development-key")


def money(amount):
    return f"{amount:,.2f}".replace(",", " ") + " EUR"


@app.template_filter("money")
def money_filter(amount):
    return money(amount)


def database_connection():
    conn = create_connection()
    create_table(conn)
    return conn


def current_month():
    return date.today().strftime("%Y-%m")


@app.get("/")
def dashboard():
    month = request.args.get("month", current_month())
    try:
        month = validate_date(month, allow_month=True)
    except ValueError:
        flash("Month must use YYYY-MM format.", "error")
        month = current_month()
    conn = database_connection()
    try:
        income, expenses = get_balance(conn, month)
        top_categories = get_expense_report(conn, month)
        recent_transactions = get_transactions(conn)[:5]
    finally:
        conn.close()
    return render_template(
        "dashboard.html",
        month=month,
        income=income,
        expenses=expenses,
        balance=income - expenses,
        top_categories=top_categories,
        recent_transactions=recent_transactions,
    )


@app.get("/transactions")
def transactions():
    date_from = request.args.get("from", "")
    date_to = request.args.get("to", "")
    category = request.args.get("category", "")
    try:
        validated_from = validate_date(date_from or None)
        validated_to = validate_date(date_to or None)
    except ValueError as error:
        flash(str(error), "error")
        validated_from = validated_to = None
    conn = database_connection()
    try:
        records = get_transactions(conn, validated_from, validated_to, category)
    finally:
        conn.close()
    return render_template(
        "transactions.html",
        transactions=records,
        filters={
            "date_from": date_from,
            "date_to": date_to,
            "category": category,
        },
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        raw_amount = request.form.get("amount", "")
        try:
            amount = float(raw_amount)
            category, description = validate_transaction(
                request.form.get("type", ""), amount,
                request.form.get("category", ""), request.form.get("description", "")
            )
            transaction_date = validate_date(request.form.get("date") or None)
        except ValueError as error:
            flash(str(error), "error")
            return render_template("add_transaction.html", form=request.form)
        conn = database_connection()
        try:
            add_transaction(
                conn,
                request.form["type"],
                amount,
                category,
                description,
                transaction_date,
            )
        finally:
            conn.close()
        flash("Transaction added successfully.", "success")
        return redirect(url_for("transactions"))
    return render_template("add_transaction.html", form={"date": date.today().isoformat()})


@app.get("/report")
def report():
    month = request.args.get("month", current_month())
    try:
        month = validate_date(month, allow_month=True)
    except ValueError:
        flash("Month must use YYYY-MM format.", "error")
        return redirect(url_for("report"))
    conn = database_connection()
    try:
        income, expenses = get_balance(conn, month)
        top_categories = get_expense_report(conn, month)
    finally:
        conn.close()
    return render_template(
        "report.html",
        month=month,
        income=income,
        expenses=expenses,
        balance=income - expenses,
        top_categories=top_categories,
    )


@app.post("/transactions/<int:transaction_id>/delete")
def delete(transaction_id):
    conn = database_connection()
    try:
        was_deleted = delete_transaction(conn, transaction_id)
    finally:
        conn.close()
    flash(
        "Transaction deleted." if was_deleted else "Transaction was not found.",
        "success" if was_deleted else "error",
    )
    return redirect(url_for("transactions"))


if __name__ == "__main__":
    app.run(debug=True)
