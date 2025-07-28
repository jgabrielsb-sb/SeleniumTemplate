class InitiliazerException(Exception):

    def __init__(self, message: str):
        if not isinstance(message,str):
            raise ValueError('message must be a str')
        self.message = message

    def __str__(self):
        message_to_return = f'{self.message}'
        return message_to_return

class SetConfigException(InitiliazerException):
    def __str__(self):
        message_to_return = f'{self.message}'
        return message_to_return

class PreConditionNotMetException(InitiliazerException):
    def __str__(self):
        message_to_return = f'{self.message}'
        return message_to_return