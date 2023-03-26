
from abc import abstractmethod


class Core:
    """ 
    Core 클래스
    수집하고자 하는 데이터별로 상속받아서 사용한다.
    프로젝트 단위로 수행할 내용의 원형을 정의한다.
    """
    def __init__(self, env):
        self.env = env
        pass

    @abstractmethod
    def extract_url(self, url):
        """ url에서 데이터를 추출하는 함수 """
        pass

    @abstractmethod
    def transform_data(self, data):
        """ 데이터를 변환하는 함수. 단일 데이터를 대상으로 한다. """
        pass

    @abstractmethod
    def load_data(self, data):
        """ 데이터를 저장하는 함수 """
        pass
