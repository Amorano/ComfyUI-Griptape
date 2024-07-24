import os
from dotenv import load_dotenv

# StructureGlobalDriversConfig,
from griptape.drivers import (
    AmazonBedrockPromptDriver,
    AzureOpenAiChatPromptDriver,
    AzureOpenAiEmbeddingDriver,
    AzureOpenAiImageGenerationDriver,
)

from griptape.config import (
    AmazonBedrockStructureConfig,
    AzureOpenAiStructureConfig,
)

from .gtUIBaseConfig import gtUIBaseConfig

load_dotenv()

SERVICE = {
    'amazon bedrock': {
        'model': [
            "anthropic.claude-3-5-sonnet-20240620-v1:0",
            "anthropic.claude-3-opus-20240229-v1:0",
            "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-3-haiku-20240307-v1:0",
            "amazon.titan-text-premier-v1:0",
            "amazon.titan-text-express-v1",
            "amazon.titan-text-lite-v1",
        ],
    },
    'azure openai': {
        'model': ["gpt-4o", "gpt-4", "gpt-3.5-turbo-16k", "gpt-3.5-turbo"]
    }
}
SERVICE_LIST = list(SERVICE.keys())

DEFAULT_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
DEFAULT_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
DEFAULT_AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"

DEFAULT_AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEFAULT_AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

class gtUIGenericConfig(gtUIBaseConfig):
    """
    The Griptape Generic Structure Config for all services.
    """

    DESCRIPTION = "Omni Prompt Driver."

    @classmethod
    def INPUT_TYPES(s):
        old_inputs = super().INPUT_TYPES()
        inputs = {
            "required": {
                "service_model": (
                    SERVICE_LIST,
                    {"default": SERVICE_LIST[0]},
                ),
                "prompt_model": (
                    SERVICE[SERVICE_LIST[0]]['model'],
                    {"default": SERVICE[SERVICE_LIST[0]]['model'][0]},
                ),
                "prompt_model_deployment_name": (
                    "STRING",
                    {"default": "gpt4o"},
                ),
            },
            "optional": {
                # PUT API KEYS AT THE BOTTOM SO THE SWITCHES ARE CLEANER
                "api_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_AZURE_OPENAI_API_KEY},
                ),
                "azure_endpoint_env_var": (
                    "STRING",
                    {"default": DEFAULT_AZURE_OPENAI_ENDPOINT},
                ),

                # AMAZON KEYS
                "aws_access_key_id_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_ACCESS_KEY_ID},
                ),
                "aws_secret_access_key_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_SECRET_ACCESS_KEY},
                ),
                "aws_default_region_env_var": (
                    "STRING",
                    {"default": DEFAULT_AWS_DEFAULT_REGION},
                ),
            }
        }
        inputs["required"].update(old_inputs.get("required", {}))
        optional = old_inputs.get("optional", {})
        optional.update(inputs["optional"])
        inputs["optional"] = optional
        return inputs

def create_AmazonBedrockStructureConfig(**kwargs):
    service = kwargs.get("service", SERVICE_LIST[0])
    model = SERVICE[service]['model'][0]
    prompt_model = kwargs.get("prompt_model", model)
    temperature = kwargs.get("temperature", 0.7)
    max_attempts = kwargs.get("max_attempts_on_fail", 10)

    custom_config = AmazonBedrockStructureConfig(
        prompt_driver=AmazonBedrockPromptDriver(
            model=prompt_model, temperature=temperature, max_attempts=max_attempts
        )
    )
    return (custom_config,)

def create_AzureOpenAIStructureConfig(**kwargs):
    service = kwargs.get("service", SERVICE_LIST[0])
    model = SERVICE[service]['model'][0]
    prompt_model = kwargs.get("prompt_model", model)

    temperature = kwargs.get("temperature", 0.7)
    seed = kwargs.get("seed", 12341)
    max_attempts = kwargs.get("max_attempts_on_fail", 10)

    image_generation_driver = kwargs.get("image_generation_driver", None)
    prompt_model_deployment_id = kwargs.get("prompt_model_deployment_name", "gpt4o")
    stream = kwargs.get("stream", False)

    AZURE_OPENAI_API_KEY = os.getenv(
        kwargs.get("api_key_env_var", DEFAULT_AZURE_OPENAI_API_KEY)
    )
    AZURE_OPENAI_ENDPOINT = os.getenv(
        kwargs.get("azure_endpoint_env_var", DEFAULT_AZURE_OPENAI_ENDPOINT)
    )

    prompt_driver = AzureOpenAiChatPromptDriver(
        api_key=AZURE_OPENAI_API_KEY,
        model=prompt_model,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_deployment=prompt_model_deployment_id,
        temperature=temperature,
        seed=seed,
        max_attempts=max_attempts,
        stream=stream,
    )

    embedding_driver = AzureOpenAiEmbeddingDriver(
        api_key=AZURE_OPENAI_API_KEY, azure_endpoint=AZURE_OPENAI_ENDPOINT
    )

    if not image_generation_driver:
        image_generation_driver = AzureOpenAiImageGenerationDriver(
            azure_deployment="dall-e-3",
            model="dall-e-3",
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
        )

    custom_config = AzureOpenAiStructureConfig(
        prompt_driver=prompt_driver,
        embedding_driver=embedding_driver,
        image_generation_driver=image_generation_driver,
    )

    return (custom_config,)