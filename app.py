import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Fußball KI-Kamera – 4P Financial Evaluator",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ KI-Taktik-Kamera: 4P-basiertes Finanzevaluations-Tool")
st.markdown("""
Dieses Tool simuliert die kaufmännischen Kennzahlen (Umsatz, Deckungsbeitrag, EBIT, Break-Even, Margen) 
eines Geschäftsjahres für das **KI-Kamera-System (VEO-Konkurrent)** auf Basis von **17 Steuerungsvariablen** des Marketing-Mix.
""")

st.sidebar.header("🕹️ Marketing-Mix Steuerung (17 Variablen)")

# ---------------------------------------------------------
# 1. PRODUCT (3 Variablen)
# ---------------------------------------------------------
st.sidebar.subheader("1. Product (Produktpolitik)")

hw_variant = st.sidebar.selectbox(
    "1. Hardware-Ausstattung",
    options=["Standard (1080p)", "Pro (4K Single Lens)", "Ultra (4K Dual Lens + IP67)"],
    index=1,
    help="Bestimmt die variablen Einkaufskosten pro Kamera (COGS)."
)

sw_variant = st.sidebar.selectbox(
    "2. KI-Software-Funktionsumfang",
    options=["Basis-KI (Taktik-Highlights & Heatmaps)", "Deep-Taktik-KI (Gegneranalyse & KI-Trainings-Generator)"],
    index=1,
    help="Bestimmt die monatlichen Cloud- & Serverkosten pro verarbeitetem Team."
)

garantie_monate = st.sidebar.slider(
    "3. Hardware-Garantiedauer (Monate)",
    min_value=12, max_value=36, value=24, step=12,
    help="Höhere Garantiedauer erzeugt kalkulatorische Garantierückstellungen pro Kamera."
)

# ---------------------------------------------------------
# 2. PRICE (4 Variablen)
# ---------------------------------------------------------
st.sidebar.subheader("2. Price (Preispolitik)")

erloesmodelle = st.sidebar.multiselect(
    "Erlösmodell(e) aktivieren",
    options=["Modell A: HW-Kauf + SW-Abo", "Modell B: All-in-One Abo"],
    default=["Modell A: HW-Kauf + SW-Abo", "Modell B: All-in-One Abo"],
    help="Mindestens ein Erlösmodell muss gewählt werden."
)

if not erloesmodelle:
    st.sidebar.warning("Bitte mindestens ein Erlösmodell auswählen!")
    erloesmodelle = ["Modell A: HW-Kauf + SW-Abo"]

preis_hw = st.sidebar.number_input(
    "4. Verkaufspreis Hardware (€ Einmalkauf)",
    min_value=200, max_value=2500, value=850, step=50
)

preis_sw_abo = st.sidebar.number_input(
    "5. Monatlicher Abopreis Software (€/Monat - Modell A)",
    min_value=10, max_value=200, value=45, step=5
)

preis_all_in_one = st.sidebar.number_input(
    "6. All-in-One Monatspreis HW+SW (€/Monat - Modell B)",
    min_value=30, max_value=300, value=79, step=5
)

rabatt_pct = st.sidebar.slider(
    "7. Saison- & Vereinsrabatt (%)",
    min_value=0, max_value=25, value=10, step=1
)

# ---------------------------------------------------------
# 3. PLACE (2 Variablen)
# ---------------------------------------------------------
st.sidebar.subheader("3. Place (Distributionspolitik)")

d2c_share_pct = st.sidebar.slider(
    "8. Vertriebskanal: % D2C Online-Shop (Rest = Fachhandel)",
    min_value=0, max_value=100, value=70, step=5,
    help="D2C bringt 100% Marge. Fachhandel erhält 30% Händlermarge."
)

sales_ma_count = st.sidebar.number_input(
    "9. Vertriebsaußendienst (Anzahl Sales-MA)",
    min_value=0, max_value=20, value=3, step=1
)

# ---------------------------------------------------------
# 4. PROMOTION (5 Variablen)
# ---------------------------------------------------------
st.sidebar.subheader("4. Promotion (Kommunikation)")

