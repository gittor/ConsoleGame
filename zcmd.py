from monotonic import monotonic
import os,sys

def run(cmd):
	code = os.system('%s > zcmd_run_180de67b5fcb.tmp 2>&1'%(cmd))
	with open('zcmd_run_180de67b5fcb.tmp') as fin:
		msg = fin.read()
	os.remove('zcmd_run_180de67b5fcb.tmp')
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