"""_summary_:Optional SQL tool.
Assume a warehouse mirror exists with a table `shipments` that include normalized `consignee_codes_key` and shipment dates.
Replace with real engine.
"""

from typing import Any, Dict, List


class SQLTool:
    def __init__(self):
        pass

    def containers_arriving_in_next_days(
        self, consignee_code_key: str, days: int
    ) -> List[Dict[str, Any]]:
        # placeholder for implementation- use SQLAlchemy against our DW
        return []


sql_tool = SQLTool()
