FROM ubuntu:18.04

RUN apt-get update
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa

RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE >/etc/timezone

RUN apt-get update && apt-get -y install \
    bash \
    zsh \
    git \
    curl \
    unzip \
    zip \
    python3.9 \
    python3-pip bc sudo

RUN apt-get install -y locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN useradd -ms /bin/bash SCAM2022

RUN zsh

RUN sudo ln -s /usr/bin/pip3 /usr/bin/pip
RUN sudo ln -s /usr/bin/python3.9 /usr/bin/python

RUN mkdir -p /workspace
RUN cd workspace && git clone https://github.com/lu-cs-sde/JFeature.git jfeature
RUN pip install 'numpy==1.19.5' 'pandas==1.1.5' 'matplotlib==3.3.4' 'seaborn==0.11.1' 'ipython==7.16.0' 'PyPDF2==1.26.0' 'tabulate==0.8.9'
ENV SDKMAN_DIR=/home/SCAM2022/.sdkman

RUN curl -s "https://get.sdkman.io" | bash
RUN bash -c "source $SDKMAN_DIR/bin/sdkman-init.sh && sdk use java 8.0.275.fx-zulu && ./gradlew build"
ENV JAVA_HOME="$SDKMAN_DIR/candidates/java/current"
ENV PATH="$JAVA_HOME/bin:~/.sdkman:$PATH"

RUN chmod 777 /workspace/**/*
RUN echo "SCAM2022:SCAM2022" | chpasswd && adduser SCAM2022 sudo
RUN chown -R SCAM2022 /workspace/
RUN chown -R SCAM2022 $SDKMAN_DIR
USER SCAM2022
