# start by pulling the python image
FROM nickgryg/alpine-pandas:3.10.4

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

RUN apk add --no-cache --update-cache gfortran build-base wget libpng-dev openblas-dev py3-scipy
# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["app.py" ]
