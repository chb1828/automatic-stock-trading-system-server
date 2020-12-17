# ASTS Server

### 실행 방법

1. [Docker](https://docs.docker.com/docker-for-windows/install/) 다운로드 
2. docker를 실행하고 준비가 완료 되었는지 확인
3. docker-compose up -d 명령어를 프로젝트 디렉토리에서 실행
4. docker ps 명령어를 실행해서 프로세스가 현재 잘 올라가 있는지 확인

아래 포트 번호를 사용해서 app과 kibana에 접속 할 수 있습니다.

예시) http://localhost:5601/ <-- kibana 접속

현재 app에 접속하면 자동으로 값이 Postgresql DB에 저장되어 동기화 되고있는 Elasticsearch 에도 값이 저장됩니다. 

##### 확인하는 방법
1. http://localhost:8089 접속
2. http://localhost:5601 키바나 접속
3. 키바나 페이지에서 dashboard 로 이동
4. Check for new data라는 문구가 뜨면 데이터가 삽입될 때까지 기다리고 Check for new data 클릭
5. Index Pattern에 movie 작성
6. Time Filter field name에 `I don`t want to use the Time Filter` 선택
7. Discover 페이지로 가서 확인, 새로고침을 누를때마다 한개씩 증가


##### Port
* app : 8089
* elasticsearch : 9200,9300
* postgresql : 5432
* kibana : 5601
* logstash : 

---
### Docker 모두 삭제

1. docker rm -vf $(docker ps -a -q) 컨테이너 삭제
2. docker volume rm $(docker volume ls -q) 볼륨 삭제
3. docker rmi -f $(docker images -a -q) 이미지 삭제


