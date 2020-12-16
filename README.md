# ASTS Server

### 실행 방법

1. [Docker](https://docs.docker.com/docker-for-windows/install/) 다운로드 
2. docker를 실행하고 준비가 완료 되었는지 확인
3. docker-compose up -d 명령어를 프로젝트 디렉토리에서 실행

---
### Docker 모두 삭제

1. docker rm -vf $(docker ps -a -q) 컨테이너 삭제
2. docker volume rm $(docker volume ls -q) 볼륨 삭제
3. docker rmi -f $(docker images -a -q) 이미지 삭제
