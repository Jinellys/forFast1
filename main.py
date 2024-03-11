import os
from datetime import date
from fastapi import FastAPI, UploadFile
from sqlalchemy import Select
from modelsFast import create_table, Documents, Documents_text
import uvicorn
import shutil
from connectDB import session
from celery_app import extract_text


app = FastAPI()

@app.get('/')
def get_hello():
    """вывод приветственной страницы"""
    return 'Hello'


@app.post('/upload_doc')
def upload_doc(file: UploadFile):
    """заполнение данными таблицы Documents"""
    with open(f'Documents/{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    with session() as Session:
        doc = Documents(path=f'Documents/{file.filename}', date=date.today())

    Session.add(doc)
    Session.commit()


@app.delete('/delete_doc')
def delete_doc(docs: int):
    """удаление данных по id из таблицы Documents"""
    with session() as Session:
        query = Select(Documents.path).filter(Documents.id == docs)
        res = Session.execute(query).one()
        os.remove(*res)

    with session() as Session:
        Session.query(Documents).filter(Documents.id == docs).delete()
        Session.commit()


@app.post("/doc_analyse/")
def doc_analyse(docs: int) -> dict:
    """запись полученного текста из image в таблицу Document_text\n
       возвращает сообщение 'it's OK'"""
    with session() as Session:
        query = Select(Documents.path).filter(Documents.id == docs)
        res = Session.execute(query).one()
        ext_text = extract_text.delay(*res)
        img_text = ext_text.get()
        print(img_text)
        doc_text = Documents_text(id_doc=docs, text=img_text)

        Session.add(doc_text)
        Session.commit()

    return {"message": "it's OK"}


@app.get("/get_text")
def get_text(docs: int):
    """получение по id данных колонки text таблицы Document_text\n
       возвращает результат запроса"""
    with session() as Session:
        query = Select(Documents_text.text).filter(Documents_text.id_doc == docs)
        res = Session.execute(query)

    return f'{res}'

if __name__ == '__main__':
    create_table()
    uvicorn.run('main:app', reload=True)
