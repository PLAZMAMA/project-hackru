FROM python:3.9

WORKDIR ./

EXPOSE 8050

COPY . .

RUN pip install --upgrade pip
RUN ls
RUN pip install --no-cache-dir -r ./requirements.txt


CMD ["python","app.py"]
