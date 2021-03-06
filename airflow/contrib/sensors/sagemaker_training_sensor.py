# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from airflow.contrib.hooks.sagemaker_hook import SageMakerHook
from airflow.contrib.sensors.sagemaker_base_sensor import SageMakerBaseSensor
from airflow.utils.decorators import apply_defaults


class SageMakerTrainingSensor(SageMakerBaseSensor):
    """
    Asks for the state of the training state until it reaches a terminal state.
    If it fails the sensor errors, failing the task.

    :param job_name: job_name of the training instance to check the state of
    :type job_name: str
    """

    template_fields = ['job_name']
    template_ext = ()

    @apply_defaults
    def __init__(self,
                 job_name,
                 region_name=None,
                 *args,
                 **kwargs):
        super(SageMakerTrainingSensor, self).__init__(*args, **kwargs)
        self.job_name = job_name
        self.region_name = region_name

    def non_terminal_states(self):
        return SageMakerHook.non_terminal_states

    def failed_states(self):
        return SageMakerHook.failed_states

    def get_sagemaker_response(self):
        sagemaker = SageMakerHook(
            aws_conn_id=self.aws_conn_id,
            region_name=self.region_name
        )

        self.log.info('Poking Sagemaker Training Job %s', self.job_name)
        return sagemaker.describe_training_job(self.job_name)

    def get_failed_reason_from_response(self, response):
        return response['FailureReason']

    def state_from_response(self, response):
        return response['TrainingJobStatus']
