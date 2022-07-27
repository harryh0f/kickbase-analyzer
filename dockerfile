FROM python:3.9

EXPOSE 8501
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt 
# pip list --format=freeze > requirements.txt

COPY . .

RUN [ "python", "./data_collector.py", "&" ]
# RUN [ "python", "./data_collector.py" ]

ENTRYPOINT ["streamlit", "run"]
CMD ["data_explorer.py"]