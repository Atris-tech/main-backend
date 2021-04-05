from type_sense_configs.typesense_client import client
from typesense.exceptions import ObjectAlreadyExists, ObjectNotFound


def create_collection(data, index):
    try:
        return client.collections[index].documents.create(data)
    except ObjectAlreadyExists:
        print("already exists")
        return client.collections[index].documents[data['id']].update(data)


def get_collection(index, id):
    try:
        return client.collections[index].documents[id].retrieve()
    except ObjectNotFound:
        return None


def update_collection(data, index):
    try:
        return client.collections[index].documents[data['id']].update(data)
    except ObjectNotFound:
        client.collections[index].documents.create(data)


def delete_collection(collections_id, index):
    try:
        return client.collections[index].documents[collections_id].delete()
    except ObjectNotFound:
        print("no such index")
