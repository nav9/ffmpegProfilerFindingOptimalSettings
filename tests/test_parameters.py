from fileAndFolder import profilers
from fileAndFolder import fileFolderOperations as fileOps
from programConstants import constants

class TestPrameterFunctionality:
    def test_odd(self):
        parameterName = "crf"
        parameterValues = [1, 2, 3, 4, 5]
        p = profilers.Parameter(parameterName, parameterValues)  
        previousResultWasGood = None                      
        val, exhaustedOptions = p.getNewParameterValue(previousResultWasGood)
        assert 3 == val
        assert exhaustedOptions == False
        
    def test_even(self):
        parameterName = "crf"
        parameterValues = [1, 2, 3, 4]
        p = profilers.Parameter(parameterName, parameterValues)  
        previousResultWasGood = None                      
        val, exhaustedOptions = p.getNewParameterValue(previousResultWasGood)
        assert 3 == val
        assert exhaustedOptions == False
        
    def test_single(self):
        parameterName = "crf"
        parameterValues = [1]
        p = profilers.Parameter(parameterName, parameterValues)  
        previousResultWasGood = None                      
        val, exhaustedOptions = p.getNewParameterValue(previousResultWasGood)
        assert 1 == val
        assert exhaustedOptions == True
    
    def test_evenSelectMoreAndReset(self):
        parameterName = "crf"
        parameterValues = [1, 2, 3, 4]
        p = profilers.Parameter(parameterName, parameterValues)  
        previousResultWasGood = None          
        val, exhaustedOptions = p.getNewParameterValue(previousResultWasGood) #val would be 3
        previousResultWasGood = False #not happy with 3
        val, exhaustedOptions = p.getNewParameterValue(previousResultWasGood) #list should now be shrunk to [1, 2]        
        assert 2 == val
        assert exhaustedOptions == True
        p.reset() #list will be back to [1, 2, 3, 4]
        previousResultWasGood = None          
        val, exhaustedOptions = p.getNewParameterValue(previousResultWasGood) #val would be 3
        previousResultWasGood = True #happy with 3
        val, exhaustedOptions = p.getNewParameterValue(previousResultWasGood) #list should now be shrunk to [3, 4]        
        assert 4 == val
        assert exhaustedOptions == True        