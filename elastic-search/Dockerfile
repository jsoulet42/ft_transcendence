FROM docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}

# set work directory
WORKDIR /usr/src/app

# copy entrypoint.sh
COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

USER root

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
