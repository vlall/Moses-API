FROM ubuntu:14.04
MAINTAINER Vishal Lall "vishal.lall@caci.com"
LABEL Description="Install Moses SMT API" Version="1.2"
EXPOSE 5000

RUN apt-get update && apt-get install -y \
   automake \
   build-essential \
   g++ \
   git \
   graphviz \
   imagemagick \
   libboost-all-dev \
   libbz2-dev \
   libgoogle-perftools-dev \
   liblzma-dev \
   libtool \
   make \
   python-dev \
   python-pip \
   subversion \
   unzip \
   wget \
   zlib1g-dev 

RUN pip install \
   flask \
   flask-api

RUN mkdir -p /home/moses
WORKDIR /home/moses
RUN wget -O /home/moses/RELEASE-3.0.zip https://github.com/moses-smt/mosesdecoder/archive/RELEASE-3.0.zip
RUN unzip /home/moses/RELEASE-3.0.zip
RUN rm RELEASE-3.0.zip
RUN mv mosesdecoder-RELEASE-3.0 mosesdecoder
RUN mkdir moses-models

#  Giza
RUN wget -O giza-pp.zip "http://github.com/moses-smt/giza-pp/archive/master.zip" 
RUN unzip giza-pp.zip
RUN rm giza-pp.zip
RUN mv giza-pp-master giza-pp
WORKDIR /home/moses/giza-pp
RUN make
WORKDIR /home/moses
RUN mkdir external-bin-dir
RUN cp giza-pp/GIZA++-v2/GIZA++ external-bin-dir
RUN cp giza-pp/GIZA++-v2/snt2cooc.out external-bin-dir
RUN cp giza-pp/mkcls-v2/mkcls external-bin-dir

#  CMPH
RUN wget -O cmph-2.0.tar.gz "http://downloads.sourceforge.net/project/cmph/cmph/cmph-2.0.tar.gz?r=&ts=1426574097&use_mirror=cznic"
RUN tar zxvf cmph-2.0.tar.gz
WORKDIR /home/moses/cmph-2.0
RUN ./configure
RUN make
RUN make install

#  IRSTLM
WORKDIR /home/moses
RUN wget -O irstlm-5.80.08.tgz "http://downloads.sourceforge.net/project/irstlm/irstlm/irstlm-5.80/irstlm-5.80.08.tgz?r=&ts=1342430877&use_mirror=kent"
RUN tar zxvf irstlm-5.80.08.tgz
WORKDIR /home/moses/irstlm-5.80.08/trunk
RUN /bin/bash -c "source regenerate-makefiles.sh"
RUN ./configure -prefix=/home/moses/irstlm
RUN make
RUN make install
WORKDIR /home/moses
ENV IRSTLM /home/moses/irstlm

#  Get Newest Boost
RUN mkdir /home/moses/Downloads
WORKDIR /home/moses/Downloads
RUN wget https://sourceforge.net/projects/boost/files/boost/1.60.0/boost_1_60_0.tar.gz
RUN tar xf boost_1_60_0.tar.gz
RUN rm boost_1_60_0.tar.gz
WORKDIR boost_1_60_0/
RUN ./bootstrap.sh
RUN /b2 -j4 --prefix=$PWD --libdir=$PWD/lib64 --layout=system link=static install || echo FAILURE

#  Buckwalter for Arabic
WORKDIR /home/moses/Downloads
RUN wget http://search.cpan.org/CPAN/authors/id/G/GR/GRAFF/Encode-Buckwalter-1.1.tar.gz
RUN tar xf Encode-Buckwalter-1.1.tar.gz
RUN rm Encode-Buckwalter-1.1.tar.gz
WORKDIR /home/moses/Downloads/Encode-Buckwalter-1.1
RUN perl Makefile.PL
RUN make
RUN make test
RUN make install

#  Get Flask API
WORKDIR /home/moses/Downloads
RUN git clone https://github.com/vlall/moses-api

WORKDIR /home/moses/mosesdecoder
# COMPILE MOSES (Takes awhile...)
RUN ./bjam --with-boost=/home/moses/Downloads/boost_1_60_0 --with-cmph=/home/moses/cmph-2.0 --with-irstlm=/home/moses/irstlm -j12
