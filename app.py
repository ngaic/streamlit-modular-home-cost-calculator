import streamlit as st
import pandas as pd
import plotly.express as px

# Constants
conversion_rate_CNY_to_AUD = 0.21  # Assuming 1 CNY = 0.21 AUD, adjust as needed
conversion_rate_AUD_to_CNY = 1/conversion_rate_CNY_to_AUD
sqm_price_CNY = 4500
sqm_price_AUD = sqm_price_CNY * conversion_rate_CNY_to_AUD
china_logistics_costs = {
    "china_shipping": 11920,
    "china_transport": 780,
    "china_security": 460,
    "china_custom": 60,
    "china_port_admin": 30,
}
australia_local_transport_cost_per_container_default = 10000
crane_costs_default = 12000
building_permit_costs = {
    "2 bed": {
        "Architectural": 1700,
        "BP Project management": 1000,
        "Client Engagement": 500,
        "Structural": 2000,
        "Civil": 1000,
        "Building Surveyor": 3500,
        "Supporting doc(Title, Reg 52, LPOD, Consent)": 500,
        "Land survey": 2700,
        "Soil report": 550,
        "VBA Application": 300,
        "Energy Rating": 350,
    },
    "1 bed": {
        "Architectural": 1500,
        "BP Project management": 1000,
        "Client Engagement": 500,
        "Structural": 1000,
        "Civil": 1000,
        "Building Surveyor": 3500,
        "Supporting doc(Title, Reg 52, LPOD, Consent)": 500,
        "Land survey": 2700,
        "Soil report": 550,
        "VBA Application": 300,
        "Energy Rating": 350,
    }
}
cost_per_stump = 600
civil_work_cost = 6000
on_site_plumbing_connection = 2500
on_site_electrical_connection = 2500
site_work_base_costs = civil_work_cost + on_site_plumbing_connection + on_site_electrical_connection

# Define default values for profit margin, overhead percentage, and contingency percentage
profit_margin_default = 0.25
overhead_percentage_default = 0.0  # Default 0.12
contingency_percentage_default = 0.05  # Default 0.07

