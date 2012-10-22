#!/usr/bin/python
"""
Copyright 2011, UChicago Argonne, LLC

All Rights Reserved

plot_mdv, Code to plot a both ppis and rhis from an MDV object, version 0.5

Scott Collis, Argonne National Laboratory, ARM Climate Research Facility

OPEN SOURCE LICENSE

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
	
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.  Software changes, modifications, or derivative works, should be noted with comments and the author and organization?s name.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the names of UChicago Argonne, LLC or the Department of Energy nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

4. The software and the end-user documentation included with the redistribution, if any, must include the following acknowledgment:

   "This product includes software produced by UChicago Argonne, LLC under Contract No. DE-AC02-06CH11357 with the Department of Energy.?

******************************************************************************************************

DISCLAIMER

THE SOFTWARE IS SUPPLIED "AS IS" WITHOUT WARRANTY OF ANY KIND.

Neither the United States GOVERNMENT, nor the United States Department of Energy, NOR uchicago argonne, LLC, nor any of their employees, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, data, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights.

USE
---
See individual docstrings for functional usage

HISTORY
-------
5/23/2011:start (0.1) scollis@anl.gov
5/25/2011:Basic version done (0.2) scollis@anl.gov
6/24/2011: Adaptation into Py-ART as plot_mdv, version nudge (0.5) scollis@anl.gov
6/24/2011:Docstrings added, still need some more to cover how titling is done... scollis@anl.gov

"""

__author__ = "Scott Collis <scollis@anl.gov>"
__version__ = "0.5"
import sys
import os
from pylab import *
from numpy import ma, sin, cos, ones, zeros, pi, abs, sign
import getopt

def plot_rangering(rnge):
	"""
	plot a circle on the current plot at range rnge
	"""
	npts=100
	theta=linspace(0,2*pi, npts)
	r=ones([npts], dtype=float32)*rnge
	x=r*sin(theta)
	y=r*cos(theta)
	plot(x,y,'k-')

def plot_x(rnge):
	"""
	plot a cross hair of length rnge
	"""
	npts=100
	#vert
	x=zeros(npts, dtype=float32)
	y=linspace(-rnge, rnge, npts)
	plot(x,y,'k-')
	#hor
	y=zeros(npts, dtype=float32)
	x=linspace(-rnge, rnge, npts)
	plot(x,y,'k-')

def dt_to_dict(dt, **kwargs):
	"""
	Returns a dictionary from a datetime object perfect for use in a formatted string
	usage dict=(datetime.datetime object, pref= prefix string for the dictionary keys)
	"""
	pref=kwargs.get('pref', '')
	return dict( [(pref+key, getattr(dt, key)) for key in    ['year', 'month', 'day', 'hour', 'minute', 'second']])

def forminator():
	"""
	The forminator is used in future functions.. create a new forminator to format the titles of plots...
	"""
	return '%(radar_name)s %(ele).1f Degree %(scan_type)s %(begin_year)04d-%(begin_month)02d-%(begin_day)02d %(begin_hour)02d:%(begin_minute)02d \n %(fancy_name)s '

def fancy_names():
	"""
	Returns a dictionary for appending fancy names to a plot of MDV files... the moment names are typical of those from a TITAN setup
	"""
	return {'DBMHC':"Horizontal recieved power", 'DBMVC':"Vertical recieved power", 'DBZ':'Horizontal equivalent reflectivity factor', 'DBZ_F':'Horizontal equivalent reflectivity factor', 'DBZVC':'Vertical equivalent reflectivity factor', 'DBZVC_F':'Vertical equivalent reflectivity factor', 'VEL':"Radial velocity of scatterers (positive away)", 'VEL_F':"Radial velocity of scatterers (positive away)", 'WIDTH':"Spectral Width", 'WIDTH_F':"Spectral Width", 'ZDR':"Differential reflectivity", 'ZDR_F':"Differential reflectivity", 'RHOHV':'Co-Polar correlation coefficient', 'RHOHV_F':'Co-Polar Correlation Coefficient', 'PHIDP':"Differential propigation phase", 'PHIDP_F':"Differential propigation phase", 'KDP':"Specific differential phase", 'KDP_F':"Specific differential phase", 'NCP':"Normalized coherent power", 'NCP_F':"Normalized coherent power"}

def names_units():
	"""
	Returns units for moments in an MDV file, moment names are typical of those in a file generated by TITAN
	"""
	return {'DBMHC':" H Rec Power (dBm)", 'DBMVC':"V Rec Power (dBm)", 'DBZ':"Hz Eq. Ref. Fac (dBz)", 'DBZ_F':"Hz Eq. Ref. Fac (dBz)", 'DBZVC':"V Eq. Ref. Fac (dBz)", 'DBZVC_F':"V Eq. Ref. Fac (dBz)", 'VEL':"Rad. Vel. (m/s, +away)", 'VEL_F':"Rad. Vel. (m/s, +away)", 'WIDTH':"Spec. Width (m/s)", 'WIDTH_F':"Spec. Width (m/s)", 'ZDR':"Dif Refl (dB)", 'ZDR_F':"Dif Refl (dB)", 'RHOHV':"Cor. Coef (frac)", 'RHOHV_F':"Cor. Coef (frac)", 'PHIDP':"Dif Phase (deg)", 'PHIDP_F':"Dif Phase (deg)", 'KDP':"Spec Dif Ph. (deg/km)", 'KDP_F':"Spec Dif Ph. (deg/km)", 'NCP':"Norm. Coh. Power (frac)" , 'NCP_F':"Norm. Coh. Power (frac)"}

