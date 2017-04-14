import unittest
import model
import infection


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.name = "TestName"
        self.version = 2.0
        self.u = model.User(self.name,self.version)
        self.student = model.User('Student', self.version)
        self.teacher = model.User('Teacher', self.version)
        self.graph = model.Graph()

    def test_user(self):
        self.assertEqual(self.name, self.u.name)
        self.assertEqual(self.version, self.u.version)
        self.assertEqual(len(self.u.enrolled), 0)
        self.assertEqual(len(self.u.teacher), 0)

    def test_graph_add_users(self):
        self.assertNotIn(self.u, self.graph.user_map)
        self.graph.add_user(self.u)
        self.assertIsNotNone(self.graph.get_user(self.u.name))

    def test_classgraph_set_classroom(self):
        self.graph.set_classroom(self.teacher, [self.student])
        self.assertIn('0', self.graph.classmembers)
        self.assertIn('0', self.student.enrolled)
        self.assertIn('0', self.teacher.teacher)

class TestTotalInfection(unittest.TestCase):
    def setUp(self):
        self.single_user = model.User('Single')
        self.user_A = model.User('A')
        self.user_B = model.User('B')
        self.user_C = model.User('C')
        self.user_D = model.User('D')
        self.user_E = model.User('E')
        self.user_F = model.User('F')
        self.user_G = model.User('G')

        self.empty_graph = model.Graph()

        self.single_graph = model.Graph()
        self.single_graph.add_user(self.single_user)

        self.cyclic_graph = model.Graph()
        self.cyclic_graph.set_classroom(self.user_A, [self.user_B])
        self.cyclic_graph.set_classroom(self.user_B, [self.user_C])
        self.cyclic_graph.set_classroom(self.user_C, [self.user_A])

        self.general_graph = model.Graph()
        self.general_graph.set_classroom(
            self.user_D, [self.user_E, self.user_F, self.user_G],
        )

    def test_total_infection__none_user(self):
        infection.total_infect(self.general_graph, None, 'NewVersion')
        for user in self.general_graph.user_map.values():
            self.assertNotEqual(user.version, 'NewVersion')

    def test_total_infection__single(self):
        new_version = 'NewVersion'
        unconnected_user = model.User('New')
        self.single_graph.add_user(unconnected_user)
        infection.total_infect(self.single_graph, self.single_user, new_version)
        self.assertEqual(new_version, self.single_user.version)
        self.assertNotEqual(new_version, unconnected_user.version)

    def test_total_infection__cyclic(self):
        new_version = 'NewVersion'
        infection.total_infect(self.cyclic_graph, self.user_A, new_version)
        for user in self.cyclic_graph.user_map.values():
            self.assertEqual(new_version, user.version)

    def test_total_infection__general(self):
        new_version = 'NewVersion'
        new_version2 = 'NewVersion2'
        infection.total_infect(self.general_graph, self.user_D, new_version)
        for user in self.general_graph.user_map.values():
            self.assertEqual(new_version, user.version)
        infection.total_infect(self.general_graph, self.user_F, new_version2)
        for user in self.general_graph.user_map.values():
            self.assertEqual(new_version2, user.version)

