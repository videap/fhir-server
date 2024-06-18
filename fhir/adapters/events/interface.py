from pydantic import BaseModel
from typing import Literal, Callable, Any, Dict

class ConnectionParams(BaseModel):
    host: str
    port: int = 5672
    user: str
    password: str

class ListenerConfig(BaseModel):
    exchange_name:str
    exchange_type:Literal["topic", "direct", "fanout", "headers"] = "direct"
    queue_name:str
    routing_key:str
    on_message_callback: Callable = lambda *args, **kwargs: None #type: ignore
    on_message_callback_error: Callable = lambda *args, **kwargs: None #type: ignore

class EventToPublish(BaseModel):
    exchange_name:str
    exchange_type:Literal["topic", "direct", "fanout", "headers"] = "direct"
    publish_interval:float = 0.1
    queue_name:str
    routing_key:str
    on_confirmation_callback: Callable = lambda *args, **kwargs: None #type: ignore
    on_confirmation_callback_error: Callable = lambda *args, **kwargs: None #type: ignore

class Message(BaseModel):
    headers:Dict[Any,Any] = {}
    content:str