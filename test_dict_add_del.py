from app import work_is_free
import lightning as L
from lightning_app.structures import Dict, List
class Work(L.LightningWork):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	def run(self, *args, **kwargs):
		print("here")
class Flow(L.LightningFlow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.workers = Dict()
		self.workers_num = 0
		self.workers_target = 2
		self.workers_id = 0
	def run(self, *args, **kwargs):
		for i in range(self.workers_num, self.workers_target):
			self.workers[str(self.workers_id)] = Work()
			print(f"worker {self.workers_id}: created")
			self.workers_id += 1
		self.workers_num = self.workers_target
		for i,w in self.workers.items():
			w.run()

app = L.LightningApp(Flow())