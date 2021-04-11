import pickle
from message import Message

with open("message.pickle", "wb") as file_:
    pickle.dump(Message(), file_, -1)
