import sys
import os

# ./Project 폴더 위치를 추가한다 (Project 폴더에 있는 모듈을 import 할 수 있도록)
# Project 폴더 내부의 코드 간에 import 할 때 root에서부터 참조하지 않고 
# 상대경로를 사용한다
sys.path.append(os.path.join(os.path.curdir, "Project")) 