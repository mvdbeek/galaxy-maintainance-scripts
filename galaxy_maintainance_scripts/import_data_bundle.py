from typing import Optional

import click
import yaml

from galaxy.config import GalaxyAppConfiguration
from galaxy.files.uris import stream_url_to_file
from galaxy.tool_util.data import (
    BundleProcessingOptions,
    ToolDataTableManager,
)


@click.command(help="Import tool data bundle. URI can be a path to a zipped file or directory.")
@click.option("-c", "--galaxy-config-file", type=click.Path(exists=True, resolve_path=True))
@click.option(
    "-t",
    "--tool-data-file-path",
    type=click.Path(exists=True, resolve_path=True),
    help="loc file to append data to. Must be be loaded in general data tables",
)
@click.argument("uri")
def run_import_data_bundle(uri: str, galaxy_config_file: str, tool_data_file_path: Optional[str] = None):
    with open(galaxy_config_file) as fh:
        galaxy_config = GalaxyAppConfiguration(**yaml.safe_load(fh))
    table_manager = ToolDataTableManager(
        tool_data_path=galaxy_config.tool_data_path,
        config_filename=[galaxy_config.shed_tool_data_table_config, galaxy_config.tool_data_table_config_path]
    )
    options = BundleProcessingOptions(
        what="data import",  # An alternative to this is sticking this in the bundle, only used for logging.
        data_manager_path=galaxy_config.galaxy_data_manager_data_path,
        target_config_file=galaxy_config.data_manager_config_file,
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
