import streamlit as st
import scripts.ui_about as ui_about
import scripts.ui_elastic as ui_elastic
import scripts.ui_workers as ui_workers

# ##################################################################################################
# UI 
def run(state):
	"""app's main menu with sidebar for various tasks"""
	# st page defaults
	st.set_page_config(
			page_title="Lighting App Demo",
			layout="wide",
			initial_sidebar_state="expanded",
	)
	# menu item
	page_names_to_func = {
		'About': ui_about.run,
		'Elastic': ui_elastic.run,
		'Workers': ui_workers.run,
	}
	page = st.sidebar.radio("Main Menu", options=page_names_to_func.keys())
	page_names_to_func[page](state)
