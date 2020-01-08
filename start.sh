#!/usr/bin/env bash

gunicorn rbm.main:app --chdir /home/work/projects -b 0.0.0.0:5000
