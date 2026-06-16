from dotenv import load_dotenv
from huggingface_hub import login
import os

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN:
   login(
    token=os.getenv("HF_TOKEN"),
    add_to_git_credential=False
)