import streamlit as st
import pandas as pd

# Constants
conversion_rate_CNY_to_AUD = 0.21  # Assuming 1 CNY = 0.21 AUD, adjust as needed
conversion_rate_AUD_to_CNY = 1 / conversion_rate_CNY_to_AUD
sqm_price_CNY = 4500
sqm_price_AUD = sqm_price_CNY * conversion_rate_CNY_to_AUD
logistics_costs = {
    "Shipping": 11920,
    "Transport": 780,
    "Secure": 460,
    "Custom": 60,
    "Port admin": 30,
}
local_transport_cost_per_container_default = 10000
crane_costs_default = 12000
building_permit_costs = {
    "2 bed": 14100,
    "1 bed": 12900
}
cost_per_stump = 600
fixed_civil_work_cost = 6000
on_site_plumbing_connection = 2500
on_site_electrical_connection = 2500
site_work_base_costs = fixed_civil_work_cost + on_site_plumbing_connection + on_site_electrical_connection
profit_margin_default = 0.3

# Translation dictionary
translations = {
    "English": {
        "title": "Modular Home Cost Evaluation",
        "price_per_sqm": "Price per Square Meter (in AUD)",
        "local_transport_cost": "Local Transport Cost per Container (in AUD)",
        "crane_costs": "Crane Costs (in AUD)",
        "profit_margin": "Profit Margin (%)",
        "1_bed_size": "1 Bed Option Size (sqm)",
        "2_bed_size": "2 Bed Option Size (sqm)",
        "1_bed_option": "1 Bed Option",
        "2_bed_option": "2 Bed Option",
        "construction_costs": "Construction Costs",
        "logistics_costs": "Logistics Costs",
        "permit_costs": "Permit Costs",
        "site_work_costs": "Site Work Costs",
        "construction_cost": "Construction Cost",
        "shipping": "Shipping",
        "transport": "Transport",
        "secure": "Secure",
        "custom": "Custom",
        "port_admin": "Port admin",
        "local_transport": "Local Transport",
        "crane_costs": "Crane Costs",
        "permit_cost": "Permit Cost",
        "stump_cost": "Stump Cost",
        "fixed_civil_work_cost": "Fixed Civil Work Cost",
        "on_site_plumbing_connection": "On-site Plumbing Connection",
        "on_site_electrical_connection": "On-site Electrical Connection",
        "building_permit_license": "Building Permit License",
        "domestic_building_insurance": "Domestic Building Insurance",
        "total_cost": "Total Cost",
        "profit": "Profit",
        "total_price": "Total Price",
        "gst": "Goods & Services Tax (GST)",
        "Construction": "Construction",
        "Logistics": "Logistics",
        "Permit": "Permit",
        "Site Work": "Site Work",
        "Profit": "Profit",
    },
    "Simplified Chinese": {
        "title": "模块化住宅成本评估",
        "price_per_sqm": "每平方米价格（人民币）",
        "local_transport_cost": "每个集装箱的本地运输费用（人民币）",
        "crane_costs": "起重机费用（人民币）",
        "profit_margin": "利润率 (%)",
        "1_bed_size": "一居室选项大小（平方米）",
        "2_bed_size": "两居室选项大小（平方米）",
        "1_bed_option": "一居室选项",
        "2_bed_option": "两居室选项",
        "construction_costs": "建筑成本",
        "logistics_costs": "物流成本",
        "permit_costs": "许可证费用",
        "site_work_costs": "现场工作成本",
        "construction_cost": "建筑成本",
        "shipping": "运输",
        "transport": "交通",
        "secure": "安全",
        "custom": "海关",
        "port_admin": "港口管理",
        "local_transport": "本地运输",
        "crane_costs": "起重机费用",
        "permit_cost": "许可证费用",
        "stump_cost": "桩成本",
        "fixed_civil_work_cost": "固定土建成本",
        "on_site_plumbing_connection": "现场管道连接",
        "on_site_electrical_connection": "现场电气连接",
        "building_permit_license": "建筑许可证",
        "domestic_building_insurance": "国内建筑保险",
        "total_cost": "总成本",
        "profit": "利润",
        "total_price": "总价",
        "gst": "商品与服务税 (GST)",
        "Construction": "建筑",
        "Logistics": "物流",
        "Permit": "许可证",
        "Site Work": "现场工作",
        "Profit": "利润",
    },
}

