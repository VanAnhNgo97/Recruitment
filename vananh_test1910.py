import re
from langdetect import detect
from lxml import etree


def remove_tags(text):
	tag_re = re.compile(r'<[^>]+>')
	return tag_re.sub('',text)
def split_word(sentences):
	special_characters = ["\n","\t","\r","{","}","[","*",",",".","\"","\'","(",")"]
	raw_sentences = ""
	for character in sentences:
		if character in special_characters:
			character = " "
		raw_sentences = raw_sentences + character
	#print(raw_sentences)
	bag_of_words = []
	ini_bag_of_words = raw_sentences.split(" ")
	for word in ini_bag_of_words:
		temp_word = word.strip()
		if temp_word == "" or temp_word in bag_of_words:
			continue
		else:
			bag_of_words.append(temp_word.lower())
	return bag_of_words
def seperate_attributes_topcv(job):
    inital_description = job['description']
    description_dom = etree.HTML(inital_description)
    first_benefit = ""
    first_requirement = ""
    if "jobBenefits" not in job:
        raw_benefits = description_dom.xpath("//*[contains(text(),'Quyền lợi')]/following-sibling::*")
        print(raw_benefits)
        root = etree.ElementTree.getroot()
        print(root.tag) 
        raw_benefits_str = ""
        for bnf in raw_benefits:
            bnf_str = etree.tostring(bnf,method='html',encoding="unicode")
            raw_benefits_str = raw_benefits_str + bnf_str
        first_benefit = etree.tostring(raw_benefits[0],method='html',encoding="unicode")
        jobBenefits = raw_benefits_str
        job["jobBenefits"] = jobBenefits
    if "experienceRequirements" not in job:
        raw_requirements = description_dom.xpath("//*[contains(text(),'Yêu cầu')]/following-sibling::*")
        requirements_str = ""
        req_length = len(raw_requirements)
        i = 0
        while i < req_length:
            req_str = etree.tostring(raw_requirements[i],method='html',encoding="unicode")
            if(first_benefit == req_str):
                folowing_req_str = etree.tostring(raw_requirements[i-1],method='html',encoding="unicode")
                requirements_str = requirements_str.replace(folowing_req_str,"")
                break
            requirements_str = requirements_str + req_str
            i += 1
        first_requirement =  etree.tostring(raw_requirements[0],method='html',encoding="unicode")
        experienceRequirements = requirements_str
        job["experienceRequirements"] = experienceRequirements 
    #
    if first_requirement.strip() != "":
        std_description = description_dom.xpath("//*[contains(text(),'Mô tả')]/following-sibling::*")
        std_description_str = ""
        i = 0
        std_description_length = len(std_description)
        while i < std_description_length:
            des_str = etree.tostring(std_description[i],method='html',encoding="unicode")
            if first_requirement == des_str:
                folowing_des_str = etree.tostring(std_description[i-1],method='html',encoding="unicode")
                std_description_str = std_description_str.replace(folowing_des_str,"")
                break
            std_description_str = std_description_str + des_str
            i += 1
        job["description"] = std_description_str

    #lay so luong tuyen dung:
    '''
    job_available_node = dom.xpath("//div[@id='col-job-right']//div[@id='box-info-job']//div[@class='job-info-item']//*[contains(text(),'cần tuyển')]/following-sibling::*[1]")
    if(len(job_available_node) == 0):
        job_available_node = dom.xpath("///*[@data-original-title='Số lượng cần tuyển']")
    if(len(job_available_node) > 0):
        job_available_text = job_available_node[0].text
        if "không giới hạn" in job_available_text.lower():
            job["totalJobOpenings"] = 50
        elif "người" in job_available_text.lower():
            num_job_available = (job_available_text.split(" ")[0])
            if(num_job_available.isdigit()):
                job["totalJobOpenings"] = int(num_job_available)
        else:
            job["totalJobOpenings"] = 1
    else:
        job["totalJobOpenings"] = 1
    #print(job["totalJobOpenings"])
    '''
    return job


