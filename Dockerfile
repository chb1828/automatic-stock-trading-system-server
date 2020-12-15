FROM openjdk:8-jre-alpine
MAINTAINER chb

COPY build/libs/server.jar /asts.jar
ENTRYPOINT ["java", "-jar", "/asts.jar"]