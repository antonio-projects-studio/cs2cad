import os
import json
import yaml
import numpy as np
import multiprocessing
from joblib import Parallel, delayed

from pathlib import Path

from terminal_app.env import PROJECT_CONFIG

from .my_client import MyClient
from .parser import FeatureListParser


# create instance of the OnShape client; change key to test on another stack
c = MyClient(logging=False)


def process_one(
    data_id: str, link: str, save_dir: Path | str = PROJECT_CONFIG.DOCUMENT_DIR
) -> int:
    save_path = os.path.join(save_dir, "{}.json".format(data_id))
    # if os.path.exists(save_path):
    #     return 1

    v_list = link.split("/")
    did, wid, eid = v_list[-5], v_list[-3], v_list[-1]

    # filter data that use operations other than sketch + extrude
    try:
        ofs_data = c.get_features(did, wid, eid).json()
        for item in ofs_data["features"]:
            if item["message"]["featureType"] not in ["newSketch", "extrude"]:
                return 0
    except Exception as e:
        print("[{}], contain unsupported features:".format(data_id), e)
        return 0

    # parse detailed cad operations
    try:
        parser = FeatureListParser(c, did, wid, eid, data_id=data_id)
        result = parser.parse()
    except Exception as e:
        print("[{}], feature parsing fails:".format(data_id), e)
        return 0
    if len(result["sequence"]) < 2:
        return 0
    with open(save_path, "w") as fp:
        json.dump(result, fp, indent=1)
    return len(result["sequence"])


def process_many(
    links_yml_file: Path | str,
    truck_id: str | None = None,
    n_jobs: int = multiprocessing.cpu_count(),
    save_dir: Path | str = PROJECT_CONFIG.DOCUMENT_DIR,
) -> None:
    if isinstance(links_yml_file, str):
        links_yml_file = Path(links_yml_file)

    if isinstance(save_dir, str):
        save_dir = Path(save_dir)

    name = links_yml_file.stem

    truck_id = name if truck_id is None else truck_id

    save_dir = save_dir / truck_id

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    with open(links_yml_file, "r") as fp:
        dwe_data = yaml.safe_load(fp)

    total_n = len(dwe_data)

    print("Processing truck: {}".format(truck_id))
    print(f"n_jobs: {n_jobs}")
    print(f"total_n: {total_n}")

    count = Parallel(n_jobs=n_jobs, verbose=2)(
        delayed(process_one)(data_id, link, save_dir)
        for data_id, link in dwe_data.items()
    )
    count = np.array(count)

    print("Valid: {}\nTotal: {}".format(np.sum(count > 0), total_n))
    print("Distribution:")

    for n in np.unique(count):
        print(n, np.sum(count == n))
