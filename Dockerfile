FROM python:3
WORKDIR /usr/src/app
COPY ["requirements.txt", "requirements.txt"]
RUN pip3 install -r requirements.txt
RUN curl -fsSL https://deb.nodesource.com/setup_15.x | bash
RUN apt-get install -y nodejs

RUN mkdir /root/.ssh
COPY ["github_ssh_key", "/root/.ssh/id_rsa"]
COPY ["github_ssh_key.pub", "/root/.ssh/id_rsa.pub"]
COPY ["update_stats", "update_stats"]
COPY ["ssh_known_hosts", "/root/.ssh/known_hosts"]