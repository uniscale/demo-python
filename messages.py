from typing import Optional
import configparser

from quart import Quart, request
from quart_cors import cors

from uniscale.core import DispatcherSession
from uniscale.core.platform.platform import Platform

from timeline_interceptors import register_interceptors

app = Quart(__name__)
app = cors(app, allow_origin="*")

builder = Platform.builder()

# Create in memory cache of users
users = {}

session: Optional[DispatcherSession] = None

@app.before_serving
async def setup_session():
    global session
    session = await builder.with_interceptors(lambda builder: register_interceptors(builder)).build()

@app.route('/api/service-to-module/<string:featureId>', methods=['POST'])
async def handle_request(featureId):
    data = await request.get_data()
    result = await session.accept_gateway_request(data)
    return result.to_json(), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    app.run(port=config.getint('Messages', 'port'))