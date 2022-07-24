from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as ddb
)
from constructs import Construct

class LeagueMLStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_lambda = _lambda.Function(
            self, 'UpdatePuuids',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='update_puuids'
        )

        table = ddb.Table(
            self, 'Data',
            partition_key={'name' : 'key', 'type': ddb.AttributeType.STRING}
        )
