#this code creates mass excess database from IAEA database. Their format has a lot of unnecessary info
#but we filter it. In the name of ZSIIR!
import re
with open ('/home/skye/Programs/myscripts/git/signal_gen/input/db_Mass_excess.txt') as db: #IAEA database
	with open('/home/skye/Programs/myscripts/git/signal_gen/input/db_Mass_excess_normal.txt', 'w') as outdb: #output file
		for line in db:
			dataline = []
			if line[0] == '0': #some lines starts from 0
				line = (re.sub(' +', ' ',line[2:]))
			
			if line[0] == ' ':  #some no
				line = (re.sub(' +', ' ',line[2:]))
			
			if line[0] == '  ': #double space from fortran, it seems
				line = (re.sub(' +', ' ',line[3:]))
			#here they have some reactions or whatever. Not everywhere, so we have to filter it	
			if line.split()[5] in {'-4n', '-3n', '-2n', '-nn', '-n', '+n', '+nn', '+3n', '4n','-p', '-pp', '+', '+p', '+pp', '+3p', '2p-n', '-n2p', 'ep', 'p-2n', '-pn', '-', 'p2n', '-a', 'x', 'IT','+a', '++', 'ea', '+n2p', '+pn', '-', '-p2n', '2n-p', 'p4n', '+t', '--'  }:
				outdb.write('{} {} {} {}\n'.format(line.split()[1], line.split()[2], line.split()[3], line.split()[6])  )
			#if no reactions given:	
			else:
				outdb.write('{} {} {} {}\n'.format(line.split()[1], line.split()[2], line.split()[3], line.split()[5])  )
			
