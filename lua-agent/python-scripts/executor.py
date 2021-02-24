import os
import urllib.request
import lupa
import subprocess
from lupa import LuaRuntime
lua = LuaRuntime(unpack_returned_tuples=True)


class LuaExecutor:

    def executeAsString(self, filePath):
        luaScriptStr = open(filePath, 'r').read()
        executorFunc = lua.eval(luaScriptStr)
        return executorFunc()

    def executeAsLuaFile(self, filePath):
        print("execution path is: " + filePath)
        execRes = self.executeLinuxCommands(["lua", filePath])
        res = ""
        for line in execRes:
            if(line):
                res += line
        return res

    def executeLinuxCommands(self, bashCommands):
        popen = subprocess.Popen(bashCommands, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line 
        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, bashCommands)
