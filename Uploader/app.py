import streamlit as st
import pandas as pd

from processor import combine_files, validate_and_prepare
from database import get_existing_order_ids, upload_rows, get_row_count

st.set_page_config(page_title="RestaurantIQ Uploader", layout="wide")
st.title("RestaurantIQ — Data Uploader")

uploaded_files = st.file_uploader(
    "Upload CSV or Excel files",
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=True
)

if uploaded_files:
    try:
        combined = combine_files(uploaded_files)

        st.subheader("Combined Data Preview")
        st.write(
            f"Rows: {len(combined):,} | "
            f"Columns: {len(combined.columns)}"
        )
        st.dataframe(combined.head(10), use_container_width=True)

        prepared, errors = validate_and_prepare(combined)

        if errors:
            st.error("Validation failed:")
            for error in errors:
                st.write(f"- {error}")
        else:
            st.success(
                f"Validation passed: {len(prepared):,} unique orders."
            )

            if st.button("Upload to Neon", type="primary"):
                existing_ids = get_existing_order_ids(
                    prepared["order_id"].astype(str).tolist()
                )

                new_data = prepared[
                    ~prepared["order_id"].astype(str).isin(existing_ids)
                ].copy()

                if new_data.empty:
                    st.info("No new orders to upload.")
                else:
                    count = upload_rows(new_data)
                    st.success(f"Uploaded {count:,} new rows.")

                st.metric("Total rows in Neon", f"{get_row_count():,}")

    except Exception as error:
        st.error(f"Processing failed: {error}")
