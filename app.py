import lightning as L
from lightning_app.structures import Dict, List
from lightning_app.frontend import StreamlitFrontend
from lit_bashwork.lit_work_utils import work_calls_len
import scripts.ui_main as ui_main
import time
import random
import pprint
from lightning_app.utilities.enum import WorkStageStatus

def work_is_free(work):
	"""this is not 100% if the work executes very fast"""
	if (work.status.stage == WorkStageStatus.NOT_STARTED) or (work.status.stage == WorkStageStatus.SUCCEEDED):
		return(True)
	else:
		return(False)


class ElasticFlow(L.LightningFlow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# wokers 
		self.num_of_workers = 0
		self.workers = Dict()		
		self.worker_call_count = {}	
		self.worker_active = {}
		self.worker_running = {}
		self.last_worker_id = 0
		# vm config
		self.target_instance_type = "default"
		self.target_preemptible = False		# feature not avail yet
		self.target_wait_timeout = None 	# feature not avail yet
		self.target_idle_timeout = None

		# state
		self.n_trials = 50
		self.current_trial = 0
		# set by UI
		self.submit_processing = True
		self.target_simultaneous_trials = 2
		
	def adjust_workers(self) -> bool:
		"""add or subtract the number of workers
			True: adjustment completed 
			False: adjustment not completed
		"""
		current_num_of_workers = self.num_of_workers
		print("begin", current_num_of_workers,  self.target_simultaneous_trials)
		# expand workers if required
		if current_num_of_workers < self.target_simultaneous_trials:
			# setup cloud config
			cloud_compute = L.CloudCompute(name=self.target_instance_type, 
				disk_size=0, 
				clusters=None, 
				preemptible=self.target_preemptible, 
				wait_timeout=self.target_wait_timeout, 
				idle_timeout=self.target_idle_timeout, 
				shm_size=0)

			for i in range(current_num_of_workers, self.target_simultaneous_trials):
				self.workers[str(self.last_worker_id)] = Work(id=self.last_worker_id, cloud_compute=cloud_compute, parallel=True,cache_calls=False)
				self.worker_call_count[str(self.last_worker_id)] = 0
				self.worker_active[str(self.last_worker_id)] = True
				print(f"worker {self.last_worker_id}: added")
				self.last_worker_id += 1
			current_num_of_workers = self.target_simultaneous_trials
		# contract workers if required starting from the end of the list if free
		else:
			remove_workers = current_num_of_workers - self.target_simultaneous_trials
			# workers that can be removed
			for i,w in self.workers.items():
				if remove_workers <= 0:
					break
				if self.worker_active[i] and work_is_free(w):
					print(f"worker {i}: status = {w.status.stage}")
					w.stop()
					self.worker_active[i] = False		
					remove_workers -= 1
					current_num_of_workers -= 1
					print(f"worker {i}: removed")

		print("end", current_num_of_workers,  self.target_simultaneous_trials)
		self.num_of_workers = current_num_of_workers
		if self.target_simultaneous_trials == self.num_of_workers:
			return(False)
		else:
			return(True)

	def run(self):

		if self.submit_processing:
			self.submit_processing = self.adjust_workers()

		if not(self.submit_processing):
			for i,w in self.workers.items():
				if self.worker_active[i] and work_is_free(w) and self.current_trial  < self.n_trials:
					w.run(self.current_trial)
					self.worker_call_count[i] += 1
					self.current_trial += 1

	def configure_layout(self):
		return(StreamlitFrontend(render_fn=ui_main.run))  

class Work(L.LightningWork):
	def __init__(self, *args, id, **kwargs):
		super().__init__(*args, **kwargs)
		self.id = id
	def run(self,seq, *args, **kwargs):
		print(f"{self.id}: start seq {seq}")
		time.sleep(random.randint(1,10))

class Flow(L.LightningFlow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.elastic_flow = ElasticFlow()

	def run(self):
		self.elastic_flow.run()

if __name__ == "__main__":
	app = L.LightningApp(Flow())