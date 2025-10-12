# Use an official OpenJDK runtime as a parent image
FROM openjdk:21-jdk-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables for OTP
ENV OTP_VERSION=2.8.1
ENV OTP_JAR=otp-shaded-$OTP_VERSION.jar
ENV OTP_URL=https://repo1.maven.org/maven2/org/opentripplanner/otp-shaded/$OTP_VERSION/$OTP_JAR

# Download OTP
RUN apt-get update && apt-get install -y curl && \
    curl -L -f -o $OTP_JAR $OTP_URL && \
    apt-get remove -y curl && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Expose the port OTP runs on
EXPOSE 8080

# Run OTP by default when the container launches
CMD ["java", "-Xmx2G", "-jar", "otp-shaded-2.8.1.jar", "--load", "."]

