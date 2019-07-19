from google.cloud import firestore


MAXIMUM_BATCH_SIZE = 400


def persist(collection_name, data, key_for_id='id'):
    db = firestore.Client()
    batch = db.batch()
    batch_count = 0
    for datum in data:
        batch.set(db.collection(collection_name).document(datum.pop(key_for_id)), datum)
        batch_count += 1

        if batch_count == MAXIMUM_BATCH_SIZE:
            batch.commit()
            batch = db.batch()
            batch_count = 0

    if batch_count > 0:
        batch.commit()
