from monotonic import monotonic
import os,sys,uuid

run_file_name = str(uuid.uuid4())
def run(cmd):
	code = os.system('%s > %s 2>&1'%(cmd, run_file_name))
	with open(run_file_name) as fin:
		msg = fin.read()
	os.remove(run_file_name)
	return (code, msg)

def where(fname):
	candy = ['.']
	candy.extend(sys.path)
	for path in candy:
		full = os.path.join(path, fname)
		if os.path.isfile(full):
			return full
	return None

def call_runtime(func, *keys, **args):
	def _mono(*keys, **args):
		start = monotonic()
		ret = func(*keys, **args)
		print str(func), monotonic()-start
		return ret
	return _mono