import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from textSummarizer.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from textSummarizer.logging import logger

STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<<")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nX==============X")
#Exception is the base class for all built-in exceptions, so this catches any type of error
except Exception as e:
    #Logs the exception with full stack trace, helping in debugging.
    logger.exception(e)
    raise e
    