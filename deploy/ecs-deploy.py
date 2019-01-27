# This file is based on a script originally written by Alex Gaynor: https://github.com/alex/ecs-terraform
#
# Changes were made to add missing parameters to the register_task_definition call.


from contextlib import contextmanager

import boto3

import click


@contextmanager
def log_call(msg):
    click.echo("start {}".format(msg))
    yield
    click.echo("finish {}".format(msg))


def get_current_task_definition(client, cluster, service):
    with log_call("describe services"):
        response = client.describe_services(cluster=cluster, services=[service])
    current_task_arn = response["services"][0]["taskDefinition"]

    with log_call("describe task definition"):
        response = client.describe_task_definition(
            taskDefinition=current_task_arn
        )

    return response


@click.group()
def cli():
    pass


@cli.command()
@click.option("--cluster")
@click.option("--service")
@click.option("--image")
def deploy(cluster, service, image):
    client = boto3.client("ecs")

    response = get_current_task_definition(client, cluster, service)
    # We don't handle tasks with multiple containers for now.
    assert len(response["taskDefinition"]["containerDefinitions"]) == 1
    container_definition = response["taskDefinition"]["containerDefinitions"][0].copy()
    container_definition["image"] = image

    with log_call("register task definition"):
        response = client.register_task_definition(
            containerDefinitions=[container_definition],
            executionRoleArn=response["taskDefinition"]["executionRoleArn"],
            family=response["taskDefinition"]["family"],
            networkMode=response["taskDefinition"]["networkMode"],
            volumes=response["taskDefinition"]["volumes"],
            requiresCompatibilities=response["taskDefinition"]["requiresCompatibilities"],
            cpu=response["taskDefinition"]["cpu"],
            memory=response["taskDefinition"]["memory"],
            # The following are not required for Fargate
            # requiresAttributes
            # placementConstraints
        )
    new_task_arn = response["taskDefinition"]["taskDefinitionArn"]

    with log_call("update task definition"):
        # noinspection PyUnusedLocal
        response = client.update_service(
            cluster=cluster,
            service=service,
            taskDefinition=new_task_arn,
        )


# noinspection PyUnusedLocal
@cli.command()
@click.option("--cluster")
@click.option("--service")
def rollback(cluster, service):
    client = boto3.client("ecs")

    response = get_current_task_definition(client, cluster, service)

    family = response["taskDefinition"]["family"]
    with log_call("list task definitions"):
        response = client.list_task_definitions(
            familyPrefix=family,
        )
    # Deploy the second to last one. Probably could use some better logic?
    new_task_arn = response["taskDefinitionArns"][-2]

    with log_call("update task definition"):
        response = client.update_service(
            cluster=cluster,
            service=service,
            taskDefinition=new_task_arn,
        )


if __name__ == "__main__":
    cli()
