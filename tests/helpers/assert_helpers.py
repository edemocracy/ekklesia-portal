from contextlib import contextmanager


@contextmanager
def assert_no_difference(func, name=None):
    """Asserts that the function result is unchanged after executing the block"""
    val = func()
    yield
    val_after = func()

    def assertion_msg():
        msg = f'result is not the same! value before {val}, after: {val_after}'
        if name:
            return f'{name}: ' + msg
        return msg

    assert val_after == val, assertion_msg()


@contextmanager
def assert_difference(func, diff, name=None):
    """
    Asserts that the function result has changed by `diff` after executing the block
    `diff` can be anything, but addition with the result of `func` must be defined.
    """
    val = func()
    yield
    val_after = func()

    def assertion_msg():
        msg = f'result for did not change by {diff}! value before {val}, after: {val_after}'
        if name:
            return f'{name}: ' + msg
        return msg

    assert val_after == val + diff, assertion_msg()