class TestLimitedInfection(unittest.TestCase):
    def setUp(self):
        self.user_A = model.User('A')
        self.user_B = model.User('B')
        self.user_C = model.User('C')
        self.user_D = model.User('D')
        self.user_E = model.User('E')
        self.user_F = model.User('F')
        self.user_G = model.User('G')
        self.user_H = model.User('H')
        self.user_I = model.User('I')
        self.user_J = model.User('J')

        self.general_graph = model.Graph()
        self.general_graph.set_classroom(
            self.user_A, [self.user_B, self.user_C, self.user_D],
        )
        self.general_graph.set_classroom(
            self.user_E, [self.user_B, self.user_F],
        )
        self.general_graph.set_classroom(
            self.user_B, [self.user_G, self.user_H, self.user_I, self.user_J],
        )

    def test_limited_infection__1(self):
        old_version = '1.0'
        new_version = 'new_version'
        for user in self.general_graph.user_map.values():
            self.assertEqual(user.version, old_version)
        infection.limited_infect(self.general_graph, self.user_B, new_version, 1)
        for user in self.general_graph.user_map.values():
            self.assertEqual(user.version, old_version)

    def test_limited_infection__2(self):
        old_version = '1.0'
        new_version = 'new_version'
        assert_infected_users = [self.user_B, self.user_E, self.user_F]
        for user in self.general_graph.user_map.values():
            self.assertEqual(user.version, old_version)
        infection.limited_infect(self.general_graph, self.user_B, new_version, 2)
        for user in self.general_graph.user_map.values():
            if user in assert_infected_users:
                self.assertEqual(user.version, new_version)
            else:
                self.assertEqual(user.version, old_version)

    def test_limited_infection__3(self):
        old_version = '1.0'
        new_version = 'new_version'
        assert_infected_users = [self.user_B, self.user_E, self.user_F]
        for user in self.general_graph.user_map.values():
            self.assertEqual(user.version, old_version)
        infection.limited_infect(self.general_graph, self.user_B, new_version, 3)
        for user in self.general_graph.user_map.values():
            if user in assert_infected_users:
                self.assertEqual(user.version, new_version)
            else:
                self.assertEqual(user.version, old_version)

    def test_limited_infection__4(self):
        old_version = '1.0'
        new_version = 'new_version'
        assert_infected_users = [self.user_B, self.user_A, self.user_C, self.user_D]
        for user in self.general_graph.user_map.values():
            self.assertEqual(user.version, old_version)
        infection.limited_infect(self.general_graph, self.user_B, new_version, 4)
        for user in self.general_graph.user_map.values():
            if user in assert_infected_users:
                self.assertEqual(user.version, new_version)
            else:
                self.assertEqual(user.version, old_version)

    def test_limited_infection__5(self):
        old_version = '1.0'
        new_version = 'new_version'
        assert_infected_users = [self.user_B, self.user_G, self.user_H, self.user_I, self.user_J]
        for user in self.general_graph.user_map.values():
            self.assertEqual(user.version, old_version)
        infection.limited_infect(self.general_graph, self.user_B, new_version, 5)
        for user in self.general_graph.user_map.values():
            if user in assert_infected_users:
                self.assertEqual(user.version, new_version)
            else:
                self.assertEqual(user.version, old_version)

    def test_limited_infection__6(self):
        old_version = '1.0'
        new_version = 'new_version'
        assert_infected_users = [
            self.user_B, self.user_A, self.user_C, self.user_D, self.user_E, self.user_F
        ]
        for user in self.general_graph.user_map.values():
            self.assertEqual(user.version, old_version)
        infection.limited_infect(self.general_graph, self.user_B, new_version, 6)
        for user in self.general_graph.user_map.values():
            if user in assert_infected_users:
                self.assertEqual(user.version, new_version)
            else:
                self.assertEqual(user.version, old_version)

    def test_limited_infection__7(self):
        old_version = '1.0'
        new_version = 'new_version'
        assert_infected_users = [
            self.user_B, self.user_G, self.user_H, self.user_I, self.user_J, self.user_E, self.user_F
        ]
        for user in self.general_graph.user_map.values():
            self.assertEqual(user.version, old_version)
        infection.limited_infect(self.general_graph, self.user_B, new_version, 7)
        for user in self.general_graph.user_map.values():
            if user in assert_infected_users:
                self.assertEqual(user.version, new_version)
            else:
                self.assertEqual(user.version, old_version)

    def test_limited_infection__8(self):
        old_version = '1.0'
        new_version = 'new_version'
        assert_infected_users = [
            self.user_B, self.user_G, self.user_H, self.user_I, self.user_J, self.user_A, self.user_D, self.user_C
        ]
        for user in self.general_graph.user_map.values():
            self.assertEqual(user.version, old_version)
        infection.limited_infect(self.general_graph, self.user_B, new_version, 8)
        for user in self.general_graph.user_map.values():
            if user in assert_infected_users:
                self.assertEqual(user.version, new_version)
            else:
                self.assertEqual(user.version, old_version)

    def test_limited_infection__9(self):
        old_version = '1.0'
        new_version = 'new_version'
        assert_infected_users = [
            self.user_E, self.user_F, self.user_B, self.user_G, self.user_H, self.user_I, self.user_J, self.user_A, self.user_D, self.user_C
        ]
        for user in self.general_graph.user_map.values():
            self.assertEqual(user.version, old_version)
        infection.limited_infect(self.general_graph, self.user_B, new_version, 9)

        for user in self.general_graph.user_map.values():
            if user in assert_infected_users:
                self.assertEqual(user.version, new_version)
            else:
                self.assertEqual(user.version, old_version)

    def test_limited_infection__10(self):
        old_version = '1.0'
        new_version = 'new_version'
        assert_infected_users = [
            self.user_E, self.user_F, self.user_B, self.user_G, self.user_H, self.user_I, self.user_J,
            self.user_A, self.user_D, self.user_C
        ]
        for user in self.general_graph.user_map.values():
            self.assertEqual(user.version, old_version)
        infection.limited_infect(self.general_graph, self.user_B, new_version, 10)

        for user in self.general_graph.user_map.values():
            if user in assert_infected_users:
                self.assertEqual(user.version, new_version)
            else:
                self.assertEqual(user.version, old_version)

    def test_limited_infection__11(self):
        old_version = '1.0'
        new_version = 'new_version'
        assert_infected_users = [
            self.user_E, self.user_F, self.user_B, self.user_G, self.user_H, self.user_I, self.user_J,
            self.user_A, self.user_D, self.user_C
        ]
        for user in self.general_graph.user_map.values():
            self.assertEqual(user.version, old_version)
        infection.limited_infect(self.general_graph, self.user_B, new_version, 11)

        for user in self.general_graph.user_map.values():
            if user in assert_infected_users:
                self.assertEqual(user.version, new_version)
            else:
                self.assertEqual(user.version, old_version)


if __name__ == '__main__':
    unittest.main()