from type_sense_configs.typesense_client import client
from typesense.exceptions import ObjectAlreadyExists, ObjectNotFound


def create_collection(data, index):
    try:
        client.collections[index].documents.create(data)
    except ObjectAlreadyExists:
        print("already exists")
        client.collections[index].documents[data['id']].update(data)


def get_collection(index, id):
    try:
        client.collections[index].documents[id].retrieve()
    except ObjectNotFound:
        return None


def update_collection(data, index):
    try:
        client.collections[index].documents[data['id']].update(data)
    except ObjectNotFound:
        client.collections[index].documents.create(data)