class AbstractUser:
    def __init__(self, is_authenticated: bool) -> None:
        self.is_authenticated = is_authenticated


class UiAuthenticatedUser(AbstractUser):
    def __init__(self, username: str, role: str, is_authenticated: bool = True) -> None:
        super().__init__(is_authenticated)
        self.username = username
        self.role = role

    @property
    def first_username_letter(self) -> str:
        return self.username[:1]


class UiAnonymousUser(UiAuthenticatedUser):
    def __init__(self) -> None:
        super().__init__('Anonymous user', 'Anonymous', is_authenticated=False)
