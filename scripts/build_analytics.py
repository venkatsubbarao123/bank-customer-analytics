from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "bank_transactions.csv"
CLEAN_DIR = ROOT / "data" / "cleaned"


def json_ready(frame: pd.DataFrame) -> list[dict]:
    """Return records with pandas/numpy values converted to JSON-safe values."""
    return json.loads(frame.to_json(orient="records", date_format="iso"))


def main() -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(RAW_PATH, low_memory=False)
    original_rows = len(raw)

    rename_map = {
        "TransactionID": "transaction_id",
        "CustomerID": "customer_id",
        "CustomerDOB": "customer_dob",
        "CustGender": "customer_gender",
        "CustLocation": "customer_location",
        "CustAccountBalance": "customer_account_balance",
        "TransactionDate": "transaction_date",
        "TransactionTime": "transaction_time",
        "TransactionAmount (INR)": "transaction_amount_inr",
    }
    df = raw.rename(columns=rename_map).copy()

    df["customer_dob"] = pd.to_datetime(df["customer_dob"], format="%d/%m/%y", errors="coerce")
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], format="%d/%m/%y", errors="coerce")
    time_text = df["transaction_time"].astype("string").str.replace(r"\D", "", regex=True).str.zfill(6)
    parsed_time = pd.to_datetime(time_text, format="%H%M%S", errors="coerce")
    df["transaction_time"] = parsed_time.dt.strftime("%H:%M:%S")
    df["transaction_hour"] = parsed_time.dt.hour
    df["customer_account_balance"] = pd.to_numeric(df["customer_account_balance"], errors="coerce")
    df["transaction_amount_inr"] = pd.to_numeric(df["transaction_amount_inr"], errors="coerce")

    df["customer_gender"] = (
        df["customer_gender"].astype("string").str.strip().str.upper().map({"M": "Male", "F": "Female"}).fillna("Unknown")
    )
    df["customer_location"] = df["customer_location"].astype("string").str.strip().str.upper().fillna("UNKNOWN")

    invalid_dob = df["customer_dob"].notna() & (
        (df["customer_dob"] > df["transaction_date"]) |
        (df["transaction_date"].dt.year - df["customer_dob"].dt.year > 100)
    )
    df.loc[invalid_dob, "customer_dob"] = pd.NaT
    duplicate_transaction_ids = int(df["transaction_id"].duplicated().sum())
    missing_required_before = int(df[["transaction_id", "customer_id", "transaction_date", "transaction_amount_inr"]].isna().any(axis=1).sum())
    df = df.drop_duplicates(subset="transaction_id", keep="first")
    df = df.dropna(subset=["transaction_id", "customer_id", "transaction_date", "transaction_amount_inr"])
    df = df[df["transaction_amount_inr"] >= 0].copy()

    max_date = df["transaction_date"].max()
    df["customer_age"] = ((max_date - df["customer_dob"]).dt.days / 365.25).round(1)
    df.loc[~df["customer_age"].between(18, 100), "customer_age"] = np.nan
    df["age_group"] = pd.cut(
        df["customer_age"],
        bins=[17, 25, 35, 45, 55, np.inf],
        labels=["18-25", "26-35", "36-45", "46-55", "56+"],
    ).astype("string").fillna("Unknown")

    df["transaction_year"] = df["transaction_date"].dt.year.astype("Int64")
    df["transaction_month"] = df["transaction_date"].dt.month.astype("Int64")
    df["transaction_month_name"] = df["transaction_date"].dt.strftime("%b")
    df["transaction_quarter"] = "Q" + df["transaction_date"].dt.quarter.astype("string")
    df["transaction_day"] = df["transaction_date"].dt.day.astype("Int64")
    df["transaction_day_name"] = df["transaction_date"].dt.day_name()
    df["time_period"] = pd.cut(
        df["transaction_hour"],
        bins=[-1, 5, 11, 16, 20, 24],
        labels=["Night", "Morning", "Afternoon", "Evening", "Night"],
        ordered=False,
    ).astype("string").fillna("Unknown")

    q1, q3 = df["transaction_amount_inr"].quantile([0.25, 0.75])
    percentiles = df["transaction_amount_inr"].quantile([0.25, 0.50, 0.75, 0.90, 0.95, 0.99])
    iqr = q3 - q1
    upper_outlier_threshold = q3 + 1.5 * iqr
    outlier_count = int((df["transaction_amount_inr"] > upper_outlier_threshold).sum())
    df["transaction_value_group"] = np.select(
        [df["transaction_amount_inr"] <= q1, df["transaction_amount_inr"] <= q3],
        ["Low Value", "Medium Value"],
        default="High Value",
    )

    date_columns = ["customer_dob", "transaction_date"]
    for column in date_columns:
        df[column] = df[column].dt.strftime("%Y-%m-%d")
    ordered_columns = [
        "transaction_id", "customer_id", "customer_dob", "customer_gender", "customer_location",
        "customer_account_balance", "transaction_date", "transaction_time", "transaction_amount_inr",
        "transaction_year", "transaction_month", "transaction_month_name", "transaction_quarter",
        "transaction_day", "transaction_day_name", "transaction_hour", "time_period", "customer_age",
        "age_group", "transaction_value_group",
    ]
    df = df[ordered_columns]
    df.to_csv(CLEAN_DIR / "bank_transactions_cleaned.csv", index=False)

    numeric = df["transaction_amount_inr"]
    customer_summary = (
        df.groupby("customer_id", as_index=False)
        .agg(
            transaction_count=("transaction_id", "count"),
            total_transaction_amount_inr=("transaction_amount_inr", "sum"),
            average_transaction_amount_inr=("transaction_amount_inr", "mean"),
            account_balance_inr=("customer_account_balance", "max"),
            customer_gender=("customer_gender", "first"),
            customer_location=("customer_location", "first"),
            age_group=("age_group", "first"),
            first_transaction_date=("transaction_date", "min"),
            last_transaction_date=("transaction_date", "max"),
        )
        .sort_values("total_transaction_amount_inr", ascending=False)
    )
    location_summary = (
        df.groupby("customer_location", as_index=False)
        .agg(
            customer_count=("customer_id", "nunique"),
            transaction_count=("transaction_id", "count"),
            total_transaction_amount_inr=("transaction_amount_inr", "sum"),
            average_transaction_amount_inr=("transaction_amount_inr", "mean"),
        )
        .sort_values("total_transaction_amount_inr", ascending=False)
    )
    monthly_summary = (
        df.assign(month=pd.to_datetime(df["transaction_date"]).dt.to_period("M").astype(str))
        .groupby("month", as_index=False)
        .agg(transaction_count=("transaction_id", "count"), total_transaction_amount_inr=("transaction_amount_inr", "sum"), average_transaction_amount_inr=("transaction_amount_inr", "mean"))
    )
    monthly_summary["period_note"] = np.where(monthly_summary["month"] == monthly_summary["month"].max(), "Partial month through 2016-10-21", "Full calendar month")
    hourly_summary = (
        df.groupby(["transaction_hour", "time_period"], as_index=False)
        .agg(transaction_count=("transaction_id", "count"), total_transaction_amount_inr=("transaction_amount_inr", "sum"))
        .sort_values("transaction_hour")
    )
    segment_summary = (
        df.groupby(["transaction_year", "customer_gender", "customer_location"], as_index=False)
        .agg(transaction_count=("transaction_id", "count"), total_value=("transaction_amount_inr", "sum"), average_value=("transaction_amount_inr", "mean"), customer_count=("customer_id", "nunique"))
    )
    segment_monthly = (
        df.assign(month=pd.to_datetime(df["transaction_date"]).dt.to_period("M").astype(str))
        .groupby(["transaction_year", "customer_gender", "customer_location", "month"], as_index=False)
        .agg(transaction_count=("transaction_id", "count"), total_value=("transaction_amount_inr", "sum"))
    )
    segment_hourly = (
        df.groupby(["transaction_year", "customer_gender", "customer_location", "transaction_hour"], as_index=False)
        .agg(transaction_count=("transaction_id", "count"), total_value=("transaction_amount_inr", "sum"))
    )
    segment_genders = (
        df.groupby(["transaction_year", "customer_gender", "customer_location"], as_index=False)
        .agg(customer_count=("customer_id", "nunique"), transaction_count=("transaction_id", "count"), total_value=("transaction_amount_inr", "sum"))
    )
    segment_age_groups = (
        df.groupby(["transaction_year", "customer_gender", "customer_location", "age_group"], as_index=False, observed=True)
        .agg(transaction_count=("transaction_id", "count"), total_value=("transaction_amount_inr", "sum"))
    )
    segment_value_groups = (
        df.groupby(["transaction_year", "customer_gender", "customer_location", "transaction_value_group"], as_index=False, observed=True)
        .agg(transaction_count=("transaction_id", "count"), total_value=("transaction_amount_inr", "sum"))
    )
    segment_distribution = (
        df.assign(amount_bin=pd.cut(df["transaction_amount_inr"], bins=[-0.01, 100, 500, 1200, 5000, 25000, 100000, np.inf], labels=["0-100", "101-500", "501-1,200", "1,201-5,000", "5,001-25,000", "25,001-100,000", "100,000+"]))
        .groupby(["transaction_year", "customer_gender", "customer_location", "amount_bin"], as_index=False, observed=True)
        .agg(transaction_count=("transaction_id", "count"))
    )
    segment_customers = (
        df.groupby(["transaction_year", "customer_gender", "customer_location", "customer_id"], as_index=False)
        .agg(transaction_count=("transaction_id", "count"), total_transaction_amount_inr=("transaction_amount_inr", "sum"), average_transaction_amount_inr=("transaction_amount_inr", "mean"), account_balance_inr=("customer_account_balance", "max"), age_group=("age_group", "first"))
        .sort_values("total_transaction_amount_inr", ascending=False)
        .groupby(["transaction_year", "customer_gender", "customer_location"], as_index=False, group_keys=False)
        .head(12)
    )
    customer_counts = {
        "year": json_ready(df.groupby("transaction_year", as_index=False).agg(customer_count=("customer_id", "nunique"))),
        "gender": json_ready(df.groupby("customer_gender", as_index=False).agg(customer_count=("customer_id", "nunique"))),
        "location": json_ready(df.groupby("customer_location", as_index=False).agg(customer_count=("customer_id", "nunique"))),
        "year_gender": json_ready(df.groupby(["transaction_year", "customer_gender"], as_index=False).agg(customer_count=("customer_id", "nunique"))),
        "year_location": json_ready(df.groupby(["transaction_year", "customer_location"], as_index=False).agg(customer_count=("customer_id", "nunique"))),
        "gender_location": json_ready(df.groupby(["customer_gender", "customer_location"], as_index=False).agg(customer_count=("customer_id", "nunique"))),
        "year_gender_location": json_ready(segment_summary[["transaction_year", "customer_gender", "customer_location", "customer_count"]]),
    }
    gender_summary = df.groupby("customer_gender", as_index=False).agg(customer_count=("customer_id", "nunique"), transaction_count=("transaction_id", "count"), total_value=("transaction_amount_inr", "sum"))
    for name, frame in {
        "customer_summary.csv": customer_summary,
        "location_summary.csv": location_summary,
        "monthly_summary.csv": monthly_summary,
        "hourly_summary.csv": hourly_summary,
    }.items():
        frame.to_csv(CLEAN_DIR / name, index=False)

    quality = {
        "source_rows": original_rows,
        "cleaned_rows": len(df),
        "source_columns": len(raw.columns),
        "duplicate_transaction_ids": duplicate_transaction_ids,
        "rows_missing_required_fields_before_cleaning": missing_required_before,
        "invalid_dob_values_set_missing": int(invalid_dob.sum()),
        "missing_values_after_cleaning": {key: int(value) for key, value in df.isna().sum().items()},
        "amount_zero_count": int((numeric == 0).sum()),
        "amount_negative_count": int((numeric < 0).sum()),
        "amount_q1_inr": round(float(q1), 2),
        "amount_q3_inr": round(float(q3), 2),
        "percentiles_inr": {str(int(key * 100)): round(float(value), 2) for key, value in percentiles.items()},
        "iqr_upper_outlier_threshold_inr": round(float(upper_outlier_threshold), 2),
        "iqr_outlier_count": outlier_count,
    }
    (CLEAN_DIR / "quality_report.json").write_text(json.dumps(quality, indent=2), encoding="utf-8")

    top_location = location_summary.iloc[0]
    top_customer = customer_summary.iloc[0]
    monthly_peak = monthly_summary.loc[monthly_summary["total_transaction_amount_inr"].idxmax()]
    time_peak = hourly_summary.loc[hourly_summary["transaction_count"].idxmax()]
    insights = [
        {"label": "Customer concentration", "value": f"Top customer represents {top_customer['total_transaction_amount_inr'] / numeric.sum():.2%} of total transaction value."},
        {"label": "Location leader", "value": f"{top_location['customer_location']} leads by value with INR {top_location['total_transaction_amount_inr']:,.0f}."},
        {"label": "Peak month", "value": f"{monthly_peak['month']} generated the highest transaction value at INR {monthly_peak['total_transaction_amount_inr']:,.0f}."},
        {"label": "Peak hour", "value": f"Hour {int(time_peak['transaction_hour']):02d}:00 had the most transactions ({int(time_peak['transaction_count']):,})."},
    ]
    (CLEAN_DIR / "insights.json").write_text(json.dumps(insights, indent=2), encoding="utf-8")

    dashboard_data = {
        "kpis": {
            "transactions": int(len(df)),
            "customers": int(df["customer_id"].nunique()),
            "total_value": float(numeric.sum()),
            "average_value": float(numeric.mean()),
            "median_value": float(numeric.median()),
            "min_value": float(numeric.min()),
            "max_value": float(numeric.max()),
            "average_balance": float(df["customer_account_balance"].mean()),
            "date_start": df["transaction_date"].min(),
            "date_end": df["transaction_date"].max(),
        },
        "monthly": json_ready(monthly_summary),
        "locations": json_ready(location_summary),
        "customers": json_ready(customer_summary.head(12)),
        "hourly": json_ready(hourly_summary),
        "genders": json_ready(gender_summary),
        "age_groups": json_ready(df.groupby("age_group", as_index=False, observed=False).agg(transaction_count=("transaction_id", "count"), total_value=("transaction_amount_inr", "sum"))),
        "value_groups": json_ready(df.groupby("transaction_value_group", as_index=False).agg(transaction_count=("transaction_id", "count"), total_value=("transaction_amount_inr", "sum"))),
        "distribution": json_ready(df.assign(amount_bin=pd.cut(df["transaction_amount_inr"], bins=[-0.01, 100, 500, 1200, 5000, 25000, 100000, np.inf], labels=["0-100", "101-500", "501-1,200", "1,201-5,000", "5,001-25,000", "25,001-100,000", "100,000+"])).groupby("amount_bin", observed=False, as_index=False).agg(transaction_count=("transaction_id", "count"))),
        "segments": json_ready(segment_summary),
        "segment_monthly": json_ready(segment_monthly),
        "segment_hourly": json_ready(segment_hourly),
        "segment_genders": json_ready(segment_genders),
        "segment_age_groups": json_ready(segment_age_groups),
        "segment_value_groups": json_ready(segment_value_groups),
        "segment_distribution": json_ready(segment_distribution),
        "segment_customers": json_ready(segment_customers),
        "customer_counts": customer_counts,
        "insights": insights,
        "quality": quality,
    }
    (CLEAN_DIR / "dashboard_data.json").write_text(json.dumps(dashboard_data, indent=2), encoding="utf-8")
    print(f"Built analytics outputs from {original_rows:,} source rows; retained {len(df):,} cleaned rows.")


if __name__ == "__main__":
    main()
