import pytesseract

from PIL import Image
from celery import Celery

from modelsFast import Documents

celery = Celery('tasks',  backend='rpc://', broker='redis://localhost:6379/0')


@celery.task
def extract_text(path):
    image = Image.open(path)
    text = pytesseract.image_to_string(image)
    return text

#celery -A celery_app worker --loglevel=INFO