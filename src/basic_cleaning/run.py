#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # iamfiscus           #
    ######################
    logger.info("downloading artifact by `input_artifact`: %s",
                args.input_artifact)
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    logger.info("read csv at path: %s", args.artifact_local_path)
    df = pd.read_csv(artifact_local_path)

    logger.info("removing outliers range(%i - %i)",
                args.min_price, args.max_price)
    idx = df["price"].between(args.min_price, args.max_price)
    df = df[idx].copy()

    idx = df['longitude'].between(-74.25, -
                                  73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="input for artifact name: file(*.csv)",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="output for artifact name: file(*.csv)",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="output for artifact type",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str
        help="output for artifact description",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="minimum price for outlier range",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="maximum price for outlier range",
        required=True
    )

    args = parser.parse_args()

    go(args)
