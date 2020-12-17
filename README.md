# ASTS Server

### 실행 방법

1. [Docker](https://docs.docker.com/docker-for-windows/install/) 다운로드 
2. docker를 실행하고 준비가 완료 되었는지 확인
3. docker-compose up -d 명령어를 프로젝트 디렉토리에서 실행

아래 포트 번호를 사용해서 app과 kibana에 접속 할 수 있습니다.

예시) http://localhost:5601/

현재 app에 접속하면 자동으로 값이 Postgresql DB에 저장되어 Elasticsearch와 동기화 하고 있습니다. 

##### Port
* app : 8089
* elasticsearch : 9200,9300
* postgresql : 5432
* kibana : 5601
* logstash : 123

---
### Docker 모두 삭제

1. docker rm -vf $(docker ps -a -q) 컨테이너 삭제
2. docker volume rm $(docker volume ls -q) 볼륨 삭제
3. docker rmi -f $(docker images -a -q) 이미지 삭제


