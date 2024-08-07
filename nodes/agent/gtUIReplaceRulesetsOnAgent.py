# from server import PromptServer
from ...py.griptape_config import get_config
from .BaseAgent import BaseAgent
from .gtComfyAgent import gtComfyAgent

default_prompt = "{{ input_string }}"
max_attempts_default = 10


def get_default_config():
    return get_config("agent_config")


class gtUIReplaceRulesetsOnAgent(BaseAgent):
    """
    Replace Rulesets on an Agent
    """

    DESCRIPTION = "Replace or Remove Rulesets on an Agent"

    def __init__(self):
        self.default_prompt = default_prompt
        self.agent = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "agent": (
                    "AGENT",
                    {
                        "forceInput": True,
                    },
                ),
                "rulesets": ("RULESET", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("AGENT",)
    RETURN_NAMES = ("AGENT",)
    FUNCTION = "run"
    OUTPUT_NODE = True

    def run(self, **kwargs):
        agent = kwargs.get("agent", None)
        rulesets = kwargs.get("rulesets", [])

        create_dict = {}

        # Get all agent attributes
        create_dict["config"] = agent.config
        create_dict["conversation_memory"] = agent.conversation_memory
        create_dict["meta_memory"] = agent.meta_memory
        create_dict["task_memory"] = agent.task_memory
        create_dict["tools"] = agent.tools

        # Rulesets
        create_dict["rulesets"] = rulesets

        try:
            # Now create the agent
            self.agent = gtComfyAgent(**create_dict)
            return (self.agent,)
        except Exception as e:
            return (f"Error creating agent: {str(e)}", None)
