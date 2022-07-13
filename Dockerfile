#FROM tensorflow/tensorflow:1.15.5
FROM tiangolo/uvicorn-gunicorn:python3.6

SHELL ["/bin/bash", "--login", "-c"]
RUN apt-get update && apt-get install -y unzip git && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/jrwnter/cddd.git 
WORKDIR cddd/

#RUN conda env create -f environment.yml
#RUN echo "conda activate cddd" >> ~/.bashrc
RUN pip install --upgrade pip
RUN pip install gdown && gdown 1oyknOulq_j0w9kzOKKIHdTLo5HphT99h && unzip default_model.zip -d cddd/data && rm default_model.zip
RUN pip install uvicorn scikit-learn rdkit-pypi pandas wget
RUN wget https://github.com/iammordaty/synology-tensorflow-wheels/raw/master/720plus_920plus/ubuntu_18.04/tensorflow-1.15.5-cp36-cp36m-linux_x86_64.whl
RUN pip install tensorflow-1.15.5-cp36-cp36m-linux_x86_64.whl

COPY requirements.txt . 
RUN pip install -r requirements.txt && rm requirements.txt

EXPOSE 80
COPY main.py .
COPY utils.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
