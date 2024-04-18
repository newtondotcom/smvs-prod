FROM debian:latest 
LABEL Developers="Robin Augereau"
RUN apt update


WORKDIR /app
COPY . /app

RUN apt install python3-pip git ffmpeg -y

# RUN pip3 install git+https://github.com/m-bain/whisperx.git --break-system-packages
RUN pip3 install -r requirements.txt --break-system-packages
RUN mkdir temp


ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]