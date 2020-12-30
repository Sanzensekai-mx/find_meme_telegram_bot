import json

with open('old_mem_dataset.json', 'w', encoding='utf-8') as old_meme, \
        open('mem_dataset.json', 'r', encoding='utf-8') as now_old_meme:
    current_old_memes = json.load(now_old_meme)
    json.dump(current_old_memes, old_meme, indent=4, ensure_ascii=False)
