from game import Game

game = Game()

while not game.bird.dead:
    if len(game.pipes) > 1:
        if game.bird.y > game.pipes[1].y - 60 and game.bird.y > 175:
            game.bird.jump()

    game.update()

print(f"Score: {str(game.score)}")