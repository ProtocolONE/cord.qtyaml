from conans import ConanFile, MSBuild, VisualStudioBuildEnvironment, tools

componentName = "QtYaml"

class QtYamlConan(ConanFile):
    name = componentName
#    version = "1.0"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Core here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "visual_studio"

    scm = {
      "type": "git",
      "url": "auto",
      "revision": "auto"
    }
    
    def build(self):
        customBuildType = self.settings.get_safe("build_type")
        #if self.options.shared == "False":
          #customBuildType = 'Static {0}'.format(customBuildType)
    
        msbuild = MSBuild(self)
        msbuild.build(
        "{0}/{0}.vcxproj".format(componentName)
         , build_type = customBuildType
         , platforms={ 
            "x86" : "Win32"
            ,'x86_64' : 'x64'
          }
      )

    def package(self):
        self.copy("*", dst="include", src="{0}/include".format(componentName))
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)

    def package_info(self):
      name = componentName
      if self.settings.arch == "x86":
        name += "x86"
        
      if self.settings.arch == "x86_64":
        name += "x64"
        
      if self.settings.build_type == "Debug":
        name += "d"

      name += ".lib"
      self.cpp_info.libs = [name] # The libs to link against
      
      
      self.cpp_info.includedirs = ['include']  # Ordered list of include paths
      self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found
      self.cpp_info.resdirs = ['res']  # Directories where resources, data, etc can be found
      self.cpp_info.bindirs = ['bin']  # Directories where executables and shared libs can be found
      self.cpp_info.defines = []  # preprocessor definitions
      self.cpp_info.cflags = []  # pure C flags
      self.cpp_info.cppflags = []  # C++ compilation flags
      self.cpp_info.sharedlinkflags = []  # linker flags
      self.cpp_info.exelinkflags = []  # linker flags
      
      #if self.options.shared == "False":
        #self.cpp_info.defines.append("{0}_STATIC_LIB".format(componentName.upper()))