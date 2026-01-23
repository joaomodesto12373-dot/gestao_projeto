import logging
from .etl_projetos import run_etl

def main(mytimer):
    logging.info("ETL iniciado")
    run_etl()
    logging.info("ETL finalizado")
