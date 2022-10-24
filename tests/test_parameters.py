from fileAndFolder import profilers
from fileAndFolder import fileFolderOperations as fileOps
from programConstants import constants as const

class TestPrameterFunctionality:
    def test_odd(self):
        parameterName = "crf"
        parameterValues = [1, 2, 3, 4, 5]
        p = profilers.Parameter(None, parameterName, parameterValues)  
        assert 3 == p.getParameterValue()
        assert False == p.isThisParameterExhausted()
        previousResultWasGood = True        
        p.createNewParameterValue(previousResultWasGood)
        assert 4 == p.getParameterValue()
        assert False == p.isThisParameterExhausted()
        previousResultWasGood = True        
        p.createNewParameterValue(previousResultWasGood)
        assert 5 == p.getParameterValue()        
        assert True == p.isThisParameterExhausted()

    def test_even(self):
        parameterName = "crf"
        parameterValues = [1, 2, 3, 4]
        p = profilers.Parameter(None, parameterName, parameterValues)  
        assert 2 == p.getParameterValue()
        assert False == p.isThisParameterExhausted()
        previousResultWasGood = False
        p.createNewParameterValue(previousResultWasGood)
        assert 1 == p.getParameterValue()
        assert True == p.isThisParameterExhausted()
        
    def test_single(self):
        parameterName = "crf"
        parameterValues = [1]
        p = profilers.Parameter(None, parameterName, parameterValues)  
        assert 1 == p.getParameterValue()
        assert True == p.isThisParameterExhausted()
        
    def test_reset(self):
        parameterName = "crf"
        parameterValues = [1, 2, 3, 4, 5]
        p = profilers.Parameter(None, parameterName, parameterValues)  
        previousResultWasGood = True        
        p.createNewParameterValue(previousResultWasGood)
        previousResultWasGood = True        
        p.createNewParameterValue(previousResultWasGood)
        p.resetIndices()
        assert 3 == p.getParameterValue()
        assert False == p.isThisParameterExhausted()
        
    
class TestBinarySearchSelector:
    def test_settingNewParameter(self):    
        param1_name = "P1"
        param1_values = [4,7,3,3]
        param2_name = "P2"
        param2_values = ['a', 's', 'd', 'f']        
        p = None        
        p = profilers.Parameter(p, param1_name, param1_values)
        p = profilers.Parameter(p, param2_name, param2_values)        
        s = profilers.BinarySearchSelector(p) 
        c = s.getParameters()
        shouldNowBe = {param2_name: 's', param1_name: 7}
        assert str(shouldNowBe) == str(c) #converted to str just to ensure it's an exact match even in terms of the sequence of keys and values
        
    def test_settingParameterRepeatedly(self):    
        param1_name = "P1"
        param1_values = [4, 7, 3]
        param2_name = "P2"
        param2_values = ['a', 's', 'd', 'f']        
        p = None        
        p = profilers.Parameter(p, param1_name, param1_values)
        p = profilers.Parameter(p, param2_name, param2_values)        
        s = profilers.BinarySearchSelector(p) 
        c = s.getParameters()
        shouldNowBe = {param2_name: 's', param1_name: 7}
        assert str(shouldNowBe) == str(c) #converted to str just to ensure it's an exact match even in terms of the sequence of keys and values
        c = s.getParameters()
        shouldNowBe = {param2_name: 's', param1_name: 7}
        assert str(shouldNowBe) == str(c) #should remain same as the earlier assert        
        previousResultWasGood = False
        s.setNewParameters(previousResultWasGood)
        c = s.getParameters()
        shouldNowBe = {param2_name: 's', param1_name: 4}
        assert str(shouldNowBe) == str(c)   
        previousResultWasGood = False
        s.setNewParameters(previousResultWasGood)
        c = s.getParameters()
        shouldNowBe = {param2_name: 'a', param1_name: 7}
        assert str(shouldNowBe) == str(c) 
        