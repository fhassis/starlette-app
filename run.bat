@echo off

SET HOST=0.0.0.0
SET PORT=8000

SET CERTFILE=./ssl/certificates/cert.pem
SET KEYFILE=./ssl/certificates/key.pem

REM SET CERTFILE=C:\Certbot\live\fhassis.ddns.net\fullchain.pem
REM SET KEYFILE=C:\Certbot\live\fhassis.ddns.net\privkey.pem

REM pipenv run python -m uvicorn src.main:app --host %HOST% --port %PORT% --proxy-headers
REM pipenv run python -m uvicorn src.main:app --host %HOST% --port %PORT% --ssl-keyfile %KEYFILE% --ssl-certfile %CERTFILE%

REM pipenv run python -m hypercorn src.main:app --bind %HOST%:%PORT%
REM pipenv run python -m hypercorn src.main:app --bind %HOST%:%PORT% --keyfile %KEYFILE% --certfile %CERTFILE%

pipenv run python -m hypercorn src.main:app --bind %HOST%:%PORT% --quic-bind "0.0.0.0:4443" --keyfile %KEYFILE% --certfile %CERTFILE%
