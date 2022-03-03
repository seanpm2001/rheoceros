# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json
import logging

from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


def create_table(ddb_resource, table_name, key_schema, attribute_def, provisioned_throughput):
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_table
    :param ddb_resource:
    :param table_name:
    :param key_schema:
    :param attribute_def:
    :param provisioned_throughput:
    :return:
    """
    try:
        table = ddb_resource.create_table(
            TableName=table_name, KeySchema=key_schema, AttributeDefinitions=attribute_def, ProvisionedThroughput=provisioned_throughput
        )
        table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
        logger.info("Successfully created the table: %s", table_name)
        return table
    except ClientError:
        raise


def delete_table(table):
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.delete
    :param table:
    :return:
    """
    try:
        response = table.delete()
        table.meta.client.get_waiter("table_not_exists").wait(TableName=table.table_name)
        logger.info("Table %s has been successfully deleted", table.table_name)
        return response
    except ClientError:
        raise


def get_ddb_item(table, key):
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.get_item
    :param table:
    :param key:
    :return:
    """
    try:
        response = table.get_item(Key=key)
        logger.info("Got successful response for Key: %s from Table %s", json.dumps(key), table.table_name)
        return response
    except ClientError:
        logger.exception("Got exception during get_item operation on key: %s and table: %s", json.dumps(key), table.table_name)
        raise


def put_ddb_item(table, item):
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.put_item
    :param table:
    :param item:
    :return:
    """
    try:
        response = table.put_item(Item=item)
        return response
    except ClientError:
        logger.exception("Got exception during put_item operation on item: %s for table: %s", json.dumps(item), table.table_name)
        raise


def delete_ddb_item(table, key):
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.delete_item
    :param table:
    :param key:
    :return:
    """
    try:
        response = table.delete_item(Key=key)
        logger.info("Successfully deleted item with key: %s from table %s", json.dumps(key), table.table_name)
        return response
    except ClientError:
        logger.exception("Got exception during delete_item operation on table: %s on" "key: %s", table.table_name, json.dumps(key))
        raise


def query_ddb_table(table, key_cond_expr, scan_index_forward, **query_kwargs):
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.query
    :param table:
    :param key_cond_expr:
    :param scan_index_forward:
    :param query_kwargs:
    :return:
    """
    try:
        response = table.query(KeyConditionExpression=key_cond_expr, ScanIndexForward=scan_index_forward, **query_kwargs)
        return response
    except ClientError:
        logger.exception(
            "Got exception during ddb table query operation. TableName: %s," "KeyConditionExpression: %s, Query Kwargs: %s",
            table.table_name,
            str(key_cond_expr),
            json.dumps(query_kwargs),
        )
        raise


def scan_ddb_table(table, **scan_kwargs):
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.scan
    :param table:
    :param scan_kwargs:
    :return:
    """
    try:
        response = table.scan(**scan_kwargs)
        return response
    except ClientError:
        logger.exception(
            "Exception occurred during scan operation for table: %s, with " "scan args: %s", table.table_name, json.dumps(scan_kwargs)
        )
        raise


def put_item_batch(batch_writer, item):
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.batch_writer
    :param batch_writer:
    :param item:
    :return:
    """
    try:
        batch_writer.put_item(Item=item)
    except ClientError:
        logger.exception("Exception occurred during put item using batch writer for table")
