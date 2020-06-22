FROM ubuntu

RUN apt update -y && \
    apt-get upgrade -y && \
    apt install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt install -y python3.8 && \
    apt install -y python3-pip && \
    apt install -y libpq-dev && \
    apt install -y python3-dev

COPY . .

# Install requirements and GDAL dependencies
RUN pip3 install -r requirements.txt && \
    add-apt-repository ppa:ubuntugis/ubuntugis-unstable && \
    apt-get install -y gdal-bin && \
    apt-get install -y python3-gdal && \
    apt-get install -y python3-numpy && \
    add-apt-repository ppa:thomas-schiex/blender

RUN chmod +x entrypoint

EXPOSE 80

ENTRYPOINT ["./entrypoint"]