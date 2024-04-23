import unittest
import pytest
from build123d import *
from ocp_addons.serializer import *

# not used now, but maybe helpful for other test cases
# TODO: remove if finally not needed


class DirectApiTestCase(unittest.TestCase):
    def assertTupleAlmostEquals(self, first, second, places=6, msg=None):
        """Check Tuples"""
        self.assertEqual(len(second), len(first))
        for i, j in zip(second, first):
            self.assertAlmostEqual(i, j, places, msg=msg)

    def assertTupleOfTupleAlmostEquals(self, first, second, places=6, msg=None):
        """Check Tuples"""
        self.assertEqual(len(second), len(first))
        for i, j in zip(second, first):
            self.assertTupleAlmostEquals(i, j, places, msg=msg)

    def assertVectorAlmostEquals(self, first, second, places=6, msg=None):
        second_vector = Vector(second)
        self.assertAlmostEqual(first.X, second_vector.X, places, msg=msg)
        self.assertAlmostEqual(first.Y, second_vector.Y, places, msg=msg)
        self.assertAlmostEqual(first.Z, second_vector.Z, places, msg=msg)


class TestSerializer3D(DirectApiTestCase):

    def test_serializer_simple_shape(self):
        shape = Box(10, 10, 10)
        buffer = serialize_shape(shape.wrapped)
        shape2 = deserialize_shape(buffer)
        self.assertAlmostEqual((shape - Solid(shape2)).volume, 0, 6)

    def test_serializer_complex_shape(self):
        shape = Box(1, 1, 1)
        shape -= Plane.YZ * Cylinder(0.2, 4)
        shape = fillet(shape.edges(), 0.1)

        buffer = serialize_shape(shape.wrapped)
        shape2 = deserialize_shape(buffer)
        self.assertAlmostEqual((shape - Solid(shape2)).volume, 0, 6)


class TestSerializer2D(DirectApiTestCase):

    def test_serializer_simple_face(self):
        shape = Circle(1)
        buffer = serialize_shape(shape.wrapped)
        shape2 = deserialize_shape(buffer)
        self.assertAlmostEqual((shape - Face(shape2)).area, 0, 6)

    def test_serializer_complex_face(self):
        shape = Circle(1)
        shape -= Pos(0.5, 0) * Circle(0.5)
        shape -= Pos(-0.6, -0.6) * Rectangle(0.4, 0.2)
        shape -= Pos(-0.2, 0.6) * RegularPolygon(0.4, 7)
        buffer = serialize_shape(shape.wrapped)
        shape2 = deserialize_shape(buffer)
        self.assertAlmostEqual((shape - Face(shape2)).area, 0, 6)


class TestSerializer1D(DirectApiTestCase):

    def test_serializer_simple_line(self):
        shape = Line((1, 0), (0, 1)).edge()
        buffer = serialize_shape(shape.wrapped)
        shape2 = deserialize_shape(buffer)
        self.assertAlmostEqual(shape.start_point(), Edge(shape2).start_point(), 0, 6)
        self.assertAlmostEqual(shape.end_point(), Edge(shape2).end_point(), 0, 6)
        self.assertAlmostEqual(shape.length, Edge(shape2).length, 0, 6)
        self.assertAlmostEqual(shape.geom_type, Edge(shape2).geom_type, 0, 6)

    def test_serializer_simple_circle(self):
        shape = Circle(1).edge()
        buffer = serialize_shape(shape.wrapped)
        shape2 = deserialize_shape(buffer)
        self.assertAlmostEqual(shape.length, Edge(shape2).length, 0, 6)
        self.assertAlmostEqual(shape.radius, Edge(shape2).radius, 0, 6)
        self.assertAlmostEqual(shape.geom_type, Edge(shape2).geom_type, 0, 6)
