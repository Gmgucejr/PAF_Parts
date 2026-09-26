#!/usr/bin/env python
# coding: utf-8

# pip list

# pip install lifelines

# pip install reliability

# pip freeze > requirement.txt

# In[ ]:


#############################
###Script by: Galileo Guce Jr.
###Email: galileo.guce@geaerospace.com
###Date: 27-September-2026
#############################

import numpy as np
import pandas as pd
import datetime
import seaborn as sb
from pylab import rcParams
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st
#import reliability
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


# In[ ]:


import warnings
warnings.filterwarnings("ignore")


# In[ ]:


paf = pd.read_csv('https://raw.githubusercontent.com/Gmgucejr/PAF_Parts/refs/heads/main/paf_del.csv')

from datetime import datetime, timedelta, date
paf['Delivered_Date'] = pd.to_datetime(paf['Delivered_Date'],format='mixed')
paf['Due_Date'] = pd.to_datetime(paf['Due_Date'])
paf['Pickup_Date'] = pd.to_datetime(paf['Pickup_Date'],format='mixed')
paf['Arrival_Date'] = pd.to_datetime(paf['Arrival_Date'],format='mixed')
paf['Customs_Release_Date'] = pd.to_datetime(paf['Customs_Release_Date'],format='mixed')

paf['Unit_Price'] = pd.to_numeric(paf['Unit_Price'].str.replace(r'[^\d.]', '', regex=True), errors='coerce')
paf['Prop_Unit_Price'] = pd.to_numeric(paf['Prop_Unit_Price'].str.replace(r'[^\d.]', '', regex=True), errors='coerce')
paf['LD'] = pd.to_numeric(paf['LD'].str.replace(r'[^\d.]', '', regex=True), errors='coerce')
paf['Total_LD'] = pd.to_numeric(paf['Total_LD'].str.replace(r'[^\d.]', '', regex=True), errors='coerce')
paf['DAP_Price'] = pd.to_numeric(paf['DAP_Price'].str.replace(r'[^\d.]', '', regex=True), errors='coerce')
paf['Total_Amount'] = pd.to_numeric(paf['Total_Amount'].str.replace(r'[^\d.]', '', regex=True), errors='coerce')

paf.info()


# In[ ]:


paf2 = pd.read_csv('https://raw.githubusercontent.com/Gmgucejr/PAF_Parts/refs/heads/main/paf_contract.csv')
paf3 = pd.read_csv('https://raw.githubusercontent.com/Gmgucejr/PAF_Parts/refs/heads/main/paf_prop.csv')
paf3['Unit Price'] = pd.to_numeric(paf3['Unit Price'].str.replace(r'[^\d.]', '', regex=True), errors='coerce')


# In[ ]:


for b in range(len(paf)):
    for c in range(len(paf2)):
        if (paf['PN'].iloc[b] == paf2['Part Number'].iloc[c]):
            paf['Contract_Qty'].iloc[b] = paf2.Qty.iloc[c]
    for d in range(len(paf3)):
        if (paf['PN'].iloc[b] == paf3['PART NUMBER'].iloc[d]):
            paf['Prop_Unit_Price'].iloc[b] = paf3['Unit Price'].iloc[d]


# In[ ]:


paf.info()


# In[ ]:


LT_Start = date(2025, 3, 17)

paf['Total_Amount']=paf['Delivered_Qty']*paf['Unit_Price']
paf['Delivery_Days']=paf['Due_Date']- pd.to_datetime(LT_Start)
paf['Delta_Pickup_Arrival'] = paf['Arrival_Date'] - paf['Pickup_Date']
paf['Delta_Arrival_Customs'] = paf['Customs_Release_Date'] - paf['Arrival_Date']
paf['Delta_Arrival_Acceptance'] = paf['Arrival_Date'] - paf['Delivered_Date']

paf = paf.fillna({'Delta_Arrival_Customs': 0})

paf['Delay'] = (paf['Delivered_Date']-paf['Due_Date']- pd.to_timedelta(paf['Delta_Arrival_Customs'], unit='D')).dt.days

