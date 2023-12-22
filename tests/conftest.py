import os
import shutil

import dramatiq
import pytest
from dramatiq.brokers.stub import StubBroker


@pytest.fixture(autouse=True, scope="session")
def remove_messes_from_folder():
    yield
    print("clearing up after test")
    shutil.rmtree(os.getenv("UPLOAD_ROOT"))
    shutil.rmtree(os.getenv("CONVERTED_ROOT"))


@pytest.fixture
def broker():
    dramatiq.set_broker(StubBroker())
    dramatiq.get_broker().declare_queue("default")
    broker = dramatiq.get_broker()
    broker.flush_all()
    return broker


@pytest.fixture
def worker(broker):
    worker = dramatiq.Worker(broker, worker_timeout=10000)
    worker.start()
    yield worker
    worker.stop()
