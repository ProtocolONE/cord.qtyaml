#pragma once

#include <QtYaml/qtyaml.h>
#include <QtYaml/qtyaml_global.h>

#include <QtCore/QString>
#include <QtCore/QDebug>

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
      const QVariantMap& data() const;
      
      template <typename T> T value(const QString& path, const T& defValue) const
      {
        T result;
        if (!tryValue(path, result))
          return defValue;

        return result;
      }

      template <typename T> bool tryValue(const QString& path, T& value) const
      {
        QStringList names = path.split('\\');
        if (names.empty()) {
          qWarning() << "Ivalid value path:" << path;
          return false;
        }

        QVariant result = this->_data[names.front()];
        names.pop_front();

        while (!names.empty()) {

          const QString& name = names.front();

          if (result.type() != QMetaType::QVariantMap)
            break;

          result = result.toMap()[name];
          names.pop_front();
        }

        if (!names.empty()) {
          qWarning() << "Value path not found:" << path;
          return false;
        }

        value = YAML::variantTo<T>(result);
        return result.isValid();
      }

    private:

    private:
      bool _isValid;
      QVariantMap _data;
    };
  }
}