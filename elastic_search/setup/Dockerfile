ARG STACK_VERSION
FROM docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}

WORKDIR /usr/share/elasticsearch

# copy entrypoint.sh
COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/share/elasticsearch/entrypoint.sh
RUN chmod +x /usr/share/elasticsearch/entrypoint.sh

USER root

ENTRYPOINT ["/usr/share/elasticsearch/entrypoint.sh"]
