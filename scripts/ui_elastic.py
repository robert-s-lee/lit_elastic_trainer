import streamlit as st

def run(state):
	# BUG: int cast is needed as somtimes float can be returned
	# BUG: target_simultaneous_trials can change even with disabled flag 
	target_simultaneous_trials = int(
		st.number_input("Number of concurrent execution", value = int(state.num_of_workers), disabled = state.submit_processing))

	instance_options = ["default", "cpu-small", "cpu-medium", "gpu", "gpu-fast", "gpu-fast-multi" ]
	target_instance_type = st.radio("Select Instance Type", options=instance_options, horizontal = True, disabled = state.submit_processing)  

	# TODO: not supported yet
	# preemptible_options = [ "No", "Yes" ]
	# target_preemptible = st.radio("Preemptible", options=preemptible_options, horizontal = True, disabled = state.submit_processing)  

	# TODO: not supported yet
	# target_wait_timeout = int(st.number_input("wait timeout (sec)", value = 600, disabled = state.submit_processing))

	target_idle_timeout = int(st.number_input("idle timeout (sec)", value = 600, disabled = state.submit_processing))

	submit = st.button("Submit", disabled = state.submit_processing)
	if submit:
		state.target_simultaneous_trials = target_simultaneous_trials
		state.target_instance_type = target_instance_type
		#state.target_preemptible = True if target_preemptible == "Yes" else False
		#state.target_wait_timeout = target_wait_timeout
		state.target_idle_timeout = target_idle_timeout
		state.submit_processing = True
	if state.submit_processing:
		st.info("The GUI will be locked during the processing")
