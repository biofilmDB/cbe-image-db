# TODO: Put a version number
FROM phusion/passenger-customizable

# Make and copy over files
RUN mkdir /code
WORKDIR /code
COPY passanger_install_python3.sh /code/
COPY environment.yml /code/


#   Python support.
RUN /pd_build/python.sh