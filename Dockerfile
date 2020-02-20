# TODO: Put a version number
FROM phusion/passenger-customizable

# Set correct environment variables.
ENV HOME /root

# Use baseimage-docker's init process.
#CMD ["/sbin/my_init"]

#   Python support.
RUN /pd_build/python.sh
# End passanger intilization code

# Dockerfile for miniconda2, changed to miniconda3
# https://hub.docker.com/r/continuumio/miniconda/dockerfile
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-4.5.11-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

#ENTRYPOINT [ "/usr/bin/tini", "--" ]
#CMD [ "/bin/bash" ]

# End of miniconda docker file

# Add repository for packages for postgres to function
RUN echo deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main >> /etc/apt/sources.list.d/pgdg.list && \
	wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc -O post-key.asc && \ 
	apt-key add post-key.asc && \
	apt-get install -y libpq-dev

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy over the environment.yml file
# Make and copy over files
RUN rm -f /etc/service/nginx/down
#RUN rm -f /etc/service/nginx/run
RUN rm /etc/nginx/sites-enabled/default
RUN mkdir /home/app/webapp/
COPY --chown=app:app * /home/app/webapp/
#COPY * /home/app/webapp/
ADD webapp.conf /etc/nginx/sites-enabled/webapp.conf

# Make var for environment.yml file so don't have to change it everywhere
ENV CONDA_ENV_FILE /home/app/webapp/environment.yml


# Create and activate the conda environment
# Pull the environment name out of the environment.yml
RUN conda env create -f $CONDA_ENV_FILE && \
	echo "source activate $(head -1 $CONDA_ENV_FILE | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 $CONDA_ENV_FILE | cut -d' ' -f2)/bin:$PATH



WORKDIR /home/app/webapp/cbeImageDB

