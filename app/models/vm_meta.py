from enum import Enum


class Meta(Enum):
    USER = "USER"
    PROJECT = "PROJECT"
    POSTGRES_PASSWORD = "POSTGRES_PASSWORD"
    REDIS_PASSWORD = "REDIS_PASSWORD"
    API_KEY = "API_KEY"
    PROJ_TOKEN = "PROJ_TOKEN"
    
    NUM_SLAVES = "NUM_SLAVES"
    GG_SHEET_URL = "GG_SHEET_URL"