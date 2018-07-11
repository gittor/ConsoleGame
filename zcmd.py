from monotonic import monotonic

def call_runtime(func, *keys, **args):
	def _mono(*keys, **args):
		start = monotonic()
		ret = func(*keys, **args)
		print str(func), monotonic()-start
		return ret
	return _mono