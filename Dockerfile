FROM python:3-onbuild
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:application"]
