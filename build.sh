#!/bin/bash

faas template pull
faas template pull https://github.com/s8sg/faasflow
faas build -f stack.yml
