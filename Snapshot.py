'''
Code from https://gist.github.com/snim2/255151
Additions by Eric Evans
'''

import pygame
import pygame.camera
import time
import os
from pygame.locals import *


DEVICE = '/dev/video0'
SIZE = (640, 480)
DIR = './captures'


class Snapshot(object):

    display = None
    camera = None
    
    def __init__(self):
        pygame.init()
        pygame.camera.init()

        
    def _get_image(self, screen):
        return self.camera.get_image(screen)

    
    def capture(self):
        screen = self._start()
      
        capture = True
        while capture:
            screen = self._get_image(screen)
            self.display.blit(screen, (0,0))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    capture = False
                elif event.type == KEYDOWN and (event.key == K_s or event.key == K_SPACE):
                    path = self._save(screen)
                    capture = False

        self._stop()
        return path

    
    def _start(self):        
        self.display = pygame.display.set_mode(SIZE, 0)
        self.camera = pygame.camera.Camera(DEVICE, SIZE)
        self.camera.start()
        
        return pygame.surface.Surface(SIZE, 0, self.display)
    

    def _save(self, img, filename=str(int(time.time()))):
        filename = '{}.png'.format(filename)
        path = os.path.join(DIR, filename)
        pygame.image.save(img, path)
        return path

    
    def _stop(self):
        self.camera.stop()
        pygame.quit()
    
    

    
if __name__ == '__main__':
    s = Snapshot()
    s.capture()