# Translation dictionary
translations = {
    "English": {
        "language": "Language",
        "title": "Modular Home Cost Evaluation",
        "price_per_sqm": "Price per Square Meter (in AUD)",
        "australia_local_transport_cost_per_container": "Local Transport Cost per Container",
        "profit_margin": "Profit Margin (%)",
        "overhead_percentage": "Overhead Percentage (%)",
        "contingency_percentage": "Contingency Percentage (%)",
        "1_bed_size": "1 Bed Option Size (sqm)",
        "2_bed_size": "2 Bed Option Size (sqm)",
        "1_bed_option": "1 Bed Option",
        "2_bed_option": "2 Bed Option",
        "manufacturing_costs": "Manufacturing Costs",
        "logistics_costs": "Logistics Costs",
        "permit_costs": "Permit Costs",
        "site_work_costs": "Site Work Costs",
        "china_shipping": "China Shipping",
        "china_transport": "China Transport",
        "china_security": "China Security",
        "china_custom": "China custom",
        "china_port_admin": "China port admin",
        "australia_local_transport": "Australia Local Transport",
        "crane_costs": "Crane Costs",
        "permit_cost": "Permit Cost",
        "stump_cost": "Stump Cost",
        "civil_work_cost": "Civil Work Cost",
        "on_site_plumbing_connection": "On-site Plumbing Connection",
        "on_site_electrical_connection": "On-site Electrical Connection",
        "building_permit_license": "Building Permit License",
        "domestic_building_insurance": "Domestic Building Insurance",
        "total_cost": "Total Cost",
        "profit": "Profit",
        "total_price": "Total Price",
        "gst": "Goods & Services Tax (GST)",
        "Architectural": "Architectural",
        "BP Project management": "BP Project management",
        "Client Engagement": "Client Engagement",
        "Structural": "Structural",
        "Civil": "Civil",
        "Building Surveyor": "Building Surveyor",
        "Supporting doc(Title, Reg 52, LPOD, Consent)": "Supporting doc(Title, Reg 52, LPOD, Consent)",
        "Land survey": "Land survey",
        "Soil report": "Soil report",
        "VBA Application": "VBA Application",
        "Energy Rating": "Energy Rating",
        "Manufacturing": "Manufacturing",
        "Logistics": "Logistics",
        "Permit": "Permit",
        "Site Work": "Site Work",
        "Profit": "Profit",
        "overhead_cost": "Overhead",
        "contingency_cost": "Contingency",
        "price_breakdown": "Price Breakdown",
        "Floor plan for": "Floor plan for",
        "Option": "Option",
        "Cost": "Cost",
        "Cost Type": "Cost Type"
    },
    "Simplified Chinese": {
        "language": "语言",
        "title": "模块化住宅成本评估",
        "price_per_sqm": "每平方米价格（人民币）",
        "australia_local_transport_cost_per_container": "每个集装箱的澳洲本地运输费用",
        "profit_margin": "利润率 (%)",
        "overhead_percentage": "管理费用百分比 (%)",
        "contingency_percentage": "应急费用百分比 (%)",
        "1_bed_size": "一居室选项大小（平方米）",
        "2_bed_size": "两居室选项大小（平方米）",
        "1_bed_option": "一居室选项",
        "2_bed_option": "两居室选项",
        "manufacturing_costs": "生产成本",
        "Manufacturing": "生产",
        "logistics_costs": "物流成本",
        "permit_costs": "许可证费用",
        "site_work_costs": "现场工作成本",
        "china_shipping": "中国船运",
        "china_transport": "中国陆运",
        "china_security": "中国安保",
        "china_custom": "中国海关",
        "china_port_admin": "中国港口行政",
        "australia_local_transport": "澳洲本地运输",
        "crane_costs": "澳洲起重机费用",
        "permit_cost": "许可证费用",
        "stump_cost": "地桩成本",
        "civil_work_cost": "土建成本",
        "on_site_plumbing_connection": "现场管道连接",
        "on_site_electrical_connection": "现场电气连接",
        "building_permit_license": "建筑许可证",
        "domestic_building_insurance": "国内建筑保险",
        "total_cost": "总成本",
        "profit": "利润",
        "total_price": "总价",
        "gst": "商品与服务税 (GST)",
        "Architectural": "建筑设计",
        "BP Project management": "项目管理",
        "Client Engagement": "客户参与",
        "Structural": "结构",
        "Civil": "土木",
        "Building Surveyor": "建筑测量员",
        "Supporting doc(Title, Reg 52, LPOD, Consent)": "支持文件(产权, 第52条法规, LPOD, 同意)",
        "Land survey": "土地测量",
        "Soil report": "土壤报告",
        "VBA Application": "VBA申请",
        "Energy Rating": "能效评级",
        "Manufacturing ": "生产",
        "Logistics": "物流",
        "Permit": "许可证",
        "Site Work": "现场工作",
        "Profit": "利润",
        "overhead_cost": "管理费用",
        "contingency_cost": "应急费用",
        "price_breakdown": "总价分解",
        "Floor plan for": "平面图为",
        "Option": "选项",
        "Cost": "成本",
        "Cost Type": "成本类别"
    },
}


# Default language setting
current_language_key = "Simplified Chinese"  # Default to Chinese
language = current_language_key  # Initialize the language variable

# Translation function
def translate(key):
    return translations.get(language, {}).get(key, key)

# Sidebar language toggle based on current language key
language = st.sidebar.selectbox(
    translate("language"),
    ["English", "Simplified Chinese"],
    index=0 if current_language_key == "English" else 1  # Default to Chinese
)

# Update the current language key based on the selection
current_language_key = language

