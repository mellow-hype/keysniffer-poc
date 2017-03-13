#!/bin/bash
# Trivial Keysniffer PoC
# Author: _hyperlogic

# Getting the keycodes
xmodmap -pm -pk                             # list all keycodes
xmodmap -pm -pk | cut -sf 1                 # select column containing keycodes

