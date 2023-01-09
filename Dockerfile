FROM python:3.9.7

COPY ./api/requirements.txt /api/requirements.txt
COPY ./api /api
COPY ./prepare-api prepare-api

RUN ./prepare-api
RUN ls
WORKDIR /api
#RUN python -m venv /api/venv
# Enable venv
ENV PATH="/venv/bin:$PATH"

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "1234"]
