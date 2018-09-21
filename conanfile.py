from conans import ConanFile, MSBuild, VisualStudioBuildEnvironment, tools
from conans.util.files import tmp_file

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
    generators = "visual_studio_multi"
    requires = "Qt/5.5.1@common/stable", "yaml-cpp/0.6.2@common/stable"
    build_requires = "Qt/5.5.1@common/stable", "yaml-cpp/0.6.2@common/stable"

    scm = {
      "type": "git",
      "url": "auto",
      "revision": "auto"
    }
    
    def build(self):
      self.output.warn('Using Qt: conan-{0}'.format(self.info.requires["Qt"].full_package_id))

      if self.options.shared == "True":
        tools.replace_in_file("{0}/{0}.vcxproj".format(componentName), "<ConfigurationType>StaticLibrary</ConfigurationType>", "<ConfigurationType>DynamicLibrary</ConfigurationType>")

      libMachine = {
        "x86" : "MachineX86"
        ,'x86_64' : 'MachineX64'
      }.get(self.settings.get_safe("arch"), "")
      
      libMachine_node = "<Lib>" \
                     "<TargetMachine>{}</TargetMachine>" \
                     "</Lib>".format(libMachine) if libMachine else ""
                     
      runtime_library = {"MT": "MultiThreaded",
                   "MTd": "MultiThreadedDebug",
                   "MD": "MultiThreadedDLL",
                   "MDd": "MultiThreadedDebugDLL"}.get(self.settings.get_safe("compiler.runtime"), "")

      runtime_node = "<RuntimeLibrary>" \
                     "{}" \
                     "</RuntimeLibrary>".format(runtime_library) if runtime_library else ""

      props_file_contents = """<?xml version="1.0" encoding="utf-8"?>
<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemDefinitionGroup>
    {0}
    <ClCompile>
      {1}
    </ClCompile>
    
  </ItemDefinitionGroup>
</Project>""".format(libMachine_node, runtime_node)

      with tmp_file(props_file_contents) as props_file_path:
        msbuild = MSBuild(self)
        msbuild.build(
        "{0}/{0}.vcxproj".format(componentName)
         , toolset = self.settings.compiler.toolset
         , platforms={ 
            "x86" : "Win32"
            ,'x86_64' : 'x64'
          }
          ,
          properties = {
            "ForceImportBeforeCppTargets" : props_file_path
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