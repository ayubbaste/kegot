import os, json, requests
from bs4 import BeautifulSoup


def get_vacancies(urls, stoplist): 
    # Create or open a file with old parsed vacancies links
    try:
        with open('spiders/base.txt', "r+") as datafile:
            old_data = json.load(datafile)
            datafile.close()
    except:
        with open('spiders/base.txt', "w+") as datafile:
            old_data = []
            json.dump(old_data, datafile)
            datafile.close()

    messages = []

    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        try:
            vcards = soup.find("ul", "jobsearch-ResultsList").find_all("div", "cardOutline")

            # Vacancy data
            for vcard in vcards:
                try:
                    vdate = vcard.find("span", "date").text
                except:
                    vdate = "error"

                try:
                    vcotitle = vcard.find("span", "companyName").text
                except:
                    vcotitle = "error"

                try:
                    vcolocation = vcard.find("div", "companyLocation").text
                except:
                    vcolocation = "error" 

                try:
                    vtitle = vcard.find("a", "jcs-JobTitle").text
                except:
                    vtitle = "error" 

                try:
                    vsalary = vcard.find("span", "estimated-salary").text
                except:
                    vsalary = "~ ~ ~"


                try:
                    vurl = vcard.find("a", "jcs-JobTitle")["href"]
                    vurl = "https://www.indeed.com/viewjob?" + vurl.split("?", 1)[1].split("&")[0]
                except:
                    vurl = "error" 


                if vurl not in old_data \
                and not any(x in vcotitle.lower() for x in stoplist.companies)\
                and not any(x in vtitle.lower() for x in stoplist.positions):
                    old_data.append(vurl)

                    # Build massages and add them to kegot messages list
                    message = "<b>Indeed</b>\n<i>{0}</i>\n<i>Co.</i> {1}\n<i>Vac.</i> <a href='{2}'>{3}</a>\n<i>Sal.</i> {4}".format(vdate, vcotitle, vurl, vtitle, vsalary)

                    messages.append(message)
        except:
            messages.append('<b>Indeed parse error</b>')


    # And add links to parsed vacancy links file
    with open('spiders/base.txt', "w+") as exportfile:
        json.dump(old_data, exportfile)
        exportfile.close()

    return messages
