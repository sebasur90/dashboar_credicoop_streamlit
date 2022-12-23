FROM python:3.10.4

EXPOSE 8501

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT ["streamlit", "run", "app.py"]