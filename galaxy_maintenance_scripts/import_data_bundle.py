import os
from typing import Optional

import click
import yaml

from galaxy.config import GalaxyAppConfiguration
from galaxy.files.uris import stream_url_to_file
from galaxy.tool_util.data import BundleProcessingOptions
from galaxy.tools.data import ToolDataTableManager


@click.command(help="Import tool data bundle. URI can be a path to a zipped file or directory.")
@click.option("--tool-data-path", type=click.Path(exists=True, resolve_path=True), help="Path were bundle data should be written to")
@click.option("--data-table-config-path", type=click.Path(exists=True, resolve_path=True), help="Path to tool_data_table_conf.xml file")
@click.option("--data-manager-config-file", type=click.Path(exists=True, resolve_path=True), help="Path to shed_data_manager_conf.xml file")
@click.option(
    "-t",
    "--tool-data-file-path",
    type=click.Path(exists=True, resolve_path=True),
    help="loc file to append data to. Must be be loaded in general data tables",
)
@click.argument("uri")
def run_import_data_bundle(uri: str, tool_data_path: str, data_table_config_path: str, data_manager_config_file: str, tool_data_file_path: Optional[str] = None):
    table_manager = ToolDataTableManager(
        tool_data_path=tool_data_path,
        config_filename=data_table_config_path,
    )
    options = BundleProcessingOptions(
        what="data import",  # An alternative to this is sticking this in the bundle, only used for logging.
        data_manager_path=tool_data_path,
        target_config_file=data_manager_config_file,
        tool_data_file_path=tool_data_file_path,
    )
    if uri.startswith("file://"):
        target = uri[len("file://") :]
    else:
        target = stream_url_to_file(uri)
    table_manager.import_bundle(
        target,
        options,
    )


if __name__ == "__main__":
    run_import_data_bundle()
