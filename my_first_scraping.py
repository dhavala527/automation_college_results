from selenium import webdriver
import pandas as pd
from BeautifulSoup import BeautifulSoup

def get_tuple(res):
	return (x for x in res)

def scrape_results(reg_no):
	PRE_URL = 'http://202.53.81.85/pvp32/index.html'
	#reg_no = '14501A0527'
	browser = webdriver.Chrome('/home/don/chromedriver')
	browser.get(PRE_URL)
	browser.find_element_by_xpath('//*[@id="AutoNumber1"]/tbody/tr[1]/td[2]/p/input').send_keys(reg_no)
	browser.find_element_by_xpath('//*[@id="AutoNumber1"]/tbody/tr[2]/td/center/input').click()

	soup = BeautifulSoup(browser.page_source)

	fail_cnt = 0

	user_data, user_data_saved = '', ''
	s = list()
	for rec in soup.findAll('tr'):
		my_str = rec.text
		if 10 < len(my_str):
			if my_str[-4:] == 'PASS' or my_str[-4:] == 'FAIL':
				if my_str[-4:] == 'PASS':
					gr = -1
					if my_str[-6:-4] == '10':
						gr = 10
					else:
						gr = int(my_str[-5])
				else:
					gr = 0
					fail_cnt += 1
				s.append(gr)
		if len(my_str) > 5:
			if my_str[:3] == 'SEM':
				sgpa = my_str.index('SGPA')
				cgpa = my_str.index('CGPA')
				s.append(float(my_str[sgpa+4:cgpa]))
				s.append(float(my_str[cgpa+4:]))
		if len(my_str) > 20:
			if my_str[:20] == 'BRANCH WISE SEM RANK':
				bwsr = my_str.index('BRANCH WISE SEM RANK:')
				cwsr = my_str.index('COLLEGE WISE SEM RANK:')
				s.append(int(my_str[bwsr+21:cwsr]))
				s.append(int(my_str[cwsr+22:]))
		if len(my_str) > 23:
			if my_str[:23] == 'BRANCH WISE CUMM.. RANK':
				bwsr = my_str.index('BRANCH WISE CUMM.. RANK:')
				cwsr = my_str.index('COLLEGE WISE CUMM.. RANK:')
				s.append(int(my_str[bwsr+24:cwsr]))
				s.append(int(my_str[cwsr+25:]))
	if fail_cnt > 0:
		for i in range(4):
			s.append(-1)
	s.append(reg_no)
		#print my_str
	browser.close()
	print s	
	return s
	
rec_list = list()

for i in range(1, 100):
	if i < 10:	
		res = scrape_results('14501A050'+str(i))
	else:
		res = scrape_results('14501A05'+str(i))
	rec_dict = get_tuple(res)
	rec_list.append(rec_dict)


x = 'AB'	
for j in x:
	for i in range(10):
		res = scrape_results('14501A05'+j+str(i))
		rec_dict = get_tuple(res)
		rec_list.append(rec_dict)
res = scrape_results('14501A05C0')
rec_list.append(get_tuple(res))


for i in range(1,25):
	if i < 10:
		res = scrape_results('15505A050'+str(i))
	else:
		res = scrape_results('15505A05'+str(i))
	rec_dict = get_tuple(res)
	rec_list.append(rec_dict)


labels = ['CS6L1', 'CS6L2', 'CS6L3', 'CS6L4', 'CS6L5', 'CS6T1', 'CS6T2', 'CS6T3', 'CS6T4', 'CS6T5', 'SGPA', 'CGPA', 'BWSR', 'CWSR', 'BWCR', 'CWCR', 'RegNo']
df = pd.DataFrame.from_records(rec_list, columns=labels)

#print df

df.to_csv('results.csv')
