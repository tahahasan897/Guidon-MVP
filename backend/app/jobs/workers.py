from rq import Worker
from app.jobs.queue import redis_conn


def main():
    worker = Worker(["default"], connection=redis_conn)
    worker.work()


if __name__ == "__main__":
    main()
