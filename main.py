from bs4 import BeautifulSoup
import requests
import time
import csv
import sys

def get_data(soup,company_count,file_name):
	file = "_".join(file_name.split())+'.csv'

	if soup != None:
		company_name = soup.find('h1', class_ = 'header-company--title')
		company_name =  (str((company_name.text).strip().replace("\n",""))) if company_name != None else "Not Specified"
		# print(company_name)

		website = soup.find('a', class_ = 'website-link__item')
		website = website['href']
		website = (str(website[:website.find('/',9)])) if website != None else "Not Specified"
		# print(website[:website.find('/',9)])

		rating = soup.find('span', class_ = 'rating sg-rating__number')
		rating = (str((rating.text).strip().replace("\n",""))) if rating != None else "Not Specified"
		# print(rating)

		reviews = soup.find('a', class_ = 'reviews-link sg-rating__reviews')
		reviews = ((reviews.text).strip().replace("\n","").split()) if reviews != None else ["Not Specified"]
		# print(reviews)

		data = soup.find('div', class_ = 'module-list')
		data = ((data.text).strip().replace("\n"," ").split('      '))
		data[0] = "Not Specified" if data[0] == None else str(data[0])
		data[1] = "Not Specified" if data[1] == None else str(data[1])
		data[2] = "Not Specified" if data[2] == None else str(data[2])
		# print(data)

		location = soup.find('span', class_ = 'city-name')
		location = (str((location.text).strip().replace("\n"," "))) if location != None else "Not Specified"
		# print(location)

		contact = soup.find('a', class_ = 'contact phone_icon')
		contact = (str((contact.text).strip().replace("\n"," "))) if contact != None else "Not Specified"
		# print(contact)

		verification = soup.find('div', class_ = 'verification-status-wrapper')
		verification = ((verification.text).strip().replace("\n"," ").split()) if verification != None else "Not Specified"
		# print(verification)

		status = soup.find('div', class_ = 'field field-name-status')
		status =  ((status.text).strip().replace("\n"," ").split())[-1] if status != None else "Not Specified"
		# print(status)

		company_id = soup.find('div', class_ = 'field field-name-id')
		company_id = ((company_id.text).strip().replace("\n","").split())[-1] if company_id != None else  ["Not", "Specified"]
		# print(company_id)

		update = soup.find('div', class_ = 'field field-name-last-updated')
		update = ((update.text).strip().replace("\n"," ").split()) if update != None else [" "," ", "Not", "Specified"]
		# print(update)

		new_data = [company_name, website, location, contact, rating, reviews[0], 
		data[1], data[0], data[2], " ".join(verification), company_id, " ".join(update[2:]), status]

		print(new_data)

		with open(file, mode='a',newline='', encoding = 'utf8') as f:
			writer = csv.writer(f)
			writer.writerow(new_data)
		with open(file , mode='r',newline='') as f1:
			rowa = csv.reader(f1)
			data_count = len(list(rowa))
			print("New row added to the file")
			print("-" * 90)
		if (data_count-1) == company_count:
			print("Done scraping,  Scrape again? (y/n): ")
			usr_inp = input()
			if 'y' == usr_inp.lower():
				source_req()
			else:
				print("Thank You for scraping")
				sys.exit()


	


def create_file(file_name):
	global file
	file = "_".join(file_name.split())+'.csv'
	try:
		fields = ['Company', 'Website', 'Location', 'Contact', 'Rating', 'Review Count', 'Hourly Rate', 
			 	'Min Project Size', 'Employee Size', 'Verification', 'Company ID', 'Last Updated', 'Status']
		with open(file , mode='w',newline='') as file:
			writer = csv.writer(file)
			writer.writerow(fields)
			print('New file Created for -- ',file_name)
	except:
		print('File Error :(')
		

				


def get_website(websites,company_count,file_name):
	if websites != None:
		for website in websites:

			links = website.find('a')
			links = links['href']

			print("Fetching company details......")
			html_text = requests.get('https://clutch.co'+ str(links))

			if html_text != None:
				soup = BeautifulSoup(html_text.text,'lxml')
				get_data(soup,company_count,file_name)
			else:
				soup = None


def get_domain(sub_domain):
	global page_count,page_no,company_count
	page_count = 1
	page_no = 0
	company_count = 0

	print('https://clutch.co'+str(sub_domain['href']))
	profile_html = requests.get('https://clutch.co'+str(sub_domain['href']+'?page='+str(page_no)))
	# print('https://clutch.co'+str(sub_domain['href']+'?page='+str(page_no)))
	profile_soup = BeautifulSoup(profile_html.text,'lxml')
	total_count = profile_soup.find('div', class_ = 'tabs-info')
	create_file(sub_domain.text)

	if total_count != None:
		total_count = (total_count.text).split()

	if page_count == 1:
		print('Enter companies count limit for scraping 10 - {}'.format(total_count[0]))
		company_count = input("==>>")

	while(page_no <= int(page_count)):
		profile_html = requests.get('https://clutch.co'+str(sub_domain['href']+'?page='+str(page_no)))
		# print('https://clutch.co'+str(sub_domain['href']+'?page='+str(page_no)))
		profile_soup = BeautifulSoup(profile_html.text,'lxml')

		if profile_soup != None:
			websites = profile_soup.find_all('li', class_ = 'website-profile')
			print("Domain Name: ",sub_domain.text)
			#getting total pages
			pages = profile_soup.find('li',class_ = 'page-item last')
			page_count = (pages.find('a'))['data-page']
			# print(page_count,page_no)
			page_no += 1

			get_website(websites,int(company_count),sub_domain.text)

		else:
			websites = None


def source_req():
	time.sleep(4)
	try:
		print("Requesting server....")
		source = requests.get('https://clutch.co/').text
		source_soup = BeautifulSoup(source,'lxml')
		domains = source_soup.find_all(class_ = 'sitemap-nav__item', href = True)
		# print("checking")
		i = 0
		for domain_options in domains:
			i+=1
			print(i,'-'.join(domain_options.text.split()))
		domain_selected = input("Enter index of choice:\n==>>")
		domain_selected = domains[int(domain_selected)-1]
		# print(domain_selected)
		get_domain(domain_selected)
	except Exception as e:
		if "('Connection aborted.', gaierror(11001, 'getaddrinfo failed'))" == str(e):
			time.sleep(2)
			print("..............")
			source_req()
		else:
			exit()


# exit()

if __name__ == '__main__':
	source_req()
