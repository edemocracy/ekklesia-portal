from contextlib import contextmanager


@contextmanager
def assert_no_difference(func):
    """Asserts that the function result is unchanged after executing the block"""
    val = func()
    yield
    val_after = func()
    assert val_after == val, f'Result is not the same! Value before {val}, after: {val_after}'


@contextmanager
def assert_difference(func, diff):
    """
    Asserts that the function result has changed by `diff` after executing the block
    `diff` can be anything, but addition with the result of `func` must be defined.
    """
    val = func()
    yield
    val_after = func()
    assert val_after == val + diff, f'Result did not change by {diff}! Value before {val}, after: {val_after}'
