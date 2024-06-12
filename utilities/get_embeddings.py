import os
import logging
from flask import flash
from openai import OpenAI

def get_embeddings(labels, model="text-embedding-3-small", dimensions=50):
    """embeddings of a str or list of words in str format,
    return embeddings as a list of tuples [(word, embedding)]"""
    word_embedding_pairs = []
    try:
      client = OpenAI(api_key=os.environ.get('GPT_SECRET_KEY'))
      response = client.embeddings.create(
        model=model,
        input=labels,
        encoding_format="float",
        dimensions=dimensions
      )
    except Exception as e:
      logging.exception(e)
      raise ConnectionError("Error in getting embeddings")
      #flag for retry
    
    if isinstance(labels, list):
      for embedding_object in response.data:
        word_embedding_pairs.append((labels[embedding_object.index], embedding_object.embedding))
      return word_embedding_pairs
    else:
      return [(labels, response.data[0].embedding)]