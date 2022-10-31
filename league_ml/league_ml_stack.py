from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    aws_apigateway as apigw,
)
from constructs import Construct

class LeagueMLStack(Stack):

    @property
    def puuid_table_name(self):
        return self._puuid_table_name
    
    @property
    def match_table_name(self):
        return self._match_table_name
    
    # @property
    # def meow_table_name(self):
    #     return self._meow_table_name


    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        puuid_table = ddb.Table(
            self, 'Puuids',
            partition_key={'name' : 'puuid', 'type': ddb.AttributeType.STRING},
            billing_mode = ddb.BillingMode.PAY_PER_REQUEST,
        )

        match_table = ddb.Table(
            self, 'MatchData',
            partition_key={'name' : 'match_id', 'type': ddb.AttributeType.STRING},
            billing_mode = ddb.BillingMode.PAY_PER_REQUEST,
        )

        collect_match_ids_lambda = _lambda.Function(
            self, 'CollectMatchIds',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='collect_match_ids.handler',
            environment={
                'MATCH_TABLE_NAME': match_table.table_name,
                'PUUID_TABLE_NAME': puuid_table.table_name,
            }
        )
        puuid_table.grant_full_access(collect_match_ids_lambda)
        match_table.grant_full_access(collect_match_ids_lambda)

        #test
        meow_table = ddb.Table(
            self, 'MeowData',
            partition_key={'name' : 'meows', 'type': ddb.AttributeType.STRING},
            billing_mode = ddb.BillingMode.PROVISIONED,
        )

        meow_lambda = _lambda.Function(
            self, 'MeowTest',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='meow_test.handler',
            environment={
                'MEOW_TABLE_NAME': meow_table.table_name
            }
        )

        meow_table.grant_full_access(meow_lambda)

        # self._meow_table_name = CfnOutput(
        #     self, 'MeowTableName',
        #     value=meow_table.table_name
        # )

        self._puuid_table_name = CfnOutput(
            self, 'PuuidTableName',
            value=puuid_table.table_name
        )

        self._match_table_name = CfnOutput(
            self, 'MatchTableName',
            value=match_table.table_name
        )



        
