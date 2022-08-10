import streamlit as st

def run(state):
	# BUG: int cast is needed as somtimes float can be returned
	# BUG: target_simultaneous_trials can change even with disabled flag 
	target_trials = int(st.number_input("Number jobs", value = int(state.n_trials)))

	st.info(f"Jobs executed {state.current_trial}")
	
	submit = st.button("Submit")
	if submit:
		state.n_trials = target_trials
