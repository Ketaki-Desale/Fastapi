def check_role(user_roles: list, required_role: str) -> bool:
    """
    Check if a user has the required role.

    Args:
        user_roles (list): A list of roles assigned to the user.
        required_role (str): The role to check against the user's roles.

    Returns:
        bool: True if the user has the required role, False otherwise.
    """
    return required_role in user_roles
