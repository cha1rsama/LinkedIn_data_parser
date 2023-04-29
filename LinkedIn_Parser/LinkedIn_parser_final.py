
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
import pandas as pd

# options

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# input of job/location
job_name = input("Please add the targeting job:\n")
country_name = input("Please add the target location:\n")
driver_service = Service(
    executable_path="C:/Users/akbar/PycharmProjects/pythonProject/selenium_project/chrome_driver/chromedriver.exe")
driver = webdriver.Chrome(service=driver_service, options=options)

# here we make input to the right format
job_url = ""
for item in job_name.split(" "):
    if item != job_name.split(" ")[-1]:
        job_url = job_url + item + "%20"
    else:
        job_url = job_url + item

country_url = ""
for item in country_name.split(" "):
    if item != country_name.split(" ")[-1]:
        country_url = country_url + item + "%20"
    else:
        country_url = country_url + item

rawlink = "https://www.linkedin.com/jobs/search?keywords={0}&location={1}"
url = rawlink.format(job_url, country_url)

# Opening the url we have just defined in our browser
driver.get(url)
for element in driver.find_elements(By.XPATH, "//div[@class='results-context-header']//h1[@class='results-context-header__context']//span[@class='results-context-header__job-count']"):
    jobs_num = int(element.text.replace(" ", ""))

# this is indicator showing that we browsed till the end
try:
    b = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/section[2]/div/p")
except Exception:
    pass
# while loop is scrolling down intil it see the indicator
i = 2

while i <= int(jobs_num/2)+1:
    # We keep scrolling down to the end of the view.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    i = i + 1
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(1, document.body.scrollHeight);")
    try:
        if b.is_displayed():
            break
    except Exception:
        pass
# this is button clicker, Linked in asks to click on it after a while scrolling
    try:
        # We try to click on the load more results buttons in case it is already displayed.
        infinite_scroller_button = driver.find_element(By.XPATH, ".//button[@aria-label='См. еще вакансии']")
        infinite_scroller_button.click()
        time.sleep(1.5)
    except(Exception,):
        # If there is no button, there will be an error, so we keep scrolling down.
        time.sleep(0.1)
        pass
job_lists = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
jobs = job_lists.find_elements(By.TAG_NAME, "li")  # return a list

job_title = []
company_name = []
location = []
date = []
job_link = []

for job in jobs:

    job_title0 = job.find_element(By.CSS_SELECTOR, "h3").get_attribute("innerText")
    job_title.append(job_title0)

    company_name0 = job.find_element(By.CSS_SELECTOR, "h4").get_attribute("innerText")
    company_name.append(company_name0)

    location0 = job.find_element(By.CLASS_NAME, "job-search-card__location").get_attribute("innerText")
    location.append(location0)

    date0 = job.find_element(By.CSS_SELECTOR, "div > div > time").get_attribute("datetime")
    date.append(date0)

    job_link0 = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    job_link.append(job_link0)

print(len(company_name), "- Jobs found!")
# here we created the lists where we store the data
jd = []
seniority = []
emp_type = []
job_func = []
industries = []
# this loop clicks on each job posting so we get the inside data stored
for item in range(len(jobs)):
    job_func0 = []
    industries0 = []
    # clicking job to view job details
    job_click_path = f"/html/body/div[1]/div/main/section[2]/ul/li[{item + 1}]"
    more_info_path = "/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/button[1]"
    time.sleep(3)
    job.find_element(By.XPATH, job_click_path).click()
    time.sleep(3)
    job.find_element(By.XPATH, more_info_path).click()
    # time.sleep(3)


    print("Current at: ", int(item+1), "Percentage at: ", int(item + 1) / len(jobs) * 100, "%")
    jd_path = "/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div"
    jd0 = job.find_element(By.XPATH, jd_path).get_attribute("innerText").replace("\n", " ")
    jd.append(jd0)

    seniority_path = "/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[1]/span"
    try:
        seniority0 = job.find_element(By.XPATH, seniority_path).get_attribute("innerText")
        seniority.append(seniority0)
    except:
        seniority0 = "-"
        seniority.append(seniority0)

    # ---------------------------------------------------------------
    emp_type_path = "/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[2]/span"
    try:
        emp_type0 = job.find_element(By.XPATH, emp_type_path).get_attribute("innerText")
        emp_type.append(emp_type0)
    except:
        emp_type0 = "-"
        emp_type.append(emp_type0)

    # ---------------------------------------------------------------
    job_func_path = "/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[3]/span"
    try:
        job_func_elements = job.find_element(By.XPATH, job_func_path).get_attribute("innerText")
        job_func.append(job_func_elements)
    except:
        job_func_final = "no info"
        job_func.append(job_func_final)

    # ---------------------------------------------------------------
    industries_path = "/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[4]/span"
    try:
        industries_elements = job.find_element(By.XPATH, industries_path).get_attribute("innerText")
        industries.append(industries_elements)
    except:
        industries_final = "no info"
        industries.append(industries_final)

#  we create pandas dataframe and then convert it to the JSON
d = ({
    'Date Posted': date,
    'Company Name': company_name,
    'Job Title': job_title,
    'Job Location': location,
    'Description': jd,
    'Years of Experience Required': seniority,
    'Employment Type': emp_type,
    'Skills Required': job_func,
    'Job Market': industries,
    'Contact Link': job_link
})

df = pd.DataFrame(data=d)

driver.minimize_window()
json_nam = input("Please write name to save JSON file:\n")
df.to_json(json_nam + ".json", orient="index")
