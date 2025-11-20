# syntax=docker/dockerfile:1

FROM gradle:8.10.1-jdk21 AS builder
WORKDIR /workspace
COPY build.gradle settings.gradle ./
COPY src ./src
RUN gradle --no-daemon bootJar

FROM eclipse-temurin:21-jre
WORKDIR /app
ENV JAVA_OPTS=""
COPY --from=builder /workspace/build/libs/isochrone-backend-0.0.1-SNAPSHOT.jar app.jar
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /app/app.jar"]
