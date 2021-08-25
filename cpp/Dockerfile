FROM ubuntu:20.04 AS build-stage

ARG DEBIAN_FRONTEND=noninteractive

LABEL tts_client_cpp_build_stage_tmp=true

ADD ./cpp /tts-client/cpp
ADD ./tools /tts-client/tools
ADD ./proto /tts-client/proto

WORKDIR /tts-client

RUN rm -rf /tts-client/cpp/build

RUN apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install -y --no-install-recommends \
    automake \
    autoconf \
    ca-certificates \
    curl \
    g++ \
    gcc \
    git \
    libssl-dev \
    libtool \
    make \
    unzip \
    wget

RUN curl -fsSL "https://github.com/Kitware/CMake/releases/download/v3.20.3/cmake-3.20.3-Linux-x86_64.sh" -o cmake-linux.sh \
    && sh cmake-linux.sh -- --skip-license --prefix=/usr && rm cmake-linux.sh

RUN curl -fsSL "https://github.com/ninja-build/ninja/releases/download/v1.10.2/ninja-linux.zip" -o ninja-linux.zip \
    && unzip ninja-linux.zip -d /usr/bin \ 
    && rm ninja-linux.zip 

RUN ./tools/install_boost.sh 4 \
    && ./tools/install_grpc.sh 4

RUN cd cpp && ./make_proto.sh

RUN hash ninja 2> /dev/null && ninja="-GNinja" || ninja= \
    && cd cpp && cmake -S . -B build "${ninja}" -DCMAKE_BUILD_TYPE=Release && cmake --build build -- -j 4

RUN strip cpp/build/tts_client

# ----------------------------------------------------------------------------------------------------- #

FROM ubuntu:20.04 

ARG DEBIAN_FRONTEND=noninteractive

LABEL maintainer="<jan.wozniak@techmo.pl>"

RUN apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install -y --no-install-recommends \
    locales 

RUN locale-gen pl_PL pl_PL.UTF-8

ENV LANG pl_PL.UTF-8
ENV LANGUAGE pl_PL
ENV LC_ALL pl_PL.UTF-8

COPY --from=build-stage /tts-client/cpp/build/tts_client /tts-client/cpp/build/tts_client
COPY --from=build-stage /opt /opt

RUN apt-get clean \
	&& rm -fr /var/lib/apt/lists/* \
	&& rm -fr /var/cache/apt/* 

WORKDIR /tts-client
