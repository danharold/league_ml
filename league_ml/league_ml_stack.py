from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    aws_lambda as _lambda,
    aws_dynamodb as ddb
)
from constructs import Construct

class LeagueMLStack(Stack):

    @property
    def table_name(self):
        return self._table_name


    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_lambda = _lambda.Function(
            self, 'CollectMatchIds',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='collect_match_ids'
        )

        table = ddb.Table(
            self, 'Data',
            partition_key={'name' : 'key', 'type': ddb.AttributeType.STRING},
            billing_mode = ddb.BillingMode.PAY_PER_REQUEST,
            
        )

        self._table_name = CfnOutput(
            self, 'DataTableName',
            value=table.table_name
        )
        
