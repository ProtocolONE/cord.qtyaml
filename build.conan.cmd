set PackageName=QtYaml/1.0.0@common/stable

call install.deps.cmd

conan create ./conanfile.py %PackageName% -pr ./conan/msvcprofiled
conan create ./conanfile.py %PackageName% -pr ./conan/msvcprofile

@rem conan test QtYamlTest QtYaml/1.0.0@common/stable -pr msvcprofile
conan upload %PackageName% --all -r=p1
