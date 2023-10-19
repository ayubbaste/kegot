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
            vcards = soup.find_all("div", "vacancy-card")

            # Vacancy data
            for vcard in vcards:
                try:
                    vdate = vcard.find("div", "vacancy-card__date").text
                except:
                    vdate = "error"

                try:
                    vcotitle = vcard.find("div", "vacancy-card__company-title").text
                    # remove linebreakes
                    vcotitle = vcotitle.strip().replace('\n', ' ')
                except:
                    vcotitle = "error"

                try:
                    vtitle = vcard.find("a", "vacancy-card__title-link").text
                    # remove linebreakes
                    vtitle = vtitle.strip().replace('\n', ' ')
                except:
                    vtitle = "error"

                try:
                    vsalary = vcard.find("div", "vacancy-card__salary").text
                except:
                    vsalary = "~ ~ ~"

                try:
                    skills = vcard.find("div", "vacancy-card__skills").text
                except:
                    skills = "~ ~ ~"

                try:
                    vurl = "https://career.habr.com" + vcard.find("a", "vacancy-card__title-link")["href"]
                except:
                    pass

                if vurl not in old_data \
                and not any(x in vcotitle.lower() for x in stoplist.companies)\
                and not any(x in vtitle.lower() for x in stoplist.positions):
                    old_data.append(vurl)

                    # Build massages and add them to kegot messages list
                    message = "<b>Habr</b>\n<i>{0}</i>\n<i>Co.</i> {1}\n<i>Vac.</i> <a href='{2}'>{3}</a>\n<i>Sal.</i> {4}\n<i>Skills:</i>\n<i>{5}</i>".format(vdate, vcotitle, vurl, vtitle, vsalary, skills)

                    messages.append(message)

        except:
            messages.append('<b>Habr parse error</b>')

    # And add links to parsed vacancy links file
    with open('spiders/base.txt', "w+") as exportfile:
        json.dump(old_data, exportfile)
        exportfile.close()

    return messages
