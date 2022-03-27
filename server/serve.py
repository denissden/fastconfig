#! /usr/bin/python3
from app import create_app
import os
import waitress


def serve_dev(host, port):
    create_app().run(host=host, port=port)


def serve_prod(host, port):
    waitress.serve(create_app(), host=host, port=port)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser("Server for storing json configuration")
    parser.add_argument('-e', '--environment', required=False, default='')

    args = parser.parse_args()
    environment = 'development'
    if args.environment != '':
        environment = args.environment
    elif env := os.environ.get('ENVIRONMENT'):
        environment = env

    serve_port = int(os.environ.get('PORT', 5000))
    serve_host = os.environ.get('HOST', '127.0.0.1')

    if environment.lower().startswith('dev'):
        serve_dev(serve_host, serve_port)
    elif environment.lower().startswith('prod'):
        serve_prod(serve_host, serve_port)