# Convert costs if Simplified Chinese is selected
if language == "Simplified Chinese":
    sqm_price = round(sqm_price_AUD * conversion_rate_AUD_to_CNY)
    australia_local_transport_cost_per_container = round(australia_local_transport_cost_per_container_default * conversion_rate_AUD_to_CNY)
    crane_costs = round(crane_costs_default * conversion_rate_AUD_to_CNY)
    cost_per_stump = round(cost_per_stump * conversion_rate_AUD_to_CNY)
    civil_work_cost = round(civil_work_cost * conversion_rate_AUD_to_CNY)
    on_site_plumbing_connection = round(on_site_plumbing_connection * conversion_rate_AUD_to_CNY)
    on_site_electrical_connection = round(on_site_electrical_connection * conversion_rate_AUD_to_CNY)
    currency_symbol = "¥"
else:
    sqm_price = round(sqm_price_AUD)
    australia_local_transport_cost_per_container = round(australia_local_transport_cost_per_container_default)
    crane_costs = round(crane_costs_default)
    cost_per_stump = round(cost_per_stump)
    civil_work_cost = round(civil_work_cost)
    on_site_plumbing_connection = round(on_site_plumbing_connection)
    on_site_electrical_connection = round(on_site_electrical_connection)
    currency_symbol = "$"

# Sidebar inputs
st.sidebar.title(translate("title"))

# Input parameters
sqm_price = st.sidebar.number_input(translate("price_per_sqm"), value=sqm_price)
# Size inputs
sqm_1_bed = st.sidebar.number_input(translate("1_bed_size"), value=38)
sqm_2_bed = st.sidebar.number_input(translate("2_bed_size"), value=58)


australia_local_transport_cost_per_container = st.sidebar.number_input(translate("australia_local_transport_cost_per_container"), value=australia_local_transport_cost_per_container)
crane_costs = st.sidebar.number_input(translate("crane_costs"), value=crane_costs)
profit_margin = st.sidebar.slider(translate("profit_margin"), value=round(profit_margin_default * 100)) / 100
overhead_percentage = st.sidebar.slider(translate("overhead_percentage"), value=round(overhead_percentage_default * 100)) / 100
contingency_percentage = st.sidebar.slider(translate("contingency_percentage"), value=round(contingency_percentage_default * 100)) / 100


def calculate_costs(option, sqm, containers, stumps, target_profit_margin, overhead_percentage, contingency_percentage):
    # Calculate manufacturing cost
    manufacturing_costs = round(sqm * sqm_price)
    
    # Calculate logistics cost
    china_logistics_cost_items = {key: value * containers * (conversion_rate_AUD_to_CNY if language == "Simplified Chinese" else 1) for key, value in china_logistics_costs.items()}
    logistics_cost = round(sum(china_logistics_cost_items.values()) + australia_local_transport_cost_per_container * containers + crane_costs)
    
    # Get permit cost details and convert if necessary
    permit_cost_details = building_permit_costs[option]
    permit_cost_items = {item: cost * (conversion_rate_AUD_to_CNY if language == "Simplified Chinese" else 1) for item, cost in permit_cost_details.items()}
    permit_cost = round(sum(permit_cost_items.values()))
    
    # Calculate stump cost
    stump_cost = round(stumps * cost_per_stump)
    
    # Calculate site work cost
    site_work_cost_items = {
        "civil_work_cost": civil_work_cost,
        "on_site_plumbing_connection": on_site_plumbing_connection,
        "on_site_electrical_connection": on_site_electrical_connection,
        "stump_cost": stump_cost
    }
    site_work_cost = round(sum(site_work_cost_items.values()))
    
    # Calculate additional costs for permit license and insurance
    permit_license_cost = round((site_work_cost + manufacturing_costs + crane_costs) * 0.05)
    insurance_cost = round((site_work_cost + manufacturing_costs + crane_costs) * 0.008)
    total_site_work_cost = round(site_work_cost + permit_license_cost + insurance_cost)
    
    # Calculate overhead costs
    overhead_cost = round((manufacturing_costs + logistics_cost + permit_cost + total_site_work_cost) * overhead_percentage)
    
    # Calculate contingency costs
    contingency_cost = round((manufacturing_costs + logistics_cost + permit_cost + total_site_work_cost) * contingency_percentage)
    
    # Calculate total cost without profit
    total_cost_without_profit = round(manufacturing_costs + logistics_cost + permit_cost + total_site_work_cost + overhead_cost + contingency_cost)
    
    # Adjust profit calculation to ensure profit margin is applied correctly
    profit = round(total_cost_without_profit * target_profit_margin / (1 - target_profit_margin))
    
    # Calculate total cost with profit
    total_cost_with_profit = round(total_cost_without_profit + profit)
    
    # Calculate GST
    gst = round(total_cost_with_profit * 0.10)
    
    # Calculate final total price including GST
    total_price = round(total_cost_with_profit + gst)
    
    return {
        "manufacturing_costs": manufacturing_costs,
        "logistics_cost": logistics_cost,
        "china_logistics_cost_items": china_logistics_cost_items,
        "permit_cost": permit_cost,
        "permit_cost_items": permit_cost_items,
        "stump_cost": stump_cost,
        "site_work_cost": site_work_cost,
        "site_work_cost_items": site_work_cost_items,
        "permit_license_cost": permit_license_cost,
        "insurance_cost": insurance_cost,
        "total_site_work_cost": total_site_work_cost,
        "overhead_cost": overhead_cost,
        "contingency_cost": contingency_cost,
        "total_cost": total_cost_without_profit,
        "profit": profit,
        "gst": gst,
        "total_price": total_price
    }

