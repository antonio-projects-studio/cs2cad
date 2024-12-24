import os
import json
from pathlib import Path
from typing import Literal

from OCC.Extend.DataExchange import write_step_file

from cs2cad.cadlib.extrude import CADSequence
from cs2cad.cadlib.visualize import create_CAD

from terminal_app.env import PROJECT_CONFIG
from terminal_app.naming import generate_path


def cs2cad(
    json_file: Path | str | dict,
    save_path: Path | str = PROJECT_CONFIG.DOCUMENT_DIR,
    name: str | None = None,
    mode: Literal["new", "replace", "continue"] = "continue",
) -> bool:
    naming: bool = name is None
    name = "cs2cad" if name is None else name

    if isinstance(json_file, str):
        json_file = Path(json_file)

    if isinstance(save_path, str):
        save_path = Path(save_path)

    assert not save_path.suffix, "cs2cad ERROR: save_path should be dir"

    if isinstance(json_file, Path):
        if naming:
            name = Path(json_file).stem

        try:
            with open(json_file, "r") as f:
                data = json.load(f)
        except Exception as ex:
            print(f"cs2cad ERROR: {json_file}, {ex}")
            return False
    else:
        data = json_file

    save_file = save_path / f"{name}.step"

    match mode:
        case "continue":
            if save_file.exists():
                return True
        case "new":
            save_file = generate_path(save_file, create=False)

    try:
        cad_seq = CADSequence.from_dict(data)
        cad_seq.normalize()
        out_shape = create_CAD(cad_seq)

    except:
        print("cs2cad ERROR: Load and create failed.")
        return False

    if not save_path.exists():
        os.mkdir(save_path)

    write_step_file(out_shape, save_file.as_posix())
    return True
