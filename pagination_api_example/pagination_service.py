import json


# from pathlib import Path
# print(Path.cwd()) --> find path to import the data.json file


class DataObject:
    count: int
    total: int
    data: [...]
    pagination: {str: {str: str}}

    def __init__(self, count, data, total, pagination):
        self.count = count
        self.data = data
        self.total = total
        self.pagination = pagination


def fetch_data(page_num: int = 1, page_size: int = 10):
    with open("/home/andreas/PycharmProjects/fastApiProject/pagination_api_example/data.json") as file:
        data = json.load(file)
        total = len(data)
        start = (page_num - 1) * page_size
        end = start + page_size
        data = data[start:end]
        count = len(data)
        pagination = {
            "next": None,
            "previous": None
        }

        if end >= total:
            if page_num > 1:
                pagination["previous"] = f"/pagination/dummy_data/?page_num={page_num - 1}&page_size={page_size}"

        else:
            pagination["next"] = f"/pagination/dummy_data/?page_num={page_num + 1}&page_size={page_size}"
            if page_num > 1:
                pagination["previous"] = f"/pagination/dummy_data/?page_num={page_num - 1}&page_size={page_size}"

        return DataObject(count, data, total, pagination)