def display_cost_details(costs, option_label, sqm, containers, image_path):
    st.subheader(f"{option_label} ({sqm} sqm)")
    # Display the specific image for the option
    translated_caption = translate("Floor plan for") + " " + option_label  # Assuming you have the translation for 'Floor plan for' in your dictionary
    st.image(image_path, use_column_width=True, caption=translated_caption, output_format='auto')
    with st.expander(f"{translate('manufacturing_costs')}: {currency_symbol}{costs['manufacturing_costs']}"):
        st.write(f"{translate('manufacturing_costs')}: {currency_symbol}{costs['manufacturing_costs']}")
    with st.expander(f"{translate('logistics_costs')}: {currency_symbol}{costs['logistics_cost']}"):
        for item, cost in costs['china_logistics_cost_items'].items():
            st.write(f"{translate(item.lower())}: {currency_symbol}{round(cost)}")
        st.write(f"{translate('australia_local_transport')}: {currency_symbol}{australia_local_transport_cost_per_container * containers}")
        st.write(f"{translate('crane_costs')}: {currency_symbol}{crane_costs}")
    with st.expander(f"{translate('permit_costs')}: {currency_symbol}{costs['permit_cost']}"):
        for item, cost in costs['permit_cost_items'].items():
            st.write(f"{translate(item)}: {currency_symbol}{round(cost)}")
    with st.expander(f"{translate('site_work_costs')}: {currency_symbol}{costs['total_site_work_cost']}"):
        for item, cost in costs['site_work_cost_items'].items():
            st.write(f"{translate(item)}: {currency_symbol}{cost}")
        st.write(f"{translate('building_permit_license')}: {currency_symbol}{costs['permit_license_cost']}")
        st.write(f"{translate('domestic_building_insurance')}: {currency_symbol}{costs['insurance_cost']}")
    with st.expander(f"{translate('overhead_cost')}: {currency_symbol}{costs['overhead_cost']}"):
        st.write(f"{translate('overhead_cost')}: {currency_symbol}{costs['overhead_cost']}")
    with st.expander(f"{translate('contingency_cost')}: {currency_symbol}{costs['contingency_cost']}"):
        st.write(f"{translate('contingency_cost')}: {currency_symbol}{costs['contingency_cost']}")
    st.write(f"{translate('total_cost')}: {currency_symbol}{costs['total_cost']}")
    st.write(f"{translate('profit')}: {currency_symbol}{costs['profit']}")
    st.write(f"{translate('gst')}: {currency_symbol}{costs['gst']}")
    st.write(f"{translate('total_price')}: {currency_symbol}{costs['total_price']}")

