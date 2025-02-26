FROM condaforge/mambaforge:23.1.0-2 AS naavre-multiply-build

RUN conda install -c conda-forge conda-pack conda-merge mamba
COPY environment.yaml .
COPY naa-vre-environment.yaml .
RUN conda-merge environment.yaml naa-vre-environment.yaml > merged-environment.yaml

ADD ./jupyterlab_vre-0.1.0-py3-none-any.whl /home/jovyan/jupyterlab_vre-0.1.0-py3-none-any.whl

RUN mamba env update --name venv -f merged-environment.yaml
RUN conda-pack -n venv -o /tmp/env.tar && \
    mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
    rm /tmp/env.tar
RUN /venv/bin/conda-unpack

FROM jupyterhub/k8s-singleuser-sample:1.1.3-n248.h20c9028e AS runtime
USER root


RUN apt-get update --allow-releaseinfo-change && apt-get -y install fuse

COPY --from=naavre-multiply-build /venv/ /venv/

ENV PATH=/venv/bin:$PATH
ENV PATH=/home/jovyan/.local/bin:$PATH
RUN source /venv/bin/activate
RUN echo "source /venv/bin/activate" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

ADD ./start-jupyter.sh /usr/local/bin/start-jupyter.sh
ADD ./start-jupyter-venv.sh /usr/local/bin/start-jupyter-venv.sh
COPY repo_utils /tmp/repo_utils

COPY .condarc /tmp/.condarc

RUN chmod ugo+x /usr/local/bin/start-jupyter.sh
RUN chmod ugo+x /usr/local/bin/start-jupyter-venv.sh
RUN chown $NB_USER -R /venv/

COPY init_script.sh /tmp
RUN chown $NB_USER -R /tmp/init_script.sh
RUN chmod ugo+x /tmp/init_script.sh

USER $NB_USER
RUN jupyter serverextension enable --py jupyterlab_vre --user
RUN jupyter serverextension enable --py jupyter_videochat --user
RUN jupyter serverextension enable --py jupyterlab_github --user


RUN jupyter lab build --debug;
COPY test_multiply.py .
RUN python test_multiply.py
RUN rm test_multiply.py
cmd ["/usr/local/bin/start-jupyter-venv.sh"]