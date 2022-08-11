import lightning as L
from lightning_app.structures import Dict, List
from lightning_app.frontend import StreamlitFrontend
from lit_bashwork.lit_work_utils import work_calls_len
import scripts.ui_main as ui_main
import time
import random
import pprint
from lightning_app.utilities.enum import WorkStageStatus #     NOT_STARTED PENDING RUNNING SUCCEEDED FAILED STOPPED
from dataclasses import dataclass
import subprocess
import shlex

@dataclass
class TtydBuildConfig(L.BuildConfig):
    def build_commands(self):
        return ["""sudo apt-get update
sudo apt-get install htop net-tools lsof
sudo apt-get install build-essential cmake git libjson-c-dev libwebsockets-dev
git clone https://github.com/tsl0922/ttyd.git
cd ttyd && mkdir build && cd build
cmake ..
make && sudo make install
"""]


def work_is_free(work):
	"""this is not 100% if the work executes very fast"""
	if (work.status.stage == WorkStageStatus.NOT_STARTED) or (work.status.stage == WorkStageStatus.SUCCEEDED):
		return(True)
	else:
		return(False)

def work_is_stopped(work):
	""" STOPPED, FAILED """
	if (work.status.stage == WorkStageStatus.FAILED) or (work.status.stage == WorkStageStatus.STOPPED):
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
		self.last_worker_id = 0
		# vm config
		self.target_instance_type = "default"
		self.target_preemptible = False		# feature not avail yet
		self.target_wait_timeout = None 	# feature not avail yet
		self.target_idle_timeout = None		# does not work on default instance

		# state
		self.n_trials = 20
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
				# should be removed from active
				elif self.worker_active[i] and work_is_stopped(w):	
					print(f"Worker {i}: removing from the active pool {w.status.stage}")
					self.worker_active[i] = False
					self.num_of_workers -= 1

	def configure_layout(self):
		return(StreamlitFrontend(render_fn=ui_main.run))

class Work(L.LightningWork):
	def __init__(self, *args, id, cloud_build_config = None, **kwargs):
		if cloud_build_config is None:
			cloud_build_config = TtydBuildConfig()
		super().__init__(*args, 
			cloud_build_config=cloud_build_config,
			**kwargs)
		self.id = id
		self._procs = {}
	def run(self,seq, *args, **kwargs):
		if "ttyd" not in self._procs:
			cmd = f"ttyd -p {self.port} bash"
			print(f"{self.id}: {cmd}")
			self._procs["ttyd"] = subprocess.Popen(cmd, shell=True, executable='/bin/bash',close_fds=True)
		sleep_sec = random.randint(1,10)
		print(f"{self.id}: start seq {seq} sleeping {sleep_sec}")
		# using subprocess to show in terminal
		subprocess.run(f"sleep {sleep_sec}", shell=True)

class Flow(L.LightningFlow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.elastic_flow0 = ElasticFlow()
		self.elastic_flow1 = ElasticFlow()
		self.elastic_flow2 = ElasticFlow()

	def run(self):
		self.elastic_flow0.run()
		self.elastic_flow1.run()
		if self.elastic_flow0.current_trial > 5 and self.elastic_flow1.current_trial > 10:
			self.elastic_flow2.run()

	def configure_layout(self):
		ui = []
		for flow_num,flow in enumerate([self.elastic_flow0, self.elastic_flow1, self.elastic_flow2]):
			ui.append({"name":f"Config {flow_num}", "content":flow})
			for i,active in flow.worker_active.items():
				if active:
					ui.append({"name":f"Flow {flow_num} Term {str(i)}","content":flow.workers[str(i)]})
		return(ui)
if __name__ == "__main__":
	app = L.LightningApp(Flow())