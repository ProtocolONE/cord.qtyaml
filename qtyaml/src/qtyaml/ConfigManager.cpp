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
      this->close();

      try {

        YAML::Node config = YAML::LoadFile(path.toStdString());
        for (YAML::iterator it = config.begin(); it != config.end(); ++it) {
          this->_data.insert(it->first.as<QString>(), it->second.as<QVariant>());
        }
        this->_isValid = true;
      }
      catch (const YAML::Exception& ex) {
        qWarning() << "Cannot read config file:" << path;
        qWarning() << "YAML::Exception:" << ex.what();
        this->_isValid = false;
      }
      
      return this->_isValid;
    }

    void ConfigManager::close()
    {
      this->_isValid = false;
      this->_data.clear();
    }

    const QVariantMap& ConfigManager::data() const
    {
      return this->_data;
    }
  }
}
