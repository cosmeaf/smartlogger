#!/bin/bash

PROJECT_DIR="/Users/cosmeaf/Desktop/Projects/django/django_smartlogger"
VENV_DIR="$PROJECT_DIR/venv/bin"
DJANGO_MANAGE="$VENV_DIR/python $PROJECT_DIR/manage.py"
CELERY_WORKER="celery -A core worker --loglevel=info"
CELERY_BEAT="celery -A core beat --loglevel=info"
CELERY_PID_WORKER="$PROJECT_DIR/celery_worker.pid"
CELERY_PID_BEAT="$PROJECT_DIR/celery_beat.pid"

start() {
    echo "Starting Django server..."
    $DJANGO_MANAGE runserver 0.0.0.0:8000 &

    echo "Starting Celery worker..."
    $CELERY_WORKER --pidfile="$CELERY_PID_WORKER" &

    echo "Starting Celery beat..."
    $CELERY_BEAT --pidfile="$CELERY_PID_BEAT" &
}

stop() {
    echo "Stopping Django server..."
    pkill -f "runserver 0.0.0.0:8000"

    echo "Stopping Celery worker..."
    if [ -f "$CELERY_PID_WORKER" ]; then
        kill -9 $(cat "$CELERY_PID_WORKER")
        rm "$CELERY_PID_WORKER"
    else
        pkill -f "celery worker"
    fi

    echo "Stopping Celery beat..."
    if [ -f "$CELERY_PID_BEAT" ]; then
        kill -9 $(cat "$CELERY_PID_BEAT")
        rm "$CELERY_PID_BEAT"
    else
        pkill -f "celery beat"
    fi
}

restart() {
    stop
    start
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
esac
