
from loguru import logger


def get_domain_logger():
    return logger.bind(layer="DOMAIN")


def get_application_logger():
    return logger.bind(layer="APPLICATION")


def get_infrastructure_logger():
    return logger.bind(layer="INFRASTRUCTURE")


def get_presentation_logger():
    return logger.bind(layer="PRESENTATION")
