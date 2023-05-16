import os
from fastapi import FastAPI, HTTPException

from src.ML_logic import MLApps, save_dir
from src.models import MLConfig, BodyFit, BodyPredict

import multiprocessing as mp
from datetime import datetime
from const import process_nums
from os.path import getctime

app = FastAPI()


@app.post("/fit")
async def fit_model(body: BodyFit):
    # global process_nums
    if process_nums.value == 0:
        raise HTTPException(status_code=503, detail="нет свободных процессов, попробуйте позже")
    process = mp.Process(target=MLApps.fit, args=(body.X, body.y, body.config, process_nums))
    process.daemon = True
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    process.start()
    with process_nums.get_lock():
        process_nums.value -= 1
    res = {'msg': f'Поставлено на обучение, время - {current_time}, свободных процессов {process_nums.value}, '}
    return res


@app.post("/predict")
async def predict(body: BodyPredict):
    filename = body.config.name + '.sav'
    if filename in os.listdir(save_dir):
        y_pred = MLApps.predict(body.X, body.config)
        time_saved = datetime.fromtimestamp(getctime(save_dir + '/' + filename)).strftime('%H:%M:%S')
        return {'время сохранения модели': {time_saved}, 'predictions': list(y_pred)}
    else:
        raise HTTPException(status_code=400, detail="Нет модели с "
                                                    "таким именем на диске")


@app.post("/remove")
async def remove(body: MLConfig):
    filename = save_dir + '/' + body.name + '.sav'
    MLApps.remove(filename)


@app.get("/remove_all")
async def remove_all():
    dir = save_dir
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
