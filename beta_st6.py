#!/usr/bin/env python
# coding: utf-8

# pip list

# pip install lifelines

# pip install reliability

# pip freeze > requirement.txt

# In[1]:


#############################
###Script by: Galileo Guce Jr.
###Email: galileo.guce@geaerospace.com
###Date: 25-September-2026
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


# In[2]:


import warnings
warnings.filterwarnings("ignore")


# In[3]:


paf = pd.read_csv(https://github.com/Gmgucejr/PAF_Parts/blob/main/paf_del.csv)

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


# In[4]:


paf2 = pd.read_csv(https://github.com/Gmgucejr/PAF_Parts/blob/main/paf_contract.csv)
paf3 = pd.read_csv(https://github.com/Gmgucejr/PAF_Parts/blob/main/paf_prop.csv)

paf3['Unit Price'] = pd.to_numeric(paf3['Unit Price'].str.replace(r'[^\d.]', '', regex=True), errors='coerce')


# In[5]:


paf3.info()


# In[6]:


for b in range(len(paf)):
    for c in range(len(paf2)):
        if (paf['PN'].iloc[b] == paf2['Part Number'].iloc[c]):
            paf['Contract_Qty'].iloc[b] = paf2.Qty.iloc[c]
    for d in range(len(paf3)):
        if (paf['PN'].iloc[b] == paf3['PART NUMBER'].iloc[d]):
            paf['Prop_Unit_Price'].iloc[b] = paf3['Unit Price'].iloc[d]


# In[7]:


paf = paf.fillna({'Delta_Arrival_Customs': 0})

paf.info()


# In[8]:


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


# In[9]:


paf.info()


# In[10]:


#######################################################################


# In[11]:


st.set_page_config(layout="wide")


# In[12]:


st.markdown(
    "<h1 style='font-family: Courier New; font-style: italic; font-weight: bold; font-size: 20px;color:red'>PAF Parts Shipment VS Contract</h1>",
    unsafe_allow_html=True,)


# In[13]:


rcParams['figure.figsize'] = 18, 6


# In[14]:


paf_sorted = paf.sort_values(by='LD',ascending=False).head(8)


# In[15]:


fig, ax = plt.subplots(figsize=(20, 10))

sb.barplot(data=paf_sorted, x="NOMENCLATURE", y="LD", hue='AWB',ax=ax)
ax.set_title('LD Cost per Part Nomenclature')
ax.set_xlabel('Part Number')
ax.set_ylabel('LD Cost, S')

#ax[0].vlines(2000,0,wb.predict(2000),linestyle='--',color='r')

plt.tight_layout(h_pad=5)
plt.show()


# In[16]:


paf4 = paf.groupby(['NOMENCLATURE']).Total_Amount.sum()
dfpie = paf4.to_frame()
dfpie2 = dfpie.reset_index(level=['NOMENCLATURE'])


# In[17]:


dfpie2 = dfpie2.sort_values(by=['Total_Amount'], ascending=False)
#dfpie3 = dfpie2.head(10)


# In[18]:


explode = [0.1, 0.1, 0, 0, 0, 0, 0, 0, 0, 0]
palette_color = sb.color_palette('bright')

fig2, ax = plt.subplots(figsize=(10, 10))

dfpie2 = dfpie2.head(10)
total_received = paf['Total_Amount'].sum()
total_LD = paf['LD'].sum()
def dollar_format(pct):
    val = int(round(pct * total_received / 100.0))
    return f"${val:,.1f}"  # Formats as $1,200

ax.pie(dfpie2['Total_Amount'], labels=dfpie2['NOMENCLATURE'], colors=palette_color, autopct=dollar_format, explode=explode)

plt.title('PAF Top 10 Parts Delivered by Cost')

plt.show()


# In[19]:


col3, col4 = st.columns([3, 3])

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

col3.metric(label="Total Receivable",value=f'${total_received:,.2f}')
col4.metric(label="Total LDs",value=f'${total_LD:,.2f}')


# In[20]:


st.pyplot(fig)


# In[21]:


st.pyplot(fig2)


# In[22]:


st.write('<p style="font-size: 18px; color: red;">Add or Edit Details on the Table Below:</p>', unsafe_allow_html=True)


# In[23]:


col7, col8 = st.columns([3, 3])


# In[24]:


if "df2" not in st.session_state:
    st.session_state.df2=paf

def filter_df():
    # Fetch the newly selected value from the selectbox widget state
    chosen_status = st.session_state.status_select
    
    st.session_state.df2 = st.session_state.df2[st.session_state.df2.Contract_Num == chosen_status]


with col7:
    st.markdown(
        """
        <style>
        div[class*="stSelectbox"] label p {
            font-size: 22 !important;
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
        """,
    unsafe_allow_html=True)
    
    contract = st.selectbox("Select Contract Number:",
    paf['Contract_Num'],
    key="status_select",
    on_change=filter_df)


# In[30]:


if "df" not in st.session_state:
    st.session_state.df = paf

# 2. Define the callback function to handle calculations
def update_dependent_columns():
    # Access the raw change dictionary tracked by the data_editor's key
    changes = st.session_state["editor_changes"]
    
    # Process only the rows that were edited
    for row_index, changed_cols in changes["edited_rows"].items():
        for col, new_val in changed_cols.items():
            # Apply the user's manual change to the session state DataFrame
            st.session_state.df.at[row_index, col] = new_val
            
        # Recalculate dependent columns for the modified row
        #Weibull_Removal_Date = st.session_state.df.at[row_index, "Weibull_Removal_Date"]
        #WTW_TAT = st.session_state.df.at[row_index, "WTW_TAT"]
        #st.session_state.df.at[row_index, "RFI_date"] = Weibull_Removal_Date + timedelta(days = WTW_TAT/1.0)

# 3. Render the data editor
# Bind the editor to session state and hook up the callback
paf2 = st.data_editor(
    st.session_state.df,
    key="editor_changes",
    on_change=update_dependent_columns,
    disabled=['AWB', 'Carrier', 'MSN', 'Invoice', 'Item_Num', 'Contract_Num', 'PN',
       'Exp_tag', 'NOMENCLATURE', 'Delivered_Qty', 'Contract_Qty',
       'Qty_Match ', 'SN', 'Unit_Price', 'Prop_Unit_Price', 'Unit_Price_Match',
       'Total_Amount', 'Accepted', 'Delivered_Date', 'Due_Date',
       'Delivery_Days', 'Delay', 'LD', 'LD_Bool', 'Total_LD', 'DAP_Price',
       'Pickup_Date', 'Arrival_Date', 'Delta_Pickup_Arrival',
       'Customs_Release_Date', 'Delta_Arrival_Customs',
       'Delta_Arrival_Acceptance', 'Payment'],
    use_container_width=True,
    #column_config={
        #"Weibull_Removal_Date": st.column_config.DateColumn("Weibull_Removal_Date ✏️"),
        #"WTW_TAT": st.column_config.NumberColumn("WTW_TAT ✏️", format="%.0f"),
        #"RFI_date": st.column_config.DateColumn("RFI_date ✏️")},
    hide_index=True,
)
#st.session_state.df.style.set_properties(subset=['Weibull_Removal_Date', 'WTW_TAT', 'RFI_date'], **{'background-color': '#FFFFCC'})


# In[31]:


st.stop()


# In[33]:


#get_ipython().system('jupyter nbconvert --to script --output-dir="C:\\Users\\212554084\\Downloads" beta_st6.ipynb')


# In[ ]:




