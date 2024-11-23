from abc import ABC, abstractmethod

class LlmDriver(ABC):
    """Abstract class for talking with an LLM.
    
    This is the lowest level driver, designed to be easy to implement
    if you want to interface to a new LLM.
    Although there are two methods here, to implement your own driver
    you only need to override chat_dialog().  The chat() method has
    default behavior defined here in terms of the required chat_dialog().
    """
    class InvalidRequestError(Exception):
        pass
    class RateLimitError(Exception):
        pass

    async def chat(self, prompt: str) -> str:
        """Given an input prompt, respond.
        
        You can use this method when you don't need to continue a previous conversation
        and don't need fine-grained control over system role vs assistant role in the conversation.
        :param prompt: Text to start the conversation.
        :returns: The LLM's response that continues the conversation.
        """