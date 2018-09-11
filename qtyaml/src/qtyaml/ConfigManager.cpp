#include <QtYaml/ConfigManager.h>

namespace P1 {
  namespace QtYaml {

    ConfigManager::ConfigManager() : _isValid(false)
    {
    }

    ConfigManager::~ConfigManager()
    {
    }

    bool ConfigManager::valid() const
    {
      return this->_isValid;
    }

    bool ConfigManager::load(const QString& path)
    {
      if (this->_isValid)
        return true;

      try {

        this->_config = YAML::LoadFile(path.toStdString());
        this->_isValid = true;
      }
      catch (const YAML::Exception& /*ex*/) {
        this->_isValid = false;
      }
      
      return this->_isValid;
    }

    void ConfigManager::close()
    {
      this->_isValid = false;
      this->_config.reset();// = YAML::Node();
    }
  }
}
