FROM python:3.5-slim
MAINTAINER Michael Hoyt <hoyt.nix@gmail.com>

# Install software.
RUN apt-get update && apt-get install -qq -y \
    build-essential libpq-dev --no-install-recommends

# Working directory.
ENV INSTALL_PATH /myallegan
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

# Install Python-packages.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Install MyAllegan-package.
COPY . .
RUN pip install --editable .

# Start service.
CMD gunicorn -c "python:config.gunicorn" "myallegan.app:create_app()"
