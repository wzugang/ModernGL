import os, sys, platform

class CustomCCompiler:
	def __init__(self, verbose = 0, dry_run = 0, force = 0):
		self.comp = 'g++ -m%s' % platform.architecture()[0][:2]
		self.compiler_type = None

	def set_include_dirs(self, dirs):
		print('set_include_dirs')
		self.inc_dirs = dirs.copy()

	def set_libraries(self, *args):
		print('set_libraries')

	def set_library_dirs(self, *args):
		print('set_library_dirs')

	def set_runtime_library_dirs(self, *args):
		print('set_runtime_library_dirs')

	def compile(self, sources, *args, **kwargs):
		print('compile')

		output_dir = kwargs['output_dir']
		if not os.path.isdir(output_dir):
			os.makedirs(output_dir)

		objects = []
		for source in sources:
			print(source)
			output_base = os.path.basename(source)
			output_name = os.path.splitext(output_base)[0]
			output_filename = os.path.join(output_dir, output_name + '.o')
			incs = ' '.join('-I %s' % inc for inc in self.inc_dirs)
			todo = '%s -c %s %s -o %s' % (self.comp, incs, source, output_filename)
			print(todo)
			ret = os.system(todo)
			objects.append(output_filename)

			if ret:
				exit(ret)

		return objects

	def detect_language(self, *args):
		print('detect_language')
		
	def link_shared_object(self, objects, output_filename, *args, **kwargs):
		print('link_shared_object')

		output_dir = os.path.dirname(output_filename)
		if not os.path.isdir(output_dir):
			os.makedirs(output_dir)

		build_temp = kwargs['build_temp']
		if not os.path.isdir(build_temp):
			os.makedirs(build_temp)

		output_base = os.path.basename(output_filename)
		output_name = os.path.splitext(output_base)[0]
		def_filename = os.path.join(build_temp, output_name + '.def')

		def_file = open(def_filename, 'w')
		def_file.write('LIBRARY %s.pyd\n' % output_name)
		def_file.write('EXPORTS\n')
		def_file.write('\n'.join(kwargs['export_symbols']))
		def_file.close()

		libs = ' '.join('-l%s' % lib for lib in kwargs['libraries'])
		objs = ' '.join(objects)

		dll = 'python%d%d.dll' % (sys.hexversion >> 24, (sys.hexversion >> 16) & 0xff)
		pydll = os.path.join(os.path.dirname(sys.executable), dll)

		todo = '%s -shared -O2 %s %s %s %s -o %s' % (self.comp, def_filename, objs, libs, pydll, output_filename)
		print(todo)

		ret = os.system(todo)
		if ret:
			exit(ret)
