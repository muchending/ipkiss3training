# Copyright (C) 2020-2025 Luceda Photonics
# This version of Luceda Academy and related packages
# (hereafter referred to as Luceda Academy) is distributed under a proprietary License by Luceda
# It does allow you to develop and distribute add-ons or plug-ins, but does
# not allow redistribution of Luceda Academy  itself (in original or modified form).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.
#
# For the details of the licensing contract and the conditions under which
# you may use this software, we refer to the
# EULA which was distributed along with this program.
# It is located in the root of the distribution folder.


from ip_manager.testing import Compare, ComponentReferenceTest
import pytest
import numpy


@pytest.mark.comparisons([Compare.LayoutToGds, Compare.LayoutToXML, Compare.NetlistToXML, Compare.SMatrix])
class Test_Mux2Heated(ComponentReferenceTest):
    @pytest.fixture
    def component(self):
        from pteam_library_si_fab.all import Mux2Heated

        return Mux2Heated(name="Mux2HeatedDefault")

    @pytest.fixture
    def wavelengths(self):
        return numpy.linspace(1.54, 1.56, 200)
