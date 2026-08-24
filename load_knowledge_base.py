import os
import shutil
import re
import requests
from bs4 import BeautifulSoup


output_dir = "knowledge_base"

if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

os.makedirs(output_dir, exist_ok=True)

entities = [
    "Артас_Менетил", "Тралл", "Джайна_Праудмур", "Иллидан_Ярость_Бури",
    "Ледяная_Скорбь", "Тёмный_портал", "Король-лич",
    "Первая_война",
    "Запределье", "Лордерон", "Восточные_королевства",
    "Азерот", "Древние_боги", "Бездна", "Дарнасский",
    "Ночные_эльфы", "Война_Древних", "Пылающий_Легион", "Орки",
    "Дренор", "Утер_Светоносный", "Альянс",
    "Орда", "Калимдор", "Нордскол", "Ледяной_Трон",
    "Малфурион_Ярость_Бури", "Плеть", "Рыцари_Черного_Клинка",
    "Ледяная_Корона"
]

base_url = "https://wowwiki.fandom.com/ru/wiki/"

for entity in entities:
    url = f"{base_url}{entity}"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    content_div = soup.find(class_="mw-parser-output")

    if content_div is None:
        print(f"Пропущено (нет контента): {entity}")
        continue

    for element in content_div.find_all(['table', 'aside', 'script', 'style', 'div']):
        element.decompose()

    clean_text = content_div.get_text(separator="\n")

    clean_text = re.sub(r'\[\s*\d+\s*\]', '', clean_text)
    clean_text = re.sub(r'\[.*?\]', '', clean_text)
    clean_text = re.sub(r'[A-Za-z]+', '', clean_text)
    clean_text = re.sub(r'[^\w\sА-Яа-яЁё.,!?;:()\-—«»"]', '', clean_text)
    clean_text = re.sub(r'\n\s*\n+', '\n\n', clean_text)
    clean_text = re.sub(r'[ \t]+', ' ', clean_text)
    clean_text = clean_text.strip()

    filename = f"{entity.replace('/', '_')}.md"
    filepath = os.path.join(output_dir, filename)

    entity_name_ru = entity.replace('_', ' ')

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {entity_name_ru}\n\n")
        f.write(clean_text)

    print(f"Success saved in {filepath}")
