# TODO: Put a version number
FROM phusion/passenger-customizable:1.0.9


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

# Cleans up the container, getting rid of zombie processes
ENTRYPOINT [ "/usr/bin/tini", "--" ]

# End of miniconda docker file


# Add repository for packages for postgres to function
RUN echo deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main >> /etc/apt/sources.list.d/pgdg.list && \
	wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc -O post-key.asc && \ 
	apt-key add post-key.asc && \
	apt-get install -y libpq-dev

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Make webapp directory
RUN mkdir /home/app/webapp/

# download wait-for-it.sh
RUN wget --quiet https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh 
RUN cp wait-for-it.sh /home/app/webapp/wait-for-it.sh 
RUN chmod +x /home/app/webapp/wait-for-it.sh

# Copy over the environment.yml file and extend base environment with cbe-image
ENV CONDA_ENV_FILE /home/app/webapp/environment.yml
COPY environment.yml $CONDA_ENV_FILE
RUN conda env update --name base --file $CONDA_ENV_FILE

# Copy over necessary files for app to run
COPY --chown=app:app cbeImageDB /home/app/webapp/

# Make files directory
RUN mkdir /home/app/webapp/files
# Make static file dir and create static files
RUN export STATIC_ROOT=/home/app/webapp/static && mkdir /home/app/webapp/static && python /home/app/webapp/manage.py collectstatic
WORKDIR /home/app/webapp/

# Give init.sh permission to run
RUN chmod +x init.sh
RUN chmod +x startup.sh
