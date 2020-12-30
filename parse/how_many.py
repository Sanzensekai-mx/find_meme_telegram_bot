import json

with open('mem_dataset.json', 'r', encoding='utf-8') as mem:
    data = json.load(mem)
    print(f'Mem_dataset - {len(data.keys())}')

with open('old_mem_dataset.json', 'r', encoding='utf-8') as mem:
    data = json.load(mem)
    print(f'OLD_mem_dataset - {len(data.keys())}')
