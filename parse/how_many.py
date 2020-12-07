import json

with open('mem_dataset.json', 'r', encoding='utf-8') as mem:
    data = json.load(mem)
    print(len(data.keys()))