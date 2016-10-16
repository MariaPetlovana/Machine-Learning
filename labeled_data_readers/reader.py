import os.path

class Reader(object):
	# directory - path from which data will be loaded
	def __init__(self, directory):
		self.directory = directory
		self.data_files = []

	def getDataFiles(self):
		if not self.data_files:
			self._collectFilesToLoad()

		return self.data_files

	def load(self):
		if not self.data_files:
			self._collectFilesToLoad()

		for f in self.data_files:
			self._loadFromFile(f)

	def _collectFilesToLoad(self):
		for root, dirs, files in os.walk(self.directory):
			for f in files:
				fullpath = os.path.join(root, f)
				if os.path.splitext(fullpath)[1] == '.csv':
					self.data_files.append(fullpath)

    # should be reimplemented in descendants
	def _loadFromFile(self, file_path):
		return

    # should be reimplemented in descendants
	def splitFileNameByPattern(self, path):
		return
