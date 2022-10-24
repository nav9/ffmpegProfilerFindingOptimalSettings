from fileAndFolder import profilers
from fileAndFolder import fileFolderOperations as fileOps
from programConstants import constants

# class TestPrameterFunctionality:
#     def test_odd(self):
#         parameterName = "crf"
#         parameterValues = [1, 2, 3, 4, 5]
#         p = profilers.Parameter(None, parameterName, parameterValues)  
#         previousResultWasGood = None                      
#         exhaustedOptions = p.createNewParameterValue(previousResultWasGood)
#         val = p.getParameterValue()
#         assert 3 == val
#         assert exhaustedOptions == False
        
#     def test_even(self):
#         parameterName = "crf"
#         parameterValues = [1, 2, 3, 4]
#         p = profilers.Parameter(None, parameterName, parameterValues)  
#         previousResultWasGood = None                      
#         exhaustedOptions = p.createNewParameterValue(previousResultWasGood)
#         val = p.getParameterValue()
#         assert 3 == val
#         assert exhaustedOptions == False
        
#     def test_single(self):
#         parameterName = "crf"
#         parameterValues = [1]
#         p = profilers.Parameter(None, parameterName, parameterValues)  
#         previousResultWasGood = None                      
#         exhaustedOptions = p.createNewParameterValue(previousResultWasGood)
#         val = p.getParameterValue()
#         assert 1 == val
#         assert exhaustedOptions == True
    
#     def test_evenSelectMoreAndReset(self):
#         parameterName = "crf"
#         parameterValues = [1, 2, 3, 4]
#         p = profilers.Parameter(None, parameterName, parameterValues)  
#         previousResultWasGood = None          
#         exhaustedOptions = p.createNewParameterValue(previousResultWasGood) #val would be 3
#         val = p.getParameterValue()
#         previousResultWasGood = False #not happy with 3
#         exhaustedOptions = p.createNewParameterValue(previousResultWasGood) #list should now be shrunk to [1, 2]        
#         val = p.getParameterValue()
#         assert 2 == val
#         assert exhaustedOptions == True
#         p.reset() #list will be back to [1, 2, 3, 4]
#         previousResultWasGood = None          
#         exhaustedOptions = p.createNewParameterValue(previousResultWasGood) #val would be 3
#         val = p.getParameterValue()
#         previousResultWasGood = True #happy with 3
#         exhaustedOptions = p.createNewParameterValue(previousResultWasGood) #list should now be shrunk to [3, 4]        
#         val = p.getParameterValue()
#         assert 4 == val
#         assert exhaustedOptions == True        
        
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
        
    
    # def test_evenSelectMoreAndReset(self):
    #     parameterName = "crf"
    #     parameterValues = [1, 2, 3, 4]
    #     p = profilers.Parameter(None, parameterName, parameterValues)  
    #     previousResultWasGood = None          
    #     exhaustedOptions = p.createNewParameterValue(previousResultWasGood) #val would be 3
    #     val = p.getParameterValue()
    #     previousResultWasGood = False #not happy with 3
    #     exhaustedOptions = p.createNewParameterValue(previousResultWasGood) #list should now be shrunk to [1, 2]        
    #     val = p.getParameterValue()
    #     assert 2 == val
    #     assert exhaustedOptions == True
    #     p.reset() #list will be back to [1, 2, 3, 4]
    #     previousResultWasGood = None          
    #     exhaustedOptions = p.createNewParameterValue(previousResultWasGood) #val would be 3
    #     val = p.getParameterValue()
    #     previousResultWasGood = True #happy with 3
    #     exhaustedOptions = p.createNewParameterValue(previousResultWasGood) #list should now be shrunk to [3, 4]        
    #     val = p.getParameterValue()
    #     assert 4 == val
    #     assert exhaustedOptions == True         