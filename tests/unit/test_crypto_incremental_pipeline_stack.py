import aws_cdk as core
import aws_cdk.assertions as assertions

from crypto_incremental_pipeline.crypto_incremental_pipeline_stack import CryptoIncrementalPipelineStack

# example tests. To run these tests, uncomment this file along with the example
# resource in crypto_incremental_pipeline/crypto_incremental_pipeline_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CryptoIncrementalPipelineStack(app, "crypto-incremental-pipeline")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
