# Copyright 2021 Northern.tech AS
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

import json
import logging
import os
import subprocess

from tempfile import NamedTemporaryFile

# The helpers assume the tools are in the path
_MENDER_ARTIFACT_TOOL_PATH = "mender-artifact"


def make_configuration_artifact(
    configuration, artifact_name, output_file, device_type="qemux86-64"
):
    configuration_file = NamedTemporaryFile(delete=False)
    try:
        configuration_json = json.dumps(configuration).encode("utf-8")
        configuration_file.write(configuration_json)
        configuration_file.close()

        cmd = "%s write module-image -T mender-configure -t %s -n %s -m %s -o %s" % (
            _MENDER_ARTIFACT_TOOL_PATH,
            device_type,
            artifact_name,
            configuration_file.name,
            output_file,
        )
        logging.debug(cmd)
        subprocess.check_call(cmd, shell=True)
    finally:
        os.unlink(configuration_file.name)
