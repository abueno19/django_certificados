FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y \
                supervisor\
		nginx\
		build-essential\
		python3-all-dev\
	--no-install-recommends && rm -rf /var/lib/apt/lists/*




RUN mkdir /code
COPY ./paquetes.txt /code/paquetes.txt
RUN pip install  -r /code/paquetes.txt
WORKDIR /code

