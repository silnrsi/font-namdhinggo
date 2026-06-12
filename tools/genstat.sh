#!/bin/sh

SRC="$1"
TGT="$2"
cp -v "$SRC" "$TGT"
gftools gen-stat --inplace "$TGT"