# Sidebar inputs
st.sidebar.title("Modular Home Cost Parameters")

# Language toggle
language = st.sidebar.selectbox("Language", ["English", "Simplified Chinese"])

# Translation function
def translate(key):
    return translations[language].get(key, key)

# Convert costs if Simplified Chinese is selected
if language == "Simplified Chinese":
    sqm_price = round(sqm_price_AUD * conversion_rate_AUD_to_CNY)
    local_transport_cost_per_container = round(local_transport_cost_per_container_default * conversion_rate_AUD_to_CNY)
    crane_costs = round(crane_costs_default * conversion_rate_AUD_to_CNY)
    cost_per_stump = round(cost_per_stump * conversion_rate_AUD_to_CNY)
    fixed_civil_work_cost = round(fixed_civil_work_cost * conversion_rate_AUD_to_CNY)
    on_site_plumbing_connection = round(on_site_plumbing_connection * conversion_rate_AUD_to_CNY)
    on_site_electrical_connection = round(on_site_electrical_connection * conversion_rate_AUD_to_CNY)
    currency_symbol = "¥"
else:
    sqm_price = round(sqm_price_AUD)
    local_transport_cost_per_container = round(local_transport_cost_per_container_default)
    crane_costs = round(crane_costs_default)
    cost_per_stump = round(cost_per_stump)
    fixed_civil_work_cost = round(fixed_civil_work_cost)
    on_site_plumbing_connection = round(on_site_plumbing_connection)
    on_site_electrical_connection = round(on_site_electrical_connection)
    currency_symbol = "$"

# Input parameters
sqm_price = st.sidebar.number_input(translate("price_per_sqm"), value=sqm_price)
local_transport_cost_per_container = st.sidebar.number_input(translate("local_transport_cost"), value=local_transport_cost_per_container)
crane_costs = st.sidebar.number_input(translate("crane_costs"), value=crane_costs)
profit_margin = st.sidebar.number_input(translate("profit_margin"), value=round(profit_margin_default * 100)) / 100

# Size inputs
sqm_1_bed = st.sidebar.number_input(translate("1_bed_size"), value=42)
sqm_2_bed = st.sidebar.number_input(translate("2_bed_size"), value=58)

# Calculate costs
def calculate_costs(option, sqm, containers, stumps):
    construction_cost = round(sqm * sqm_price)
    logistics_cost = round(sum(logistics_costs.values()) * containers + local_transport_cost_per_container * containers + crane_costs)
    permit_cost = round(building_permit_costs[option] * (conversion_rate_AUD_to_CNY if language == "Simplified Chinese" else 1))
    stump_cost = round(stumps * cost_per_stump)
    site_work_cost = round(site_work_base_costs + stump_cost)
    permit_license_cost = round(site_work_cost * 0.05)
    insurance_cost = round(site_work_cost * 0.008)
    total_site_work_cost = round(site_work_cost + permit_license_cost + insurance_cost)
    total_cost = round(construction_cost + logistics_cost + permit_cost + total_site_work_cost)
    profit = round(total_cost * profit_margin)
    total_cost_with_profit = round(total_cost + profit)
    gst = round(total_cost_with_profit * 0.10)
    total_price = round(total_cost_with_profit + gst)
    return {
        "construction_cost": construction_cost,
        "logistics_cost": logistics_cost,
        "permit_cost": permit_cost,
        "stump_cost": stump_cost,
        "site_work_cost": site_work_cost,
        "permit_license_cost": permit_license_cost,
        "insurance_cost": insurance_cost,
        "total_site_work_cost": total_site_work_cost,
        "total_cost": total_cost,
        "profit": profit,
        "gst": gst,
        "total_price": total_price
    }

