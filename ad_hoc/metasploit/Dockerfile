# ActiveMQ 5.18.2 is deliberately vulnerable to CVE-2023-46604.
# The historical version is installed from Apache's official archive because
# the activemq-classic Docker repository does not publish a 5.18.2 image tag.
FROM eclipse-temurin:17-jre-jammy

ARG ACTIVEMQ_VERSION=5.18.2

RUN curl -fsSL --retry 3 \
       "https://repo.maven.apache.org/maven2/org/apache/activemq/apache-activemq/${ACTIVEMQ_VERSION}/apache-activemq-${ACTIVEMQ_VERSION}-bin.tar.gz" \
       | tar -xz -C /opt \
    && ln -s "/opt/apache-activemq-${ACTIVEMQ_VERSION}" /opt/activemq \
    && sed -i 's/<property name="host" value="127.0.0.1"\/>/<property name="host" value="0.0.0.0"\/>/' \
       "/opt/apache-activemq-${ACTIVEMQ_VERSION}/conf/jetty.xml" \
    && useradd --system --home-dir /opt/activemq --shell /usr/sbin/nologin activemq \
    && chown -R activemq:activemq "/opt/apache-activemq-${ACTIVEMQ_VERSION}" \
    && mkdir -p /opt/hacklabs

COPY flag.txt /opt/hacklabs/flag.txt
RUN chmod 0444 /opt/hacklabs/flag.txt

USER activemq
WORKDIR /opt/activemq
EXPOSE 61616 8161
CMD ["bin/activemq", "console"]
