import pandas as pd

EXPECTED_COLUMNS = [
    "order_id", "order_date", "order_datetime", "year", "month",
    "month_name", "week", "day_type", "hour", "customer_id",
    "gender", "age", "customer_segment", "membership",
    "restaurant_id", "restaurant_name", "city", "area", "cuisine",
    "price_category", "restaurant_rating", "food_amount", "discount",
    "discount_percent", "delivery_fee", "tax", "net_revenue",
    "order_status", "is_completed", "is_cancelled", "delivery_minutes",
    "delivery_status", "is_late", "payment_method", "payment_status",
    "rating", "food_rating", "delivery_rating", "has_review", "Order_Month"
]

INTEGER_COLUMNS = [
    "year", "month", "week", "hour", "age",
    "is_completed", "is_cancelled", "is_late", "has_review"
]

NUMERIC_COLUMNS = [
    "restaurant_rating", "food_amount", "discount",
    "discount_percent", "delivery_fee", "tax", "net_revenue",
    "delivery_minutes", "rating", "food_rating", "delivery_rating"
]


def read_file(file):
    file.seek(0)

    if file.name.lower().endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    df.columns = [str(column).strip() for column in df.columns]
    return df


def combine_files(files):
    dataframes = [read_file(file) for file in files]

    # Append rows from all files.
    return pd.concat(dataframes, ignore_index=True, sort=False)


def validate_and_prepare(df):
    df = df.copy()
    errors = []

    missing = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    extra = [col for col in df.columns if col not in EXPECTED_COLUMNS]

    if missing:
        errors.append("Missing columns: " + ", ".join(missing))

    if extra:
        errors.append("Unexpected columns: " + ", ".join(extra))

    if errors:
        return df, errors

    df = df[EXPECTED_COLUMNS].copy()

    # Validate order IDs.
    df["order_id"] = df["order_id"].astype("string").str.strip()

    blank_ids = df["order_id"].isna() | df["order_id"].eq("")
    if blank_ids.any():
        errors.append(f"{blank_ids.sum()} rows have blank order IDs.")

    # Convert dates.
    for col in ["order_date", "order_datetime"]:
        converted = pd.to_datetime(df[col], errors="coerce")
        invalid = df[col].notna() & converted.isna()

        if invalid.any():
            errors.append(f"Invalid date/time values in {col}.")

        df[col] = converted

    # Convert integer columns.
    for col in INTEGER_COLUMNS:
        converted = pd.to_numeric(df[col], errors="coerce")
        invalid = df[col].notna() & converted.isna()

        if invalid.any():
            errors.append(f"Invalid numeric values in {col}.")

        df[col] = converted.astype("Int64")

    # Convert decimal/numeric columns.
    for col in NUMERIC_COLUMNS:
        converted = pd.to_numeric(df[col], errors="coerce")
        invalid = df[col].notna() & converted.isna()

        if invalid.any():
            errors.append(f"Invalid numeric values in {col}.")

        df[col] = converted

    if errors:
        return df, errors

    # Keep the first occurrence of repeated order IDs.
    df = df.drop_duplicates(subset=["order_id"], keep="first")

    # Convert pandas missing values into database-friendly NULLs.
    df = df.astype(object).where(pd.notna(df), None)

    return df, []