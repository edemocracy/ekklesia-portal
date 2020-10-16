def identity_manages_department(identity, department):
    if identity.has_global_admin_permissions:
        return True

    return department in identity.user.managed_departments
