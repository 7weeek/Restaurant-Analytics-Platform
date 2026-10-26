```python
import streamlit as st
import pandas as pd

from processor import combine_files, validate_and_prepare
from database import get_existing_order_ids, upload_rows, get_row_count

st.set_page_config(
    page_title="RestaurantIQ | Data Ingestion",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    .hero {
        padding: 1.7rem;
        border-radius: 16px;
        background: linear-gradient(120deg, #142d4e, #246b75);
        color: white;
        margin-bottom: 1.5rem;
    }
    .hero h1 {
        color: white;
        margin-bottom: .35rem;
        font-size: 2rem;
    }
    .hero p {
        color: #e2edf2;
        margin-bottom: 0;
    }
    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,.25);
        padding: 1rem;
        border-radius: 12px;
    }
    div[data-testid="stFileUploader"] {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("RestaurantIQ")
    st.caption("Restaurant analytics data pipeline")
    st.divider()
    st.markdown("### Workflow")
    st.markdown(
        "1. Upload files\n\n"
        "2. Validate data\n\n"
        "3. Review records\n\n"
        "4. Upload to PostgreSQL\n\n"
        "5. Refresh Power BI"
    )
    st.divider()
    st.caption("Database credentials are managed separately using environment secrets.")

st.markdown("""
<div class="hero">
    <h1>Data Ingestion Center</h1>
    <p>Prepare, validate and load restaurant order data into Neon PostgreSQL.</p>
</div>
""", unsafe_allow_html=True)

# Database status
try:
    database_count = get_row_count()
    db_connected = True
except Exception:
    database_count = None
    db_connected = False

m1, m2, m3 = st.columns(3)
m1.metric("Database records", f"{database_count:,}" if db_connected else "Unavailable")
m2.metric("Accepted file types", "CSV / Excel")
m3.metric("Database", "Connected" if db_connected else "Connection issue")

st.divider()

st.subheader("1. Upload data")
st.write("Upload one or more files with the expected restaurant analytics columns.")

uploaded_files = st.file_uploader(
    "Select CSV or Excel files",
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=True,
)

if uploaded_files:
    st.markdown("#### Selected files")

    file_rows = [
        {
            "Filename": file.name,
            "Size (KB)": round(file.size / 1024, 1),
            "Format": file.name.rsplit(".", 1)[-1].upper(),
        }
        for file in uploaded_files
    ]
    st.dataframe(
        pd.DataFrame(file_rows),
        use_container_width=True,
        hide_index=True,
    )

    try:
        combined = combine_files(uploaded_files)

        st.subheader("2. Combined dataset")
        c1, c2, c3 = st.columns(3)
        c1.metric("Input rows", f"{len(combined):,}")
        c2.metric("Columns detected", len(combined.columns))
        c3.metric("Files processed", len(uploaded_files))

        with st.expander("Preview uploaded data", expanded=True):
            st.dataframe(combined.head(20), use_container_width=True)

        prepared, errors = validate_and_prepare(combined)

        st.subheader("3. Validation")

        if errors:
            st.error("Validation failed. Correct the following issues before uploading.")
            for error in errors:
                st.markdown(f"- {error}")
        else:
            st.success(
                f"Validation passed. {len(prepared):,} unique order IDs are ready."
            )

            with st.expander("Review cleaned data"):
                st.dataframe(prepared.head(20), use_container_width=True)

            st.subheader("4. Load into Neon")

            if not db_connected:
                st.warning(
                    "The database is currently unreachable. Check your connection "
                    "and try again."
                )

            confirm = st.checkbox(
                "I have reviewed the data and want to insert new records."
            )

            if st.button(
                "Upload validated records",
                type="primary",
                use_container_width=True,
                disabled=not confirm or not db_connected,
            ):
                try:
                    progress = st.progress(0, text="Checking existing order IDs...")

                    ids = prepared["order_id"].astype(str).tolist()
                    existing_ids = get_existing_order_ids(ids)

                    new_data = prepared[
                        ~prepared["order_id"].astype(str).isin(existing_ids)
                    ].copy()

                    skipped = len(prepared) - len(new_data)

                    progress.progress(50, text="Uploading new records...")

                    if new_data.empty:
                        progress.progress(100, text="Complete")
                        st.info("No new records found. All order IDs already exist.")
                    else:
                        inserted = upload_rows(new_data)
                        progress.progress(100, text="Upload complete")

                        st.success(f"Successfully inserted {inserted:,} new records.")

                    r1, r2 = st.columns(2)
                    r1.metric("New records inserted", f"{len(new_data):,}")
                    r2.metric("Existing IDs skipped", f"{skipped:,}")

                    st.metric("Updated database row count", f"{get_row_count():,}")

                    st.info(
                        "Your Power BI report uses Import mode. Open Power BI Desktop "
                        "and select Home → Refresh to retrieve the latest records."
                    )

                except Exception as error:
                    st.error("Upload failed. No success is assumed; inspect the error below.")
                    st.exception(error)

    except Exception as error:
        st.error(f"Could not process the uploaded files: {error}")

else:
    st.info("Upload a CSV or Excel file to begin.")

st.divider()
st.caption("RestaurantIQ · Data ingestion and analytics")
```
