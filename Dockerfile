FROM ubuntu:latest
LABEL authors="blodstone"

ENTRYPOINT ["top", "-b"]