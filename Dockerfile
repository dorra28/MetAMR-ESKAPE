FROM continuumio/miniconda3:24.1.2-0

WORKDIR /opt/metamr-eskape

COPY environment.yml .
RUN conda env create -f environment.yml && conda clean -afy

# Activate the env by default in interactive shells
SHELL ["conda", "run", "-n", "metamr-eskape", "/bin/bash", "-c"]
ENV PATH /opt/conda/envs/metamr-eskape/bin:$PATH

# AMRFinderPlus needs its database initialized once at build time
RUN amrfinder_update --force_update || true

COPY . .

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "metamr-eskape"]
CMD ["bash"]
