def extract(url, params = None):
    '''
    .env 파일으로 보호된 접근 정보를 사용하여 api 데이터 호출 함수
    '''
    import requests
    import xmltodict

    if params:
        response = requests.get(url, params = params)
        html = response.text
        html_dict = xmltodict.parse(html)
        return html_dict
    
    # 어떤 형태로 리퀘스트 하며 
    # param이 없어도 독립실행 가능한 케이스가 있는지 추가 학습 필요
    # 일반적으로 json 파일로 바로 받을 수 있음, cp1과 유사
    # 수정필요
    else:
        response = requests.get(url)
        html = response.text
        html_dict = xmltodict.parse(html)
        return html_dict