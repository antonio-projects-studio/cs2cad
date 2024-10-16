import os
import json
from pathlib import Path

from OCC.Extend.DataExchange import write_step_file

from cs2cad.cadlib.extrude import CADSequence
from cs2cad.cadlib.visualize import create_CAD

from terminal_app.naming import generate_path


def cs2cad(
    json_file: Path | str | dict, save_path: Path | str, name: str | None = None
) -> None:
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

        with open(json_file, "r") as f:
            data = json.load(f)
    else:
        data = json_file

    try:
        cad_seq = CADSequence.from_dict(data)
        cad_seq.normalize()
        out_shape = create_CAD(cad_seq)

    except:
        print("cs2cad ERROR: Load and create failed.")

    if not save_path.exists():
        os.mkdir(save_path)

    write_step_file(out_shape, generate_path(save_path / f"{name}.step"))


# src_dir = args.src
# print(src_dir)
# out_paths = sorted(glob.glob(os.path.join(src_dir, "*.{}".format(args.form))))
# if args.num != -1:
#     out_paths = out_paths[args.idx : args.idx + args.num]
# save_dir = args.src + "_step" if args.outputs is None else args.outputs
# ensure_dir(save_dir)

# for path in out_paths:
#     print(path)
#     try:
#         if args.form == "h5":
#             with h5py.File(path, "r") as fp:
#                 out_vec = fp["out_vec"][:].astype(np.float)
#                 out_shape = vec2CADsolid(out_vec)
#         else:
#             with open(path, "r") as fp:
#                 data = json.load(fp)
#             cad_seq = CADSequence.from_dict(data)
#             cad_seq.normalize()
#             out_shape = create_CAD(cad_seq)

#     except Exception as e:
#         print("load and create failed.")
#         continue

#     if args.filter:
#         analyzer = BRepCheck_Analyzer(out_shape)
#         if not analyzer.IsValid():
#             print("detect invalid.")
#             continue

#     name = path.split("/")[-1].split(".")[0]
#     save_path = os.path.join(save_dir, name + ".step")
#     write_step_file(out_shape, save_path)
