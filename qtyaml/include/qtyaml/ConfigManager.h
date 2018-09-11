#include <QtYaml/qtyaml.h>
#include <QtYaml/qtyaml_global.h>

#include <QtCore/QString>
#include <yaml-cpp/yaml.h>

namespace P1 {
  namespace QtYaml {

    class QTYAML_EXPORT ConfigManager
    {
    public:
      ConfigManager();
      ~ConfigManager();

    public:
      bool load(const QString& fname);
      void close();
      bool valid() const;

      template <typename T> T value(const QString& name, const T& defValue) const
      {
        try {
          return this->_config[name].as<T>();
        }
        catch (const YAML::Exception& /*ex*/) {
          return defValue;
        }
      }

      template <typename T> bool value(const QString& name, T& value) const
      {
        try {
          T result = this->_config[name].as<T>();
          value = result;
          return true;
        }
        catch (const YAML::Exception& /*ex*/) {
          return false;
        }
      }

    private:

    private:
      bool _isValid;
      YAML::Node _config;
    };
  }
}