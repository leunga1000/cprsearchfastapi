FROM python:3

WORKDIR /usr/src/app


COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_md
# RUN python -m spacy download en_core_web_lg

COPY . .

CMD [ "bash", "run.sh" ] 