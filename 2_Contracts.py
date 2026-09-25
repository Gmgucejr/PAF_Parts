#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import streamlit as st


# In[2]:


paf2 = pd.read_csv(r'C:\Users\212554084\Box\Python_data\paf_contract.csv')


# In[ ]:


st.write("## PAF Contract List")
st.dataframe(paf2, use_container_width=True)


# In[ ]:


#get_ipython().system('jupyter nbconvert --to script --output-dir="C:\\Users\\212554084\\Downloads" Contracts.ipynb')