def make_info(mdvobj, fld):
	"""
	Concatinate metadata from the MDV file and info about the moment fld into one dictionary
	usage: dictionary=make_info(mdvobject, string of the moment you want to append)
	"""
	info=mdvobj.radar_info
	info.update({'scan_type':mdvobj.scan_type.upper()})
	info.update(dt_to_dict(mdvobj.times['time_begin'], pref='begin_'))
	info.update(dt_to_dict(mdvobj.times['time_end'], pref='end_'))
	name=names_units()[fld]
	units=dict([ (mdvobj.fields[i],mdvobj.field_headers[i]['units']) for i in range(len(mdvobj.fields))])[fld]
	fancy_name=fancy_names()[fld]
	info.update({'name':name, 'units':units, 'fancy_name' : fancy_name})
	return info
	

def corner_to_point(corner, point):
	"""
	Distance from a corner to a point in lat-lons given a spherical earth
	usage: x_distance, y_distance=corner_to_point([lat1, lon1], [lat2, lon2])
	"""
	pi=3.145
	Re=6371.0*1000.0
	Rc=ax_radius(point[0], units='degrees')
	#print Rc/Re
	y=((point[0]-corner[0])/360.0)*pi*2.0*Re
	x=((point[1]-corner[1])/360.0)*pi*2.0*Rc
	return x,y

def ax_radius(lat, units='radians'):
	"""Determine the radius of a circle of constant longitude at a certain Latitude
	usage radius=(latitude, units='degrees' or 'radians')
	"""
	Re=6371.0*1000.0
	if units=='degrees':
		const=pi/180.0
	else:
		const=1.0
	
	R=Re*sin(pi/2.0 - abs(lat*const))
	return R



def single_panel_ppi(mdvobj, sweep, fld, **kwargs):
	"""
	Make a single panel ppi (overhead view) plot of sweep number sweep of moment fld
	Usage
	single_panel_ppi(mdv_object, sweep_number, fld, rangerings=rnge_list, cross=crossnum, ylim=ylim_tup, xlim=xlim_tup, locs=loc_list, labels=label_list, tc=cross_col, sym=loc_sym, mask=mask_tup )
	mdv_object: py_mdv object for the radar
	sweep_number: int of the sweep number
	fld: String of the field (eg 'DBZ_F')
	rnge_list: a list of ranges that you want rings at (omit for none) eg: [100.0, 200.0]
	crossnum: float for the lenth of the cross (eg 100.0)
	ylim_tup: a (2) tuple to set the ylimits
	xlim_tup: a (2) tuple to set the xlimits
	loc_list: a list of tuples [lat, lon] where you want to plot locations
	label_list: a len(loc_list) list of strings to annotate loc_list positions
	cross_col: Matplotlib color string (eg 'w') for the the labels in label_list
	loc_sym: Matplotlib symbol identifier to be plotted at loc_list (eg 'bo' or 'r+' etc...)
	mask_tup: set for masking on another moment. eg to mask all data where NCP < 0.5 mask_tup=['NCP', 0.5]
	"""
	locs=kwargs.get('locs', [])
	labels=kwargs.get('labels', [])
	def_ranges={'DBMHC':[-100,0], 'DBMVC':[-100,0],
	'DBZ':[-16.0, 64.0], 'DBZ_F':[-16.0, 64.0], 'DBZVC':[-16.0, 64.0], 'DBZVC_F':[-16.0, 64.0],
	 'VEL':[-1.0*mdvobj.radar_info['unambig_vel_mps'],mdvobj.radar_info['unambig_vel_mps']], 'VEL_F':[-1.0*mdvobj.radar_info['unambig_vel_mps'],mdvobj.radar_info['unambig_vel_mps']], 
	 'WIDTH':[0.0, 10.0], 'WIDTH_F':[0.0, 10.0], 
	 'ZDR':[-3,6.0], 'ZDR_F':[-3,6.0], 
	 'RHOHV':[0.6, 1.0], 'RHOHV_F':[0.6, 1.0],
	 'PHIDP':[0,180.0], 'PHIDP_F':[-180.0,180.0],
	 'KDP':[-2,6], 'KDP_F':[-2,6], 
	 'NCP':[0,1], 'NCP_F':[0,1]}
	rges=kwargs.get('rges', def_ranges[fld])
	info_dict=make_info(mdvobj, fld)
	info_dict.update({'ele':mdvobj.el_deg[sweep]})
	tit_str=kwargs.get('tit_str', forminator())
	my_title=tit_str % info_dict
	x=mdvobj.carts['x'][sweep, :, :,]
	y=mdvobj.carts['y'][sweep, :, :,]
	z=mdvobj.carts['z'][sweep, :, :,]
	if 'mask' in kwargs.keys():
		mask=mdvobj.read_a_field(mdvobj.fields.index(kwargs['mask'][0]))[sweep,:,:]
		data=ma.masked_where(mask < kwargs['mask'][1],mdvobj.read_a_field(mdvobj.fields.index(fld))[sweep,:,:] )
	else:
		data=mdvobj.read_a_field(mdvobj.fields.index(fld))[sweep,:,:]
	pcolormesh(x/1000.0,y/1000.0,  data, vmin=rges[0], vmax=rges[1])
	radar_loc=[info_dict['latitude_deg'], info_dict['longitude_deg']]
	for i in range(len(locs)):
		carts=corner_to_point(radar_loc, locs[i])
		plot([carts[0]/1000.0, carts[0]/1000.0], [carts[1]/1000.0, carts[1]/1000.0], kwargs.get('sym', ['r+']*len(locs))[i])
		text(carts[0]/1000.0-5.0, carts[1]/1000.0, labels[i], color=kwargs.get('tc', 'k'))
	if 'rangerings' in kwargs.keys():
		for rge in kwargs['rangerings']:
			plot_rangering(rge)
	if 'cross' in kwargs.keys():
		plot_x(kwargs['cross'])
	xlabel('x (km)')
	ylabel('y (km)')
	if 'ylim' in kwargs.keys():
		ylim(kwargs['ylim'])
	if 'xlim' in kwargs.keys():
		xlim(kwargs['xlim'])
	cb=colorbar()
	cb.set_label(info_dict['name'])
	title(my_title)


