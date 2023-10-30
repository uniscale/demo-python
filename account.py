import string
from typing import Optional, List
from uuid import UUID, uuid4
import configparser

from quart import Quart, request
from quart_cors import cors

from uniscale.core import Result, DispatcherSession
from uniscale.core.platform.platform import Platform
from uniscale.core.utilisation.utilisation_session_base import FeatureContext

from uniscale.uniscaledemo.account.patterns import Patterns
from uniscale.uniscaledemo.account.account.user_full import UserFull

app = Quart(__name__)
app = cors(app, allow_origin="*")

builder = Platform.builder()

# Create in memory cache of users
users = {}

session: Optional[DispatcherSession] = None


@app.before_serving
async def setup_session():
    global session
    session = await builder.with_interceptors(
        lambda i: i.intercept_request(
            Patterns.account.get_or_register.all_request_usages,
            Patterns.account.get_or_register.handle(_get_or_register),
        )
        .intercept_request(
            Patterns.account.lookup_users.all_request_usages,
            Patterns.account.lookup_users.handle(_lookup_users),
        )
        .intercept_request(
            Patterns.account.search_all_users.all_request_usages,
            Patterns.account.search_all_users.handle(_search_all_users),
        )
    ).build()


@app.route("/api/service-to-module/<string:featureId>", methods=["POST"])
async def handle_request(featureId):
    data = await request.get_data()
    result = await session.accept_gateway_request(data)
    return result.to_json(), 200, {"Content-Type": "application/json"}


def _get_or_register(input: string, ctx: FeatureContext) -> Result[UserFull]:
    existingUser = {}
    for user in users.values():
        if user.handle == input:
            existingUser = user
    if existingUser:
        return Result.ok(existingUser)

    # Create a new user and return it
    new_user_id = uuid4()
    users[new_user_id] = UserFull(user_identifier=new_user_id, handle=input)

    return Result.ok(users[new_user_id])


def _lookup_users(input: List[UUID], ctx: FeatureContext) -> Result[List[UserFull]]:
    filtered_users = []
    for key in users.keys():
        if key in input:
            filtered_users.append(users[key])
    return Result.ok(list(filtered_users))


def _search_all_users(input: string, ctx: FeatureContext) -> Result[List[UserFull]]:
    filtered_users = []
    for key, value in users.items():
        if input.lower() in value.handle.lower():
            filtered_users.append(users[key])
    return Result.ok(list(filtered_users))


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    app.run(port=config.getint("Account", "port"))
