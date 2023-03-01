# Copyright 2023 Fuzz Introspector Authors
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

MAX_FUZZERS_PER_PROJECT = 10
MAX_TARGET_PER_PROJECT_HEURISTIC = 100
MAX_THREADS = 4

BATCH_SIZE_BEFORE_DOCKER_CLEAN = 40

MAVEN_URL = "https://downloads.apache.org/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.zip"
GRADLE_URL = "https://services.gradle.org/distributions/gradle-7.4.2-bin.zip"

MAVEN_PATH = "apache-maven-3.6.3/bin"
GRADLE_HOME = "gradle-7.4.2"
GRADLE_PATH = f"{GRADLE_HOME}/bin"

git_repos = {
    'python': [
        # 'https://github.com/davidhalter/parso',
        'https://github.com/nvawda/bz2file',
        # 'https://github.com/executablebooks/markdown-it-py'
    ],
    'jvm': [
        'https://github.com/eclipse-ee4j/angus-mail',
        'https://github.com/junrar/junrar',
        'https://github.com/dom4j/dom4j',
        # 'https://github.com/spring-projects/spring-data-mongodb',
        # 'https://github.com/apache/commons-jxpath',
        # 'https://github.com/google/gson',
        # 'https://github.com/qos-ch/logback',
        # 'https://github.com/x-stream/xstream',
        # 'https://github.com/HtmlUnit/htmlunit',
        # 'https://github.com/spring-cloud/spring-cloud-config',
        # 'https://github.com/google/brotli',
        # 'https://github.com/qos-ch/reload4j',
        # 'https://github.com/apache/commons-beanutils',
        # 'https://github.com/qos-ch/slf4j',
        # 'https://github.com/openjdk/jdk/tree/master/src/java.xml/share/classes',
        # 'https://github.com/jboss-javassist/javassist',
    ]
}
