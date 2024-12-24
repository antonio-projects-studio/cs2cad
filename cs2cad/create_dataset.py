import numpy as np
from typing import Sequence

from joblib import Parallel, delayed

from cs2cad import cs2cad
from cs2cad.onshape_parser.my_client import MyClient
from cs2cad.onshape_parser import process_many, ParsingStatistic


def create_dataset(query: str, limit: int = 200) -> tuple[ParsingStatistic, int]:
    file_path = MyClient(logging=False).query2yml(query=query, limit=limit)
    json_path, st = process_many(file_path)
    cs2cad_error = int(np.sum(
        np.array([cs2cad(file, json_path) for file in json_path.iterdir()]) == False
    ))

    return st, cs2cad_error


def create_datasets(queries: Sequence[tuple[str, int] | str], n_jobs: int = -1):
    func_list = []

    for query in queries:
        if isinstance(query, str):
            func_list.append(delayed(create_dataset)(query))
        else:
            func_list.append(delayed(create_dataset)(query[0], query[1]))

    results = Parallel(n_jobs, verbose=2)(func_list)

    return results
