import lightning as L
from lightning_app.structures import Dict, List
from lightning_app.utilities.enum import WorkStageStatus
import time

def work_is_free(work):
	"""this is not 100% if the work executes very fast"""
	if (work.status.stage == WorkStageStatus.NOT_STARTED) or (work.status.stage == WorkStageStatus.SUCCEEDED):
		return(True)
	else:
		return(False)

class Work(L.LightningWork):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.calls = 0
	def run(self):
		self.calls += 1
		print("here", self.calls)
		time.sleep(5)

class Flow2(L.LightningFlow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.workers = Work(parallel=True, cache_calls=False)
		self.calls = 0
	def run(self):
		w = self.workers
		w.run()
		self.calls += 1
		print(self.calls, self.workers.calls)

class Flow(L.LightningFlow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.workers = List()
		self.workers_len = 1
		self.calls = 0
	def run(self):
		if len(self.workers) < self.workers_len:
			self.workers.append(Work(parallel=True, cache_calls=False) )
		w = self.workers[0]
		if work_is_free(w):
			w.run()
			self.calls += 1
			print(self.calls, w.calls)

if __name__ == "__main__":			
	app = L.LightningApp(Flow())
