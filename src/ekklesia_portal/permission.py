from ekklesia_common.permission import CreatePermission, EditPermission, ViewPermission, WritePermission


class SupportPermission(WritePermission):
    pass


class VotePermission(WritePermission):
    pass