for a in range(len(paf)):
    if paf['Delay'].iloc[a]>1:
        paf['LD'].iloc[a]= paf['Delay'].iloc[a]*0.1*0.01*paf['Total_Amount'].iloc[a]
        paf['LD_Bool'].iloc[a] = 'YES'
    else:
        paf['LD'].iloc[a] = 0
        paf['LD_Bool'].iloc[a] = 'NO'


# In[ ]:


paf.info()


# In[ ]:


#######################################################################


# In[ ]:


st.set_page_config(layout="wide")


# In[ ]:


st.markdown(
    "<h1 style='font-family: Courier New; font-style: italic; font-weight: bold; font-size: 40px;color:red'>PAF Parts Shipment VS Contractual Requirements</h1>",
    unsafe_allow_html=True,)


# In[ ]:


rcParams['figure.figsize'] = 18, 6


# In[ ]:


paf['Name_PN']=""
for a in range(len(paf)):
    paf['Name_PN'].iloc[a] = str(paf['NOMENCLATURE'].iloc[a]) + ", PN " + str(paf['PN'].iloc[a])


# In[ ]:


paf_sorted = paf.sort_values(by='LD',ascending=False).head(8)


# In[ ]:


plt.close('all')
fig, ax = plt.subplots(figsize=(20, 10))

sb.barplot(data=paf_sorted, x="NOMENCLATURE", y="LD", hue='AWB',ax=ax)
ax.set_title('Liquidated Damages Cost per Part Nomenclature', fontsize=22)
ax.set_xlabel('Part Number', fontsize=18)
ax.set_ylabel('LD Cost,US $',fontsize=18)

#ax[0].vlines(2000,0,wb.predict(2000),linestyle='--',color='r')
ax.legend(title="AWB No.", fontsize=18)
ax.set_xticklabels(labels=paf_sorted.Name_PN,rotation=45, ha='right', fontsize=18)
ax.tick_params(axis='y', labelsize=18)

plt.tight_layout(h_pad=5)

plt.show()


# In[ ]:


paf4 = paf.groupby(['Name_PN']).Total_Amount.sum()
dfpie = paf4.to_frame()
dfpie2 = dfpie.reset_index(level=['Name_PN'])


# In[ ]:


dfpie2 = dfpie2.sort_values(by=['Total_Amount'], ascending=False)
#dfpie3 = dfpie2.head(10)


# In[ ]:


explode = [0.1, 0.1, 0, 0, 0, 0, 0, 0, 0, 0]
palette_color = sb.color_palette('bright')

fig2, ax = plt.subplots(figsize=(10, 10))

dfpie2 = dfpie2.head(10)
total_received = paf['Total_Amount'].sum()
total_LD = paf['LD'].sum()
def dollar_format(pct):
    val = int(round(pct * total_received / 100.0))
    return f"${val:,.1f}"  # Formats as $1,200

ax.pie(dfpie2['Total_Amount'], labels=dfpie2['Name_PN'], colors=palette_color, autopct=dollar_format, explode=explode)

plt.title('PAF Top 10 Parts Delivered by Cost')

plt.show()


# In[ ]:


###########Critical Parts Shipment on LDs


# In[ ]:


paf20 = pd.read_csv(r'C:\Users\212554084\Box\Python_data\paf_contract.csv')
paf5 = paf20.groupby(['Part Number', 'Nomenclature', 'LT', 'Due date']).Qty.sum()
paf6 = paf5.to_frame()
paf6 = paf6.reset_index(level=['Part Number', 'Nomenclature','Due date', 'LT'])

paf6['Delivered_Qty']=0

for b in range(len(paf6)):
    for c in range(len(paf)):
        if (paf6['Part Number'].iloc[b] == paf['PN'].iloc[c]):
            paf6['Delivered_Qty'].iloc[b] = paf.Delivered_Qty.iloc[c]

paf6['Qty_Match']=""
for a in range(len(paf6)):
    if paf6['Qty'].iloc[a] == paf6['Delivered_Qty'].iloc[a]:
        paf6['Qty_Match'].iloc[a] = "YES"
    else:
        paf6['Qty_Match'].iloc[a] = "NO"


# In[ ]:


paf6['Due date'] = pd.to_datetime(paf6['Due date'],format='mixed')
paf6_sorted = paf6.sort_values(by=['Due date'], ascending=True)


# In[ ]:


paf6_sorted = paf6_sorted[paf6_sorted.Qty_Match=="NO"]


