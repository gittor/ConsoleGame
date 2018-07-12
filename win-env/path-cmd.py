import _winreg as win
import os,sys

def reg_save(value):
	v = ';'.join(value)
	win.SetValueEx(user_key(), 'path', 0, judge_type(v), v)
def reg_get():
	try:
		return win.QueryValueEx(user_key(), 'path')[0].split(';')
	except Exception as e:
		print e
		return []

def user_key():
    return win.OpenKey(win.HKEY_CURRENT_USER, 'Environment', 0, win.KEY_ALL_ACCESS)

def judge_type(value):
    return win.REG_EXPAND_SZ if '%' in value else win.REG_SZ

def cmd_list():
	vals = reg_get()
	if not vals: return
	print('-'*42)
	for i,v in enumerate(vals):
		if '%' in v: print '%d. %s=>%s'%(i, v, win.ExpandEnvironmentStrings(v))
		else: print '%d. %s'%(i, v)
	print('='*42)

def cmd_add(item):
	value = reg_get()
	item = os.path.abspath(item)
	if item not in value:
		value.append( os.path.abspath(item) )
		reg_save(value)

def cmd_del(idx):
	value = reg_get()
	del value[idx]
	reg_save(value)

def main():
	cmds = sys.argv[1:]
	if len(cmds)==0:
		cmd_list()
	else:
		if cmds[0]=='add':
			cmd_add(cmds[1])
		elif cmds[0]=='del':
			cmd_del(int(cmds[1]))
		else:
			print 'error command'
if __name__ == '__main__':
	main()