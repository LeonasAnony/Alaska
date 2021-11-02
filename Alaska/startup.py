import optparse
import subprocess
import sys
import os
import time

try:
    from Alaska import lib
    from Alaska import main
    from Alaska import config as cfg
except:
    pass



class StartUp:
    def __init__(self):
        self.ArgParser()
            
        if not self.options.skipchecks:
            deps = []
            self.missing_deps = []
        
            with open('requirements.txt') as f:
                self.requirements = f.read().splitlines()
                
            for i in self.requirements:
                deps.append(i.split("==")[0])
                
            self.check_deps(deps)
            
            if not self.passed:
                while True:
                    inp = input("\033[34mTry to install missing dependencies? [y/n]\033[0m")
                    if inp == "y":
                        self.installdeps()
                        break
                    elif inp == "n":
                        sys.exit("\033[31mDependency Check Failed\033[0m")
                    else:
                        pass
                    
        self.mapping = lib.Mappings(self.options.disablemqtt)

        if not os.path.exists(f"Alaska/lib/Neural/{cfg.neural_cfg['assistant_lang']}-{cfg.neural_cfg['assistant_version']}"):
            os.mkdir(f"Alaska/lib/Neural/{cfg.neural_cfg['assistant_lang']}-{cfg.neural_cfg['assistant_version']}")
            self.retrain_model()
        elif self.options.retrainmodel:
            self.retrain_model()
            
        main.Alaska(self.mapping, self.options.terminalmode)
        
    
    def ArgParser(self):
        usage = 'bin/Alaska'
        parser = optparse.OptionParser(usage=usage)
        parser.add_option('-r', '--retrainmodel',
                          action="store_true",
                          default=False,
                          dest="retrainmodel",
                          help='Boolean. If set to "True", the Neural Net will be retrained on startup.')
        parser.add_option('-c', '--skipchecks',
                          action="store_true",
                          default=False,
                          dest="skipchecks",
                          help='Boolean. If set to "True", all startup checks will be skipped. NOT RECOMMENDED, CAN CAUSE ERRORS')
        parser.add_option('-t', '--terminalmode',
                          action="store_true",
                          default=False,
                          dest="terminalmode",
                          help='Boolean. If set to "True", input will be taken from terminal rather than Mic.')
        parser.add_option('-m', '--disablemqtt',
                          action="store_true",
                          default=False,
                          dest="disablemqtt",
                          help='Boolean. If set to "True", MQTT will not be used.')
        self.options, args = parser.parse_args()
        
        
    def retrain_model(self):
        assistant = lib.GenericAssistant(f"Alaska/lib/Neural/Alaska_{cfg.neural_cfg['assistant_lang']}-{cfg.neural_cfg['assistant_version']}.json", intent_methods=self.mapping.get_mappings(True), model_name=f"{cfg.neural_cfg['assistant_lang']}-{cfg.neural_cfg['assistant_version']}")
        assistant.train_model()
        assistant.save_model()
        
    
    def check_deps(self, dependencies):
        self.passed = True
        for i in range(len(dependencies)):
            try:
                if i == 0:
                    import gtts
                elif i == 1:
                    import ibm_watson
                elif i == 2:
                    import jellyfish
                elif i == 3:
                    import paho
                elif i == 4:
                    import pyjokes
                elif i == 5:
                    import pyowm
                elif i == 6:
                    import pytz
                elif i == 7:
                    import spotipy
                elif i == 8:
                    import wikipedia
                elif i == 9:
                    import wolframalpha

            except:
                print(f"\033[31mImport failed for: {dependencies[i]}\033[0m\n")
                self.missing_deps.append(dependencies[i])
                self.passed = False
                
        if self.passed:
            print("\033[32mRequirements already satisfied.\033[0m\n")
        else:
            print(f"\033[33mRequires: {str(self.missing_deps)}\033[0m\n")
            print("\033[31mNot all requirements satisfied.\033[0m")
            
        
    def installdeps(self):
        self.installed = True
        for i in self.missing_deps:
            ret = subprocess.call(f"pip3 install {i}")
            time.sleep(5)

            if ret == 0:
                print(f"\033[32mInstallation for: {i} was successfull.\033[0m\n")
            else:
                print(f"\033[31mInstallation failed for: {i}\033[0m\n")
                self.installed = False
                
        if self.installed:
            print("\033[32mAll missing packages successfully installed.\033[0m\n")
        else:
            sys.exit("\033[31mPACKAGE INSTALLATION FAILED\033[0m")