# In[ ]:


paf7 = paf6_sorted [['Part Number', 'Nomenclature', 'LT', 'Due date', 'Qty']]
paf7['Quantity'] = 'Contracted'
paf8 = paf6_sorted [['Part Number', 'Nomenclature', 'LT', 'Due date', 'Delivered_Qty']]
paf8.rename(columns = {'Delivered_Qty':'Qty'}, inplace = True)
paf8['Quantity'] = 'Delivered' 
paf9 = pd.concat([paf7, paf8], axis=0)


# In[ ]:


paf9_sorted = paf9.sort_values(by=['Due date','Part Number'], ascending=True)
paf9_sorted['Part_Due_Date'] = ""
paf9_sorted['Due date'] = paf9_sorted['Due date'].dt.strftime('%Y-%b-%d')
for a in range(len(paf9_sorted)):
    paf9_sorted['Part_Due_Date'].iloc[a] = str(paf9_sorted['Nomenclature'].iloc[a]) + " "+ str(paf9_sorted['Part Number'].iloc[a]) + ' - [' + str(paf9_sorted['Due date'].iloc[a]) + "]"


# In[ ]:


plt.close('all')
fig3, ax = plt.subplots(figsize=(20, 10))

sb.barplot(data=paf9_sorted.head(30), x="Part_Due_Date", y='Qty', hue='Quantity', ax=ax)
ax.set_title('Parts for Delivery and Due Dates', fontsize=22)
ax.set_xlabel('Part Nomenclature', fontsize=18)
ax.set_ylabel('Quantity',fontsize=18)


ax.legend(title="Part Quantity", fontsize=18)
ax.set_xticklabels(labels=paf9_sorted.Part_Due_Date,rotation=45, ha='right', fontsize=18)
ax.tick_params(axis='y', labelsize=18)


plt.tight_layout(h_pad=5)

plt.show()

#st.bar_chart(paf6.sort_values(by=['Due date'], ascending=True), x='Nomenclature', y=['Qty', 'Delivered_Qty'])


# In[ ]:


total_contract = 6563893.79


# In[ ]:


col3, col4, col5 = st.columns([3, 3, 3])

st.markdown(
"""
<style>
div[class*="stSelectbox"] label p {
    font-size: 26 !important;
    font-weight: bold !important;
    font-family: 'Courier New', monospace !important;
    font-weight: bold;
    color: green;
}  
div[data-baseweb="select"] span {
    font-size: 20 !important;
    font-family: 'Courier New', monospace !important;
}
</style>
""",unsafe_allow_html=True)

col3.metric(label="Total Contract Price",value=f'${total_contract:,.2f}')
col4.metric(label="Total Receivables",value=f'${total_received:,.2f}')
col5.metric(label="Total LDs",value=f'${total_LD:,.2f}')


# In[ ]:


paf9_sorted['Due date'] = pd.to_datetime(paf9_sorted['Due date'])
paf9_sorted['Year']=paf9_sorted['Due date'].dt.year
paf9_sorted.info()


# In[ ]:


col0, col1, col2 = st.columns([3, 3, 3])


# In[ ]:


with col0:
    if "df_bar" not in st.session_state:
        st.session_state.df_bar = paf9_sorted
        
    st.subheader("Filtered Data Editor")
    
    # 2. Setup the Filter Selectbox
    categories = ["All"] + list(st.session_state.df_bar["Year"].unique())
    selected_category = st.selectbox("Filter due dates by Year:", categories)
    
    # 3. Apply the Filter to the DataFrame
    if selected_category != "All":
        filtered_df = st.session_state.df_bar[st.session_state.df_bar["Year"] == selected_category]
    else:
        filtered_df = st.session_state.df_bar

# 4. Render the Data Editor with the Filtered Rows
edited_df = st.data_editor(
    filtered_df, 
    key="my_data_editor",
    use_container_width=True
)


# In[ ]:


plt.close('all')
fig4, ax = plt.subplots(figsize=(20, 10))

sb.barplot(data=edited_df.head(30), x="Part_Due_Date", y='Qty', hue='Quantity', ax=ax)
ax.set_title('Parts for Delivery and Due Dates', fontsize=22)
ax.set_xlabel('Part Nomenclature', fontsize=18)
ax.set_ylabel('Quantity',fontsize=18)


