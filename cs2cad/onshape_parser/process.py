import os
import json
import yaml
import numpy as np
from joblib import Parallel, delayed

from pathlib import Path
from dataclasses import dataclass

from terminal_app.env import PROJECT_CONFIG

from .my_client import MyClient
from .parser import FeatureListParser


# create instance of the OnShape client; change key to test on another stack
c = MyClient(logging=False)


@dataclass
class ParsingStatistic:
    truck_id: str
    total: int
    valid: int
    distribution: list[tuple[int, int]]

    def __str__(self) -> str:
        return "Total: {}\nValid: {}\nDistribution: {}".format(
            self.total,
            self.valid,
            "\n".join(f"{n}: {cnt}" for n, cnt in self.distribution),
        )


def process_one(
    data_id: str, link: str, save_dir: Path | str = PROJECT_CONFIG.DOCUMENT_DIR
) -> int:
    save_path = os.path.join(save_dir, "{}.json".format(data_id))
    if os.path.exists(save_path):
        return 1

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
    n_jobs: int = -1,
    save_dir: Path | str = PROJECT_CONFIG.DOCUMENT_DIR,
) -> tuple[Path, ParsingStatistic]:
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

    statistic = ParsingStatistic(
        truck_id=truck_id,
        total=total_n,
        valid=int(np.sum(count > 0)),
        distribution=[(int(n), int(np.sum(count == n))) for n in np.unique(count)],
    )

    return save_dir, statistic
