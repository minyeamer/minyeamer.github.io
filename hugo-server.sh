#!/bin/bash

TMP_PUBLIC="public_tmp"
rm -rf "$TMP_PUBLIC"
hugo server --gc --destination "public_tmp"