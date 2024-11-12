from enum import StrEnum
from typing import Self

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSerializable
from langchain_ollama import ChatOllama
from pydantic import BaseModel, model_validator

from config import base_logger, base_settings


class LLMNames(StrEnum):
    llama = "llama3.1"
    phi = "phi3.5"
    qwen = "qwen2:0.5b"
    gemma = "gemma2:2b"


class localLLM(BaseModel):
    name: LLMNames
    model: ChatOllama | None = None
    prompt: ChatPromptTemplate | None = None
    chain: RunnableSerializable | None = None

    @model_validator(mode="after")
    def set_prompt(self) -> Self:
        self.model = ChatOllama(
            model=self.name,
            temperature=0,
            base_url=base_settings.OLLAMA_BASE_URL,
        )
        return self

    @model_validator(mode="after")
    def set_model(self) -> Self:
        self.prompt = ChatPromptTemplate.from_template(
            """En utilisant les documents entre les balises <doc> et </doc> répond à la question de l'utilisateur : {query}
            <doc> {docs} </doc>
            """
        )
        return self

    @model_validator(mode="after")
    def set_chain(self) -> Self:
        if self.prompt is not None and self.model is not None:
            parser = StrOutputParser()
            self.chain = self.prompt | self.model | parser
        return self

    def call(self, query: str, docs) -> str:
        if self.chain is not None:
            result = self.chain.invoke(
                {
                    "query": query,
                    "docs": "\n".join(docs),
                }
            )
            base_logger.debug(result)
            return result
        else:
            raise UnboundLocalError("Chain was not correctly instantiated")


LLAMA = localLLM(name=LLMNames.llama)
PHI = localLLM(name=LLMNames.phi)
QWEN = localLLM(name=LLMNames.qwen)
GEMMA = localLLM(name=LLMNames.gemma)

if __name__ == "__main__":
    GEMMA.call(query="Hi", docs=["Un premier doc", "Un deuxieme doc"])
