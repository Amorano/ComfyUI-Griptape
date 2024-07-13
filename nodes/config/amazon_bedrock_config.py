from griptape.config import (
    AmazonBedrockStructureConfig,
)

# StructureGlobalDriversConfig,
from griptape.drivers import (
    AmazonBedrockImageQueryDriver,
    AmazonBedrockPromptDriver,
    BedrockClaudeImageQueryModelDriver,
)

from .base_config import gtUIBaseConfig

amazonBedrockPromptModels = [
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "anthropic.claude-3-opus-20240229-v1:0",
    "anthropic.claude-3-sonnet-20240229-v1:0",
    "anthropic.claude-3-haiku-20240307-v1:0",
    "amazon.titan-text-premier-v1:0",
    "amazon.titan-text-express-v1",
    "amazon.titan-text-lite-v1",
]
amazonBedrockImageQueryModels = [
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "anthropic.claude-3-opus-20240229-v1:0",
    "anthropic.claude-3-sonnet-20240229-v1:0",
    "anthropic.claude-3-haiku-20240307-v1:0",
]


class gtUIAmazonBedrockStructureConfig(gtUIBaseConfig):
    """
    The Griptape Amazon Bedrock Structure Config
    """

    DESCRIPTION = "Amazon Bedrock Prompt Driver."

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "prompt_model": (
                    amazonBedrockPromptModels,
                    {"default": amazonBedrockPromptModels[0]},
                ),
                "image_query_model": (
                    amazonBedrockImageQueryModels,
                    {"default": amazonBedrockImageQueryModels[0]},
                ),
            },
        )
        return inputs

    def create(
        self,
        prompt_model,
        image_query_model,
        temperature,
        seed,
        image_generation_driver=None,
    ):
        custom_config = AmazonBedrockStructureConfig()
        custom_config.prompt_driver = AmazonBedrockPromptDriver(
            model=prompt_model, temperature=temperature
        )
        custom_config.image_query_driver = AmazonBedrockImageQueryDriver(
            image_query_model_driver=BedrockClaudeImageQueryModelDriver(),
            model=image_query_model,
        )
        if image_generation_driver:
            custom_config.image_generation_driver = image_generation_driver
        return (custom_config,)