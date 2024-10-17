import logging
import const
import functools

def global_error_handler_async(func):

    """general handler for Internal Server Error logging of async functions"""

    @functools.wraps(func) #in order to see original function name
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            log_raise_error(e, func)
    return wrapper


def global_error_handler_sync(func):

    """general handler for Internal Server Error logging of sync functions"""

    @functools.wraps(func) 
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_raise_error(e, func)
    return wrapper



def log_raise_error(exception, func):

    """The function for errors detailed handling"""

    if not hasattr(exception, '_logged'):
        module_name = func.__module__
        function_name = func.__name__ 
        error_text = const.ErrorArose.format(function_name, module_name, str(exception))
        try:
            logging.error(error_text)

        except Exception as e: #if smth happend with the logger
            print(const.LoggerError.format(error_text, str(e)))
        setattr(exception, '_logged', True)  
            #add a new attribute in order to mark the error as logged already. 
            #Otherwise we will see the same error for each function in the stack
        raise


class WrongStatusError(Exception):

    """ the error for the case when the API returns wrong error code"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)