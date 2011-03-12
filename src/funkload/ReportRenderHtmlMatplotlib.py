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
import numpy

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

        plt.legend(loc='best')
        plt.savefig(image_path)


    # The rest of this file defines the same interface provided by the gd plotting file

    def appendDelays(self, delay, delay_low, delay_high, stats):
        """ Show percentiles or min, avg and max in chart. """
        pass

    def getYTitle(self):
        pass

    def createPageChart(self):
        """Create the page chart."""
        pages_spps_path = str(os.path.join(self.report_dir, 'pages_spps.png'))
        pages_path = str(os.path.join(self.report_dir, 'pages.png'))
        self._response_chart(filename_per_second=pages_spps_path,
                             filename_response=pages_path,
                             key='page',
                             key_name='Pages',
                             key_abbr='SP')

        return None

    def _hi_low_plot(self, ax, x, low, boxlow, med, boxhigh, high,labellow=None,labelhigh=None):
        """
        Make a plot which at each x-value a box with whiskers
        extending to the high and low values.
        """
        start=x
        # lower part of bars
        width=(x[-1]-x[0])/(2*len(x))
        from matplotlib import transforms
        ax.bar(left=start, 
               height=med-boxlow,
               bottom=boxlow,
               align='center',
               color='g',
               alpha=0.25,
               width=width,label=labellow)
        ax.errorbar(x=start,y=boxlow,
                  yerr=[boxlow-low,[0]*len(x)],
                  ecolor='g',fmt=None)

        # upper part of bars
        ax.bar(left=start, 
                height=boxhigh-med,
                bottom=med,
                align='center',
                color='r',
                alpha=0.25,
                width=width, label=labelhigh)
        ax.errorbar(x=start,y=boxhigh,
                  yerr=[[0]*len(x),high-boxhigh],
                  ecolor='r',fmt=None)


        #ax.set_xticks(start)
        #ax.set_xticklabels(x)
        return ax
        
    def _response_chart(self,filename_per_second,filename_response,key,
                        key_name, key_abbr):
        """Create response charts."""
        stats = self.stats
        cvus = []
        rps = []
        errors = []
        resp_min = []
        resp_avg = []
        resp_max = []
        percentile_10 = []
        percentile_50 = []
        percentile_90 = []
        percentile_95 = []
        scores = []
        apdexes = []
        has_error = False
        lines=0
        apdex_t = 0
        for cycle in self.cycles:
            if key not in stats[cycle]:
                continue
            lines+=1
            resp = stats[cycle][key]
            cvus.append(resp.cvus)
            error = resp.error_percent
            if error:
                has_error=True
            rps.append(resp.rps)
            errors.append(error)
            resp_min.append(resp.min)
            resp_avg.append(resp.avg)
            resp_max.append(resp.max)
            percentile_10.append(resp.percentiles.perc10)
            percentile_50.append(resp.percentiles.perc50)
            percentile_90.append(resp.percentiles.perc90)
            percentile_95.append(resp.percentiles.perc95)
            score = resp.apdex_score
            scores.append(score)
            apdex_t = resp.apdex.apdex_t
            apdex = [0]*5
            if score < 0.5:
                apdex[4] = score
            elif score < 0.7:
                apdex[3] = score
            elif score < 0.85:
                apdex[2] = score
            elif score < 0.94:
                apdex[1] = score
            else:
                apdex[0] = score
            apdexes.append(apdex)
        if lines==1:
            #no pages finished
            return

        cvus=numpy.asarray(cvus)
        resp_min=numpy.asarray(resp_min)
        resp_avg=numpy.asarray(resp_avg)
        resp_max=numpy.asarray(resp_max)
        percentile_10=numpy.asarray(percentile_10)
        percentile_50=numpy.asarray(percentile_50)
        percentile_90=numpy.asarray(percentile_90)
        percentile_95=numpy.asarray(percentile_95)
        fig=plt.figure()
        ax1=fig.add_subplot(211)
        ax2=fig.add_subplot(212, sharex=ax1)
        ax1.set_title(key_name+' Per Second')
        ax1.set_xlabel('Concurrent Users')
        ax1.set_ylabel(key_name+' per second')
        # turn off tick labels for upper axes
        plt.setp( ax1.get_xticklabels(), visible=False)
        
        #plt.ylim(ymin=0.0,ymax=max(stps))
        ax1.plot(cvus, rps, marker='.', label=key_abbr+'PS')
        ax1.grid(True)
        
        ax2.set_ylabel("Apdex %.1f"%apdex_t)
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f %%'))
        width=(cvus[-1]-cvus[0])/(1.2*len(cvus)*5)
        print width
        #width=0.12
        # transpose apdexes
        apdexes=numpy.asarray(apdexes).T
        start=numpy.asarray(cvus)
        ax2.bar(start, apdexes[0], width=width, label='E', color='#99CDFF')
        ax2.bar(start+width, apdexes[1],width=width,label='G', color='#00FF01')
        ax2.bar(start+2*width, apdexes[2],width=width,label='F', color='#FFFF00')
        ax2.bar(start+3*width, apdexes[3],width=width,label='P', color='#FF7C81')
        ax2.bar(start+4*width, apdexes[4],width=width,label='U', color='#C0C0C0')
        ax2.set_ylim(0,1)
        plt.axes(ax2)
        #plt.xticks(range(len(cvus)), cvus)

        # if has_error:
        #     ax2=plt.twinx()
        #     plt.ylabel("Error %")
        #     ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f %%'))
        #     plt.plot(errors, marker='^', label="Error %")
        #     plt.ylim(0,100)
        #     plt.axes(ax)
        ax1.legend(loc='best')
        fig.legend(*ax2.get_legend_handles_labels(), loc='lower right')
        fig.savefig(filename_per_second)

        fig=plt.figure()
        ax=fig.add_subplot(111)
        ax.set_title(key_name+' Response Time')
        ax.set_xlabel('Concurrent Users')
        ax.set_ylabel('Duration (s)')
        self._hi_low_plot(ax,cvus, 
                          low=resp_min,
                          boxlow=percentile_10,
                          med=percentile_50,
                          boxhigh=percentile_90,
                          high=percentile_95,
                          labellow='min/p10/p50',
                          labelhigh='p50/p90/p95')
        ax.plot(cvus,resp_avg,marker='x',color='b',label='avg')
        ax.legend(loc='best')
        ax.set_xlim(left=0)
        fig.savefig(filename_response)
        

    def createAllResponseChart(self):
        """Create global responses chart."""
        requests_rps_path = str(os.path.join(self.report_dir, 'requests_rps.png'))
        requests_path = str(os.path.join(self.report_dir, 'requests.png'))
        self._response_chart(filename_per_second=requests_rps_path,
                             filename_response=requests_path,
                             key='response',
                             key_name='Requests',
                             key_abbr='R')
        return None



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

