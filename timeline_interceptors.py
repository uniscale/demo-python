from typing import List

from uniscale.core import PlatformInterceptorBuilder, Result
from uniscale.core.utilisation.utilisation_session_base import FeatureContext

from uniscale.uniscaledemo.messages.patterns import Patterns
from uniscale.uniscaledemo.messages.messages.empty import Empty
from uniscale.uniscaledemo.messages.messages.send_message_input import SendMessageInput
from uniscale.uniscaledemo.messages.messages.message_full import MessageFull

# Create in memory cache of messages
users = {}

def register_interceptors(builder: PlatformInterceptorBuilder):
    # Register an interceptor for the message feature SendMessage
    builder.with_interceptors(lambda i: i
        # Specify the AllMessageUsages pattern so that the implementation
        # picks up features for all use case instances this feature
        # is used in
        .intercept_message(Patterns.messages.send_message.all_message_usages,
                           # Define a handler for the feature
                           Patterns.messages.send_message.handle(_send_message))
        # Register an interceptor for the request/response feature GetMessageList
        .intercept_request(Patterns.messages.get_message_list.all_request_usages,
                           Patterns.messages.get_message_list.handle(_get_message_list))
                             )

def _send_message(input: SendMessageInput, ctx: FeatureContext) -> Result[Empty]:
    # TODO: Send message logic
    return Result.ok(Empty())

def _get_message_list(input: Empty, ctx: FeatureContext) -> Result[List[MessageFull]]:
    # TODO: Get message list logic
    messages = []
    return Result.ok(messages)