job = {"@context":"http://schema.org","@type":"JobPosting","title":"Retail Sales Associate - NJ","description":"\n\n<strong>Job Description</strong>\n<div style=\"text-align: center;\"><strong>NOW HIRING </strong></div>\n<div style=\"text-align: center;\"><strong>FULL TIME SALES ASSOCIATES</strong></div>\n<div style=\"text-align: center;\"><strong> FOR THE FOLLOWING SHOWROOM LOCATIONS IN </strong>\n<div style=\"text-align: center;\"><strong>NEW JERSEY:<br /> <br /> </strong></div>\n</div>\n<p></p>\n<div style=\"text-align: center;\"><strong><span style=\"text-decoration: underline;\">NEW JERSEY</span></strong></div>\n<div style=\"text-align: center;\"><strong>East Brunswick</strong></div>\n<div style=\"text-align: center;\"><strong>Hanover</strong></div>\n<div style=\"text-align: center;\"><strong>Lawrenceville</strong></div>\n<div style=\"text-align: center;\"><strong>Raritan</strong></div>\n<div style=\"text-align: center;\"><strong>Paramus</strong></div>\n<div style=\"text-align: center;\"><strong>Watchung<br /> </strong><strong>Woodbridge<br /> </strong></div>\n<div style=\"text-align: center;\"></div>\n<div style=\"text-align: center;\"><strong><br /> The Sales Position includes but is not limited to:</strong></div>\n<ul>\n<li>Helping customers select merchandise by explaining the features and benefits of each product.</li>\n<li>Selling extended service protection and installations on selected merchandise.</li>\n<li>Gaining product and sales knowledge through various manufacturer and in-house training programs.</li>\n<li>Entering the sale in our computerized Point of Sale system, including customer, product, pricing, delivery, order status and payment information. Follow up on open orders through completion.</li>\n<li>Promoting our P.C. Richard and Son credit card and processing the applications through a computerized program.</li>\n<li>Providing excellent customer service before, during and after the sale in person and over the telephone.</li>\n</ul>\n<p><br /> <strong>*All new P.C. Richard & Son sales counselors must attend a two week paid in-house training program prior to being placed in a showroom location, to learn corporate culture, selling techniques, product knowledge, and internal computer system.<br /> <br /> Visit  [ Link Removed ]  for more company information and locations</strong></p>\n<p></p>\n\n<strong>Job Requirements</strong>\n<strong>Must be flexible with hours in order to work a retail schedule, including evenings, weekends and holidays. </strong><br />\r<ul>\r    <li>To be a successful P.C Richard & Son sales counselor, you must possess excellent interpersonal skills with the ability to work as a team player in a fast paced environment.  </li>\r    <li>The ideal candidate must be motivated to create a good shopping experience for our customers and to build customer loyalty for future business.  </li>\r    <li>If you desire a career with a Company who has a proven reputation of \"Honesty, Integrity and Reliability,\" and provides the opportunity to earn top income, then apply to join the P.C. Richard & Son Winning Team!</li>\r</ul>\r<p></p>\r<ul>\r</ul>\rExcellent <strong>BENEFITS </strong>available including: <br />\r<br />\r<ul>\r    <li>Health Plan Options providing comprehensive coverage for the employee and family (if applicable).</li>\r    <li>Health Savings Account (if applicable).</li>\r    <li>Voluntary Vision & Dental Plan.</li>\r    <li>Life Insurance and Supplemental Insurance Programs.</li>\r    <li>401k Retirement Savings Plan with a discretionary annual Company match, Flexible Spending Plan and an Employee Discount.</li>\r    <li>Accrued Vacation Time</li>\r    <li>If you desire a career with a Company who has a proven reputation of \"Honesty, Integrity and Reliability,\" and provides the opportunity to earn top income, then apply to join the P.C. Richard & Son Winning Team!</li>\r</ul>\r<p></p>\r<ul>\r</ul>\r<div style=\"text-align: center\"><em>P.C. Richard & Son is an Equal Opportunity Employer</em></div>","estimatedSalary":{"@type":"MonetaryAmountDistribution","currency":"USD","unitText":"HOUR","percentile10":9.9,"median":12.45,"percentile90":21.65},"industry":"Household Appliance Stores","datePosted":"2019-10-19T01:08:19Z","validThrough":"2019-11-18T23:59:59Z","employmentType":["FULL_TIME"],"hiringOrganization":{"@type":"Organization","@id":"C8B1VT5YRWJDHW5SGDK","name":"P.C. Richard & Son","image":"https://secure.icbdr.com/MediaManagement/YV/Mwt3N668J82YWBW8MYV.jpg","logo":"https://secure.icbdr.com/MediaManagement/Y0/M7V5GZ6PTL6VD5VM9Y0.jpg","sameAs":"http://www.pcrichard.com","url":"http://www.pcrichard.com"},"jobLocation":{"@type":"Place","address":{"@type":"PostalAddress","addressLocality":"Watchung","addressRegion":"NJ","streetAddress":"1515 U.S. 22","postalCode":"07069","addressCountry":"US"},"geo":{"@type":"GeoCoordinates","latitude":"40.64043220","longitude":"-74.42253730"}},"educationRequirements":"None","occupationalCategory":["41-2031.00","Retail Salespersons"],"qualifications":"Must be flexible with hours in order to work a retail schedule, including evenings, weekends and holidays. * To be a successful P.C Richard & Son sales counselor, you must possess excellent interpersonal skills with the ability to work as a team player in a fast paced environment. * The ideal candidate must be motivated to create a good shopping experience for our customers and to build customer loyalty for future business. * If you desire a career with a Company who has a proven reputation of \"Honesty, Integrity and Reliability,\" and provides the opportunity to earn top income, then apply to join the P.C. Richard & Son Winning Team!","responsibilities":"* Helping customers select merchandise by explaining the features and benefits of each product. * Selling extended service protection and installations on selected merchandise. * Gaining product and sales knowledge through various manufacturer and in-house training programs. * Entering the sale in our computerized Point of Sale system, including customer, product, pricing, delivery, order status and payment information. Follow up on open orders through completion. * Promoting our P.C. Richard and Son credit card and processing the applications through a computerized program. * Providing excellent customer service before, during and after the sale in person and over the telephone.","jobBenefits":"* Health Plan Options providing comprehensive coverage for the employee and family (if applicable). * Health Savings Account (if applicable). * Voluntary Vision & Dental Plan. * Life Insurance and Supplemental Insurance Programs. * 401k Retirement Savings Plan with a discretionary annual Company match, Flexible Spending Plan and an Employee Discount. * Accrued Vacation Time * If you desire a career with a Company who has a proven reputation of \"Honesty, Integrity and Reliability,\" and provides the opportunity to earn top income, then apply to join the P.C. Richard & Son Winning Team! P.C. Richard & Son is an Equal Opportunity Employer","skills":"Selling Techniques, Scheduling, Customer Service, Sales, Retailing, Loyalty Programs, Point Of Sale","workHours":"evenings, weekends and holidays","salaryCurrency":"USD","identifier":{"@type":"PropertyValue","propertyID":"jobID","value":"NJ Retail Sales"},"url":"https://www.careerbuilder.com/job/JHL6FM6NXYSC8M9LF2W"}
des = job["description"]
#print(des)
des_removed_tags = remove_tags(des).strip()
#print(des_removed_tags)
eng_words = split_word(des_removed_tags)
#print(len(eng_words))
#print(eng_words[0:10])
result = detect(des_removed_tags)
#

