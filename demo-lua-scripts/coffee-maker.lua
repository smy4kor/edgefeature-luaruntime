function()
                    function brewBeans()
                     return 'beans are brewed'
                    end
            
                    function prepareHotWater()
                     return 'hot water prepared'
                    end
            
                    function makeCoffee()
                     return 'coffee is ready'
                    end
                    result = brewBeans()..'\n'
                    result = result..prepareHotWater()..'\n'
                    result = result..makeCoffee()
                    return result
end
