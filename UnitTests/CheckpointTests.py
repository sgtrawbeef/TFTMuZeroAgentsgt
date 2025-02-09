import ray
import numpy as np
from storage import Storage
import config


def setup(episode):
    storage = Storage.remote(episode)
    return storage

def store_checkpoint_test(storage):
    storage.store_checkpoint.remote(0)
    checkpoint_list = ray.get(storage.get_checkpoint_list.remote())
    assert checkpoint_list[-1].epoch == 0
    storage.store_checkpoint.remote(100)
    checkpoint_list = ray.get(storage.get_checkpoint_list.remote())
    assert checkpoint_list[-1].epoch == 100
    storage.store_checkpoint.remote(1000000)
    checkpoint_list = ray.get(storage.get_checkpoint_list.remote())
    assert checkpoint_list[-1].epoch == 1000000
    return

def update_checkpoint_score_test(storage):
    # First test is for a random checkpoint,
    storage.store_checkpoint.remote(123456)
    storage.update_checkpoint_score.remote(123456, 1)
    checkpoint_list = ray.get(storage.get_checkpoint_list.remote())
    assert checkpoint_list[-1].q_score < 1
    return

def sample_past_model_test():
    return

def get_model_test():
    return

def update_q_score_test():
    return

# So let me make a list of the methods that I need to test
# Storage - store_checkpoint, update_checkpoint, update_checkpoint_score, sample_past_model, get_model
# Checkpoint - get_model, update_q_score
def list_of_tests():
    storage = setup(0)
    store_checkpoint_test(storage)
    update_checkpoint_score_test(storage)
    sample_past_model_test()
    get_model_test()
    update_q_score_test()
