from Db import TableModel


class _ModelSession(TableModel):
    def __init__(self):
        super().__init__(table="sessions")


Model_Session = _ModelSession()