budget_social_ads = st.sidebar.number_input(
    "10. Social Media & Performance Ads (€/Jahr)",
    min_value=0, max_value=200000, value=40000, step=5000
)

budget_verbands_sponsoring = st.sidebar.number_input(
    "11. Verbandskooperationen & Sponsoring (€/Jahr)",
    min_value=0, max_value=150000, value=25000, step=5000
)

testmonate_tage = st.sidebar.radio(
    "12. Gratis-Testphase für Neukunden",
    options=[0, 30, 60],
    format_func=lambda x: f"{x} Tage Gratis",
    index=1
)

budget_botschafter = st.sidebar.number_input(
    "13. Trainer- & Testimonial-Botschafter (€/Jahr)",
    min_value=0, max_value=100000, value=15000, step=2500
)

budget_messen = st.sidebar.number_input(
    "14. Messe- & Turnier-Präsenzbudget (€/Jahr)",
    min_value=0, max_value=80000, value=10000, step=2500
)

# ---------------------------------------------------------
# 5. OPERATIONS & STRUCTURE (3 Variablen)
# ---------------------------------------------------------
st.sidebar.subheader("5. Operations & Struktur")

budget_fe = st.sidebar.number_input(
    "15. F&E-Budget für KI-Training & Daten (€/Jahr)",
    min_value=10000, max_value=300000, value=60000, step=10000
)

dev_eu_count = st.sidebar.number_input("16a. Software-Entwickler Europa (Anzahl)", min_value=0, max_value=15, value=2)
dev_asia_count = st.sidebar.number_input("16b. Software-Entwickler Asien (Anzahl)", min_value=0, max_value=20, value=3)

churn_rate_pct = st.sidebar.slider(
    "17. Jährliche Software-Kündigungsquote / Churn (%)",
    min_value=2, max_value=30, value=10, step=1
)

# Baseline Volume Drivers
st.sidebar.subheader("📊 Marktdynamik / Absatzmenge")
neukunden_jahr = st.sidebar.number_input("Neukunden / Verkaufte Einheiten im Jahr", min_value=50, max_value=10000, value=800, step=50)
bestandskunden_start = st.sidebar.number_input("Bestandskunden Vorjahr (Aktive Abos)", min_value=0, max_value=20000, value=500, step=50)

# =========================================================
# CALCULATIONS LOGIC
# =========================================================

# Cost per Unit (COGS) based on HW Variant
cogs_dict = {"Standard (1080p)": 280, "Pro (4K Single Lens)": 420, "Ultra (4K Dual Lens + IP67)": 620}
cogs_hw = cogs_dict[hw_variant]

# Cloud Server Cost per team per month based on SW Variant
cloud_cost_dict = {"Basis-KI (Taktik-Highlights & Heatmaps)": 3.50, "Deep-Taktik-KI (Gegneranalyse & KI-Trainings-Generator)": 7.50}
cloud_cost_sw_monat = cloud_cost_dict[sw_variant]

# Warranty reserve
garantie_ruestung_pro_stk = (garantie_monate / 12) * 15.0

# Split units between Erlösmodell A and B
if "Modell A: HW-Kauf + SW-Abo" in erloesmodelle and "Modell B: All-in-One Abo" in erloesmodelle:
    units_a = neukunden_jahr * 0.6
    units_b = neukunden_jahr * 0.4
elif "Modell A: HW-Kauf + SW-Abo" in erloesmodelle:
    units_a = neukunden_jahr
    units_b = 0
else:
    units_a = 0
    units_b = neukunden_jahr

# Effective Hardware Price considering Discount and Retailer Margin
eff_rabatt = (1 - (rabatt_pct / 100.0))
retailer_margin_factor = (d2c_share_pct / 100.0) * 1.0 + ((100 - d2c_share_pct) / 100.0) * 0.70

eff_hw_preis_a = preis_hw * eff_rabatt * retailer_margin_factor

# Revenue Calculations
# HW Revenue (only Model A selling hardware)
umsatz_hw = units_a * eff_hw_preis_a

