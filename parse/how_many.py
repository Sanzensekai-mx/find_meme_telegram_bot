import json

with open('mem_dataset.json', 'r', encoding='utf-8') as meme_new:
    data_new = json.load(meme_new)
    print(f'Mem_dataset - {len(data_new.keys())}')
    with open('old_mem_dataset.json', 'r', encoding='utf-8') as meme_old:
        data_old = json.load(meme_old)
        print(f'OLD_mem_dataset - {len(data_old.keys())}')
    for i in set(data_new.keys()) - set(data_old.keys()):
        print(i)
    # print(set(data_new.keys()) - set(data_old.keys()))
