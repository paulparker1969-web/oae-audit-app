import streamlit as st
import pandas as pd
from datetime import datetime

# Set Page Configuration for Mobile
st.set_page_config(page_title="OAE Master Site Audit", layout="centered")

st.title("🌊 OAE Salt Pan Master Audit")
st.markdown("### Brazil (RGN) & Global Site Evaluation")

# 1. Site Metadata & GPS Header
with st.expander("📍 Site Identity & Metadata", expanded=True):
    site_id = st.text_input("Site ID (e.g. RGN-Mossoro-01)", "RGN-01")
    evaluator = st.text_input("Evaluator Name")
    lat_lon = st.text_input("GPS Coordinates (Lat, Lon)", placeholder="-5.1234, -36.5678")
    st.caption(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 2. Main Site Evaluation (From your Checklist)
st.header("📋 Primary Site Evaluation")
st.info("Directly mapped to GNG Database via Import IDs.")

# Data structure based on your uploaded CSV
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

audit_results = []

for entry in site_checklist:
    with st.container():
        st.markdown(f"**{entry['Arena']} | {entry['Item']}** (IDs: {entry['IDs']})")
        st.write(f"*{entry['Q']}*")
        
        # User Inputs
        status = st.selectbox("Status", ["To Be Done", "Pass", "Fail", "In Progress", "N/A"], key=f"stat_{entry['IDs']}")
        observations = st.text_area("Site Observations (Dictate here)", placeholder="Tap mic to speak notes...", key=f"obs_{entry['IDs']}")
        photo = st.file_uploader("Capture/Attach Photo", type=['jpg', 'jpeg', 'png'], key=f"img_{entry['IDs']}")
        
        audit_results.append({
            "GNG ID(s)": entry['IDs'],
            "Item": entry['Item'],
            "Status": status,
            "Observations": observations,
            "Site": site_id,
            "Evaluator": evaluator,
            "GPS": lat_lon
        })
        st.divider()

# 3. Regional Annex (Secondary Check)
with st.expander("🌍 Regional Annex Checklist"):
    st.write("Regional context items from GNG database.")
    # You can populate this similar to above if you need to evaluate regional data onsite.
    st.caption("Common regional identifiers included in export: 29, 59, 23, 53, 45, 24, 54, 36, 66, 9, 13, 10, 14, 11, 15, 8")

# 4. Finalize & Export
if st.button("🚀 Finalize & Export Site Audit"):
    df_final = pd.DataFrame(audit_results)
    csv = df_final.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Audit Results (CSV)",
        data=csv,
        file_name=f"OAE_Audit_{site_id}.csv",
        mime='text/csv'
    )
    st.success("Audit complete. Data ready for GNG Database integration.")