# SW Revenue Calculations
# Free trial adjustment factor
free_trial_factor = (12.0 - (testmonate_tage / 30.0)) / 12.0

# Active Subscriptions Calculation
active_sw_abos_a = (bestandskunden_start * (1 - churn_rate_pct/100.0) * 0.6) + units_a
active_sw_abos_b = (bestandskunden_start * (1 - churn_rate_pct/100.0) * 0.4) + units_b

umsatz_sw_a = active_sw_abos_a * (preis_sw_abo * eff_rabatt) * 12.0 * free_trial_factor
umsatz_sw_b = active_sw_abos_b * (preis_all_in_one * eff_rabatt) * 12.0 * free_trial_factor

umsatz_gesamt = umsatz_hw + umsatz_sw_a + umsatz_sw_b

# Variable Costs (COGS & Operations)
var_kosten_hw = neukunden_jahr * (cogs_hw + garantie_ruestung_pro_stk + 25.0) # 25€ shipping/packaging
var_kosten_sw = (active_sw_abos_a + active_sw_abos_b) * cloud_cost_sw_monat * 12.0

var_kosten_gesamt = var_kosten_hw + var_kosten_sw

# Contribution Margin (Deckungsbeitrag)
deckungsbeitrag_gesamt = umsatz_gesamt - var_kosten_gesamt
db_marge_pct = (deckungsbeitrag_gesamt / umsatz_gesamt * 100.0) if umsatz_gesamt > 0 else 0

# Fixed Costs (OPEX)
# Personnel Costs
gehalt_sales_eu = 65000.0
gehalt_dev_eu = 80000.0
gehalt_dev_asia = 30000.0
gehalt_admin_mgt = 120000.0 # Fixed management overhead

personalkosten = (sales_ma_count * gehalt_sales_eu) + (dev_eu_count * gehalt_dev_eu) + (dev_asia_count * gehalt_dev_asia) + gehalt_admin_mgt

# Marketing Expenses
marketing_total = budget_social_ads + budget_verbands_sponsoring + budget_botschafter + budget_messen

# Fixed Expenses Total
fixkosten_gesamt = personalkosten + budget_fe + marketing_total + 45000.0 # 45k admin/office/legal

# EBIT Calculation
ebit = deckungsbeitrag_gesamt - fixkosten_gesamt
ebit_marge_pct = (ebit / umsatz_gesamt * 100.0) if umsatz_gesamt > 0 else 0

# Break-Even Point (In New Units)
db_pro_stk_a = eff_hw_preis_a - (cogs_hw + garantie_ruestung_pro_stk + 25.0) + ((preis_sw_abo * eff_rabatt * 12 * free_trial_factor) - (cloud_cost_sw_monat * 12))
db_pro_stk_b = (preis_all_in_one * eff_rabatt * 12 * free_trial_factor) - (cogs_hw + garantie_ruestung_pro_stk + 25.0 + cloud_cost_sw_monat * 12)

db_mitteleinheit = (db_pro_stk_a + db_pro_stk_b) / 2.0
break_even_units = int(np.ceil(fixkosten_gesamt / db_mitteleinheit)) if db_mitteleinheit > 0 else 0

# =========================================================
# DASHBOARD OUTPUT (KPIs & VISUALS)
# =========================================================

col1, col2, col3, col4 = st.columns(4)
col1.metric("Gesamtumsatz (€)", f"{umsatz_gesamt:,.0f} €")
col2.metric("Deckungsbeitrag (€)", f"{deckungsbeitrag_gesamt:,.0f} €", delta=f"{db_marge_pct:.1f}% Marge")
col3.metric("EBIT (€)", f"{ebit:,.0f} €", delta=f"{ebit_marge_pct:.1f}% EBIT-Marge")
col4.metric("Break-Even-Punkt", f"{break_even_units:,} Einheiten", help="Nötige Neukunden/Verkäufe zur Fixkostendeckung")

st.markdown("---")

