from Db import TableModel


class _ModelUser(TableModel):
    def __init__(self):
        super().__init__(table="authenticated")


Model_User = _ModelUser()
