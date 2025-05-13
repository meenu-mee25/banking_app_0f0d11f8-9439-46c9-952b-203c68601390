FROM python:3.10.9-alpine3.17

# Install dependency packages
RUN apk update && apk upgrade
RUN apk --update add openssl ca-certificates py-openssl curl postgresql-dev
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev build-base

RUN python -m pip install --upgrade pip

RUN adduser -D worker
USER worker
WORKDIR /home/worker

COPY --chown=worker:worker requirements.txt requirements.txt

# Install python libraries
RUN pip install --user -r requirements.txt
ENV PATH = "/home/worker/.local/bin:${PATH}"

# Copy Source files
copy --chown=worker:worker . .

EXPOSE 5000
CMD [ "python","app_routes.py"]