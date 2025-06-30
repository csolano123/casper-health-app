import streamlit as st
import pandas as pd
import io
from openpyxl import load_workbook
import sqlite3



# Load the Excel file
EXCEL_FILE = 'Casper Data.xlsx'  # Make sure this file is in the same folder

# Read Excel
#OLD: xl = pd.ExcelFile(EXCEL_FILE)

# Connect to the database
conn = sqlite3.connect('casper.db')
c = conn.cursor()

# Fetch medication records
med_df = pd.read_sql_query("SELECT * FROM medication", conn)

# Fetch urination records
urination_df = pd.read_sql_query("SELECT * FROM urination", conn)

# Set up page layout and sidebar
st.set_page_config(page_title="Casper's Site", layout="centered")
st.title("🐾 Welcome to Casper's Site!")

# Sidebar navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Home", "📘 About Me", "📷 Photos", "💊 Casper's Health", "🧪 Ingredients"])

# ---------------- Home Page ----------------
with tab1:
    st.image("casper.jpg", caption="Casper, the king of the house", use_container_width=True)
    st.header("Welcome to Casper's Site!")
    st.markdown("""
            This is **Casper’s website**!
            From here you can:
            - Learn more **About Me**
            - View cute **Photos**
            - Track my **Health**

            
        """)

# ---------------- About Me ----------------
with tab2:
    st.header("About Casper")
    st.markdown("""
        I'm Casper, a gentle and dramatic kitty recovering from a urinary blockage.  
        I love snuggling, knocking over water cups, and hunting flies indoors.  

        **Age:** 2 years  
        **Favorite toy:** Crinkle tunnel  
        **Special skill:** Sits in litter box even when he's not peeing.  
    """)

# ---------------- Photos ----------------
with tab3:
    st.header("📸 Casper’s Photo Album")
    st.markdown("Coming soon! You'll be able to upload or view cute photos here.")

# ---------------- Health Dashboard ----------------
with tab4:
    st.header("💊 Casper’s Health Dashboard")

    # --- Medication Log ---
    st.subheader("Medication Log")
    st.dataframe(med_df)

    st.markdown("### ➕ Add a New Medication Entry")
    with st.form("add_medication_form"):
        med_name = st.text_input("Medication Name")
        med_date = st.date_input("Date", key="med_date")
        med_time = st.time_input("Time", key="med_time")
        med_dose = st.number_input("Dose (e.g., 0.25)", step=0.01)
        med_units = st.selectbox("Units", ["mL", "mg", "tablets", "other"])
        med_submit = st.form_submit_button("Add Medication Entry")

    if med_submit:
        c.execute(
            "INSERT INTO medication (medication, date, time, dose, units) VALUES (?, ?, ?, ?, ?)",
            (med_name, str(med_date), med_time.strftime("%H:%M:%S"), med_dose, med_units)
        )
        conn.commit()
        st.success("New medication entry added!")
        med_df = pd.read_sql_query("SELECT * FROM medication", conn)
        st.dataframe(med_df)

    # --- Urination Log ---
    st.subheader("Urination Log")
    st.dataframe(urination_df)

    st.markdown("### ➕ Add a New Urination Log Entry")
    with st.form("add_urination_form"):
        uri_date = st.date_input("Date", key="uri_date")
        uri_time = st.time_input("Time", key="uri_time")
        uri_size = st.selectbox("Size", ["Small", "Normal", "Large"])
        uri_location = st.selectbox("Location", ["House", "Vet", "Other"])
        uri_submit = st.form_submit_button("Add Urination Entry")

    if uri_submit:
        c.execute(
            "INSERT INTO urination (date, time, size, location) VALUES (?, ?, ?, ?)",
            (str(uri_date), uri_time.strftime("%H:%M:%S"), uri_size, uri_location)
        )
        conn.commit()
        st.success("New urination entry added!")
        urination_df = pd.read_sql_query("SELECT * FROM urination", conn)
        st.dataframe(urination_df)

