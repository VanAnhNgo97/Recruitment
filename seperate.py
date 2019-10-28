import re

def remove_tags(text):
	tag_re = re.compile(r'<[^>]+>')
	txt = tag_re.sub('',text).strip()
	txt = txt.replace("\n", " ")
	txt = txt.replace("\t", " ")
	return txt
	
def get_start_index(raw_text,title):
	title_position = ""
	if title == 'quyền lợi':
		title_position = re.search(r'(Quyền lợi được hưởng)', raw_text)
	elif title == 'yêu cầu':
		title_position = re.search(r'(Yêu cầu ứng viên)', raw_text)
	elif title == "mô tả":
		title_position = re.search(r'(Mô tả công việc)', raw_text)
	#print("start")
	#print(title_position.start())
	return title_position.start()

def get_end_index(raw_text,title):
	print("---------------------------")
	title_position = ""
	if title == 'quyền lợi':
		title_position = re.search(r'(Quyền lợi được hưởng)', raw_text)
	elif title == 'yêu cầu':
		title_position = re.search(r'(Yêu cầu ứng viên)', raw_text)
	elif title == "mô tả":
		title_position = re.search(r'(Mô tả công việc)', raw_text)
	#print("end")
	#print(title_position.end())
	return title_position.end()
	

def extract_info(raw_text,title):
	text = remove_tags(raw_text)
	start = 0
	end = 0
	#print(raw_text)
	if title == 'quyền lợi':
		start = get_end_index(text,"quyền lợi")
		end = len(text)
	elif title == 'yêu cầu':
		end = get_start_index(text,"quyền lợi")
		start = get_end_index(text,'yêu cầu')
	else:
		end = get_start_index(text,"yêu cầu")
		start = get_end_index(text,'mô tả') 
	info = text[start:end]
	info = info.strip()
	return info
#for timviecnhanh
def get_start_index_tvn(raw_text,title):
	title_position = ""
	if title == 'lương':
		title_position = re.search(r'(mức lương:)', raw_text)
	elif title == 'ngày hết hạn':
		title_position = re.search(r'(hạn nộp hồ sơ:)', raw_text)
	elif title == "công ty":
		title_position = re.search(r'(tại)', raw_text)
	#print("start")
	#print(title_position.start())
	return title_position.start()

def get_end_index_tvn(raw_text,title):
	print("---------------------------")

	title_position = ""
	if title == 'lương':
		title_position = re.search(r'(mức lương:)', raw_text)
	elif title == 'ngày hết hạn':
		title_position = re.search(r'(hạn nộp hồ sơ:)', raw_text)
	elif title == "công ty":
		title_position = re.search(r'(tại)', raw_text)
	#print("end")
	#print(title_position.end())
	return title_position.end()

def extract_info_tvm(raw_text,title):
	text = raw_text.lower()
	start = 0
	end = 0
	#print(raw_text)
	if title == 'ngày hết hạn':
		start = get_end_index_tvn(text,"ngày hết hạn")
		end = len(text)
	elif title == 'lương':
		end = get_start_index_tnv(text,"ngày hết hạn")
		start = get_end_index_tnv(text,'lương')
	else:
		end = get_start_index_tvn(text,"lương")
		start = get_end_index_tvn(text,'công ty') 
	info = raw_text[start:end]
	info = info.strip()
	return info

def extract_salary_tvn(raw_text):
	text_list = raw_text.strip().split(" ")
	salary_values = []
	baseSalary = {}
	for text in text_list:
		if text.isdigit():
			salary_values.append(int(text))
	if len(salary_values) == 2:
		if salary_values[0] <= salary_values[1]:
			baseSalary["minValue"] = salary_values[0]
			baseSalary["maxValue"] = salary_values[1]
		else:
			baseSalary["maxValue"] = salary_values[0]
			baseSalary["minValue"] = salary_values[1]
	elif len(salary_values) == 1:
		baseSalary["minValue"] = salary_values[0]
		baseSalary["maxValue"] = salary_values[0]
	else:
		baseSalary["minValue"] = 0
		baseSalary["maxValue"] = 0
	baseSalary["currency"] = "VND"
	baseSalary["unitText"] = "MONTH"
	return baseSalary








	