# 1 Bed Option
containers_1_bed = 1
stumps_1_bed = 8
costs_1_bed = calculate_costs("1 bed", sqm_1_bed, containers_1_bed, stumps_1_bed, profit_margin, overhead_percentage, contingency_percentage)
image_path_1_bed = 'assets/option1_floor_plan.png'

# 2 Bed Option
containers_2_bed = 2
stumps_2_bed = 16
costs_2_bed = calculate_costs("2 bed", sqm_2_bed, containers_2_bed, stumps_2_bed, profit_margin, overhead_percentage, contingency_percentage)
image_path_2_bed = 'assets/option2_floor_plan.png'

# Display costs
st.title(translate("title"))

col1, col2 = st.columns(2)
with col1:
    display_cost_details(costs_1_bed, translate("1_bed_option"), sqm_1_bed, containers_1_bed, image_path_1_bed)

with col2:
    display_cost_details(costs_2_bed, translate("2_bed_option"), sqm_2_bed, containers_2_bed, image_path_2_bed)

# Define colour map
color_map = {
    translate("Manufacturing"): 'rgb(54, 162, 235)',  # Blue
    translate("Logistics"): 'rgb(255, 99, 132)',     # Red
    translate("Permit"): 'rgb(75, 192, 192)',        # Teal
    translate("Site Work"): 'rgb(153, 102, 255)',    # Purple
    translate("Profit"): 'rgb(255, 206, 86)',        # Yellow
    translate("overhead_cost"): 'rgb(201, 203, 207)',# Light Grey
    translate("contingency_cost"): 'rgb(255, 159, 64)', # Orange
    translate("gst"): 'rgb(0, 128, 0)', # Green
}

# Prepare data for Plotly
data = {
    "Cost Type": [translate("Manufacturing"), translate("Logistics"), translate("Permit"), translate("Site Work"), translate("overhead_cost"), translate("contingency_cost"), translate("Profit"), translate("gst")],
    translate("1_bed_option"): [
        costs_1_bed['manufacturing_costs'],
        costs_1_bed['logistics_cost'],
        costs_1_bed['permit_cost'],
        costs_1_bed['total_site_work_cost'],
        costs_1_bed['overhead_cost'],
        costs_1_bed['contingency_cost'],
        costs_1_bed['profit'],
        costs_1_bed['gst']
    ],
    translate("2_bed_option"): [
        costs_2_bed['manufacturing_costs'],
        costs_2_bed['logistics_cost'],
        costs_2_bed['permit_cost'],
        costs_2_bed['total_site_work_cost'],
        costs_2_bed['overhead_cost'],
        costs_2_bed['contingency_cost'],
        costs_2_bed['profit'],
        costs_2_bed['gst']
    ],
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Melt the DataFrame to long format for Plotly
df_long = df.melt(id_vars="Cost Type", var_name="Option", value_name="Cost")

# Create the Plotly bar chart
fig_bar = px.bar(df_long, x="Option", y="Cost", color="Cost Type", 
                 title=translate("title"),
                 labels={
                     "Option": translate("Option"),
                     "Cost": translate("Cost"),
                     "Cost Type": translate("Cost Type")
                 },
                 color_discrete_map=color_map,
                 barmode='stack')  # Change 'group' to 'stack' to create a stacked bar chart

# Display the Plotly bar chart in Streamlit
st.plotly_chart(fig_bar, use_container_width=True)

# Pie chart for 1 Bed Option
fig_1_bed = px.pie(df, names="Cost Type", values=translate("1_bed_option"), 
                   title=f"{translate('1_bed_option')} ({sqm_1_bed} sqm) - {translate('price_breakdown')}",
                   color="Cost Type", color_discrete_map=color_map)

# Pie chart for 2 Bed Option
fig_2_bed = px.pie(df, names="Cost Type", values=translate("2_bed_option"), 
                   title=f"{translate('2_bed_option')} ({sqm_2_bed} sqm) - {translate('price_breakdown')}",
                   color="Cost Type", color_discrete_map=color_map)

# Display the pie charts in Streamlit
st.plotly_chart(fig_1_bed, use_container_width=True)
st.plotly_chart(fig_2_bed, use_container_width=True)