# ---------------- Ingredients Dashboard ----------------
with tab5:
    col_icon, col_title = st.columns([0.08, 1])  # Adjust widths as needed

    with col_icon:
        st.image("Checklist_icon.png", width=50)  # Make sure this image exists in your project folder

    with col_title:
        st.subheader("Ingredients Management")
    st.markdown("### What would you like to do?")

    col1, col2, col3 = st.columns(3)

    with col1:
        upload_click = st.button("📄 Upload from Excel", use_container_width=True)
    with col2:
        manual_click = st.button("✍️ Enter Manually", use_container_width=True)
    with col3:
        view_click = st.button("📋 View All Ingredients", use_container_width=True)

    if upload_click:
        option = "upload"
    elif manual_click:
        option = "manual"
    elif view_click:
        option = "view"
    else:
        option = None

    if option == "upload":
        st.markdown("## 📄 Upload from Excel")

        sample_df = pd.DataFrame({
            "medication": ["ExampleMed"],
            "ingredient": ["ExampleIngredient"],
            "chemical_class": ["Alkaloid"],
            "large_availability": ["Yes"]
        })
        buffer = io.BytesIO()
        sample_df.to_excel(buffer, index=False)
        buffer.seek(0)
        st.download_button(
            label="📅 Download Excel Template",
            data=buffer,
            file_name="ingredients_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
        if uploaded_file:
            try:
                df_uploaded = pd.read_excel(uploaded_file)
                required_columns = {'medication', 'ingredient', 'chemical_class', 'large_availability'}
                if not required_columns.issubset(df_uploaded.columns):
                    st.error(f"❌ Excel must contain: {', '.join(required_columns)}")
                else:
                    for _, row in df_uploaded.iterrows():
                        c.execute(
                            "INSERT INTO ingredients (medication, ingredient, chemical_class, large_availability) VALUES (?, ?, ?, ?)",
                            (
                                row['medication'],
                                row['ingredient'],
                                row['chemical_class'],
                                row['large_availability']
                            )
                        )
                    conn.commit()
                    st.success("✅ Ingredients imported successfully!")

            except Exception as e:
                st.error(f"🚨 Error processing file: {e}")

    elif option == "manual":
        st.markdown("## ✍️ Enter Ingredient Manually")

        with st.form("manual_ingredient_form"):
            med_name = st.text_input("Medication Name")
            ingredient_name = st.text_input("Ingredient")
            chemical_class = st.text_input("Chemical Class")
            availability = st.radio("Large Availability?", ["Yes", "No"])
            submit_ing = st.form_submit_button("Add Ingredient")

        if submit_ing:
            c.execute(
                "INSERT INTO ingredients (medication, ingredient, chemical_class, large_availability) VALUES (?, ?, ?, ?)",
                (med_name, ingredient_name, chemical_class, availability)
            )
            conn.commit()
            st.success("✅ Ingredient added!")

    elif option == "view":
        st.markdown("## 📋 All Ingredients")
        ingredients_df = pd.read_sql_query("SELECT * FROM ingredients", conn)
        st.dataframe(ingredients_df)

        st.markdown("---")
        st.subheader("🚩 Delete an Ingredient")

        if not ingredients_df.empty:
            ingredients_df['label'] = ingredients_df.apply(
                lambda row: f"{row['ingredient']} (from {row['medication']})", axis=1
            )
            to_delete = st.selectbox("Select ingredient to delete", ingredients_df['label'])
            if st.button("Delete Selected Ingredient"):
                selected_id = ingredients_df.loc[ingredients_df['label'] == to_delete, 'id'].values[0]
                c.execute("DELETE FROM ingredients WHERE id = ?", (selected_id,))
                conn.commit()
                st.success("✅ Ingredient deleted!")
                st.rerun()
        else:
            st.info("No ingredients available to delete.")

# Close DB connection after page logic finishes
conn.close()
