FROM django

WORKDIR /code
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY compile_Nginx.sh ./
RUN bash compile_Nginx.sh
RUN mkdir /config
RUN mkdir /upload
