import re

def remove_tags(text):
	tag_re = re.compile(r'<[^>]+>')
	txt = tag_re.sub('',text).strip()
	txt = txt.replace("\n", " ")
	
def get_start_index(raw_text,title):
	title_position = ""
	if title == 'quyền lợi':
		title_position = re.search(r'(Quyền lợi)', raw_text)
	elif title == 'yêu cầu':
		title_position = re.search(r'\b(<h2>Yêu cầu ứng viên</h2>)\b', raw_text)
	elif title == "mô tả":
		title_position = re.search(r'\b(<h2>Mô tả công việc</h2>)\b', raw_text)
	print("start")
	print(title_position)
	return title_position.start()

def get_end_index(raw_text,title):
	title_position = ""
	if title == 'quyền lợi':
		title_position = re.search(r'\b(Quyền lợi được hưởng)\b', raw_text)
	elif title == 'yêu cầu':
		title_position = re.search(r'\b(<h2>Yêu cầu ứng viên</h2>)\b', raw_text)
	elif title == "mô tả":
		title_position = re.search(r'\b(<h2>Mô tả công việc</h2>)\b', raw_text)
	return title_position.end()
	print("end")
	print(title_position)

def extract_info(raw_text,title):
	print(raw_text)
	if title == 'quyền lợi':
		start = get_end_index(raw_text,"quyền lợi") + 1
		end = len(raw_text)
	elif title == 'yêu cầu':
		start = get_start_index(raw_text,"quyền lợi") + 1
		end = get_end_index(raw_text,'yêu cầu') - 1
	else:
		start = get_start_index(raw_text,"yêu cầu") + 1
		end = get_end_index(raw_text,'mô tả') - 1
	return raw_text[start:end]



	
