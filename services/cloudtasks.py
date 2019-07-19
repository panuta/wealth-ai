from google.cloud import tasks_v2
from settings import QUEUE_PROJECT_NAME, QUEUE_NAME, QUEUE_REGION


def trigger_app_engine_task(relative_uri, http_method='POST'):
    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(QUEUE_PROJECT_NAME, QUEUE_REGION, QUEUE_NAME)

    task = {
        'app_engine_http_request': {
            'http_method': http_method,
            'relative_uri': relative_uri
        }
    }

    return client.create_task(parent, task)
