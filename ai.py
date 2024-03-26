from game import Game, Bird, SCREEN_Y
import neat
import os
import pickle

def eval_genomes(genomes, config):
    game = Game()
    nets = []
    
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        game.birds.append(Bird())
        game.sprites.append(game.birds[-1])

    while len(game.birds) > 0:
        game.update()

        for i, bird in enumerate(game.birds):
            if bird.dead:
                nets.pop(i)
                genomes.pop(i)
                game.birds.pop(i)
                game.sprites.pop(i)
            else:
                genome.fitness = game.score 
                if len(game.pipes) > 1:
                    output = nets[i].activate((bird.y, abs(bird.y - game.pipes[0].y), abs(bird.y - game.pipes[1].y)))
                    if output[0] > 0.5:
                        bird.jump()

                else:
                    output = nets[i].activate((bird.y, SCREEN_Y - bird.y, SCREEN_Y - bird.y))
                    if output[0] > 0.5:
                        bird.jump()

    best_genome = None
    for genome_id, genome in genomes:
        if best_genome == None or genome.fitness > best_genome.fitness:
            best_genome = genome

    with open("ai.pickle", "wb") as f:
        pickle.dump(best_genome, f)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)