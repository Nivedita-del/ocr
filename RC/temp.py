from invoice2data import extract_data
from invoice2data.extract.loader import read_templates
import os



templates = read_templates('./datasets')
result = extract_data('datasets/MktPlace-Myntra.pdf', templates=templates)