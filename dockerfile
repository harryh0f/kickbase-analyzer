FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN [ "python", "./data_collector.py" ]
CMD [ "python", "-c", "streamlit", "run", "data_explorer.py" ]