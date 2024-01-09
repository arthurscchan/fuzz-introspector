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

SINK_FUNCTION = {
    'CWE79': {
        'c-cpp': [
            ('', 'system'),
            ('', 'execl'),
            ('', 'execlp'),
            ('', 'execle'),
            ('', 'execv'),
            ('', 'execvp'),
            ('', 'execve'),
            ('', 'wordexp'),
            ('', 'popen'),
        ],
        'python': [
            ('<builtin>', 'exec'), ('<builtin>', 'eval'),
            ('subprocess', 'call'), ('subprocess', 'run'),
            ('subprocess', 'Popen'), ('subprocess', 'check_output'),
            ('os', 'system'), ('os', 'popen'), ('os', 'spawn'),
            ('os', 'spawnl'), ('os', 'spawnle'), ('os', 'spawnlp'),
            ('os', 'spawnlpe'), ('os', 'spawnv'), ('os', 'spawnvp'),
            ('os', 'spawnve'), ('os', 'spawnvpe'), ('os', 'exec'),
            ('os', 'execl'), ('os', 'execle'), ('os', 'execlp'),
            ('os', 'execlpe'), ('os', 'execv'), ('os', 'execve'),
            ('os', 'execvp'), ('os', 'execlpe'),
            ('asyncio', 'create_subprocess_shell'),
            ('asyncio', 'create_subprocess_exec'), ('asyncio', 'run'),
            ('asyncio', 'sleep'), ('logging.config', 'listen'),
            ('code.InteractiveInterpreter', 'runsource'),
            ('code.InteractiveInterpreter', 'runcode'),
            ('code.InteractiveInterpreter', 'write'),
            ('code.InteractiveConsole', 'push'),
            ('code.InteractiveConsole', 'interact'),
            ('code.InteractiveConsole', 'raw_input'), ('code', 'interact'),
            ('code', 'compile_command')
        ],
        'jvm': [
            ('java.lang.Runtime', 'exec'),
            ('javax.xml.xpath.XPath', 'compile'),
            ('javax.xml.xpath.XPath', 'evaluate'), ('java.lang.Thread', 'run'),
            ('java.lang.Runnable', 'run'),
            ('java.util.concurrent.Executor', 'execute'),
            ('java.util.concurrent.Callable', 'call'),
            ('java.lang.System', 'console'), ('java.lang.System', 'load'),
            ('java.lang.System', 'loadLibrary'),
            ('java.lang.System', 'mapLibraryName'),
            ('java.lang.System', 'runFinalization'),
            ('java.lang.System', 'setErr'), ('java.lang.System', 'setIn'),
            ('java.lang.System', 'setOut'),
            ('java.lang.System', 'setProperties'),
            ('java.lang.System', 'setProperty'),
            ('java.lang.System', 'setSecurityManager'),
            ('java.lang.ProcessBuilder', 'directory'),
            ('java.lang.ProcessBuilder', 'inheritIO'),
            ('java.lang.ProcessBuilder', 'command'),
            ('java.lang.ProcessBuilder', 'redirectError'),
            ('java.lang.ProcessBuilder', 'redirectErrorStream'),
            ('java.lang.ProcessBuilder', 'redirectInput'),
            ('java.lang.ProcessBuilder', 'redirectOutput'),
            ('java.lang.ProcessBuilder', 'start')
        ]
    },
    'CWE78': {
        'c-cpp': [],
        'python': [],
        'java': []
    },
    'CWE787': {
        'c-cpp': [],
        'python': [],
        'java': []
    },
    'CWE89': {
        'c-cpp': [],
        'python': [],
        'java': []
    },
    'CWE416': {
        'c-cpp': [],
        'python': [],
        'java': []
    },
    'CWE20': {
        'c-cpp': [],
        'python': [],
        'java': []
    },
    'CWE125': {
        'c-cpp': [],
        'python': [],
        'java': []
    },
    'CWE22': {
        'c-cpp': [],
        'python': [],
        'java': []
    },
    'CWE352': {
        'c-cpp': [],
        'python': [],
        'java': []
    },
    'CWE434': {
        'c-cpp': [],
        'python': [],
        'java': []
    },
}
