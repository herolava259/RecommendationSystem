import re
import shutil
import tempfile
import os
import urllib
import zipfile
import tarfile
from typing import Self, List, Dict, Set, Sequence, Literal
from datetime import datetime
from functools import partial

import urllib3
from tensorflow import Module
#from tensorflow.keras.utils import Sequence as Sq
from tensorflow.io import gfile
from typing import Any

class ML100KDataWorkspace(Module):


    def __init__(self, name: str, data_dir: str, include_files: Sequence[str] | None = None,exclude_files: Sequence[str] | None = None):
        super().__init__(name)
        self.data_dir = data_dir
        self.include_files: Set[str]  = set(include_files)
        self.exclude_files: Set[str] = set(exclude_files)

    def mark_as_exclude(self, filenames: str | Set[str]):
        if isinstance(filenames, str):
            self.exclude_files.add(filenames)
            self.include_files -= {filenames}
        elif isinstance(filenames, (list, set, tuple)):
            self.exclude_files |= set(filenames)
            self.include_files -= set(filenames)

    def mark_as_include(self, filename: str):
        pass

    def stats(self, exclude_visible: bool = False):
        pass

    def exists_file(self, filename: str) -> bool:
        return gfile.exists(gfile.join(self.data_dir, filename))

    def create_sub_workspace(self, new_ws_name: str,
                             takeaway_type: Literal[
                                 "replicate", "all-include-move", "all-exclude-move", "all-include-copy",
                                 "all-exclude-copy", "custom"] = "all-include-copy",
                             replicate_files: List[str] | Dict[str] | None = None,
                             moved_files: List[str] | Dict[str] | None = None,
                             mark_way: Literal["as-original", "all-include", "all-exclude", "custom"] = "as-original",
                             new_file_marks: Dict[str, Sequence[str]] | None = None) -> Self:

        new_ws_dir = gfile.join(self.data_dir, new_ws_name + datetime.now().strftime("_%Y_%m_%d__%H_%M_%S"))
        gfile.mkdir(new_ws_dir)

        data_fn = lambda sa, sb, cp: (sa | sb, sa, sb, cp)

        behaviour_mapping = {"replicate": partial(data_fn, sa=self.include_files, sb=self.exclude_files, cp=shutil.copy),
                         "all-include-copy": partial(data_fn, sa=self.include_files, sb=set(), cp=shutil.copy),
                         "all-exclude-copy": partial(data_fn, sa=set(), sb=self.exclude_files, cp=shutil.copy),
                         "all-include-move": partial(data_fn, sa=self.include_files, sb=set(), cp=shutil.move),
                         "all-exclude-move": partial(data_fn, sa=set(), sb=self.exclude_files, cp=shutil.move)}

        if takeaway_type in behaviour_mapping.keys():
            # copy all
            target_files, include_files, exclude_files, data_fn = behaviour_mapping[takeaway_type]()
            for fn in target_files:
                file_src = gfile.join(self.data_dir, fn)
                file_dst = gfile.join(new_ws_dir, fn)
                data_fn(file_src, file_dst)
            return ML100KDataWorkspace(data_dir=new_ws_dir, name=new_ws_name, include_files=include_files,
                                       exclude_files=exclude_files)


        # custom takeaway type
        if isinstance(replicate_files, list):
            replicate_files = {fname: fname for fname in replicate_files}
        elif replicate_files is None:
            replicate_files = dict()

        if moved_files is None:
            moved_files = dict()
        elif isinstance(moved_files, list):
            moved_files = {fname: fname for fname in moved_files}

        # prune no exists filenames
        all_file_names = self.include_files | self.exclude_files
        joint_rep_file_names = set(replicate_files.keys()) & all_file_names
        joint_moved_file_names = set(moved_files.keys()) & all_file_names

        replicate_files = {fn: replicate_files[fn] for fn in (joint_rep_file_names - joint_moved_file_names)}
        moved_files = {fn: moved_files[fn] for fn in joint_moved_file_names}

        # validate extensions
        for k, v in replicate_files.items():
            if k.split(".")[-1] != v.split(".")[-1]:
                raise RuntimeError("Destination file has not corrected format.")

        for k, v in moved_files.items():
            if k.split(".")[-1] != v.split(".")[-1]:
                raise RuntimeError("Destination file has not corrected format.")

        # copy or move to dest
        for fs, fd in replicate_files:
            f_src = gfile.join(self.data_dir, fs)
            f_dst = gfile.join(self.data_dir, fd)
            shutil.copy(f_src, f_dst)

        for fs, fd in moved_files:
            f_src = gfile.join(self.data_dir, fs)
            f_dst = gfile.join(self.data_dir, fd)
            shutil.move(f_src, f_dst)

        all_taken_files = set(replicate_files.keys()) | set(moved_files.keys())

        inc_files = set()
        exc_files = set()
        if mark_way == "as-original":
            inc_files = all_taken_files & self.include_files
            exc_files = all_taken_files & self.exclude_files
        elif mark_way == "all-include":
            inc_files = set(all_taken_files)
        elif mark_way == "all-exclude":
            exc_files = set(all_taken_files)
        elif mark_way == "custom" and new_file_marks is not None:
            inc_files = set(new_file_marks.get("include", None))
            exc_files = set(new_file_marks.get("exclude", None))
        else:
            raise TypeError("Argument mark-way and new_file_marks are invalids.")

        inc_files = {replicate_files[fn] for fn in (set(replicate_files.keys()) & inc_files)} | {moved_files[fn] for fn
                                                                                                 in (set(moved_files.keys()) & inc_files)}
        exc_files = {replicate_files[fn] for fn in (set(replicate_files.keys()) & exc_files)} | {moved_files[fn] for fn
                                                                                                 in (set(moved_files.keys()) & exc_files)}

        return ML100KDataWorkspace(name=new_ws_name, data_dir=new_ws_dir, include_files=inc_files, exclude_files=exc_files)

    ## read files info in workspace
    def get_file_info(self, file_name: str, show_infos: List[str] | None = None) -> Dict[str, Any]:
        pass

    def get_all_file_infos(self, file_name: str
                               , prefix_filter: str | None
                               , suffix_filer: str | None
                               , keyword: str | None
                               , show_include: bool = True
                               , show_exclude: bool = True
                               , show_infos: List[str] | None = None):
        pass

    def create_replicate(self, take_exclude_files: bool = False, in_temp: bool = True,
                         ws_dir: str | None = None) -> Self:
        inc_files = self.include_files
        exc_files = self.exclude_files if take_exclude_files else set()
        if in_temp:
            ws_dir = gfile.join(tempfile.gettempdir(), self.name + datetime.now().strftime("_%Y_%m_%d__%H_%M_%S"))
        elif not ws_dir:
            ws_dir = gfile.join(self.data_dir, self.name + datetime.now().strftime("_%Y_%m_%d__%H_%M_%S"))

        for fn in (inc_files | exc_files):
            f_src = gfile.join(self.data_dir, fn)
            f_dst = gfile.join(ws_dir, fn)
            shutil.copy(f_src, f_dst)

        return ML100KDataWorkspace(data_dir=ws_dir, name=self.name, include_files=inc_files)

    def prune(self, ):
        """remove all exclude files and files not include types"""
        remove_files = set(gfile.listdir(self.data_dir)) - self.include_files
        for ffn in remove_files:
            gfile.remove(gfile.join(self.data_dir, ffn))
        self.exclude_files = set()

    ## implement later
    def __enter__(self, ):
        pass

    def __exit__(self, ):
        pass

    def add_metadata(self, metadata: dict):
        pass