tab1, tab2, tab3 = st.subplots(["📊 Erlös & Kostenstruktur", "💡 4P-Hebelanalyse", "📋 Ausführliche P&L"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Umsatz-Splitting (Hardware vs. Recurring SaaS)")
        df_rev = pd.DataFrame({
            "Umsatzquelle": ["Hardware Verkauf (Modell A)", "Software Abo (Modell A)", "All-in-One Abo (Modell B)"],
            "Umsatz (€)": [umsatz_hw, umsatz_sw_a, umsatz_sw_b]
        })
        st.bar_chart(df_rev.set_index("Umsatzquelle"))
    
    with c2:
        st.subheader("Kostenaufschlüsselung (Fix vs. Variable Kosten)")
        df_cost = pd.DataFrame({
            "Kostenart": ["Var. HW-Kosten (COGS)", "Var. Cloud/IT-Kosten", "Personalkosten", "F&E-Budget", "Marketing-Budget", "Sonst. Admin/Fix"],
            "Betrag (€)": [var_kosten_hw, var_kosten_sw, personalkosten, budget_fe, marketing_total, 45000.0]
        })
        st.bar_chart(df_cost.set_index("Kostenart"))

with tab2:
    st.subheader("Stellschrauben-Analyse der 4Ps auf den EBIT")
    st.markdown(f"""
    * **Product-Hebel:** Hardware-Variante *{hw_variant}* erzeugt **{cogs_hw:.0f} € COGS/Stk.** | Cloud-Kosten: **{cloud_cost_sw_monat:.2f} €/Monat/Team**.
    * **Price-Hebel:** Nach Rabatt ({rabatt_pct}%) und Händlermarge beträgt der eff. Hardware-Nettoerlös **{eff_hw_preis_a:,.0f} €**.
    * **Place-Hebel:** Durch **{d2c_share_pct}% D2C-Anteil** verbleiben Höhermargen im eigenen Unternehmen. {sales_ma_count} Sales-MA verursachen **{sales_ma_count*gehalt_sales_eu:,.0f} €** Fixkosten.
    * **Promotion-Hebel:** Gesamtbudget für Kommunikation beträgt **{marketing_total:,.0f} €** ({testmonate_tage} Tage Gratis-Test verringert Jahresabo-Ertrag um {testmonate_tage/30:.0f} Monat(e)).
    * **Operations/Churn-Hebel:** Bei **{churn_rate_pct}% Churn** bleiben {(100-churn_rate_pct)}% der Bestandskunden im Folgejahr erhalten.
    """)

with tab3:
    st.subheader("Gewinn- und Verlustrechnung (GuV) im Detail")
    guv_data = {
        "Position": [
            "1. Hardware-Umsatz (Einmalkauf)",
            "2. Software-Umsatz (Abo Modell A)",
            "3. All-in-One Abo-Umsatz (Modell B)",
            "= Umsatzerlöse Gesamt",
            "4. - Variable Hardwarekosten (COGS + Versand + Garantie)",
            "5. - Variable Cloud- & IT-Kosten",
            "= DECKUNGSBEITRAG (DB)",
            "6. - Personalkosten (Sales, Dev, Admin)",
            "7. - F&E / KI-Entwicklungsbudget",
            "8. - Marketing- & Kommunikationsbudget",
            "9. - Administrative Fixkosten & Miete",
            "= BETRIEBSERGEBNIS (EBIT)"
        ],
        "Betrag (€)": [
            f"{umsatz_hw:,.2f} €",
            f"{umsatz_sw_a:,.2f} €",
            f"{umsatz_sw_b:,.2f} €",
            f"{umsatz_gesamt:,.2f} €",
            f"-{var_kosten_hw:,.2f} €",
            f"-{var_kosten_sw:,.2f} €",
            f"{deckungsbeitrag_gesamt:,.2f} €",
            f"-{personalkosten:,.2f} €",
            f"-{budget_fe:,.2f} €",
            f"-{marketing_total:,.2f} €",
            f"-{45000.0:,.2f} €",
            f"{ebit:,.2f} €"
        ]
    }
    st.table(pd.DataFrame(guv_data))
