import redis
import argparse


HOST = "localhost"
PORT = 6379


def _setup_redis_client():
    return redis.Redis(host=HOST, port=PORT, db=0)


redis_client = _setup_redis_client()


def increment_requests():
    redis_client.incr("requests")


def show_requests_count():
    count = redis_client.get("requests")
    print("Number of requests:", count.decode())


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--increment", action="store_true", help="Increment request count.")
    parser.add_argument("-c", "--show", action="store_true", help="Show request count.")
    args = parser.parse_args()

    if args.increment:
        increment_requests()
    elif args.show:
        show_requests_count()

