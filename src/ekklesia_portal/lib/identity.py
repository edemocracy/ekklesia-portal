def identity_manages_department(identity, department):
    if identity.has_global_admin_permissions:
        return True

    return department in identity.user.managed_departments


def identity_manages_any_department(identity):
    if identity.has_global_admin_permissions:
        return True

    return bool(identity.user.managed_departments)

