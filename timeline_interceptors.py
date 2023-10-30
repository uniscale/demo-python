from typing import List
from uuid import uuid4
from datetime import datetime

from uniscale.core import PlatformInterceptorBuilder, Result
from uniscale.core.utilisation.utilisation_session_base import FeatureContext

from uniscale.uniscaledemo.messages_1_0.error_codes import ErrorCodes
from uniscale.uniscaledemo.messages.patterns import Patterns
from uniscale.uniscaledemo.messages.messages.empty import Empty
from uniscale.uniscaledemo.messages.messages.user_tag import UserTag
from uniscale.uniscaledemo.messages.messages.send_message_input import SendMessageInput
from uniscale.uniscaledemo.messages.messages.message_full import MessageFull

# Create in memory cache of messages
messages = {}


def register_interceptors(builder: PlatformInterceptorBuilder):
    # Register an interceptor for the message feature SendMessage
    builder.with_interceptors(
        lambda i: i
        # Specify the AllMessageUsages pattern so that the implementation
        # picks up features for all use case instances this feature
        # is used in
        .intercept_message(
            Patterns.messages.send_message.all_message_usages,
            # Define a handler for the feature
            Patterns.messages.send_message.handle(_send_message),
        )
        # Register an interceptor for the request/response feature GetMessageList
        .intercept_request(
            Patterns.messages.get_message_list.all_request_usages,
            Patterns.messages.get_message_list.handle(_get_message_list),
        )
    )


def _send_message(input: SendMessageInput, ctx: FeatureContext) -> Result[Empty]:
    if len(input.message) not in range(3, 60):
        return Result.bad_request(ErrorCodes.messages.invalid_message_length)
    msg = MessageFull(
        messageIdentifier=uuid4(),
        message=input.message,
        created=UserTag(by=input.by, at=datetime.now()),
    )
    messages[msg.message_identifier] = msg
    return Result.ok(Empty())


def _get_message_list(input: Empty, ctx: FeatureContext) -> Result[List[MessageFull]]:
    return Result.ok(
        sorted(messages.values(), key=lambda i: i.created.at, reverse=True)
    )
