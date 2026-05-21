FROM alpine:3.21

RUN apk add --no-cache curl jq

COPY seed-model.sh /app/seed-model.sh

ENTRYPOINT ["sh", "/app/seed-model.sh"]
CMD ["http://open-web-ui:8080"]
