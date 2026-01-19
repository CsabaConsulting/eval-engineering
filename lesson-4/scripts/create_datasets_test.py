import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from create_dataset_from_csv import create_dataset_from_csv

# Create the datasets for the grounding data, and for the rows that don't fail
create_dataset_from_csv("grounding-data-test")
create_dataset_from_csv("no-fail-test")
