class TaskLimitError(Exception):
    def __init__(self, limit: int) -> None:
        self.limit = limit
        super().__init__(f"Task limit exceeded. Maximum allowed: [{limit}].")