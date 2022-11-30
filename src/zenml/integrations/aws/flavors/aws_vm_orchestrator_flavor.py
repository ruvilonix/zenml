#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
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
"""VM orchestrator flavor."""

from typing import TYPE_CHECKING, Dict, Optional, Tuple, Type

from zenml.integrations.aws import AWS_VM_ORCHESTRATOR_FLAVOR
from zenml.orchestrators import BaseOrchestratorConfig, BaseOrchestratorFlavor

if TYPE_CHECKING:
    from zenml.integrations.aws.orchestrators import AWSVMOrchestrator


class AWSVMOrchestratorConfig(
    BaseOrchestratorConfig,
):
    """Configuration for the VM orchestrator.

    Attributes:
        project: AWS project name. If `None`, the project will be inferred from
            the environment.
        location: Name of AWS region where the pipeline job will be executed.
            VM AI Pipelines is available in the following regions:
            https://cloud.google.com/vertex-ai/docs/general/locations#feature
            -availability
        labels: Labels to assign to the pipeline job.
        pipeline_root: a Cloud Storage URI that will be used by the VM AI
            Pipelines. If not provided but the artifact store in the stack used
            to execute the pipeline is a
            `zenml.integrations.aws.artifact_stores.AWSArtifactStore`,
            then a subdirectory of the artifact store will be used.
        encryption_spec_key_name: The Cloud KMS resource identifier of the
            customer managed encryption key used to protect the job. Has the form:
            `projects/<PRJCT>/locations/<REGION>/keyRings/<KR>/cryptoKeys/<KEY>`
            . The key needs to be in the same region as where the compute
            resource is created.
        workload_service_account: the service account for workload run-as
            account. Users submitting jobs must have act-as permission on this
            run-as account.
            If not provided, the default service account will be used.
        network: the full name of the Compute Engine Network to which the job
            should be peered. For example, `projects/12345/global/networks/myVPC`
            If not provided, the job will not be peered with any network.
        synchronous: If `True`, running a pipeline using this orchestrator will
            block until all steps finished running on VM AI Pipelines
            service.
        cpu_limit: The maximum CPU limit for this operator. This string value
            can be a number (integer value for number of CPUs) as string,
            or a number followed by "m", which means 1/1000. You can specify
            at most 96 CPUs.
            (see. https://cloud.google.com/vertex-ai/docs/pipelines/machine-types)
        memory_limit: The maximum memory limit for this operator. This string
            value can be a number, or a number followed by "K" (kilobyte),
            "M" (megabyte), or "G" (gigabyte). At most 624GB is supported.
        node_selector_constraint: Each constraint is a key-value pair label.
            For the container to be eligible to run on a node, the node must have
            each of the constraints appeared as labels.
            For example a GPU type can be providing by one of the following tuples:
                - ("cloud.google.com/gke-accelerator", "NVIDIA_TESLA_A100")
                - ("cloud.google.com/gke-accelerator", "NVIDIA_TESLA_K80")
                - ("cloud.google.com/gke-accelerator", "NVIDIA_TESLA_P4")
                - ("cloud.google.com/gke-accelerator", "NVIDIA_TESLA_P100")
                - ("cloud.google.com/gke-accelerator", "NVIDIA_TESLA_T4")
                - ("cloud.google.com/gke-accelerator", "NVIDIA_TESLA_V100")
            Hint: the selected region (location) must provide the requested accelerator
            (see https://cloud.google.com/compute/docs/gpus/gpu-regions-zones).
        gpu_limit: The GPU limit (positive number) for the operator.
            For more information about GPU resources, see:
            https://cloud.google.com/vertex-ai/docs/training/configure-compute#specifying_gpus
    """

    project: Optional[str] = None
    location: str
    pipeline_root: Optional[str] = None
    labels: Dict[str, str] = {}
    encryption_spec_key_name: Optional[str] = None
    workload_service_account: Optional[str] = None
    network: Optional[str] = None
    synchronous: bool = False

    cpu_limit: Optional[str] = None
    memory_limit: Optional[str] = None
    node_selector_constraint: Optional[Tuple[str, str]] = None
    gpu_limit: Optional[int] = None

    @property
    def is_remote(self) -> bool:
        """Checks if this stack component is running remotely.

        This designation is used to determine if the stack component can be
        used with a local ZenML database or if it requires a remote ZenML
        server.

        Returns:
            True if this config is for a remote component, False otherwise.
        """
        return True


class AwsVMOrchestratorFlavor(BaseOrchestratorFlavor):
    """VM Orchestrator flavor."""

    @property
    def name(self) -> str:
        """Name of the orchestrator flavor.

        Returns:
            Name of the orchestrator flavor.
        """
        return AWS_VM_ORCHESTRATOR_FLAVOR

    @property
    def config_class(self) -> Type[AWSVMOrchestratorConfig]:
        """Returns AWSVMOrchestratorConfig config class.

        Returns:
                The config class.
        """
        return AWSVMOrchestratorConfig

    @property
    def implementation_class(self) -> Type["AWSVMOrchestrator"]:
        """Implementation class for this flavor.

        Returns:
            Implementation class for this flavor.
        """
        from zenml.integrations.aws.orchestrators import VMOrchestrator

        return VMOrchestrator