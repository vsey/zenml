#  Copyright (c) ZenML GmbH 2024. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""Slurm step operator implementation."""

from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Type, cast

from zenml.client import Client
from zenml.config.build_configuration import BuildConfiguration
from zenml.config.resource_settings import ByteUnit, ResourceSettings
from zenml.enums import ExecutionStatus, StackComponentType
from zenml.integrations.slurm.flavors import (
    SlurmStepOperatorConfig,
    SlurmStepOperatorSettings,
)
from zenml.logger import get_logger
from zenml.orchestrators.publish_utils import publish_step_run_metadata
from zenml.stack import Stack, StackValidator
from zenml.step_operators import BaseStepOperator

if TYPE_CHECKING:
    from zenml.config.base_settings import BaseSettings
    from zenml.config.step_run_info import StepRunInfo
    from zenml.models import PipelineSnapshotBase, StepRunResponse

logger = get_logger(__name__)


class ModalStepOperator(BaseStepOperator):
    """Step operator to run a step with Slurm.

    This class defines code that creates a slurm script and submits it
    """

    @property
    def config(self) -> SlurmStepOperatorConfig:
        """Get the Slurm step operator configuration.

        Returns:
            The Slurm step operator configuration.
        """
        return cast(SlurmStepOperatorConfig, self._config)

    @property
    def settings_class(self) -> Optional[Type["BaseSettings"]]:
        """Get the settings class for the Slurm step operator.

        Returns:
            The Slurm step operator settings class.
        """
        return SlurmStepOperatorSettings

    def submit(
        self,
        info: "StepRunInfo",
        entrypoint_command: List[str],
        environment: Dict[str, str],
    ) -> None:
        """Submits a step run to Modal.

        Args:
            info: The step run information.
            entrypoint_command: The entrypoint command for the step.
            environment: The environment variables for the step.

        Raises:
            RuntimeError: If no Docker credentials are found for the container registry.
            ValueError: If no container registry is found in the stack.
        """
        settings = cast(SlurmStepOperatorSettings, self.get_settings(info))

    def get_status(self, step_run: "StepRunResponse") -> ExecutionStatus:
        """Gets the status of a submitted Modal sandbox.

        Args:
            step_run: The step run.

        Returns:
            The step status.
        """
        sandbox_id = str(step_run.run_metadata[STEP_SANDBOX_ID_METADATA_KEY])
        sandbox = modal.Sandbox.from_id(sandbox_id)
        return_code = sandbox.poll()
        if return_code is None:
            return ExecutionStatus.RUNNING
        if return_code == 0:
            return ExecutionStatus.COMPLETED
        return ExecutionStatus.FAILED

    def cancel(self, step_run: "StepRunResponse") -> None:
        """Cancels a submitted Modal sandbox.

        Args:
            step_run: The step run.
        """
        sandbox_id = str(step_run.run_metadata[STEP_SANDBOX_ID_METADATA_KEY])
        sandbox = modal.Sandbox.from_id(sandbox_id)
        sandbox.terminate()
