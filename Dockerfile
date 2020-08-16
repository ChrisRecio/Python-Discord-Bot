FROM python:3-onbuild

RUN pip install --upgrade pip && \
    pip install discord.py && \
    pip install discord.py[voice] && \
    pip install numpy && \
    pip install requests

CMD [ "python", "./main.py" ]