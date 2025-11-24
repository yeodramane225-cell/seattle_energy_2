FROM python:3.10-slim

# Installer les dépendances
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir bentoml==1.3.4.post1 && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# Copier le Bento correct
COPY ./bentos/building_energy_predictor/et5lefwiy2bc7xom /bento

WORKDIR /bento
EXPOSE 3000

CMD ["bentoml", "serve", "/bento", "--port", "3000"]

