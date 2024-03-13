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
"""Initialization of the Skypilot RunPod integration for ZenML.

The Skypilot integration sub-module powers an alternative to the local
orchestrator for a remote orchestration of ZenML pipelines on VMs.
"""
from typing import List, Type

from zenml.integrations.constants import (
    SKYPILOT_RUNPOD,
)
from zenml.integrations.integration import Integration
from zenml.stack import Flavor

SKYPILOT_AWS_ORCHESTRATOR_FLAVOR = "vm_aws"


class SkypilotRunPodIntegration(Integration):
    """Definition of Skypilot RunPod Integration for ZenML."""

    NAME = SKYPILOT_RUNPOD
    REQUIREMENTS = ["skypilot[runpod]<=0.4.1", "runpod>=1.5.1"]

    @classmethod
    def flavors(cls) -> List[Type[Flavor]]:
        """Declare the stack component flavors for the Skypilot RunPod integration.

        Returns:
            List of stack component flavors for this integration.
        """
        from zenml.integrations.skypilot_runpod.flavors import (
            SkypilotRunPodOrchestratorFlavor,
        )

        return [SkypilotRunPodOrchestratorFlavor]


SkypilotRunPodIntegration.check_installation()