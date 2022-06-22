#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from envlib.weather_store import *
from envlib.accf import *
from envlib.io import *


class ClimateImpact(object):
    def __init__(self, path, **problem_config):
        self.p_settings = { # Default settings
            'lat_bound': None,
            'lon_bound': None,
            'time_bound': None,
            'rhi_threshold': 1.0,
            'horizontal_resolution': None,
            'NOx&inverse_EIs': 'TTV',
            'ac_type': None,
            'output_format': 'netCDF', 
            'mean': False,
            'std': False,
            'efficacy': False,
            'emission_scenario': 'pulse', 
            'climate_indicator': 'ATR', 
            'time_horizon': '20',
            'ac_type': 'wide-body',    
            'color': 'Reds', 
            'geojson': True,
            'save_path': None}
        self.p_settings.update(problem_config)
        self.ds_pl = xr.open_dataset(path['path_pl'])
        if path['path_sur']:
            self.ds_sur = xr.open_dataset(path['path_sur'])
        else:
            self.ds_sur = None
        ws = WeatherStore(self.ds_pl, self.ds_sur, ll_resolution=self.p_settings['horizontal_resolution'])
        if self.p_settings['lat_bound'] and self.p_settings['lon_bound']:
            ws.reduce_domain({'latitude': self.p_settings['lat_bound'], 'longitude': self.p_settings['lon_bound']})
        self.ds = ws.get_xarray()
        self.variable_names = ws.variable_names
        self.pre_variable_names = ws.pre_variable_names
        self.coordinate_names = ws.coordinate_names
        self.pre_coordinate_names = ws.pre_coordinate_names
        self.coordinates_bool = ws.coordinates_bool
        self.aCCF_bool = ws.aCCF_bool
        self.axes = ws.axes
        self.var_xr = ws.var_xr
        if path['path_lib']:
            self.path_lib = path['path_lib']

    def calculate_accfs(self, **seetings):
        confg = self.p_settings
        confg.update(seetings)
        clim_imp = GeTaCCFs(self, confg['rhi_threshold'])
        clim_imp.get_accfs(**confg)
        aCCFs, encoding_ = clim_imp.get_xarray()
        if self.p_settings['save_path']:
            path = self.p_settings['save_path']
            aCCFs.to_netcdf(path,  encoding=encoding_)
            print('\033[92m' + 'netCDF file has netCDF file has been successfully generated.' + "\033[0m" + f' (location: {path})')
            print('** The format of the generated file is compatible with Panoply ('
                  'https://www.giss.nasa.gov/tools/panoply/download/), an application for quickly visualizing '
                  'data **')
        pass
        if confg['Chotspots'] and confg['geojson']: 
            chotspots = gen_geojson_hotspots (aCCFs, self.p_settings['save_path'], self.p_settings['color'], time_pl=None)
            path_json = os.path.split(path) [0]
            print('\033[92m' + 'GeoJSON files have netCDF file has been successfully generated.' + "\033[0m" + f' (location: {path_json}'+'/json_files/)')

    def auto_plotting(self):
        pass

    def generate_output(self):
        pass
