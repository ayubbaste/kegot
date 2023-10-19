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
            vcards = soup.find_all("div", "base-card")

            # Vacancy data
            for vcard in vcards:
                try:
                    vdate = vcard.find("time")["datetime"]
                except:
                    vdate = "error"

                try:
                    vcotitle = vcard.find("h4", "base-search-card__subtitle").text
                    # remove linebreakes
                    vcotitle = vcotitle.strip().replace('\n', ' ')
                except:
                    vcotitle = "error"

                try:
                    vtitle = vcard.find("h3", "base-search-card__title").text
                    # remove linebreakes
                    vtitle = vtitle.strip().replace('\n', ' ')
                except:
                    vtitle = "error" 

                try:
                    vurl = vcard.find("a", "base-card__full-link")["href"]
                    vurl = vurl.split("?", 1)[0]
                except:
                    vurl = "error" 

                if vurl not in old_data \
                and not any(x in vcotitle.lower() for x in stoplist.companies)\
                and not any(x in vtitle.lower() for x in stoplist.positions):
                    old_data.append(vurl)

                    # Build massages and add them to kegot messages list
                    message = "<b>LinkedIn</b>\n<i>{0}</i>\n<i>Co.</i> {1}\n<i>Vac.</i> <a href='{2}'>{3}</a>".format(vdate, vcotitle, vurl, vtitle)

                    messages.append(message)

        except:
            messages.append('<b>LinkedIn parse error</b>')


    # And add links to parsed vacancy links file
    with open('spiders/base.txt', "w+") as exportfile:
        json.dump(old_data, exportfile)
        exportfile.close()

    return messages
