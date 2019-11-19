from server import config
from server import app

if __name__ == '__main__':
	app.run(debug=config.debug, host=config.host, port=config.port)
