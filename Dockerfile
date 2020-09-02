FROM godatadriven/pyspark

MAINTAINER c.s.vankhede@gmail.com

COPY ./work_dir /app

WORKDIR /app

RUN pip install --upgrade pip  \
  && pip install -r requirements.txt \
  && rm -rf /var/cache/apk/*


CMD python Rest_API.py
