from datetime import datetime
from typing import List, Tuple
from pydantic import BaseModel


# class Metric(BaseModel):
#     label: str
#     values: List[Tuple[datetime, float]]
#
#
# influx_metrics = [
#     Metric(label="yo", values=[(datetime(2022, 10, 22, 23, 55, 59, 342380), 20.0), (datetime(2022, 10, 18, 23, 55, 59, 342380), 30.0)]),
#     Metric(label="teers", values=[(datetime(2022, 10, 19, 23, 55, 59, 342380), 40.0), (datetime(2022, 10, 28, 13, 55, 59, 342380), 10.0)]),
#     Metric(label="ap", values=[(datetime(2022, 10, 17, 23, 55, 59, 342380), 60.0), (datetime(2022, 10, 28, 23, 55, 59, 342380), 50.0)]),
# ]
#
# values = []
#
# for influx_metric in influx_metrics:
#     values.extend(influx_metric.values)
# last_metric = max(values, key=lambda item: item[0])

dict1 = {
    "spectrum": {"uuid": "kbxjwbxwkjxl"}
}

dict2 = {
    "infinity": {"uuid": "blkwdnc"}
}

my_list = [dict1, dict2]

my_list = [element["spectrum"] for element in my_list if "spectrum" in element][0]

print("arisnaos: ", my_list)
