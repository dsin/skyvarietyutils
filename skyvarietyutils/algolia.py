from algoliasearch.search_client import SearchClient

class Algolia:
  def __init__(self, application_id, api_key, index_name):
    client = SearchClient.create(application_id, api_key)
    self.index = client.init_index(index_name)

  # https://www.algolia.com/doc/api-reference/api-methods/partial-update-objects/
  def partial_update_objects(self, *args, **kwargs):
    res = self.index.partial_update_objects(*args, **kwargs)

  # https://www.algolia.com/doc/api-reference/api-methods/search/
  def search(self, *args, **kwargs):
    return self.index.search(*args, **kwargs)
