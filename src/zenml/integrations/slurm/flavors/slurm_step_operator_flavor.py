from typing import TYPE_CHECKING, Optional, Type

from zenml.config.base_settings import BaseSettings
from zenml.integrations.slurm import SLURM_STEP_OPERATOR_FLAVOR
from zenml.step_operators import BaseStepOperatorConfig, BaseStepOperatorFlavor

if TYPE_CHECKING:
    from zenml.integrations.slurm.step_operators import SlurmStepOperator


class SlurmStepOperatorSettings(BaseSettings):
    """Per-step/per-pipeline runtime overrides for Slurm jobs.

    These can be set per step:
        @step(settings={"step_operator": SlurmStepOperatorSettings(
            partition="gpu", time="08:00:00", gpus="gpu:a100:2"
        )})
    """

    # Slurm partition
    partition: Optional[str] = None

    # Time limit (HH:MM:SS)
    time: Optional[str] = None

    # Memory (e.g., "16G")
    memory: Optional[str] = None

    # CPUs per task
    cpus: Optional[int] = None

    # GRES string for GPUs (e.g., "gpu:1", "gpu:a100:2")
    gpus: Optional[str] = None

    # Slurm QOS
    qos: Optional[str] = None

    # Additional sbatch flags as key-value pairs
    extra_sbatch_options: dict[str, str] = {}


class SlurmStepOperatorConfig(BaseStepOperatorConfig):
    """Infrastructure-level config set once at registration time.

    These are defaults/constants for the Slurm cluster itself.
    """

    # Cluster-level defaults (overridable by settings)
    partition: str = "default"
    time: str = "01:00:00"
    default_memory: str = "4G"
    default_cpus: int = 1
    default_gpus: Optional[str] = None

    # Cluster-level constants (NOT overridable per step)
    account: Optional[str] = None
    job_scripts_dir: str = "/tmp/zenml_slurm_jobs"
    source_code_path: Optional[str] = None

    # SSH access to login node (infrastructure concern)
    ssh_host: Optional[str] = None
    ssh_username: Optional[str] = None
    ssh_key_path: Optional[str] = None


class SlurmStepOperatorFlavor(BaseStepOperatorFlavor):
    """Slurm step operator flavor."""

    @property
    def name(self) -> str:
        """Name of the flavor.

        Returns:
            The name of the flavor.
        """
        return SLURM_STEP_OPERATOR_FLAVOR

    @property
    def config_class(self) -> Type[SlurmStepOperatorConfig]:
        """Returns `SlurmStepOperatorConfig` config class.

        Returns:
            The config class.
        """
        return SlurmStepOperatorConfig

    @property
    def implementation_class(self) -> Type["SlurmStepOperator"]:
        """Implementation class for this flavor.

        Returns:
            The implementation class.
        """
        from zenml.integrations.slurm.step_operators import SlurmStepOperator

        return SlurmStepOperator
