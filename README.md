# ASTS Server

### 실행 방법

1. [Docker](https://docs.docker.com/docker-for-windows/install/) 다운로드 
2. docker를 실행하고 준비가 완료 되었는지 확인
3. docker-compose up -d 명령어를 프로젝트 디렉토리에서 실행
4. docker ps 명령어를 실행해서 프로세스가 현재 잘 올라가 있는지 확인

아래 포트 번호를 사용해서 app과 kibana에 접속 할 수 있습니다.

##### Port
* app : 80 (프록시 서버를 이용, 웹 서버 포트는 8000)
* elasticsearch : 9200,9300
* postgresql : 5432
* kibana : 5601
* logstash :

예시) http://localhost:5601/ <-- kibana 접속

현재 app에 접속해 Postgresql DB의 employee 테이블에 데이터를 추가하면 동기화 되고있는 Elasticsearch 에도 값이 저장됩니다. 

##### DB에 저장 하는 방법
1. http://localhost/api 접속
2. department url 클릭
3. Title 에 넣고싶은 이름 기입후 POST 버튼 클릭이번주
4. http://localhost/api로 다시 접속
5. employee url 클릭   
6. Fullname과 Department는 필수 필드이기 때문에 기입후 POST 버튼 클릭
7. 저장 완료

##### DB에 수정과 삭제 하는 방법
1. http://localhost/api/id/  << 직원의 id 값을 추가

`예시) http://localhost/api/1/` 
2. 저장과 유사한 방식으로 진행
3. Fullname 과 Department는 필수 필드이기 때문에 항상 기입
4. 수정,삭제 완료

##### 확인하는 방법
1. http://localhost/api 접속
2. 부서를 추가하고 직원을 추가
3. http://localhost:5601 키바나 접속
4. 키바나 페이지에서 dashboard 로 이동
5. Check for new data라는 문구가 뜨면 데이터가 삽입될 때까지 기다리고 Check for new data 클릭
6. Index Pattern에 * 작성
7. Time Filter field name에 `I don`t want to use the Time Filter` 선택, 없으면 스킵
8. Refresh 버튼을 눌러 실시간으로 데이터가 동기화되는 모습 확인

##### 개발하는 방법
1. docker에 sugarpowder/asts:latest 를 제외하고 나머지 모듈이 전부 켜져있어야 한다.
2. docker-compose up -d 명령어를 실행한 이후에 sugarpowder/asts:latest 만 삭제한다.
3. docker rm [컨테이너 id값] 을 실행해서 삭제한다.
4. django를 실행시키기 위해서는 가상환경이 필요한데 virtualenv venv 명령어를 실행해서 생성한다. (python에 virtualenv가 없을시 pip install virtualenv 명령어로 설치)
5. 설치가 완료되면 venv 파일이 생성되는데 venv 폴더 안에 있는 Scripts폴더에서 activate.bat를 실행하면 가상환경에 접속 할 수있다.
6. 가상환경에 접속후 프로젝트 디렉토리로 돌아와 pip install -r requirements.txt 명령어를 실행한다.
7. python manage.py runserver 명령어를 실행해 django를 시작한다.
8. http://127.0.0.1:8000/api/ 주소를 통해서 개발을 진행한다. (localhost로 접속하면 css load가 되지 않는다) 
---
### Docker 모두 삭제

1. docker rm -vf $(docker ps -a -q) 컨테이너 삭제
2. docker volume rm $(docker volume ls -q) 볼륨 삭제 ,기존 데이터는 전부 삭제 됩니다.
3. docker rmi -f $(docker images -a -q) 이미지 삭제


