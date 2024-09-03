FROM chat:django_base_latest 

WORKDIR /chat

COPY manage.py .
COPY chat/ ./chat/
