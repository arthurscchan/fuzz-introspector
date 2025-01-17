# Copyright 2022 Fuzz Introspector Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""High-level routines and CLI entrypoints"""

import logging
import os
import json
import yaml
import shutil
from typing import List, Optional

from fuzz_introspector import analysis
from fuzz_introspector import constants
from fuzz_introspector import diff_report
from fuzz_introspector import html_report
from fuzz_introspector import utils

from fuzz_introspector.frontends import oss_fuzz

logger = logging.getLogger(name=__name__)


def diff_two_reports(report1: str, report2: str) -> int:
    diff_report.diff_two_reports(report1, report2)
    return constants.APP_EXIT_SUCCESS


def correlate_binaries_to_logs(binaries_dir: str) -> int:
    pairings = utils.scan_executables_for_fuzz_introspector_logs(binaries_dir)
    logger.info("Pairings: %s", str(pairings))
    with open("exe_to_fuzz_introspector_logs.yaml", "w+") as etf:
        etf.write(yaml.dump({'pairings': pairings}))
    return constants.APP_EXIT_SUCCESS


def end_to_end(args) -> int:
    """Runs both frontend and backend."""
    if not args.language:
        args.language = utils.detect_language(args.target_dir)

    if args.out_dir:
        out_dir = args.out_dir
    else:
        out_dir = os.getcwd()

    if args.language == 'jvm':
        entrypoint = 'fuzzerTestOneInput'
    else:
        entrypoint = 'LLVMFuzzerTestOneInput'

    oss_fuzz.analyse_folder(language=args.language,
                            directory=args.target_dir,
                            entrypoint=entrypoint,
                            out=out_dir)

    if 'c' in args.language:
        language = 'c-cpp'
    else:
        language = args.language

    props: dict[str, str] = {}
    for property in args.properties:
        if property.count('=') == 1:
            key, value = property.split('=', 1)
            props[key] = value

    return run_analysis_on_dir(target_folder=out_dir,
                               coverage_url=args.coverage_url,
                               analyses_to_run=args.analyses,
                               correlation_file='',
                               enable_all_analyses=(not args.analyses),
                               report_name=args.name,
                               language=language,
                               out_dir=out_dir,
                               props=props)


def run_analysis_on_dir(target_folder: str,
                        coverage_url: str,
                        analyses_to_run: List[str],
                        correlation_file: str,
                        enable_all_analyses: bool,
                        report_name: str,
                        language: str,
                        output_json: Optional[List[str]] = None,
                        parallelise: bool = True,
                        dump_files: bool = True,
                        out_dir: str = '',
                        props: dict[str, str] = {}) -> int:
    """Runs Fuzz Introspector analysis from based on the results
    from a frontend run. The primary task is to aggregate the data
    and generate a HTML report."""

    constants.should_dump_files = dump_files

    if enable_all_analyses:
        for analysis_interface in analysis.get_all_analyses():
            if analysis_interface.get_name() not in analyses_to_run:
                analyses_to_run.append(analysis_interface.get_name())

    introspection_proj = analysis.IntrospectionProject(language, target_folder,
                                                       coverage_url)
    introspection_proj.load_data_files(parallelise, correlation_file, out_dir)

    logger.info("Analyses to run: %s", str(analyses_to_run))
    logger.info("[+] Creating HTML report")
    if output_json is None:
        output_json = []
    html_report.create_html_report(introspection_proj,
                                   analyses_to_run,
                                   output_json,
                                   report_name,
                                   dump_files,
                                   out_dir=out_dir,
                                   props=props)

    return constants.APP_EXIT_SUCCESS


def light_analysis(args) -> int:
    """Performs a light analysis, without any data from the frontends, so
    no compilation is needed for this analysis."""
    src_dir = os.getenv('SRC', '/src/')
    inspector_dir = os.path.join(src_dir, 'inspector')
    light_dir = os.path.join(inspector_dir, 'light')

    if not os.path.isdir(light_dir):
        os.makedirs(light_dir, exist_ok=True)

    all_tests = analysis.extract_tests_from_directories({src_dir},
                                                        args.language)

    with open(os.path.join(light_dir, 'all_tests.json'), 'w') as f:
        f.write(json.dumps(list(all_tests)))

    pairs = analysis.light_correlate_source_to_executable(args.language)
    with open(os.path.join(light_dir, 'all_pairs.json'), 'w') as f:
        f.write(json.dumps(list(pairs)))

    all_source_files = analysis.extract_all_sources(args.language)
    light_out_src = os.path.join(light_dir, 'source_files')

    for source_file in all_source_files:
        dst = light_out_src + '/' + source_file
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(source_file, dst)
    with open(os.path.join(light_dir, 'all_files.json'), 'w') as f:
        f.write(json.dumps(list(all_source_files)))

    return 0
