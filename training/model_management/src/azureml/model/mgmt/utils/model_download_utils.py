# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Model download utils."""

import os
import shutil
import stat
from datetime import datetime
from pathlib import Path
from azureml.model.mgmt.config import PathType
from azureml.model.mgmt.utils.common_utils import run_command, log_execution_time, switch_dir


def _get_system_time_utc():
    return "{0:%Y-%m-%d %H:%M:%S}".format(datetime.utcnow())


def _get_size(path: Path, size: int = 0) -> int:
    if os.path.isfile(path):
        return os.stat(path).st_size
    for entry in os.scandir(path):
        size += _get_size(entry)
    return size


def _round_size(size: int) -> str:
    CONST = 1024
    dim = ["B", "KB", "MB", "GB", "TB"]
    count = 0
    while size / CONST > 1:
        count += 1
        size /= CONST
    return f"{size:.2f} {dim[count]}"


def _onerror(func, path, exc_info):
    """Error Handler for shutil rmtree."""
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


def _download_git_model(model_uri: str, model_dir: Path) -> None:
    """Download model files from GIT repository.

    :param model_url: git clonable uri of a public repo
    :type model_url: str
    :param model_dir: local directory to clone model to
    :type: Path
    """
    # do shallow fetch
    clone_cmd = f"git clone --depth=1 {model_uri} {model_dir}"
    exit_code, stdout = run_command(clone_cmd)
    if exit_code != 0:
        raise Exception(f"Could not clone repo {model_uri}. Error => {stdout}")

    download_details = {}
    download_details["download_time_utc"] = _get_system_time_utc()
    # fetch commit details
    with switch_dir(model_dir):
        cmd = "git log --oneline -n 1 --pretty=tformat:'%H'"
        exit_code, stdout = run_command(cmd)
        if exit_code != 0:
            raise Exception(f"Could not capture commit HEAD. Error => {stdout}")
        download_details["commit_hash"] = stdout
    git_path = os.path.join(model_dir, ".git")
    shutil.rmtree(git_path, onerror=_onerror)
    download_details["model_size"] = _round_size(_get_size(model_dir))
    return download_details


def _download_azure_artifacts(model_uri, model_dir):
    """Download model files from blobstore.

    :param model_url: Publicly readable blobstore URI of model files
    :type model_url: str
    :param model_dir: local directory to download model to
    :type: Path
    """
    try:
        download_cmd = f"azcopy cp --recursive=true {model_uri} {model_dir}"
        # TODO: Handle error case correctly, since azcopy exits with 0 exit code, even in case of error.
        # https://github.com/Azure/azureml-assets/issues/283
        exit_code, stdout = run_command(download_cmd)
        if exit_code != 0:
            raise Exception(f"Failed to download model files with URL: {model_uri}. Error => {stdout}")
        download_details = {}
        download_details["download_time_utc"] = _get_system_time_utc()
        download_details["model_size"] = _round_size(_get_size(model_dir))
        return download_details
    except Exception as e:
        raise e


@log_execution_time
def download_model(model_path_type: PathType, model_uri: str, model_dir: Path) -> None:
    """Prepare the Download Environment.

    :param model_path_type: Model path type
    :type model_path_type: PathType
    :param model_uri: uri to model files
    :type model_uri: str
    :param model_dir: local folder to download model files too
    :type model_dir: Path
    """
    if model_path_type == PathType.GIT.value or model_path_type == PathType.GIT:
        return _download_git_model(model_uri, model_dir)
    elif model_path_type == PathType.AZUREBLOB.value or model_path_type == PathType.AZUREBLOB:
        return _download_azure_artifacts(model_uri, model_dir)
    else:
        raise Exception("Unsupported Model Download Method.")