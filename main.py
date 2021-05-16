import pygame
import os

pygame.init()

SKY_TEXT = ["Hey bud, I saw that dude take your controller so I brought something to help out!",
            "Use W,A,S,D to move around!", "Use SPACE to attack!",
            "Use E to interact with stuff... oh I guess you figured that one out.",
            "ok im out of tips so good luck bud!", "No seriously there are no more tips. Go play the game.",
            "Dude, I only programmed this sprite to have so many text boxes its really gonna have to loop because you cant just go play the game."]
WIDTH, HEIGHT = 650, 650
TILE_SIZE = 33
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tyler's Tetris Adventure")

BACK = (255, 255, 255)
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'sky.png')), (WIDTH, HEIGHT))
FPS = 60

class Player:
    def __init__(self, x, y):
        self.images_right = []
        self.images_right.append(
            pygame.transform.scale(pygame.image.load(os.path.join('Assets','Tyler_Charc_Stand.png')),(40, 80)))
        self.images_right.append(
            pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Tyler_Charc_Walk1.png')), (40, 80)))
        self.images_right.append(
            pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Tyler_Charc_Stand.png')), (40, 80)))
        self.images_right.append(
            pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Tyler_Charc_Walk2.png')), (40, 80)))

        self.index = 0
        self.counter = 0
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False

    def update(self):
        dx = 0
        dy = 0
        walk_buffer = 20
        # get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
        if key[pygame.K_RIGHT]:
            dx += 5

        #changes walk animation
        self.counter += 1
        if self.counter > walk_buffer:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            self.image = self.images_right[self.index]

        # add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check for collision

        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            dy = 0

        # draw player onto screen
        WIN.blit(self.image, self.rect)


class World:
    def __init__(self, data):
        self.tile_list = []

        # load images
        dirt_img = pygame.image.load(os.path.join('Assets', 'dirt.png'))
        grass_img = pygame.image.load(os.path.join('Assets', 'grass.png'))

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            WIN.blit(tile[0], tile[1])


world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

world = World(world_data)
ty = Player(100, HEIGHT - 130)

def draw_window():
    WIN.fill(BACK)
    WIN.blit(BACKGROUND, (0, 0))



def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()
        world.draw()
        ty.update()
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