# 1 Bed Option
containers_1_bed = 1
stumps_1_bed = 8
costs_1_bed = calculate_costs("1 bed", sqm_1_bed, containers_1_bed, stumps_1_bed)

# 2 Bed Option
containers_2_bed = 2
stumps_2_bed = 16
costs_2_bed = calculate_costs("2 bed", sqm_2_bed, containers_2_bed, stumps_2_bed)

# Display costs
st.title(translate("title"))

col1, col2 = st.columns(2)
with col1:
    st.subheader(f"{translate('1_bed_option')} ({sqm_1_bed} sqm)")
    with st.expander(f"{translate('construction_costs')}: {currency_symbol}{costs_1_bed['construction_cost']}"):
        st.write(f"{translate('construction_cost')}: {currency_symbol}{costs_1_bed['construction_cost']}")
    with st.expander(f"{translate('logistics_costs')}: {currency_symbol}{costs_1_bed['logistics_cost']}"):
        st.write(f"{translate('shipping')}: {currency_symbol}{round(logistics_costs['Shipping'] * containers_1_bed * (conversion_rate_AUD_to_CNY if language == 'Simplified Chinese' else 1))}")
        st.write(f"{translate('transport')}: {currency_symbol}{round(logistics_costs['Transport'] * containers_1_bed * (conversion_rate_AUD_to_CNY if language == 'Simplified Chinese' else 1))}")
        st.write(f"{translate('secure')}: {currency_symbol}{round(logistics_costs['Secure'] * containers_1_bed * (conversion_rate_AUD_to_CNY if language == 'Simplified Chinese' else 1))}")
        st.write(f"{translate('custom')}: {currency_symbol}{round(logistics_costs['Custom'] * containers_1_bed * (conversion_rate_AUD_to_CNY if language == 'Simplified Chinese' else 1))}")
        st.write(f"{translate('port_admin')}: {currency_symbol}{round(logistics_costs['Port admin'] * containers_1_bed * (conversion_rate_AUD_to_CNY if language == 'Simplified Chinese' else 1))}")
        st.write(f"{translate('local_transport')}: {currency_symbol}{local_transport_cost_per_container}")
        st.write(f"{translate('crane_costs')}: {currency_symbol}{crane_costs}")
    with st.expander(f"{translate('permit_costs')}: {currency_symbol}{costs_1_bed['permit_cost']}"):
        st.write(f"{translate('permit_cost')}: {currency_symbol}{costs_1_bed['permit_cost']}")
    with st.expander(f"{translate('site_work_costs')}: {currency_symbol}{costs_1_bed['total_site_work_cost']}"):
        st.write(f"{translate('stump_cost')}: {currency_symbol}{costs_1_bed['stump_cost']}")
        st.write(f"{translate('fixed_civil_work_cost')}: {currency_symbol}{fixed_civil_work_cost}")
        st.write(f"{translate('on_site_plumbing_connection')}: {currency_symbol}{on_site_plumbing_connection}")
        st.write(f"{translate('on_site_electrical_connection')}: {currency_symbol}{on_site_electrical_connection}")
        st.write(f"{translate('building_permit_license')}: {currency_symbol}{costs_1_bed['permit_license_cost']}")
        st.write(f"{translate('domestic_building_insurance')}: {currency_symbol}{costs_1_bed['insurance_cost']}")
    st.write(f"{translate('total_cost')}: {currency_symbol}{costs_1_bed['total_cost']}")
    st.write(f"{translate('profit')}: {currency_symbol}{costs_1_bed['profit']}")
    st.write(f"{translate('gst')}: {currency_symbol}{costs_1_bed['gst']}")
    st.write(f"{translate('total_price')}: {currency_symbol}{costs_1_bed['total_price']}")

