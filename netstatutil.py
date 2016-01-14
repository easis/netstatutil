#netstatutil by Blau (14/01/2016)

import subprocess, re

class netstatutil():
	invalid_strings = ['0.0.0.0', '*:*', '[::]', '[::1]']
	
	@classmethod
	def get_connections(self, pid='', protocol='', status='', src_ip='', src_port='', dst_ip='', dst_port=''):
		output = subprocess.Popen(['netstat', '-ano'], stdout=subprocess.PIPE).communicate()
		valid = [line for line in output[0].split('\r\n') if not any(xs in line for xs in self.invalid_strings)] #split by new lines and not containing invalid_strings
		valid = valid[4:len(valid)-1] #remove first 4 lines and last
		
		connection_list = []
		for s in valid:
			s = re.sub('\s\s+' , ' ', s.lstrip()) #replace all whitespaces by one
			con_split = s.split(' ')
			connection = {
							'protocol' : con_split[0],
							'src_ip' : con_split[1].split(':')[0],
							'src_port' : con_split[1].split(':')[1],
							'dst_ip' : con_split[2].split(':')[0],
							'dst_port' : con_split[2].split(':')[1],
							'status' : con_split[3],
							'pid' : con_split[4]
				}
				
			#filter by params
			if pid 		!= '' 	and connection['pid'] 		!= pid: 				continue
			if src_ip 	!= '' 	and connection['src_ip'] 	!= src_ip: 				continue
			if dst_ip 	!= '' 	and connection['dst_ip'] 	!= dst_ip: 				continue
			if src_port != '' 	and connection['src_port'] 	!= src_port: 			continue
			if dst_port != '' 	and connection['dst_port'] 	!= dst_port: 			continue
			if protocol != '' 	and connection['protocol'] 	!= protocol.lower(): 	continue
			if status 	!= '' 	and connection['status'] 	!= status.lower(): 		continue

			connection_list.append(connection)
		return connection_list

#usage
connections = netstatutil.get_connections(dst_port='80')
connections = netstatutil.get_connections(dst_port='80', status='established')

#print connections
for c in connections:
	print c
