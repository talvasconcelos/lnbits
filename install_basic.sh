#!/bin/bash

# install from GitHub
echo "# get the github code user(${githubUser}) branch(${githubBranch})"
git clone https://github.com/lnbits/lnbits-legend.git
cd lnbits

# prepare .env file
echo "# preparing env file"
cp .env.example .env
