FROM python:latest

RUN pip3 install selectors
RUN pip3 install redis

COPY ./socket_echo.py /

CMD [ "python", "./socket_echo.py", "0.0.0.0", "5000" ]

EXPOSE 5000

