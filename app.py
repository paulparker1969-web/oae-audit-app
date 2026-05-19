import streamlit as st
import pandas as pd
from datetime import datetime
import openpyxl
from openpyxl.drawing.image import Image as OpenpyxlImage
from io import BytesIO
import PIL.Image

st.set_page_config(page_title="OAE Master Audit Pro", layout="centered")

st.title("🌊 OAE Salt Pan Master Audit Pro")
st.markdown("### Captures Primary Site Data & Regional Annex Framework")

# Site Metadata Header
with st.expander("📍 Site Identity & Metadata", expanded=True):
    site_id = st.text_input("Site ID (e.g., RGN-Mossoro-01)", "RGN-01")
    evaluator = st.text_input("Evaluator Name")
    lat_lon = st.text_input("GPS Coordinates (Lat, Lon)", placeholder="-5.1234, -36.5678")
    st.caption(f"Audit Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- DATA STRUCTURE DEFINITIONS ---

# 1. Primary Site Checklist Items (From your CSV)
site_checklist = [
    {"Arena": "Viability", "Item": "Site Infrastructure & Condition", "IDs": "26, 56", "Q": "Are existing dikes, sluice gates, and tidal channels structurally sound for Phase 4 flow rates (~600–800 m3/day), or is capital required for refurbishment?"},
    {"Arena": "Viability", "Item": "Bathymetry & Mixing", "IDs": "22, 52, 28, 58", "Q": "Is the water depth at the specific outfall point at least 2–3 m below the lowest tide to ensure rapid dilution of alkaline effluent?"},
    {"Arena": "Viability", "Item": "Energy & Utility Footprint", "IDs": "25, 55", "Q": "Is there a secure, high-ground (flood-safe) area of ~500 m2 for a 15–25 kWp solar array and mineral processing?"},
    {"Arena": "Viability", "Item": "Raw Materials Logistics", "IDs": "29, 59", "Q": "Does the site have heavy-vehicle road access for 20 t bitterns tankers and limestone delivery without impacting local traffic?"},
    {"Arena": "Viability", "Item": "MRV Security", "IDs": "0, 1", "Q": "Are there safe, non-turbulent points for 'Blue Box' sensor installation at the intake and discharge that are protected from theft/vandalism?"},
    {"Arena": "Viability", "Item": "Embodied Carbon (Local)", "IDs": "48", "Q": "Is the onsite transport distance between mineral stockpiles and injection points minimized to prevent carbon credit erosion?"},
    {"Arena": "Stability", "Item": "Site Tenure & Duration", "IDs": "37, 67", "Q": "Is a long-term horizon (20–99 years) legally available via direct ownership or lease to match CDR durability requirements?"},
    {"Arena": "Stability", "Item": "Cluster Scaling Potential", "IDs": "46", "Q": "Are adjacent pans owned by the same entity, and is there a 'right of first refusal' to expand the pilot from 5 ha to 50+ ha?"},
    {"Arena": "Stability", "Item": "Commercial Partner Alignment", "IDs": "39", "Q": "Is the owner/operator aligned with a 'staged introduction' of bitterns that may limit initial salt production?"},
    {"Arena": "Stability", "Item": "Exit & Failure Strategy", "IDs": "18", "Q": "Are there clear termination clauses if Phase 2 chemistry trials fail to meet pH recovery KPIs?"},
    {"Arena": "Governance", "Item": "Specific Land Zoning", "IDs": "12, 16", "Q": "Is the plot specifically zoned for 'Industrial' or 'Mariculture' use, and does it sit outside of protected mangrove exclusion zones?"},
    {"Arena": "Governance", "Item": "Additionality Proof", "IDs": "44", "Q": "Does the site have a 4-week baseline history proving it does not naturally produce the required alkalinity flux?"},
    {"Arena": "Governance", "Item": "Alignment with Portfolio", "IDs": "19", "Q": "Does the site's hydraulic profile allow for the 'Appropriate-Tech' direct injection design without requiring reactor builds?"},
    {"Arena": "Credibility", "Item": "Marine Baseline Access", "IDs": "20, 21, 4, 5", "Q": "Can we secure immediate access for seasonal seawater TA/DIC/pH variability surveys?"},
    {"Arena": "Credibility", "Item": "Plume Sensitivity", "IDs": "20, 4", "Q": "Are there specific coral patches or sensitive aquaculture zones within 1 km of the discharge point?"},
    {"Arena": "Credibility", "Item": "Community Partnership (Local)", "IDs": "2, 6, 70", "Q": "Is the site near enough to the AMBAP or Rio do Fogo cooperatives to leverage their existing macroalgae expertise?"}
]

# 2. Regional Annex Items (From your CSV)
regional_checklist = [
    {"Category": "Regional Viability", "Arena": "Viability", "Item": "Raw Material Availability", "IDs": "29, 59", "Q": "Verify general regional proximity to Jandaíra limestone quarries and Mossoró saltworks."},
    {"Category": "Regional Viability", "Arena": "Viability", "Item": "Acid Feedstock Volumes", "IDs": "29", "Q": "Verify regional volume capacity of cashew apple waste and sugarcane vinasse streams."},
    {"Category": "Regional Viability", "Arena": "Viability", "Item": "Neighborhood Suitability", "IDs": "23, 53", "Q": "Verify overall regional alignment with industrial/agricultural OAE operations."},
    {"Category": "Regional Stability", "Arena": "Stability", "Item": "Local Buyer Presence", "IDs": "45", "Q": "Assess regional market presence for long-term credit offtake and corporate buyers."},
    {"Category": "Regional Stability", "Arena": "Stability", "Item": "Climate Risk Assessment", "IDs": "24, 54", "Q": "Review regional projections for extreme rainfall, sea-level rise, or storm surges."},
    {"Category": "Regional Stability", "Arena": "Stability", "Item": "Permit Risk Trends", "IDs": "36, 66", "Q": "Track broader regulatory attitudes or regional legal precedents concerning marine outfalls."},
    {"Category": "Regional Governance", "Arena": "Governance", "Item": "Incentive Programs", "IDs": "9, 13", "Q": "Identify state-level tax exemptions, federal labor loading benefits, or carbon incentives."},
    {"Category": "Regional Governance", "Arena": "Governance", "Item": "Cultural Suitability", "IDs": "10, 14", "Q": "Assess institutional ease-of-access and baseline operational acceptance in NE Brazil."},
    {"Category": "Regional Governance", "Arena": "Governance", "Item": "Integrity", "IDs": "11, 15", "Q": "Review transparency indexes and regulatory governance security for the state/municipality."},
    {"Category": "Regional Credibility", "Arena": "Credibility", "Item": "Strategic Leadership", "IDs": "8", "Q": "Evaluate potential for RGN variant to spearhead global tropical OAE methodology frameworks."},
    {"Category": "Regional Credibility", "Arena": "Credibility", "Item": "Commercial Partnerships", "IDs": "2, 6", "Q": "Assess broad regional framework agreements with raw feedstock and industrial partners."},
    {"Category": "Regional Credibility", "Arena": "Credibility", "Item": "Macroalgae Species", "IDs": "", "Q": "Confirm warm-water optimization metrics for local Hypnea or Kappaphycus arrays."}
]

# --- RENDER WEB APP INTERFACE ---

app_tab1, app_tab2 = st.tabs(["📋 Site Evaluation (Priority)", "🌍 Regional Annex (Context)"])

# Render Sheet 1: Site Evaluation
site_rows = []
with app_tab1:
    st.info("💡 Tap the mic icon on your phone keyboard to dictate observations directly.")
    for entry in site_checklist:
        st.markdown(f"**{entry['Arena']} — {entry['Item']}** (IDs: {entry['IDs']})")
        st.write(f"*{entry['Q']}*")
        
        status = st.selectbox("Status", ["To Be Done", "Pass", "Fail", "In Progress"], key=f"site_stat_{entry['IDs']}")
        obs = st.text_area("Observations", placeholder="Dictate or type notes...", key=f"site_obs_{entry['IDs']}")
        photo = st.file_uploader("Capture Photo Proof", type=['jpg', 'jpeg', 'png'], key=f"site_img_{entry['IDs']}")
        
        site_rows.append({"Meta": entry, "Status": status, "Obs": obs, "Photo": photo})
        st.divider()

# Render Sheet 2: Regional Annex
regional_rows = []
with app_tab2:
    st.caption("These higher-level framework metrics can be updated via local authority or desktop validation.")
    for entry in regional_checklist:
        key_id = f"{entry['Category']}_{entry['Item']}".replace(" ", "_")
        st.markdown(f"**{entry['Category']} | {entry['Item']}** (IDs: {entry['IDs']})")
        st.write(f"*{entry['Q']}*")
        
        status = st.selectbox("Regional Context / Status", ["Pending", "Confirmed", "Risk Identified", "N/A"], key=f"reg_stat_{key_id}")
        obs = st.text_area("Contextual Notes", placeholder="Add regional data points...", key=f"reg_obs_{key_id}")
        
        regional_rows.append({"Meta": entry, "Status": status, "Obs": obs})
        st.divider()

# --- MULTI-SHEET EXCEL EXPORT LOGIC ---

st.markdown("### 📥 Save Audit Progress")
if st.button("🚀 Export Comprehensive Multi-Sheet Excel"):
    wb = openpyxl.Workbook()
    
    # Setup Tab 1: Site Evaluation Sheet
    ws1 = wb.active
    ws1.title = "Site Evaluation"
    ws1.append(["Arena", "Checklist Item", "Evaluation Question / Task", "Site Observations / Answer", "Status", "GNG Import Order ID(s)", "Photo Evidence", "Site ID", "GPS Location"])
    
    for idx, row in enumerate(site_rows, start=2):
        ws1.append([
            row["Meta"]["Arena"], row["Meta"]["Item"], row["Meta"]["Q"],
            row["Obs"], row["Status"], row["Meta"]["IDs"], "", site_id, lat_lon
        ])
        
        # Inline photo rendering logic if an image was captured
        if row["Photo"] is not None:
            pil_img = PIL.Image.open(BytesIO(row["Photo"].read()))
            pil_img.thumbnail((140, 140))
            img_bytecode = BytesIO()
            pil_img.save(img_bytecode, format="PNG")
            img_bytecode.seek(0)
            
            xl_img = OpenpyxlImage(img_bytecode)
            ws1.row_dimensions[idx].height = 110
            ws1.add_image(xl_img, f"G{idx}")
            
    # Setup Tab 2: Regional Annex Sheet
    ws2 = wb.create_sheet(title="Regional Annex")
    ws2.append(["Category", "Arena", "Item", "GNG Import Order ID(s)", "Regional Context / Status", "Original GNG Context"])
    
    for row in regional_rows:
        ws2.append([
            row["Meta"]["Category"], row["Meta"]["Arena"], row["Meta"]["Item"],
            row["Meta"]["IDs"], row["Obs"], row["Status"]
        ])
        
    # Compile sheets directly into mobile downloads folder
    output = BytesIO()
    wb.save(output)
    processed_data = output.getvalue()
    
    st.download_button(
        label="📥 Download Structured Excel (.xlsx)",
        data=processed_data,
        file_name=f"OAE_Master_Audit_{site_id}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.success("App has compiled a dual-tab spreadsheet file containing all site specifics, regional summaries, and photo buffers.")
