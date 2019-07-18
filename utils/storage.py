from google.cloud import firestore


def persist(collection_name, data, key_for_id='id'):
    db = firestore.Client()
    batch = db.batch()
    for datum in data:
        batch.set(db.collection(collection_name).document(datum.pop(key_for_id)), datum)
    batch.commit()
