#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st


# In[2]:


paf3 = pd.read_csv('https://github.com/Gmgucejr/PAF_Parts/blob/main/paf_prop.csv')


# In[3]:


st.write("## PAF Proposed Items")
st.dataframe(paf3, use_container_width=True)


# In[ ]:


#get_ipython().system('jupyter nbconvert --to script --output-dir="C:\\Users\\212554084\\Downloads" Proposal.ipynb')


# In[ ]:




