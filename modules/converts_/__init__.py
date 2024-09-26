
print('this is modules/converts_ __init__.py')

# TODO : 프로젝트별로 굉장히 의존성이 큰 코드는 주요 코드에 넣지 않기
def convert_method_to_int(method):
    """ method를 int로 변환하는 함수 """
    if method == 'POST':
        return 1
    elif method == 'GET':
        return 2
    elif method == 'PUT':
        return 3
    elif method == 'DELETE':
        return 4
    else:
        return 0