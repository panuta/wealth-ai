from google.cloud import firestore


MAXIMUM_BATCH_SIZE = 400


def save(collection_name, data, id_function=None):
    db = firestore.Client()
    batch = db.batch()
    batch_count = 0
    for datum in data:
        batch.set(db.collection(collection_name).document(
            id_function(datum) if id_function is not None else datum['id']), datum)
        batch_count += 1

        if batch_count == MAXIMUM_BATCH_SIZE:
            batch.commit()
            batch = db.batch()
            batch_count = 0

    if batch_count > 0:
        batch.commit()
