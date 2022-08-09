import streamlit as st
import altair as alt
import pandas as pd

def run(state):	
	""" graph works calls count as bar
	work,calls
	0,23
	1,12
	"""
	data=[ [i,v,state.worker_active[i]] for i,v in state.worker_call_count.items() ]
	chart_data = pd.DataFrame(data, columns=["work","calls", "active"])
	c = alt.Chart(chart_data).mark_bar().encode(x='work', y='calls', color=alt.Color('active'))
	st.altair_chart(c, use_container_width=True)   