ax.legend(title="Part Quantity", fontsize=18)
ax.set_xticklabels(labels=paf9_sorted.Part_Due_Date,rotation=45, ha='right', fontsize=18)
ax.tick_params(axis='y', labelsize=18)


plt.tight_layout(h_pad=5)

plt.show()

#st.bar_chart(paf6.sort_values(by=['Due date'], ascending=True), x='Nomenclature', y=['Qty', 'Delivered_Qty'])


# In[ ]:


st.subheader("Parts Priority for Shipment")
st.pyplot(fig4)


# In[ ]:


st.pyplot(fig2)


# In[ ]:


st.pyplot(fig)


# In[ ]:


paf["Delivered_Date"] = pd.to_datetime(paf["Delivered_Date"])
paf["Pickup_Date"] = pd.to_datetime(paf["Pickup_Date"])
paf["Arrival_Date"] = pd.to_datetime(paf["Arrival_Date"])


# In[ ]:


col6, col7 = st.columns([3, 3])


# In[ ]:


with col6:
    # 1. Initialize the DataFrame in session_state so it persists across reruns
    if "df" not in st.session_state:
        st.session_state.df = paf
    
    # 2. Create the input form
    with st.form(key="user_form", clear_on_submit=True):
        st.subheader("Add New Entry")
        AWB = st.text_input("AWB")
        Carrier = st.text_input("Carrier")
        MSN = st.text_input("MSN")
        Invoice = st.text_input("Invoice")
        Item_Num = st.text_input("Item Number")
        Contract_Num = st.text_input("Contract Number")
        PN = st.selectbox("Part Number", list(paf['PN']))
        Exp_tag = st.text_input("Exp tag")
        Nomenclature = st.text_input("Nomenclature")

        with col7:
            Delivered_Qty = st.number_input("Delivered Quantity")
            SN = st.text_input("Serial Number")
            Unit_Price = st.number_input("Unit Price")
            Accepted = st.selectbox("Accepted?", list(paf['Accepted']))
            Delivered_Date = st.date_input("Delivery Date")
            Pickup_Date = st.date_input("Pickup Date")
            Arrival_Date = st.date_input("Arrival Date")
            
            # Every form must have a submit button
        submitted = st.form_submit_button("Add to DataFrame")
    
    # 3. Handle the form submission
    if submitted:
        if AWB:  # Validation check
            # Create a new row as a temporary DataFrame
            new_row = pd.DataFrame([{'AWB': AWB, 'Carrier':Carrier, 'MSN':MSN, 'Invoice':Invoice, 'Item_Num':Item_Num, 'Contract_Num':Contract_Num, 'PN':PN,
           'Exp_tag':Exp_tag, 'NOMENCLATURE':Nomenclature, 'Delivered_Qty':Delivered_Qty,
           'SN':SN, 'Unit_Price':Unit_Price,'Accepted':Accepted, 'Delivered_Date':Delivered_Date, 'Pickup_Date':Pickup_Date, 'Arrival_Date':Arrival_Date}])
            
            # Append to the session state DataFrame using pd.concat
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            st.success(f"Added {AWB} successfully!")
        else:
            st.error("Please enter a name.")
    
    # 4. Display the updated DataFrame
st.session_state.df["Delivered_Date"] = pd.to_datetime(st.session_state.df["Delivered_Date"])
st.session_state.df["Pickup_Date"] = pd.to_datetime(st.session_state.df["Pickup_Date"])
st.session_state.df["Arrival_Date"] = pd.to_datetime(st.session_state.df["Arrival_Date"])

st.subheader("Current Data")
st.dataframe(st.session_state.df)

st.session_state.df.to_csv('https://raw.githubusercontent.com/Gmgucejr/PAF_Parts/refs/heads/main/paf_latest.csv')


# In[ ]:


st.write('<p style="font-size: 18px; color: red;">App development still work in progress...</p>', unsafe_allow_html=True)


# In[ ]:


st.stop()


# In[ ]:


get_ipython().system('jupyter nbconvert --to script --output-dir="C:\\Users\\212554084\\Downloads" beta_st9.ipynb')


# In[ ]:


#paf.info()


# In[ ]:




