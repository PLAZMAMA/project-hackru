FROM python:3.9

WORKDIR ./

COPY . .

RUN pip install --upgrade pip
RUN ls
RUN pip install --no-cache-dir -r ./requirements.txt


CMD ["python","app.py"]
