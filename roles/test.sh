#!/bin/bash
for test in ./*/ ; do (cd "$test" && molecule lint); done
