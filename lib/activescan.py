
try:
	import tempfile
	from threading import Thread
	from lib.active.osscan import OsScan
	from lib.active.pingscan import PingScan
	from lib.active.portscan import PortScan
	from lib.core.core import Core,FileExists
	from lib.active.scriptscan import ScriptScan
except ImportError, err:
	from lib.core.core import Core
	Core.print_error(err)


class ActiveScan(FileExists):

	def __init__(self, args, output_dir):

		FileExists.__init__(self, ["nmap"])	
		
		self.__args = args
		self.__output_dir  = output_dir
                self.__ip_file_to_scan = tempfile.NamedTemporaryFile(mode='w+t')


	def _run(self):
		
                if self.__args.is_alive:
                        ping_scan = PingScan(self.__args.destination, self.__output_dir, self.__args.nmap_optimize, "PingScan")
                        ping_scan.run(self.__ip_file_to_scan)
                else:   
                        self.__ip_file_to_scan.write("\n".join([ip.strip() for ip in self.__args.destination.split(",")]))

		port_scan = PortScan(self.__args.config_file, self.__output_dir, self.__ip_file_to_scan, self.__args.nmap_optimize, "PortScan")
                os_scan = OsScan(self.__output_dir, self.__ip_file_to_scan, self.__args.nmap_optimize, "OsScan")
                script_scan = ScriptScan(self.__args.config_file, self.__output_dir, self.__ip_file_to_scan, self.__args.nmap_optimize, "ScriptScan")

                thread_list = []
                try:
                        for counter, func in enumerate(( port_scan, os_scan, script_scan)):
                                thread_number = "t_{0}".format(counter)
                                thread_number = Thread(target = func.run, args = ())
                                thread_number.start()
                                thread_list.append(thread_number)

                        for t in thread_list:
                                t.join()
                except Exception, err:
                        Core.print_error(err)
