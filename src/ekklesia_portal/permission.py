from ekklesia_common.permission import WritePermission, CreatePermission, EditPermission, ViewPermission


class SupportPermission(WritePermission):
    pass


class VotePermission(WritePermission):
    pass
