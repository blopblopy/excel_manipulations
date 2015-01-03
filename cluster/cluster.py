
import itertools
from collections import defaultdict

class Vector(object):
    def __init__(self, name, coord):
        self.name = name
        self.coord = tuple(coord)

    def distance(self, other):
        return sum((x-y)**2 for x,y in zip(self.coord, other.coord))**0.5

    def __eq__(self, other):
        return (self.name == other.name and self.coord == other.coord)

    def __ne__(self, other):
        return not self==other

    def __hash__(self):
        return hash(self.name) ^ hash(self.coord)

    def __str__(self):
        return 'Vector("%(name)s", %(coord)s)' % self.__dict__
    __repr__ = __str__
    

class Cluster(object):
    def __init__(self, center, covers):
        self.center = center
        self.covers = frozenset(covers) | frozenset([center])

    def __eq__(self, other):
        return (self.center == other.center and
                self.covers == other.covers)

    def __len__(self):
        return len(self.covers)

    def __str__(self):
        return "Cluster(%(center)s, %(covers)s)" % self.__dict__
    __repr__ = __str__

    

class ClusterAlgo(object):
    def __init__(self, r, points):
 
        self.uncovered = set(points)
        self.clusters = []

        self.r = r
        self.distances = defaultdict(dict)
        # find the pair-wise distance between points
        for x,y in itertools.combinations(points, 2):
            dist = x.distance(y)
            self.distances[x][y] = dist
            self.distances[y][x] = dist

    def propose_clusters(self):
        for point in self.uncovered:
            covers = (y for y,dist in self.distances[point].iteritems()
                      if dist <= self.r)
            yield Cluster(point, covers)
        
    def solve(self):
        while self.uncovered:
            cluster_candidates = self.propose_clusters()
            next_cluster = max(cluster_candidates,
                               key=lambda cluster:len(cluster))
            self.uncovered -= next_cluster.covers
            self.clusters.append(next_cluster)

        return self.clusters
