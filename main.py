import requests
from bs4 import BeautifulSoup
import json


def pageContent(pageNumber):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
    url = f'https://www.python.org.ar/trabajo/?page={pageNumber}'
    r = requests.get(url, headers)
    content = BeautifulSoup(r.content, 'html.parser')

    return content


def getTotalPages():
    site = pageContent(1)
    pagination = site.find('div', class_ = 'pagination')
    pages = pagination.find_all('a', class_ = 'page')
    lastPage = pages[len(pages)-1].text

    return int(lastPage)


def getLinks(page):
    links = []

    container = page.find('div', class_ = 'col-md-12')
    list = container.find_all('h4')
    
    for item in list:
        link = 'https://www.python.org.ar' + item.a['href']

        links.append(link)

    return links

def getAllLinks():
    links = []

    for i in range(1, getTotalPages()+1):
        page = pageContent(i)
        links.extend(getLinks(page))
    
    return links


def getJobInfo(link):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
    r = requests.get(link, headers)
    content = BeautifulSoup(r.content, 'html.parser')

    jobDetails = content.find_all('dd')

    try:
        job = {
        'name': content.find('div', class_ = 'page-header').h2.text.strip(),
        'location': jobDetails[1].text.strip(),
        'company': jobDetails[2].text.strip(),
        'email': jobDetails[5].text.strip(),
        'link': link,
        }
    except:
        job = {
        'name': '',
        'location': '',
        'company': '',
        'email': '',
        'link': link,
        }

    return job


def getJobs():
    print("Getting jobs. Please wait...")
    
    links = getAllLinks()
    jobs = []

    print("Saving jobs...") 

    for link in links:
        job = getJobInfo(link)
        jobs.append(job)

    with open('jobs.json', 'w') as file:
        json.dump(jobs, file, indent=2)

    print(f'{len(jobs)} jobs has been saved on file: {file.name}')

    
if __name__ == '__main__':
    getJobs()
