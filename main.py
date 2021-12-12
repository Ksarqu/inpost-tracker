from requests import get
from time import sleep
from os import system as command
import json
import os

check_list = []

lang_files_dir = "languages"
lang_files = os.listdir(lang_files_dir)
languages_data = {}
for file in lang_files:
    language = file.split(".")[0]  # separates the filename from the extension
    with open(f"{lang_files_dir}\\{file}", "r", encoding="utf-8") as current_file:
        languages_data[language] = json.load(current_file)

if not os.path.isfile("config.json"):
    with open("config.json", 'w', encoding="utf-8") as config_file:
        config_data = {"language": "en"}
        json.dump(config_data,
                  config_file,
                  indent=4,
                  sort_keys=True)
        print("Please edit the config file as you want!")
        exit()
else:
    with open("config.json", "r") as config_file:
        config_data = json.load(config_file)
        lang = config_data["language"]


status_codes = ["Przygotowana przez Nadawcę.",
                "Odebrana od klienta.",
                "Przyjęta w Sortowni.",
                "Przyjęta w oddziale InPost.",
                "Umieszczona w Paczkomacie (odbiorczym)."]

# thats site status codes, not the printed out :)

trackcode = input(languages_data[lang]["enter_track_code"])

if len(trackcode) == 24:

    for character in trackcode:
        check_list.append(character.isalpha())

    if True in check_list:
        print(languages_data[lang]["wrong_code"])

    else:
        print(languages_data[lang]["warner"])
        while True:
            r = get(f"https://furgonetka.pl/zlokalizuj/{trackcode}/inpost")
            for code in status_codes:
                if code in r.text:
                    print(languages_data[lang][code])
            sleep(60)
            command("cls")

else:
    print(languages_data[lang]["invalid_length"])
