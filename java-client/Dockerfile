FROM oraclelinux:9

# Install Java and dependencies
# libaio is required for OCI
RUN dnf install -y java-17-openjdk-devel wget unzip libaio && \
    dnf clean all

WORKDIR /app

# Download Instant Client Basic for ARM64 (Specific version 19.19)
RUN wget https://download.oracle.com/otn_software/linux/instantclient/1919000/instantclient-basic-linux.arm64-19.19.0.0.0dbru.zip -O instantclient.zip && \
    unzip instantclient.zip && \
    rm instantclient.zip && \
    mv instantclient* instantclient

# Set environment variables for OCI
ENV LD_LIBRARY_PATH=/app/instantclient
ENV PATH=$PATH:/app/instantclient

# Download JDBC Driver (Matching Instant Client 19.19 EXACTLY)
RUN mkdir lib && \
    wget -O lib/ojdbc10.jar https://repo1.maven.org/maven2/com/oracle/database/jdbc/ojdbc10/19.19.0.0/ojdbc10-19.19.0.0.jar

COPY OracleThickClientTest.java .

# Compile
RUN javac -cp .:lib/ojdbc10.jar OracleThickClientTest.java

# Run
CMD ["java", "-cp", ".:lib/ojdbc10.jar", "OracleThickClientTest"]
