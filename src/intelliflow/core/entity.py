# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from intelliflow.core.serialization import Serializable


class CoreData(Serializable):
    """Provide basic dunder implementations for serializable core 'data' entities

    Use this for backwards compatibility on Plain Old Data Object cases where NamedTuple is causing
    runtime issues particularly on environments with Livy, PySpark running Python 3.6
    """

    def __eq__(self, other) -> bool:
        return type(other) is type(self) and self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.__dict__.items())))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({','.join([f'{name}={repr(value)}' for name, value in self.__dict__.items()])})"

    def __str__(self) -> str:
        return self.__repr__()
