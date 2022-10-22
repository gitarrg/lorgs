#!/usr/bin/env python

import glob
import hashlib
import io
import os
import shutil
import subprocess
import typing

import boto3
import botocore

LAMBDA_CLIENT = boto3.client('lambda')
S3_CLIENT = boto3.client('s3')


# SETTINGS
DEPLOY_BUCKET = os.getenv("DEPLOY_BUCKET") or "lorrgs-code"

DEPLOY_DIR = "./.deploy"


################################################################################
# Utils
#

def calc_checksum(path):
    """Calc an MD5 Checksum for a given path"""
    hash = hashlib.md5()

    for filepath in glob.glob(path, recursive=True):
        with open(filepath, "rb") as f:
            hash.update(f.read())

    return hash.hexdigest()


def zip_folder(src, tar):
    zip_file = shutil.make_archive("tmp_zip", "zip", base_dir=src)
    return shutil.move(zip_file, tar)


def checksum_compare(name: str, files: str, s3Bucket=DEPLOY_BUCKET):
    """Compare the Checksum of `files` with an prev. version stored on S3.
        Returns True if they are the same.
    """
    # fetch old checksum
    try:
        old_sha = S3_CLIENT.get_object(Bucket=s3Bucket, Key=f"{name}.md5")
        old_sha = old_sha.get("Body").read().decode('utf-8')
    except S3_CLIENT.exceptions.NoSuchKey:
        old_sha = ""

    # calc new checksum
    new_sha = calc_checksum(files)

    # cache latest
    if old_sha != new_sha:
        print(name, "has changed", old_sha, ">", new_sha)
        S3_CLIENT.put_object(
            Bucket=s3Bucket,
            Key=f"{name}.md5",
            Body=io.BytesIO(new_sha.encode("utf-8"))
        )
    else:
        print(name, "did not change. :)")

    return old_sha == new_sha


################################################################################

def get_layer_versions(name, max=50):
    response = LAMBDA_CLIENT.list_layer_versions(LayerName=name, MaxItems=max)
    return response.get("LayerVersions") or []


def _deploy_layer(name, path):
    zip_file = shutil.make_archive(base_name=path, format="zip", root_dir=path)
    S3_CLIENT.upload_file(zip_file, DEPLOY_BUCKET, f"{name}.zip")
    return LAMBDA_CLIENT.publish_layer_version(
        LayerName=name,
        Content={
            "S3Bucket": DEPLOY_BUCKET,
            "S3Key": f"{name}.zip",
        }
    )


def delete_layer_versions(name):

    for layer_version in get_layer_versions(name):
        version = layer_version.get("Version")
        if version:
            LAMBDA_CLIENT.delete_layer_version(LayerName=name, VersionNumber=version)
            print(f"deleting {name}.{version}")


def deploy_layer(name, src_dir):

    if checksum_compare(name=name, files=f"{src_dir}/**/*.py"):
        return

    path = f"{DEPLOY_DIR}/{name}"
    shutil.copytree(src_dir, f"{path}/python/{src_dir}")
    delete_layer_versions(name)
    return _deploy_layer(name, path)


def deploy_requirements_layer(name="requirements"):

    if checksum_compare(name=name, files="requirements.txt"):
        return

    path = f"{DEPLOY_DIR}/{name}"

    subprocess.call([
        "pip",
        "install", "-r", "requirements.txt",
        f"--target={path}/python"
    ])

    delete_layer_versions(name)
    return _deploy_layer(name, path)


def deploy_lambda(name: str, src: str):
    """Update the Lambda with `name` to use the Code found in `src`."""
    if checksum_compare(name=name, files=f"{src}/**/*.py"):
        return

    # zip
    zip_file = zip_folder(src=src, tar=f"{DEPLOY_DIR}/{name}.zip")

    # upload and update
    S3_CLIENT.upload_file(zip_file, DEPLOY_BUCKET, f"{name}.zip")
    LAMBDA_CLIENT.update_function_code(FunctionName=name, S3Bucket=DEPLOY_BUCKET, S3Key=f"{name}.zip")


def update_used_layers(lambda_names: typing.List[str], layer_names: typing.List[str]):


    layers = []
    for layer in layer_names:
        layer_versions = get_layer_versions(layer, max=1)
        if layer_versions:
            latest = layer_versions[0]  # seems to be sorted
            arn = latest.get("LayerVersionArn")
            if arn:
                layers.append(arn)

    for name in lambda_names:
        print("Updting Layers for", name, layers)
        LAMBDA_CLIENT.update_function_configuration(
            FunctionName=name,
            Layers=layers
        )


################################################################################


def main():

    if os.path.exists(DEPLOY_DIR):
        shutil.rmtree(DEPLOY_DIR)
    os.mkdir(DEPLOY_DIR)

    # Layers
    core_layer = deploy_layer("lorrgs-core", src_dir="lorgs")
    reqs_layer = deploy_requirements_layer(name="lorrgs-requirements")

    # Lambdas
    deploy_lambda(name="lorrgs-api", src="lorgs")
    deploy_lambda(name="lorrgs-sqs", src="lorrgs_sqs")

    # Update if one of them got deployed
    if core_layer or reqs_layer or True:
        update_used_layers(
            lambda_names=["lorrgs-api", "lorrgs-sqs"],
            layer_names=["lorrgs-core", "lorrgs-requirements"]
        )


if __name__ == "__main__":
    main()
