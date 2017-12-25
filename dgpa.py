def pdfToCsv(filename):
	
	import os
	import os.path
	

	outname = filename.split('.')[0] + '.csv'
	exists = os.path.isfile(outname) 

	if exists:
		print 'csv already here, no request needed'
	else:
		req = 'curl -F f=@"' + filename + '" "https://pdftables.com/api?key=8ero7kemmxjk&format=csv" > "' + outname + '"' 
		os.system(req)

	f = open(outname, 'r')
	text = f.read().split('\n')
	f.close()
	return text

def extractCourses(filename):
	data = pdfToCsv(filename)


	i = 0
	for line in data:
		if 'Semester :' in line:
			break
		i+=1

	data = data[i:]

	courses = {} #dict entry -> {code.section: {grade, credit, ects, type, repeat, term, name}}

	brk = False
	while not brk:
		index = 0
		term = data[0].split(',')[0].split(':')[1].strip()

		index+=1

		while 'Code.Section' not in data[index]:
			index+=1

		data = data[index:]

		index = 1
		while 'Semester :' not in data[index]:
			if 'Commitee Records' in data[index]:
				brk = True
				break

			if ('Page' in data[index] and 'of' in data[index]):
				index+=1
			if data[index].strip() == '':
				index+=1
			if 'Academic Records' in data[index]:
				index+=1


			course = data[index].split(',')
			course = filter(None, course)
			code = course[0].split('.')[0].strip()

			

			name = ''
			grade = ''
			credit = ''
			ects = ''
			ctype = ''
			repeat = ''

			nexti = 2
			if course[2] in gpa_map.keys():
				grade = course[2]
				nexti = 3
			else:
				grade = ''

			credit = course[nexti]
			nexti+=1
			ects = course[nexti]
			nexti+=1
			if nexti < len(course):
				ctype = course[nexti]
				if course[nexti]=='R':
					code+='R'
			else:
				ctype = ''
			nexti+=1
			if nexti < len(course):
				repeat = course[nexti]
			else:
				repeat = ''

			courses[code] = {'term': term, 'name': name, 'grade': grade, 'credit': credit, 'ects': ects, 'type': ctype, 'repeat': repeat}
		
			#print courses[code]
			#print

			index+=1

		data = data[index:]
	
	return courses

def calculateGpa(filename, depts):
	courses = extractCourses(filename)
	total_credits = 0.0
	real_total_credits = 0.0
	total_points = 0.0
	spas = {}
	term_credits = {}
	count=0

	codes = []
	nonexistents = []

	if len(depts) != 0:
		import re
		existents = []
		for code in courses:
			for dept in depts:
				m = re.search('[a-zA-Z]*', code)
				if dept.upper() == m.group(0).upper():
					codes.append(code)
					existents.append(dept)
		nonexistents = list(set(depts)-set(existents))
		depts = list(set(depts)-set(nonexistents))
					
	else:
		codes = courses.keys()

	for code in codes:				
		course = courses[code]
		term = course['term']
		if term not in spas:
			spas[term] = 0
			term_credits[term]=0
		if course['grade'] == 'P' or course['grade'] == '' or course['type'] =='NC':
			count+=1
			real_total_credits+=float(course['credit'])
			continue
		if course['type'] == 'R':
			total_points -= gpa_map[courses[course['repeat']]['grade']] * float(courses[course['repeat']]['credit']) #revert
			total_credits-= float(courses[course['repeat']]['credit'])
			real_total_credits-=float(courses[course['repeat']]['credit'])

		point = gpa_map[course['grade']] * float(course['credit'])
		credit = float(course['credit'])

		total_points += point
		spas[term] += point

		total_credits += credit
		real_total_credits += credit
		term_credits[term] += credit
		count+=1


	gpa = total_points/total_credits
	for term in spas:
		if term_credits[term] == 0: 
			continue
		spas[term]/=term_credits[term]


	return (depts, gpa, spas, count, real_total_credits, nonexistents)

def print_output(calculations):
	depts, gpa, spas, count, total_credits, nonexistents = calculations


	print 
	if len(depts) == 0:
		print 'Departments: all'
	else:
		if len(nonexistents) != 0:
			print 'WARNING: Departments', str(nonexistents), 'does not exist in your transcript. Do you have a typo?'
			print 'Still calculating for', str(depts), '...'
		else:
			print 'Departments:', str(depts)
		

	print 'GPA:'
	print '\t', gpa
	print 'SPAs:'
	for term in sorted(spas.keys()):
		print '\t' + term, ':', spas[term]

	if len(depts) == 0:
		print 'Total courses:',count
		print 'Total credits:',total_credits
	else:
		print 'Total', str(depts), 'courses:',count
		print 'Total', str(depts),'credits:',total_credits

	print 



def main():
	import sys 

	filename = sys.argv[1]
	argv = sys.argv[2:]

	depts = []

	if ('-d' in argv and len(argv) == 1) or ('-d' not in argv and len(argv) > 0): 
		print ' Usage: python depav.py path/to/file -d <deptname1> <deptname2> ...'
		sys.exit()


	if len(argv) > 0:
		depts = argv[1:]
	

	print_output(calculateGpa(filename, depts))

	

if __name__ == "__main__":
    gpa_map = {'AA' : 4.00,'BA' : 3.50,'BB' : 3.00,'CB' : 2.50,'CC' : 2.00,'DC' : 1.50,'DD' : 1.00,'F' : 0.00,'P' : -1}
    main()
