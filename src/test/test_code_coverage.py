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

"""Test code_coverage.py"""

import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from fuzz_introspector import code_coverage  # noqa: E402
from fuzz_introspector.datatypes import function_profile  # noqa: E402

TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')


@pytest.fixture
def sample_jvm_coverage_xml():
    """Fixture for a sample jvm_coverage_xml"""
    cfg_str = """<!DOCTYPE report PUBLIC "-//JACOCO//DTD Report 1.1//EN" "report.dtd">
<report name="JaCoCo Coverage Report">
  <sessioninfo id="9253a4a5cb62-c5efb6cd" start="1669995723552" dump="1669995724729"/>
  <package name="">
    <class name="BASE64EncoderStreamFuzzer" sourcefilename="BASE64EncoderStreamFuzzer.java">
      <method name="&lt;init&gt;" desc="()V" line="23">
        <counter type="INSTRUCTION" missed="3" covered="0"/>
        <counter type="LINE" missed="1" covered="0"/>
        <counter type="COMPLEXITY" missed="1" covered="0"/>
        <counter type="METHOD" missed="1" covered="0"/>
      </method>
      <method name="fuzzerTestOneInput" desc="(LFuzzedDataProvider;)V" line="25">
        <counter type="INSTRUCTION" missed="2" covered="16"/>
        <counter type="LINE" missed="1" covered="1"/>
        <counter type="COMPLEXITY" missed="0" covered="1"/>
        <counter type="METHOD" missed="0" covered="1"/>
      </method>
    </class>
    <sourcefile name="BASE64EncoderStreamFuzzer.java">
      <line nr="23" mi="3" ci="0" mb="0" cb="0"/>
      <line nr="25" mi="0" ci="3" mb="0" cb="0"/>
      <line nr="27" mi="0" ci="6" mb="0" cb="0"/>
      <counter type="INSTRUCTION" missed="3" covered="21"/>
      <counter type="LINE" missed="1" covered="6"/>
      <counter type="COMPLEXITY" missed="1" covered="1"/>
      <counter type="METHOD" missed="1" covered="1"/>
      <counter type="CLASS" missed="0" covered="1"/>
    </sourcefile>
  </package>
</report>"""
    return cfg_str


def test_load_llvm_coverage():
    """Tests loading llvm coverage from a .covreport file."""
    cov_profile = code_coverage.load_llvm_coverage(TEST_DATA_PATH, 'sample_cov')
    assert len(cov_profile.covmap) > 0
    assert len(cov_profile.file_map) == 0
    assert len(cov_profile.branch_cov_map) > 0
    assert cov_profile._cov_type == "function"
    assert len(cov_profile.coverage_files) == 1
    assert len(cov_profile.dual_file_map) == 0

    assert cov_profile.covmap['BZ2_bzCompress'][0] == (408, 4680)
    assert cov_profile.covmap['BZ2_bzCompress'][7] == (416, 9360)
    assert cov_profile.covmap['BZ2_bzCompress'][10] == (420, 0)
    assert cov_profile.covmap['add_pair_to_block'][0] == (217, 36000000)
    assert cov_profile.covmap['add_pair_to_block'][4] == (221, 144000000)
    assert cov_profile.covmap['add_pair_to_block'][11] == (228, 3510000)
    assert cov_profile.covmap['fromtext_md'][1] == (21, 38)
    assert cov_profile.covmap['fromtext_md'][-2] == (40, 13)
    assert cov_profile.covmap['fallbackQSort3'][1] == (136, 1620000000)

    assert cov_profile.branch_cov_map['BZ2_bzCompress:411,8'] == [0, 4680]
    assert cov_profile.branch_cov_map['BZ2_bzCompress:414,8'] == [0, 4680]
    assert cov_profile.branch_cov_map['BZ2_bzCompress:417,4'] == [0, 9360, 0, 4680, 0, 4680]
    assert cov_profile.branch_cov_map['BZ2_bzCompress:425,20'] == [0, 0]
    assert cov_profile.branch_cov_map['BZ2_bzCompress:443,14'] == [0, 0]
    assert cov_profile.branch_cov_map['add_pair_to_block:220,16'] == [144000000, 36000000]
    assert cov_profile.branch_cov_map['add_pair_to_block:224,4'] == (
        [3260, 36000000, 3260, 3510000, 1570000])


def write_coverage_file(tmpdir, coverage_file):
    # Write the coverage_file
    path = os.path.join(tmpdir, "jacoco.xml")
    with open(path, "w") as f:
        f.write(coverage_file)


def generate_temp_function_profile(name, source):
    elem = dict()
    elem["functionName"] = name
    elem["functionSourceFile"] = source
    elem["functionLinenumber"] = 13
    elem['linkageType'] = None
    elem['returnType'] = None
    elem['argCount'] = None
    elem['argTypes'] = None
    elem['argNames'] = None
    elem['BBCount'] = None
    elem['ICount'] = None
    elem['EdgeCount'] = None
    elem['CyclomaticComplexity'] = None
    elem['functionsReached'] = []
    elem['functionUses'] = None
    elem['functionDepth'] = None
    elem['constantsTouched'] = None
    elem['BranchProfiles'] = []
    elem['Callsites'] = []

    return function_profile.FunctionProfile(elem)


def test_jvm_coverage(tmpdir, sample_jvm_coverage_xml):
    """Basic test for jvm coverage"""
    write_coverage_file(tmpdir, sample_jvm_coverage_xml)

    # Generate Coverage Profile
    cp = code_coverage.load_jvm_coverage(tmpdir)

    # Assure coverage profile has been correctly retrieved
    assert cp is not None

    # Ensure getting the correct coverage file
    assert len(cp.coverage_files) == 1
    assert cp.coverage_files == [os.path.join(tmpdir, "jacoco.xml")]

    # Ensure the coverage map result is correct
    assert len(cp.covmap) == 2
    assert "[BASE64EncoderStreamFuzzer].<init>()" in cp.covmap
    assert "[BASE64EncoderStreamFuzzer].fuzzerTestOneInput(FuzzedDataProvider)" in cp.covmap
    assert cp.covmap["[BASE64EncoderStreamFuzzer].<init>()"] == [(23, 0)]
    assert cp.covmap[
        "[BASE64EncoderStreamFuzzer].fuzzerTestOneInput(FuzzedDataProvider)"] == [(25, 3), (27, 6)]
