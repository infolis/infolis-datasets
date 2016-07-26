#!/bin/bash
find ./SSOAR -print | file -if - | grep -v "application/pdf" 
