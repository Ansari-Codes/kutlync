from Db import TableModel


class _ModelLink(TableModel):
    def __init__(self):
        super().__init__(table="links")


Model_Link = _ModelLink()
