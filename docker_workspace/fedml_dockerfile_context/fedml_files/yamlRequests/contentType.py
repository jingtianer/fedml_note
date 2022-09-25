from enum import Enum
class ContentType(Enum):
    Json = 'json'
    Binary = 'binary'
    Text = 'text'

def getContentType(value):
    return ContentType._value2member_map_[value]