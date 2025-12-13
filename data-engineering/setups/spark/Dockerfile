FROM python:3.11-bullseye
RUN apt-get update
RUN apt-get install -y --no-install-recomends openjdk-17-jdk
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
ENV SPARK_HOME="/opt/spark"
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
ENV PATH="${JAVA_HOME}:${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}"
RUN mkdir -p ${SPARK_HOME}
WORKDIR ${SPARK_HOME}

# fetch latest spark 3.5.x version and download the appropriate binary file
# explain: get all versions are 3.5.x => extract them => sort and take latest version => download latest-version
RUN curl -s https://dlcdn.apache.org/spark/ | grep -oP 'spark-3\.5\.[0-9]+' | sort -V | tail -1 | \
    xargs -I {} curl -O https://dlcdn.apache.org/spark/{}/{}-bin-hadoop3.tgz

# unpack the file and cleanup the binary file
RUN tar xvzf spark-3.5.*-bin-hadoop*.tgz --directory ${SPARK_HOME} --strip-components 1 \
    && rm -rf spark-3.5.*-bin-hadoop*.tgz


ENV SPARK_MASTER_PORT="7077"
ENV SPARK_MASTER_HOST="spark-master"

COPY ./spark.defaults.conf "${SPARK_HOME}/conf"

# install sbt coursier (cs) to build jars
# explain: chmod +x cs: grat cs permission that is execute
RUN cirl -fL https://github.com/coursier/coursier/releases/latest/download/cs-x86_64-pc-linux.gz | gzip -d > cs && chmod +x cs
ENV PATH="$PATH:/root/.local/share/coursier/bin"
RUN ./cs setup

# download postgres latest jar and add it to spark jars
RUN curl -s https://jdbc.postgresql.org/download/ | grep -oP 'postgresql-42\.7\.[0-9]+' | sort -V | tail -1 | xargs  -I {} wget -P ${SPARK_HOME}/jars/ https://jdbc.postgresql.org/download/{}.jar;

# download aws jar and add it to spark jars

RUN wget -P ${SPARK_HOME}/jars/ https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar;
RUN wget -P ${SPARK_HOME}/jars/ https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar;

RUN useradd -u 1000 -m -d /home/sparkuser sparkuser
ENV HOME="/home/sparkuser"
RUN chown -R 1000:1000 ${SPARK_HOME}
USER sparkuser

COPY ./spark-defaults.conf "${SPARK_HOME}/conf"

ENTRYPOINT ["/bin/bash"]

ENTRYPOINT ["/bin/bash"]
