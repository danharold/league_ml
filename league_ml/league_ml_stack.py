from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    aws_lambda as _lambda,
    aws_dynamodb as ddb
)
from constructs import Construct

class LeagueMLStack(Stack):

    # @property
    # def puuids_table_name(self):
    #     return self._puuids_table_name
    
    # @property
    # def match_table_name(self):
    #     return self._puuids_table_name


    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_lambda = _lambda.Function(
            self, 'UpdatePuuids',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='update_puuids'
        )

        puuids_table = ddb.Table(
            self, 'Puuids',
            partition_key={'name' : 'puuid', 'type': ddb.AttributeType.STRING},
            billing_mode = ddb.BillingMode.PAY_PER_REQUEST,
            
        )

        match_table = ddb.Table(
            self, 'MatchData',
            partition_key = {'name': 'match_id', 'type': ddb.AttributeType.STRING},
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST
        )

        # self._puuids_table_name = CfnOutput(
        #     self, 'PuuidsTableName',
        #     value=puuids_table.table_name
        # )

        # self._match_table_name = CfnOutput(
        #     self, 'PuuidsTableName',
        #     value=match_table.table_name
        # )
        