class ML100KDataSourcer(Module):
    def __init__(self, data_source="/kaggle/input/movielens-100k-dataset/ml-100k/"):
        super().__init__()
        self.data_source = data_source
        self.main_dir = self.data_source
        self.list_files = []

    @staticmethod
    def extr_file_extension(filepath: str) -> str:
        return filepath.split(".")[-1]

    @staticmethod
    def extr_file_name(filepath: str) -> str:
        return filepath.split("/")[-1].split(".")[0]

    @staticmethod
    def _download_and_extract_data(url, target_dir) -> None:
        temp_dir = tempfile.gettempdir()

        file_extension = ML100KDataSourcer.extr_file_extension(url)
        file_name = ML100KDataSourcer.extr_file_name(url)

        temp_down_path = gfile.join(temp_dir, file_name)
        pool_manager = urllib3.PoolManager()
        with pool_manager.request("GET", url) as resp, gfile.GFile(temp_down_path, "w") as f:
            num_read = 0
            CHUNK = 1024 * 8
            while num_read < 10000:
                chunk = resp.read(CHUNK)
                if not chunk:
                    break
                f.write(chunk)
                num_read += 1

        if num_read >= 10000:
            raise RuntimeError("file is very large.")
        print("Completely download!")

        if file_extension == "zip":
            with zipfile.ZipFile(temp_down_path, "r") as zr:
                zr.extractall(target_dir)
        elif file_extension == "tar":
            with tarfile.open(temp_down_path, "r") as tar:
                tar.extractall(path=target_dir)
        else:
            raise RuntimeError("Unsupported data type of downloaded file to extract.")

        print("Completely extract file")
        print("all extracted file")
        print(gfile.listdir(target_dir))
        try:
            gfile.remove(temp_down_path)
        except Exception as ex:
            print(f"Error while remove compress file:\n{ex}")

    def load(self):
        if re.match(r"https?://\S+|www\.\S+", self.data_source):
            self.main_dir = gfile.join(tempfile.gettempdir(), "ml_100k")
            gfile.mkdir(self.main_dir) if not gfile.exists(self.main_dir) else None
            ML100KDataSourcer._download_and_extract_data(self.data_source, self.main_dir)

        self.list_files = gfile.listdir(self.main_dir)

    def create_new_data_workspace(self, workspace_name: str,
                                  dst_dir: str | None = None, filenames: List[str] | None | Dict[str, str] = None) \
            -> ML100KDataWorkspace:

        if dst_dir is None:
            dst_dir = gfile.join(tempfile.gettempdir(), "ml_100k_workspace")

        if not gfile.exists(dst_dir):
            gfile.mkdir(dst_dir)

        ws_dir = gfile.join(dst_dir, workspace_name + datetime.now().strftime("_%Y_%m_%d__%H_%M_%S"))
        gfile.mkdir(ws_dir)

        # move data or copy to dest dir
        if filenames is None:
            # if not pass filenames load all files
            filenames = self.list_files if len(self.list_files) > 0 else gfile.listdir(self.main_dir)
        if isinstance(filenames, list):
            filenames = {fn: fn for fn in filenames}

        # validate file extension same as the original
        for src_f, dst_f in filenames.items():
            if src_f.split(".")[-1] != dst_f.split(".")[-1]:
                raise RuntimeError("Desdtination file has not conrrected format.")

        for src_f, dst_f in filenames.items():
            abs_src_p = gfile.join(self.main_dir, src_f)
            dst_src_p = gfile.join(ws_dir, dst_f)
            gfile.copy(abs_src_p, dst_src_p, overwrite=True)

        return ML100KDataWorkspace(name=workspace_name, data_dir=ws_dir, include_files=filenames.values())

