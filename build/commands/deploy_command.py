# Copyright 2012 Google Inc. All Rights Reserved.

"""Runs a build and copies all output results of the specified rules to a path.
All of the output files of the specified rules will be copied to the target
output path. The directory structure will be exactly that of under the
various build-*/ folders but collapsed into one.

A typical deploy rule will bring together many result srcs, for example
converted audio files or compiled code, for a specific configuration.
One could have many such rules to target different configurations, such as
unoptimized/uncompiled vs. optimized/packed.

Examples:
# Copy all output files of :release_all to /some/bin/, merging the output
manage.py deploy --output=/some/bin/ :release_all
# Clean (aka delete) /some/bin/ before doing the copy
manage.py deploy --clean --output=/some/bin/ :release_all
"""

__author__ = 'benvanik@google.com (Ben Vanik)'


import argparse
import os
import shutil
import sys

import build.commands.util as commandutil
from build.manage import manage_command


def _get_options_parser():
  """Gets an options parser for the given args."""
  parser = argparse.ArgumentParser(prog='manage.py deploy')

  # Add all common args
  commandutil.add_common_args(parser)
  commandutil.add_common_build_args(parser, targets=True)

  # 'deploy' specific
  parser.add_argument('-o', '--output',
                      dest='output',
                      required=True,
                      help=('Output path to place all results. Will be created '
                            ' if it does not exist.'))
  parser.add_argument('-c', '--clean',
                      dest='clean',
                      action='store_true',
                      help=('Whether to remove all output files before '
                            'deploying.'))

  return parser


@manage_command('deploy', 'Builds and copies output to a target path.')
def deploy(args, cwd):
  parser = _get_options_parser()
  parsed_args = parser.parse_args(args)

  # Build everything first
  (result, all_target_outputs) = commandutil.run_build(cwd, parsed_args)
  if not result:
    # Failed - don't copy anything
    return False

  # Delete output, if desired
  if parsed_args.clean:
    shutil.rmtree(parsed_args.output)

  # Ensure output exists
  if not os.path.isdir(parsed_args.output):
    os.makedirs(parsed_args.output)

  # Copy results
  for target_output in all_target_outputs:
    # Get path relative to root
    # This will contain the build-out/ etc
    rel_path = os.path.relpath(target_output, cwd)

    # Strip the build-*/
    rel_path = os.path.join(*(rel_path.split(os.sep)[1:]))

    # Make output path
    deploy_path = os.path.normpath(os.path.join(parsed_args.output, rel_path))

    # Ensure directory exists
    # TODO(benvanik): cache whether we have checked yet to reduce OS cost
    deploy_dir = os.path.dirname(deploy_path)
    if not os.path.isdir(deploy_dir):
      os.makedirs(deploy_dir)

    # Copy!
    print '%s -> %s' % (target_output, deploy_path)
    shutil.copy2(target_output, deploy_path)

  return result
