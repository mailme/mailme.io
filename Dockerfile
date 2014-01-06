FROM stackbrew/ubuntu:12.04
RUN apt-get -qq update
RUN apt-get install -y python python-pip stunnel ruby-full rubygems1.8
sudo gem install sass
sudo gem install compass
sudo echo "deb http://deb.theforeman.org/ precise stable" > /etc/apt/sources.list.d/foreman.list
sudo wget -q http://deb.theforeman.org/foreman.asc -O- | sudo apt-key add -
sudo apt-get -qq update
sudo apt-get install -y foreman
ADD . /src
WORKDIR /src
RUN pip install -r requirements.txt
EXPOSE 5000
CMD foreman start
