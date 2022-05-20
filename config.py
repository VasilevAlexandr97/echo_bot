import os
from pathlib import Path, PosixPath

import yaml
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR.joinpath(".env")
MESSAGE_FILE_PATH = BASE_DIR.joinpath("message.yaml")

load_dotenv(dotenv_path=ENV_PATH)

TOKEN = os.getenv("TOKEN")


def load_message_from_file(file_path: PosixPath):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


MESSAGE_SCHEMA = load_message_from_file(MESSAGE_FILE_PATH)

print(MESSAGE_SCHEMA)
