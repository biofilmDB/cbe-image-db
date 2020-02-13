# TODO: Put a version number
FROM phusion/passenger-customizable

# Set correct environment variables.
ENV HOME /root

# Use baseimage-docker's init process.
CMD ["/sbin/my_init"]

#   Python support.
RUN /pd_build/python.sh
# End passanger intilization code

# Run code from Dockerfile for continuumio/anaconda
# Changed from anaconda2 to anaconda3 in the second run command
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-5.3.0-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb

ENTRYPOINT [ "/usr/bin/tini", "--" ]

# Add repository for packages for postgres to function
RUN echo deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main >> /etc/apt/sources.list.d/pgdg.list && \
	wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc -O post-key.asc && \ 
	apt-key add post-key.asc && \
	apt-get install -y libpq-dev

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# CMD [ "/bin/bash" ]

# Copy over the environment.yml file
# Make and copy over files
RUN mkdir /code
WORKDIR /code
COPY environment.yml /code/

# Create and activate the conda environment

# Pull the environment name out of the environment.yml
RUN conda env create -f environment.yml && \
	echo "source activate $(head -1 environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 environment.yml | cut -d' ' -f2)/bin:$PATH