#print(result2)
error_job = {"@context":"http:\/\/schema.org\/","@type":"JobPosting","title":"Nh\u00e2n vi\u00ean K\u1ebf to\u00e1n C\u00f4ng n\u1ee3","description":"<h2>M\u00f4 t\u1ea3 c\u00f4ng vi\u1ec7c<\/h2>\n1. L\u00e0m Debit Notes m\u1ed7i khi xu\u1ea5t h\u00e0ng, theo d\u00f5i c\u00f4ng n\u1ee3 ph\u1ea3i thu.\r\n2. Theo d\u00f5i c\u00f4ng n\u1ee3, h\u1ee3p \u0111\u1ed3ng \" Ph\u1ea3i tr\u1ea3 \" Kh\u00e1ch h\u00e0ng, cu\u1ed1i th\u00e1ng ki\u1ec3m tra \u0111\u1ed1i chi\u1ebfu c\u00f4ng n\u1ee3, ch\u1ed1t s\u1ed1 l\u01b0\u1ee3ng h\u00f3a \u0111\u01a1n, li\u00ean h\u1ec7 kh\u00e1ch h\u00e0ng l\u1ea5y h\u00f3a \u0111\u01a1n, s\u1eafp x\u1ebfp theo th\u1ee9 t\u1ef1 , l\u01b0u theo th\u00e1ng, g\u1eedi k\u1ebf to\u00e1n thu\u1ebf b\u1ed9 g\u1ed1c.\r\n<p>3. Qu\u1ea3n l\u00fd v\u1eadt t\u01b0 c\u00f4ng ty, theo d\u00f5i XU\u1ea4T-NH\u1eacP-T\u1ed0N, l\u00ean k\u1ebf ho\u1ea1ch \u0111\u1ec1 xu\u1ea5t g\u1ecdi v\u1eadt t\u01b0 khi c\u1ea7n thi\u1ebft. C\u1ea5p \u0111\u1ed5i kim, dao, c\u00e1c v\u1eadt t\u01b0 kh\u00e1c v\u00e0 thu\u1ed1c y t\u1ebf cho c\u00f4ng nh\u00e2n.\r\n4. Theo d\u00f5i c\u1eadp nh\u1eadt \" XU\u1ea4T - NH\u1eacP - T\u1ed2N\" m\u00e1y m\u00f3c x\u01b0\u1edfng, cu\u1ed1i th\u00e1ng.\r\n5. Theo d\u00f5i th\u00f4ng b\u00e1o ti\u1ec1n \u0111i\u1ec7n v\u00e0 ti\u1ec1n \u0111i\u1ec7n tho\u1ea1i \u0111\u1ec3 \u0111\u00f3ng ti\u1ec1n k\u1ecbp th\u1eddi, theo d\u00f5i \u0111\u1ec3 l\u1ea5y h\u00f3a \u0111\u01a1n.\r\n6. Ki\u1ec3m tra l\u01b0\u01a1ng, Chi l\u01b0\u01a1ng v\u00e0 \u1ee9ng l\u01b0\u01a1ng cho c\u00f4ng nh\u00e2n theo ng\u00e0y qui \u0111\u1ecbnh.\r\n7. Theo d\u00f5i c\u00e1c h\u1ee3p \u0111\u1ed3ng v\u00e0 h\u1ed3 s\u01a1 h\u1ebft h\u1ea1n \u0111\u1ec3 l\u00e0m l\u1ea1i, k\u00fd l\u1ea1i.\r\n8. Ghi thu chi h\u00e0ng ng\u00e0y. Ghi s\u1ed5 qu\u1ef9.\u00a0\r\n9. Ki\u1ec3m tra ti\u1ec1n tr\u1ee3 c\u1ea5p ch\u1ebf \u0111\u1ed9 b\u1ea3o hi\u1ec3m tr\u1ea3 v\u1ec1 ng\u00e2n h\u00e0ng \u0111\u1ec3 thanh to\u00e1n cho ng\u01b0\u1eddi lao \u0111\u1ed9ng\r\n10. Ki\u1ec3m tra b\u1ea3ng t\u1ed3n nguy\u00ean ph\u1ee5 li\u1ec7u t\u1ed3n v\u00e0 order t\u1eeb k\u1ebf ho\u1ea1ch.\r\n11. L\u00e0m h\u1ee3p \u0111\u1ed3ng, theo d\u00f5i s\u1ed1 l\u01b0\u1ee3ng \u0111i v\u00e0 v\u1ec1, t\u00ednh ti\u1ec1n khi c\u00f3 \u0111\u01a1n h\u00e0ng gia c\u00f4ng ngo\u00e0i.<\/p>\n<h2>Y\u00eau c\u1ea7u \u1ee9ng vi\u00ean<\/h2>\n- C\u00f3 kinh nghi\u1ec7m l\u0129nh v\u1ef1c k\u1ebf to\u00e1n 1 n\u0103m tr\u1edf l\u00ean.\r\n- \u01afu ti\u00ean nh\u1eefng \u1ee9ng vi\u00ean \u0111\u00e3 l\u00e0m c\u00f4ng ty may H\u00e0n Qu\u1ed1c\n<h2>Quy\u1ec1n l\u1ee3i \u0111\u01b0\u1ee3c h\u01b0\u1edfng<\/h2>\n- L\u00e0m vi\u1ec7c trong m\u00f4i tr\u01b0\u1eddng n\u0103ng \u0111\u1ed9ng, chuy\u00ean nghi\u1ec7p c\u00f3 nhi\u1ec1u c\u01a1 h\u1ed9i th\u0103ng ti\u1ebfn.\r\n                                - Cung c\u1ea5p trang thi\u1ebft b\u1ecb \u0111\u1ea7y \u0111\u1ee7 \u0111\u1ec3 ph\u1ee5c v\u1ee5 c\u00f4ng vi\u1ec7c.\r\n                                - \u0110\u01b0\u1ee3c \u0111\u00f3ng BHXH, BHYT, BHTN.\r\n                                - \u0110\u01b0\u1ee3c h\u01b0\u1edfng c\u00e1c ch\u00ednh s\u00e1ch ph\u00fac l\u1ee3i theo quy \u0111\u1ecbnh c\u1ee7a c\u00f4ng ty.\r\n - \u0110\u01b0\u1ee3c \u0111\u00e0o t\u1ea1o, n\u00e2ng cao nghi\u1ec7p v\u1ee5 th\u01b0\u1eddng xuy\u00ean.\r\n- \u0110\u01b0\u1ee3c h\u01b0\u1edfng \u0111\u1ea7y \u0111\u1ee7 c\u00e1c quy\u1ec1n l\u1ee3i theo ph\u00e1p lu\u1eadt Vi\u1ec7t Nam. \r\n- BHXH, BHYT, BHTN. \r\n- C\u01a1m tr\u01b0a t\u1ea1i c\u00f4ng ty.\r\n- Th\u00e1ng l\u01b0\u01a1ng 13\r\n- T\u0103ng l\u01b0\u01a1ng 2 l\u1ea7n\/n\u0103m.\u00a0","identifier":{"@type":"PropertyValue","name":"C\u00f4ng ty TNHH Max Vina","value":18424},"datePosted":"2019-10-08","validThrough":"2019-11-07T23:59:59+07:00","employmentType":"FULL_TIME","hiringOrganization":{"@type":"Organization","name":"C\u00f4ng ty TNHH Max Vina","sameAs":"https:\/\/www.topcv.vn\/cong-ty\/cong-ty-tnhh-max-vina\/18424.html","logo":"https:\/\/www.topcv.vn\/v3\/images\/topcv-logo-gray.png"},"jobLocation":[{"@type":"Place","address":{"@type":"PostalAddress","streetAddress":"47\/80 \u0110\u01b0\u1eddng Ao \u0110\u00f4i, Khu ph\u1ed1 6, Ph\u01b0\u1eddng B\u00ecnh Tr\u1ecb \u0110\u00f4ng A, Qu\u1eadn B\u00ecnh T\u00e2n, Th\u00e0nh ph\u1ed1 H\u1ed3 Ch\u00ed Minh","addressLocality":"47\/80 \u0110\u01b0\u1eddng Ao \u0110\u00f4i, Khu ph\u1ed1 6, Ph\u01b0\u1eddng B\u00ecnh Tr\u1ecb \u0110\u00f4ng A, Qu\u1eadn B\u00ecnh T\u00e2n, Th\u00e0nh ph\u1ed1 H\u1ed3 Ch\u00ed Minh","addressRegion":"H\u1ed3 Ch\u00ed Minh","postalCode":700000,"addressCountry":"Vi\u1ec7t Nam"}}],"baseSalary":{"@type":"MonetaryAmount","currency":"VND","value":{"@type":"QuantitativeValue","unitText":"MONTH","value":"Tr\u00ean 8 tri\u1ec7u","minValue":"8 tri\u1ec7u"}},"skills":"K\u1ebf to\u00e1n \/ Ki\u1ec3m to\u00e1n"}

print(error_job)
string = 'Hôm nay tôi đi học'

a = re.search(r'\b(đi)\b', string)
print(a.start())
print(a.end())
length = len(string)
print(string[0:length])
#normalized_job = seperate_attributes_topcv(error_job)
