FROM bjwebb/bookish
RUN cp demo/env.demo .env
RUN python manage.py migrate
RUN python manage.py createdemodata

