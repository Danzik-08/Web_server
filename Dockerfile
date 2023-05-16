#
FROM python:3.10

#
WORKDIR /code

#
RUN mkdir output

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY . /code/src

ENV PYTHONPATH=/code/src

#
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]