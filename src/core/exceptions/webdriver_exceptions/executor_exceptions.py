class ExecutorException(Exception):

    def __init__(self, message: str):
        if not isinstance(message,str):
            raise ValueError('message must be a str')

    def __str__(self):
        message_to_return = f'Error while executing the process: {self.message}'
        return message_to_return
