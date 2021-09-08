pipenv run python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 
REM pipenv run python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --ssl-keyfile ./ssl/certificates/key.pem --ssl-certfile ./ssl/certificates/cert.pem

REM pipenv run python -m hypercorn src.main:app --bind "0.0.0.0:8000"
REM pipenv run python -m hypercorn src.main:app --bind "0.0.0.0:8000" --keyfile ./ssl/certificates/key.pem --certfile ./ssl/certificates/cert.pem

pause