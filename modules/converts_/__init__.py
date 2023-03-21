
print('this is modules/converts_ __init__.py')

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