with col2:
    st.subheader(f"{translate('2_bed_option')} ({sqm_2_bed} sqm)")
    with st.expander(f"{translate('construction_costs')}: {currency_symbol}{costs_2_bed['construction_cost']}"):
        st.write(f"{translate('construction_cost')}: {currency_symbol}{costs_2_bed['construction_cost']}")
    with st.expander(f"{translate('logistics_costs')}: {currency_symbol}{costs_2_bed['logistics_cost']}"):
        st.write(f"{translate('shipping')}: {currency_symbol}{round(logistics_costs['Shipping'] * containers_2_bed * (conversion_rate_AUD_to_CNY if language == 'Simplified Chinese' else 1))}")
        st.write(f"{translate('transport')}: {currency_symbol}{round(logistics_costs['Transport'] * containers_2_bed * (conversion_rate_AUD_to_CNY if language == 'Simplified Chinese' else 1))}")
        st.write(f"{translate('secure')}: {currency_symbol}{round(logistics_costs['Secure'] * containers_2_bed * (conversion_rate_AUD_to_CNY if language == 'Simplified Chinese' else 1))}")
        st.write(f"{translate('custom')}: {currency_symbol}{round(logistics_costs['Custom'] * containers_2_bed * (conversion_rate_AUD_to_CNY if language == 'Simplified Chinese' else 1))}")
        st.write(f"{translate('port_admin')}: {currency_symbol}{round(logistics_costs['Port admin'] * containers_2_bed * (conversion_rate_AUD_to_CNY if language == 'Simplified Chinese' else 1))}")
        st.write(f"{translate('local_transport')}: {currency_symbol}{local_transport_cost_per_container}")
        st.write(f"{translate('crane_costs')}: {currency_symbol}{crane_costs}")
    with st.expander(f"{translate('permit_costs')}: {currency_symbol}{costs_2_bed['permit_cost']}"):
        st.write(f"{translate('permit_cost')}: {currency_symbol}{costs_2_bed['permit_cost']}")
    with st.expander(f"{translate('site_work_costs')}: {currency_symbol}{costs_2_bed['total_site_work_cost']}"):
        st.write(f"{translate('stump_cost')}: {currency_symbol}{costs_2_bed['stump_cost']}")
        st.write(f"{translate('fixed_civil_work_cost')}: {currency_symbol}{fixed_civil_work_cost}")
        st.write(f"{translate('on_site_plumbing_connection')}: {currency_symbol}{on_site_plumbing_connection}")
        st.write(f"{translate('on_site_electrical_connection')}: {currency_symbol}{on_site_electrical_connection}")
        st.write(f"{translate('building_permit_license')}: {currency_symbol}{costs_2_bed['permit_license_cost']}")
        st.write(f"{translate('domestic_building_insurance')}: {currency_symbol}{costs_2_bed['insurance_cost']}")
    st.write(f"{translate('total_cost')}: {currency_symbol}{costs_2_bed['total_cost']}")
    st.write(f"{translate('profit')}: {currency_symbol}{costs_2_bed['profit']}")
    st.write(f"{translate('gst')}: {currency_symbol}{costs_2_bed['gst']}")
    st.write(f"{translate('total_price')}: {currency_symbol}{costs_2_bed['total_price']}")

# Create dataframes for chart visualization
data = {
    "Cost Type": ["Construction", "Logistics", "Permit", "Site Work", "Profit"],
    "1 Bed Option": [
        costs_1_bed['construction_cost'],
        costs_1_bed['logistics_cost'],
        costs_1_bed['permit_cost'],
        costs_1_bed['total_site_work_cost'],
        costs_1_bed['profit'],
    ],
    "2 Bed Option": [
        costs_2_bed['construction_cost'],
        costs_2_bed['logistics_cost'],
        costs_2_bed['permit_cost'],
        costs_2_bed['total_site_work_cost'],
        costs_2_bed['profit'],
    ],
}

# Translate legend labels
data["Cost Type"] = [translate(item) for item in data["Cost Type"]]

df = pd.DataFrame(data)

# Stacked bar chart
chart_data = df.set_index("Cost Type").T
st.bar_chart(chart_data, use_container_width=True, height=500)
