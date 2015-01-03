import unittest

import cluster
from cluster import Vector, Cluster

class ClusterAlgoTest(unittest.TestCase):
    def test_one(self):

        center = cluster.Vector("1",[0,0,0])
        points = set([center])
        expected_clusters = cluster.Cluster(center=center, covers=set([center]))

        result_clusters = cluster.ClusterAlgo(r=1, points=points).solve()             
        self.assertEqual(result_clusters, [expected_clusters])

    def test_another(self):

        center = cluster.Vector("2",[1,1,1])
        points = set([center])
        expected_clusters = cluster.Cluster(center=center, covers=set([center]))

        result_clusters = cluster.ClusterAlgo(r=1, points=points).solve()             
        self.assertEqual(result_clusters, [expected_clusters])

    def test_three(self):

        center = Vector("0",[0,0,0])
        points = set([center,
                      Vector("1",[1,0,0]),
                      Vector("-1",[0,0,-1])
                      ])
        expected_clusters = cluster.Cluster(center=center, covers=points)

        result_clusters = cluster.ClusterAlgo(r=1, points=points).solve()             
        self.assertEqual(result_clusters, [expected_clusters])

    def test_two_cluster(self):

        center1 = Vector("0_1",[0,0,0])
        points1 = set([center1,
                      Vector("1_1",[1,0,0]),
                      Vector("-1_1",[0,0,-1])
                      ])


        center2 = Vector("0_2",[0,100,0])
        points2 = set([center2,
                      Vector("1_2",[1,100,0]),
                      Vector("-1_2",[0,100,-1])
                      ])
        
        expected_clusters = [Cluster(center=center1, covers=points1),
                             Cluster(center=center2, covers=points2)]

        result_clusters = cluster.ClusterAlgo(r=1, points=points1|points2).solve()             
        self.assertEqual(result_clusters, expected_clusters)        


class VectorTest(unittest.TestCase):
    def setUp(self):
        self.vector1 = Vector("0", [0,0])
        self.vector2 = Vector("1", [3,4])
        
    def test_self_distance(self):
        self.assertEquals(self.vector1.distance(self.vector1), 0)

    def test_distance(self):
        self.assertEquals(self.vector1.distance(self.vector2), 5)
        
    def test_equivalence(self):
        self.assertEquals(self.vector1.distance(self.vector2),
                          self.vector2.distance(self.vector1))
        

if __name__ == "__main__":
    unittest.main()
