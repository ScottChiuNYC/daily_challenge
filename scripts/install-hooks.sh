#!/bin/sh
# Install git hooks to use the repository .githooks directory
git config core.hooksPath .githooks
echo "Configured git to use .githooks for hooks (run 'git config --get core.hooksPath' to verify)."