def single_panel_rhi(mdvobj, sweep, fld, **kwargs):
	"""
	single_panel_rhi(mdv_object, sweep_number, fld, rangerings=rnge_list, ylim=ylim_tup, xlim=xlim_tup, mask=mask_tup )
	mdv_object: py_mdv object for the radar
	sweep_number: int of the sweep number
	fld: String of the field (eg 'DBZ_F')
	rnge_list: a list of ranges that you want rings at (omit for none) eg: [100.0, 200.0]
	ylim_tup: a (2) tuple to set the ylimits
	xlim_tup: a (2) tuple to set the xlimits
	mask_tup: set for masking on another moment. eg to mask all data where NCP < 0.5 mask_tup=['NCP', 0.5]
	"""
	locs=kwargs.get('locs', [])
	labels=kwargs.get('labels', [])
	def_ranges={'DBMHC':[-100,0], 'DBMVC':[-100,0],
	'DBZ':[-16.0, 64.0], 'DBZ_F':[-16.0, 64.0], 'DBZVC':[-16.0, 64.0], 'DBZVC_F':[-16.0, 64.0],
	 'VEL':[-1.0*mdvobj.radar_info['unambig_vel_mps'],mdvobj.radar_info['unambig_vel_mps']], 'VEL_F':[-1.0*mdvobj.radar_info['unambig_vel_mps'],mdvobj.radar_info['unambig_vel_mps']], 
	 'WIDTH':[0.0, 10.0], 'WIDTH_F':[0.0, 10.0], 
	 'ZDR':[-3,6.0], 'ZDR_F':[-3,6.0], 
	 'RHOHV':[0.6, 1.0], 'RHOHV_F':[0.6, 1.0],
	 'PHIDP':[0,180.0], 'PHIDP_F':[0,180.0],
	 'KDP':[-2,6], 'KDP_F':[-2,6], 
	 'NCP':[0,1], 'NCP_F':[0,1]}
	rges=kwargs.get('rges', def_ranges[fld])
	info_dict=make_info(mdvobj, fld)
	info_dict.update({'ele':mdvobj.az_deg[sweep]})
	tit_str=kwargs.get('tit_str', forminator())
	my_title=tit_str % info_dict
	x=mdvobj.carts['x'][sweep, :, :,]
	y=mdvobj.carts['y'][sweep, :, :,]
	z=mdvobj.carts['z'][sweep, :, :,]
	if 'mask' in kwargs.keys():
		mask=mdvobj.read_a_field(mdvobj.fields.index(kwargs['mask'][0]))[sweep,:,:]
		data=ma.masked_where(mask < kwargs['mask'][1],mdvobj.read_a_field(mdvobj.fields.index(fld))[sweep,:,:] )
	else:
		data=mdvobj.read_a_field(mdvobj.fields.index(fld))[sweep,:,:]
	pcolormesh(sign(y)*sqrt(y**2+x**2)/1000.0, z/1000.0,  data, vmin=rges[0], vmax=rges[1])
	if 'rangerings' in kwargs.keys():
		for rge in kwargs['rangerings']:
			plot_rangering(rge)
	xlabel(kwargs.get('xlab', 'Range (km)'))
	ylabel(kwargs.get('ylab', 'Distance above radar (km)'))
	if 'ylim' in kwargs.keys():
		ylim(kwargs['ylim'])
	if 'xlim' in kwargs.keys():
		xlim(kwargs['xlim'])
	cb=colorbar()
	cb.set_label(info_dict['name'])
	title(my_title)