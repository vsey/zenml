from typing import List, Type

from zenml.integrations.constants import SLURM
from zenml.integrations.integration import Integration
from zenml.stack import Flavor

SLURM_STEP_OPERATOR_FLAVOR = "slurm"


class SlurmIntegration(Integration):
    """Definition of slurm integration for ZenML."""

    NAME = SLURM

    @classmethod
    def flavors(cls) -> List[Type[Flavor]]:
        """Declare the stack component flavors for the slurm integration.

        Returns:
            List of new stack component flavors.
        """
        from zenml.integrations.slurm.flavors import SlurmStepOperatorFlavor

        return [SlurmStepOperatorFlavor]