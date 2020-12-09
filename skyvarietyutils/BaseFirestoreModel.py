from firebase_admin import credentials, firestore, initialize_app
import os, datetime

# https://firebase.google.com/docs/firestore/query-data/get-data
# https://cloud.google.com/community/tutorials/building-flask-api-with-cloud-firestore-and-deploying-to-cloud-run
class BaseFirestoreModel():
  if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ :
    cred = credentials.Certificate(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    default_app = initialize_app(cred)
    db = firestore.client()

  @staticmethod
  def from_doc(doc):
    # turn your document back into a object
    pass

  @classmethod
  def appendCreatedDate(cls, data):
    data['created'] = datetime.datetime.now()
    return data

  @classmethod
  def appendUpdatedDate(cls, data):
    data['updated'] = datetime.datetime.now()
    return data

  @classmethod
  def getCollection(self):
    return self.db.collection(self.kind)

  @classmethod
  def set(self, data, id=None):
    data = self.appendCreatedDate(data)
    data = self.appendUpdatedDate(data)

    if id:
      self.getCollection().document(id).set(data)
    else :
      self.getCollection().document().set(data)

  @classmethod
  def update(self, id, data):
    data = self.appendUpdatedDate(data)

    doc_ref = self.getCollection().document(id)
    doc_ref.update(data)

  @classmethod
  def get(self, id):
    doc_ref = self.getCollection().document(id)

    doc = doc_ref.get()
    if doc.exists:
      return self.from_doc(doc)
    else:
      return None

  @classmethod
  def get_by_condition(self, conditions):
    collection = self.getCollection()
    for condition in conditions:
      collection = collection.where(condition)

    elements = self.fetch(
      collection=collection,
      limit=1
    )
    if elements:
      element = elements[0]
      return element
    else:
      return None

  @classmethod
  def fetch(self, limit=None, startAfter=None, endBefore=None, collection=None, orderBy=None, direction=firestore.Query.DESCENDING, returnType="object"):
    if collection == None:
      collection = self.getCollection()

    q = collection

    if orderBy:
      q = q.order_by(orderBy, direction=direction)
    if startAfter:
      q = q.start_after({orderBy: startAfter})
    if endBefore:
      q = q.end_before({orderBy: endBefore})

    if limit:
      q = q.limit(limit)

    docs = q.stream()
    if returnType == 'stream':
      return docs

    results = None
    if returnType == 'dictOfObject' or returnType == 'dictOfModel':
      results = {}
      for doc in docs:
        if returnType == 'dictOfObject':
          resultDict = doc.to_dict()
          resultDict['id'] = doc.id
          results[doc.id] = resultDict
        elif returnType == 'dictOfModel':
          results[doc.id] = self.from_doc(doc)
    else :
      results = []
      for doc in docs:
         if returnType == 'dict':
           resultDict = doc.to_dict()
           resultDict['id'] = doc.id
           results.append(resultDict)
         else:
           results.append(self.from_doc(doc))
      #  results[doc.id] = doc.to_dict()

    return results

  @classmethod
  def delete(self, id):
    return self.getCollection().document(id).delete()
