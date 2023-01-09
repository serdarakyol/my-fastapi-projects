from fastapi import FastAPI
from typing import Callable

from loguru import logger

from pathlib import Path
from pandas import read_pickle

from api.utils.utils_cf import load_json

ROOT_DIR = str(Path(__file__).parent.parent)

def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        logger.info("Running app start handler.")
        app.state.cf_matrix = read_pickle(ROOT_DIR + "/data/cf_data.pkl")
        app.state.product_info = load_json(ROOT_DIR + "/data/meta.json")['meta']
    
    return startup

def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running app shutdown handler.")
        del app.state.cf_matrix
        del app.state.product_info

    return shutdown
