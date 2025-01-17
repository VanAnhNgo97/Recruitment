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

def extract_info_tvn(raw_text,title):
	text = raw_text.lower()
	start = 0
	end = 0
	#print(raw_text)
	if title == 'ngày hết hạn':
		start = get_end_index_tvn(text,"ngày hết hạn")
		end = len(text)
	elif title == 'lương':
		end = get_start_index_tvn(text,"ngày hết hạn")
		start = get_end_index_tvn(text,'lương')
	else:
		end = get_start_index_tvn(text,"lương")
		start = get_end_index_tvn(text,'công ty') 
	info = raw_text[start:end]
	info = info.strip()
	return info

def extract_salary_tvn(raw_text):
	ini_text = raw_text.strip()
	match_sample = re.match(r"^[0-9]+\s*-\s*\d+\s*(triệu|tr)",ini_text)
	baseSalary = {}
	if match_sample is not None:
		min_salary = int(re.match(r"^[0-9]+",ini_text).group())
		start_index = re.match(r"^[0-9]+",ini_text).span()[1] + 1
		ini_text = ini_text[start_index:]
		ini_text = re.sub(r"-"," ",ini_text)
		ini_text = ini_text.strip()
		max_salary = int(re.match(r"^[0-9]+",ini_text).group())
		baseSalary["minValue"] = min_salary
		baseSalary["maxValue"] = max_salary
	else:
		text_list = ini_text.split(" ")
		salary_values = []
		
		for text in text_list:
			text = text.strip()
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
	if baseSalary["minValue"] < 100:
		baseSalary["minValue"] = baseSalary["minValue"] * 1000000
	if baseSalary["maxValue"] < 100:
		baseSalary["maxValue"] = baseSalary["maxValue"] * 1000000
	baseSalary["minValue"] = str(baseSalary["minValue"])
	baseSalary["maxValue"] = str(baseSalary["maxValue"])
	baseSalary["currency"] = "VND"
	baseSalary["unitText"] = "MONTH"
	return baseSalary

def normalize_date_tvn(ini_date):
	words_list = ini_date.split("-")
	date_str = words_list[1] + "-" + words_list[0] + "-" + words_list[2]
	return date_str

def normalize_org_name_tvn(ini_name):
	if ini_name[-1] == "!":
		ini_name = ini_name[:-1]
	ini_name = ini_name.lower()
	ini_name = ini_name.replace("công ty","c_t")
	count = 0
	for word in ini_name:
		if word == 'c_t':
			count = count + 1
	if count == 1:
		ini_name = ini_name.replace("c_t","công ty")
	else:
		ini_name = ini_name.replace("c_t","",1)
		ini_name = ini_name.replace("c_t","công ty")
	return ini_name
	









	
