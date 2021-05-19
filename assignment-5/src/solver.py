# -*- coding: utf-8 -*-
"""
In this file your task is to write the solver function!

"""


def membership_function(x, a, c):
    b = (a + c) / 2
    return max(
        0,
        min(
            (x - a) / (b - a),
            1,
            (c - x) / (c - b)
        )
    )


def compute_membership_degrees(sett, x):
    membership_degrees = []
    for ab_pair in sett:
        membership_degrees.append(membership_function(x, ab_pair[0], ab_pair[1]))
    return membership_degrees


class Solver(object):
    def __init__(self):
        self.theta_sets = [
            (-1000, -25),  # NVB
            (-40, -10),    # NB
            (-20, 0),      # N
            (-5, 5),       # ZO
            (0, 20),       # P
            (10, 40),      # PB
            (25, 1000),    # PVB
        ]

        self.omega_sets = [
            (-1000, -3), # NB
            (-6, -0),    # N
            (-1, 1),     # ZO
            (0, 6),      # P
            (3, 1000)    # PB
        ]

        self.f_sets = [-32, -24, -16, -8, 0, 8, 16, 24, 32]

        self.rules_table = [[0 for j in range(len(self.omega_sets))] for i in range(len(self.theta_sets))]
        self.theta_memberships_degrees = []
        self.omega_memberships_degrees = []
        self.f_memberships_degrees = []

    def compute_membership_degrees_F(self):
        for i in range(len(self.theta_sets)):
            for j in range(len(self.omega_sets)):
                min_1 = self.theta_memberships_degrees[len(self.theta_sets) - i - 1]
                min_2 = self.omega_memberships_degrees[len(self.omega_sets) - j - 1]
                self.rules_table[i][j] = min(min_1, min_2)

        # for PVVB
        self.f_memberships_degrees.append(max(self.rules_table[0][0], self.rules_table[0][1], self.rules_table[1][0]))

        self.f_memberships_degrees.append(max(self.rules_table[2][0], self.rules_table[1][1], self.rules_table[0][2]))
        self.f_memberships_degrees.append(max(self.rules_table[3][0], self.rules_table[2][1], self.rules_table[1][2], self.rules_table[0][3]))
        self.f_memberships_degrees.append(max(self.rules_table[4][0], self.rules_table[3][1], self.rules_table[2][2], self.rules_table[1][3], self.rules_table[0][4]))
        self.f_memberships_degrees.append(max(self.rules_table[5][0], self.rules_table[4][1], self.rules_table[3][2], self.rules_table[2][3], self.rules_table[1][4]))
        self.f_memberships_degrees.append(max(self.rules_table[6][0], self.rules_table[5][1], self.rules_table[4][2], self.rules_table[3][3], self.rules_table[2][4]))
        self.f_memberships_degrees.append(max(self.rules_table[6][1], self.rules_table[5][2], self.rules_table[4][3], self.rules_table[3][4]))
        self.f_memberships_degrees.append(max(self.rules_table[6][2], self.rules_table[5][3], self.rules_table[4][4]))

        # for NVVB
        self.f_memberships_degrees.append(max(self.rules_table[6][4], self.rules_table[5][4], self.rules_table[6][3]))

    def defuzzify_f(self):
        denominator = sum(self.f_memberships_degrees)
        if denominator == 0:
            return None

        nominator = 0
        i = 0
        for membership_degree in reversed(self.f_memberships_degrees):
            nominator += membership_degree * self.f_sets[i]
            i += 1

        return nominator / denominator

    def solver(self, theta: float, omega: float):
        """
        Parameters
        ----------
        theta : TYPE: float
            DESCRIPTION: the angle theta
        omega : TYPE: float
            DESCRIPTION: the angular speed omega

        Returns
        -------
        F : TYPE: float
            DESCRIPTION: the force that must be applied to the cart
        or

        None :if we have a division by zero

        """

        # *** Step 1: Fuzzify Input Data: compute the membership degrees for theta and omega
        self.theta_memberships_degrees = compute_membership_degrees(self.theta_sets, theta)
        self.omega_memberships_degrees = compute_membership_degrees(self.omega_sets, omega)

        # *** Step 2: Compute the membership degree of F to each set
        self.compute_membership_degrees_F()

        # *** Step 3: Defuzzify the result of F
        return self.defuzzify_f()

