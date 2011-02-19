# (C) Copyright 2011 Jason Grout
# Author: Jason Grout, jason.grout@drake.edu
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
"""Render chart using Matplotlib.
"""

import os
from ReportRenderRst import rst_title
from ReportRenderHtmlBase import RenderHtmlBase
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

MATPLOTLIB_DEFAULT=False

class RenderHtmlMatplotlib(RenderHtmlBase):
    """Render stats in html using matplotlib.

    Simply render stuff in ReST than ask docutils to build an html doc.
    """
    def createTestChart(self):
        """Create the test chart."""
        image_path = str(os.path.join(self.report_dir, 'tests.png'))
        stats = self.stats
        errors = []
        stps = []
        cvus = []
        has_error = False
        lines=0
        for cycle in self.cycles:
            if 'test' not in stats[cycle]:
                continue
            lines+=1
            test = stats[cycle]['test']
            stps.append(test.tps)
            error = test.error_percent
            if error:
                has_error = True
            errors.append(error)
            cvus.append(str(test.cvus))

        plt.figure()
        ax=plt.axes()
        plt.title('Successful Tests Per Second')
        plt.xlabel('Concurrent Users')
        plt.ylabel('Tests per second')
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        plt.ylim(ymin=0.0,ymax=max(stps))
        plt.plot(stps, marker='.', label='STPS')
        plt.grid(True)
        plt.xticks(range(len(cvus)), cvus)

        if has_error:
            ax2=plt.twinx()
            plt.ylabel("Error %")
            ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f %%'))
            plt.plot(errors, marker='^', label="Error %")
            plt.ylim(0,100)
            plt.axes(ax)

        plt.legend(loc=0)
        plt.savefig(image_path)


    # The rest of this file defines the same interface provided by the gd plotting file

    def appendDelays(self, delay, delay_low, delay_high, stats):
        """ Show percentiles or min, avg and max in chart. """
        pass

    def getYTitle(self):
        pass

    def createPageChart(self):
        """Create the page chart."""


    def createAllResponseChart(self):
        """Create global responses chart."""
        pass


    def createResponseChart(self, step):
        """Create responses chart."""
        pass


    # monitoring charts
    def createMonitorCharts(self):
        """Create all montirored server charts."""
        pass


    def createMonitorChart(self, host):
        """Create monitrored server charts."""
        pass

