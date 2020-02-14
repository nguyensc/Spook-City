from league import *
import pygame


class Controller():
    """
    Responsible for exchanging data between entities
    """
    def __init__(self):
        self.num_subscribers = 0
        self,subscribers = []
        self.impassables = []

    def get_subscribers(self):
        return self.subscribers

    def get_num_subscribers(self):
        return self.num_subscribers

    def get_impassables(self):
        return self.impassables

    def add_impassables(self, impassable):
        return self.impassables

    def add_subscriber(self, subscriber):
        self.num_subscribers += 1
        self.subscribers.append(subscriber)

    def update_subscribers_blocks(self):
        for subscriber in self.get_subscribers:
            subscriber.blocks = self.impassables

        
