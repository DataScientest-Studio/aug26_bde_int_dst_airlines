
def exception_handling(function):
    def execute_exception_handling(*args,**kwargs):
        try:
            return function(*args,**kwargs)
        except Exception as err:
            print(f"Error: {err}")
            return None
    return execute_exception_handling
