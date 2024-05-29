FROM python:3.12

WORKDIR /application

COPY . .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libgl1 libegl1 -y

RUN pip install -r requirements.txt

RUN chmod +x build.bash

CMD ["bash", "build.bash"]
