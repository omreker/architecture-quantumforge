import os
import json
import re


dir = "knowledge_base"
tm_path = "terms_map.json"

with open(tm_path, "r", encoding="utf-8") as f:
    terms_map = json.load(f)


def replace_all_terms(text, mapping):
    sorted_keys = sorted(mapping.keys(), key=len, reverse=True)

    for key in sorted_keys:
        pattern = re.compile(r'\b' + re.escape(key) + r'\b', re.IGNORECASE)
        text = pattern.sub(mapping[key], text)
    return text


files = [f for f in os.listdir(dir) if f.endswith(
    '.md') or f.endswith('.txt')]

for filename in files:
    file_path = os.path.join(dir, filename)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = replace_all_terms(content, terms_map)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    new_filename = filename
    for key, val in terms_map.items():
        file_key = key.replace(" ", "_")
        file_val = val.replace(" ", "_")

        if file_key.lower() in new_filename.lower():
            new_filename = re.sub(file_key, file_val,
                                  new_filename, flags=re.IGNORECASE)

    if new_filename != filename:
        new_file_path = os.path.join(dir, new_filename)
        os.rename(file_path, new_file_path)
