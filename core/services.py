from logs.statistics_saving import statistics
from logs.log import log_data
from storage.csv_database import csv_database
from extractor.extract_data import DivarExtractor
from storage.json_save_and_load import save_and_load_json
from core.translate import Translate
from managares.Dialog_manager import Dialog


stats = statistics()
log = log_data()
save = csv_database()
extractor = DivarExtractor()
json_database = save_and_load_json()
translate = Translate()
Message = Dialog()