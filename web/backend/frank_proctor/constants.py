import os

from frank_proctor.utils import get_first_model_at

MODEL_DIR = os.getenv('MODEL_DIR', './models')
DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', get_first_model_at(MODEL_DIR))
