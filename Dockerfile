# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.9.1

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip config set global.trusted-host pypi.python.org
RUN pip config set global.trusted-host pypi.org
RUN pip config set global.trusted-host files.pythonhosted.org
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip config set global.trusted-host mirrors.aliyun.com
RUN pip install --no-cache-dir -r requirements.txt --trusted-host=mirrors.aliyun.com --trusted-host=pypi.python.org

# Mounts the application code to the image
COPY . nanocmdb
WORKDIR /nanocmdb

EXPOSE 8000

# runs the production server
ENTRYPOINT ["python", "nanocmdb/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]