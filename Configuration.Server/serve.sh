if [[ -z "${HOST}" ]]; then
	echo "HOST environment variable is empty. Defaulting to localhost"
	RUN_HOST="localhost"
else
	RUN_HOST="${HOST}"
fi

if [[ -z "${PORT}" ]]; then
	echo "PORT environment variable is empty. Defaulting to 5000"
	RUN_PORT="5000"
else
	RUN_PORT="${PORT}"
fi

echo "Serving waitress on ${RUN_HOST}:${RUN_PORT}"
waitress-serve --no-ipv6 ${@:1} --host=$RUN_HOST --port=$RUN_PORT --call "app:create_app"
