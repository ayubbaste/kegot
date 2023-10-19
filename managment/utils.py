import os, json

def clean_db():
    try:
        with open('spiders/base.txt', "r+") as datafile:
            data = json.load(datafile)
            datafile.close()

        # if there are too match records in base file,
        # then leave only 300 newest ones
        if len(data) > 500:
            new_data = data[len(data) - 300:]
            with open('spiders/base.txt', "w+") as exportfile:
                json.dump(new_data, exportfile)
                exportfile.close()
    except:
        pass
