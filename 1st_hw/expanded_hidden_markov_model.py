# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 18:15:06 2018

@author: wattai
"""

import numpy as np


class exHMM():

    def __init__(self, pi, A, B, chi):
        self.pi = pi.copy()
        self.A_f = A.copy()
        self.A_b = A.T
        self.B = B.copy()
        self.chi = chi.copy()
        self.alpha_list = []
        self.beta_list = []
        self.p_forward = None
        self.p_backward = None

    def forward(self, alpha, s):
        # s: observed state.
        return self.B[:, s] * (alpha @ self.A_f)

    def p_terminate_forward(self, alpha_tail):
        return np.sum(self.A_f[:, -1] * alpha_tail, axis=0)

    def foralg(self, S):
        # n: number of iter.
        alpha = self.pi.copy()
        self.alpha_list = []
        for n, s in enumerate(S):
            alpha = self.B[:, s] * (alpha @ self.A_f)
            self.alpha_list.append(alpha)
        self.p_forward = self.p_terminate_forward(alpha_tail=alpha)

    def backward(self, beta, s):
        # s: observed state.
        return (self.B[:, s] * beta) @ self.A_b

    def p_terminate_backward(self, beta_head, s_head):
        print(self.B[:, 0] * beta_head)
        return np.sum(self.A_b[:, 0] * self.B[:, s_head] * beta_head, axis=0)

    def backalg(self, S):
        # n: number of iter.
        beta = self.chi.copy()
        self.beta_list = [beta]
        for n, s in enumerate(S[1:][::-1]):
            beta = (self.B[:, s] * beta) @ self.A_b
            self.beta_list.append(beta)
        self.p_backward = self.p_terminate_backward(beta_head=beta,
                                                    s_head=S[0])


if __name__ is "__main__":

    # HW params setting. -----------------------------------------
    n2, n1, n0 = 3, 1, 7
    S = np.array([2, 1, 0])  # state allocation is "0:H, 1:S, 2:A".

    pi = np.array([1, 0, 0, 0])
    A = np.array([[0, n0/10, (10-n0)/10, 0],
                  [0, (2+n2)/20, n0/20, (18-n0-n2)/20],
                  [0, (10-n0)/20, (n0+n1)/20, (10-n1)/20],
                  [0, 0, 0, 0]])
    # axis=0 is num of hidden state, axis=1 is num of state.
    # B.sum(axis=1) must be 1.
    # state allocation on axis=1 is "H, S, A".
    B = np.array([[0, 0, 0],
                  [n0/20, (19-n0-n1)/20, (1+n1)/20],  # Mother.
                  [(4+n2)/30, (20-n1-n2)/30, (6+n1)/30],  # Father.
                  [0, 0, 0]])
    chi = np.array([0, 0, 0, 1]) @ A.T
    # ---------------------------------------------------------
    """
    # 4-th class example for working test. --------------------
    pi = np.array([1, 0, 0, 0])
    S = np.array([0, 0, 1])  # state allocation is "0:H, 1:T".
    A = np.array([[0, 0.6, 0.4, 0],
                  [0, 0.9, 0.1, 0],
                  [0, 0.2, 0.8, 0],
                  [0, 0, 0, 0]])
    # axis=0 is num of hidden state, axis=1 is num of state.
    # B.sum(axis=1) must be 1.
    B = np.array([[1, 1],
                  [0.5, 0.5],
                  [0.3, 0.7],
                  [1, 1]])
    chi = np.array([1, 1, 1, 1])
    # ---------------------------------------------------------
    """
    # execution of HMM.
    N = len(S)
    hmm = exHMM(pi=pi, A=A, B=B, chi=chi)
    hmm.foralg(S)
    hmm.backalg(S)
    for i in range(N):
        print("alpha_%d: " % (i+1), hmm.alpha_list[i])
    for i in range(N-1, -1, -1):
        print("beta_%d: " % (N-i), hmm.beta_list[i])
    print("p_forward(X|lambda): %f" % hmm.p_forward)
    print("p_backward(X|lambda): %f" % hmm.p_backward)
