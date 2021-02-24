import os
import urllib.request
import lupa
from lupa import LuaRuntime
lua = LuaRuntime(unpack_returned_tuples=True)

class LuaExecutor:
    def execute(self,filePath):
        print("execution path is: " + filePath)
        luaScriptStr = open(filePath, 'r').read()
        executorFunc = lua.eval(luaScriptStr)
        return executorFunc()
