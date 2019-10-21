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



	
