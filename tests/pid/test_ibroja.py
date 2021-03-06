# -*- coding: utf-8 -*-

"""
Tests for dit.pid.ibroja.
"""

import pytest

from dit.pid.measures.ibroja import PID_BROJA
from dit.pid.measures.iproj import PID_Proj
from dit.pid.distributions import bivariates, trivariates


@pytest.mark.flaky(reruns=5)
def test_pid_broja1():
    """
    Test ibroja on a generic distribution.
    """
    d = bivariates['diff']
    pid = PID_BROJA(d, ((0,), (1,)), (2,))
    assert pid[((0,), (1,))] == pytest.approx(0.12255624891826589, abs=1e-4)
    assert pid[((0,),)] == pytest.approx(0.18872187554086706, abs=1e-4)
    assert pid[((1,),)] == pytest.approx(0.18872187554086706, abs=1e-4)
    assert pid[((0, 1),)] == pytest.approx(0.0, abs=1e-4)


@pytest.mark.flaky(reruns=5)
def test_pid_broja2():
    """
    Test ibroja on another generic distribution.
    """
    d = trivariates['anddup']
    pid = PID_BROJA(d, [[0], [1], [2]], [3])
    for atom in pid._lattice:
        if atom == ((0,), (1,), (2,)):
            assert pid[atom] == pytest.approx(0.31127812445913305, abs=1e-4)
        elif atom == ((0, 1), (1, 2)):
            assert pid[atom] == pytest.approx(0.5, abs=1e-4)
        else:
            assert pid[atom] == pytest.approx(0.0, abs=1e-4)


@pytest.mark.flaky(reruns=5)
def test_pid_broja3():
    """
    Test that iproj and ibroja are the same on reduced or.
    """
    d = bivariates['reduced or']
    pid1 = PID_BROJA(d)
    pid2 = PID_Proj(d)
    assert pid1 == pid2


@pytest.mark.flaky(reruns=5)
def test_pid_broja4():
    """
    Test that xor cat is incomplete, but nonnegative and consistent.
    """
    d = trivariates['xor cat']
    pid = PID_BROJA(d)
    assert not pid.complete
    assert pid.nonnegative
    assert pid.consistent
