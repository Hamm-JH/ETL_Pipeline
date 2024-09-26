def save_local(json_data):
    '''
    불러온 json 데이터를 로컬에 저장하는 함수
    '''
    import json
    
    path = 'CP2/data.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)