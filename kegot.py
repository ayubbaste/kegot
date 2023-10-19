import os, emoji, json, sender
from managment.utils import clean_db
from spiders import habr, linkedin, indeed
from sources import python_sources, python_stoplist, frontend_sources, frontend_stoplist
from dotenv import load_dotenv
load_dotenv() 


# python recipients & messages to send
python_recipients = os.getenv('PYTHON_RECIPIENTS')
channel_name = "Python developer vacancies"
python_messages = []
# get vacancies
python_messages += habr.get_vacancies(python_sources.habr_urls,
                                      python_stoplist)
python_messages += linkedin.get_vacancies(python_sources.linkedin_urls,
                                          python_stoplist)
python_messages += indeed.get_vacancies(python_sources.indeed_urls,
                                        python_stoplist)
# send messages
sender.send_messages(python_recipients, python_messages, channel_name)


# frontend recipients & messages to send
frontend_recipients = os.getenv('FRONTEND_RECIPIENTS')
channel_name = "Frontend developer vacancies"
frontend_messages = []
# get vacancies
frontend_messages += habr.get_vacancies(frontend_sources.habr_urls,
                                        frontend_stoplist)
# send messages
sender.send_messages(frontend_recipients, frontend_messages, channel_name)

# remove oldest vacancies from the base file
clean_db()
