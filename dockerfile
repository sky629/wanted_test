FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY . /code/


RUN sh setup_env.sh
RUN python -m pip install --upgrade pip
RUN pip install -r req.txt
RUN pip freeze

ENTRYPOINT ["bash", "/code/docker_entrypoint.sh"]