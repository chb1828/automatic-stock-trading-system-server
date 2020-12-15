FROM openjdk:8-jre-alpine
MAINTAINER chb

COPY build/libs/asts.jar /asts.jar
ENTRYPOINT ["java", "-jar", "/scheduler.jar"]