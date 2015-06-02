import sys


# Module for funcs that need python 2 syntax to work in python 2
def ignores_exc_tb(*args, **kwargs):
    """
    PYTHON 2 ONLY VERSION -- needs to be in its own file for syntactic reasons

    ignore_exc_tb decorates a function and remove both itself
    and the function from any exception traceback that occurs.

    This is useful to decorate other trivial decorators
    which are polluting your stacktrace.

    if IGNORE_TRACEBACK is False then this decorator does nothing
    (and it should do nothing in production code!)

    References:
        https://github.com/jcrocholl/pep8/issues/34  # NOQA
        http://legacy.python.org/dev/peps/pep-3109/
    """
    import utool as ut
    outer_wrapper = kwargs.get('outer_wrapper', True)
    def ignores_exc_tb_closure(func):
        if not ut.IGNORE_TRACEBACK:
            # if the global enforces that we should not ignore anytracebacks
            # then just return the original function without any modifcation
            return func
        #@wraps(func)
        def wrp_noexectb(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                # Define function to reraise with python 2 syntax
                #exc_type, exc_value, exc_traceback = sys.exc_info()
                # Code to remove this decorator from traceback
                # Remove two levels to remove this one as well
                exc_type, exc_value, exc_traceback = sys.exc_info()
                try:
                    exc_traceback = exc_traceback.tb_next
                    exc_traceback = exc_traceback.tb_next
                    #exc_traceback = exc_traceback.tb_next
                except Exception:
                    print('too many reraise')
                    pass
                raise exc_type, exc_value, exc_traceback
        if outer_wrapper:
            wrp_noexectb = ut.preserve_sig(wrp_noexectb, func)
        return wrp_noexectb
    if len(args) == 1:
        # called with one arg means its a function call
        func = args[0]
        return ignores_exc_tb_closure(func)
    else:
        # called with no args means kwargs as specified
        return ignores_exc_tb_closure