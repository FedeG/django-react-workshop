FROM python:3.5

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install nodejs and gettext
ENV NODE_VERSION 8.x
RUN curl -sL https://deb.nodesource.com/setup_${NODE_VERSION} | bash -
RUN apt-get install -y nodejs gettext \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install python requirements
COPY ./src/requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Install node modules
COPY ./src/front/package.json /usr/src/app/front/
COPY ./src/front/yarn.lock /usr/src/app/front/
WORKDIR /usr/src/app/front
RUN npm install -g yarn webpack
RUN yarn install
WORKDIR /usr/src/app

# Copy test script file
COPY ./test.sh /usr/src/app/test.sh

# Copy python code and collectstatics
COPY ./src /usr/src/app
RUN python manage.py collectstatic --noinput

# Compile reactjs code
RUN cd /usr/src/app/front && webpack --config webpack.prod.config.js

# Compile .po files
RUN sed -i 's@#~ @@g' /usr/src/app/locale/*/LC_MESSAGES/djangojs.po
RUN python manage.py compilemessages

EXPOSE 8000

VOLUME /usr/src/app

CMD ["tail", "-f", "/dev/null"]
