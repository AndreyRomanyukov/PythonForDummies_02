from functools import wraps

def is_ajax(method):

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if "X-Requested-With" in self.request.headers:
            if self.request.headers['X-Requested-With'] == "XMLHttpRequest":
                return method(self, *args, **kwargs)

        else:                                                                                                                                                                 
            self.redirect("/")                                                     

    return wrapper 