#pragma once

#include <QtCore/qglobal.h>

#ifdef QTYAML_CPP_DLL
# if defined(QTYAML_LIB)
#  define QTYAML_EXPORT Q_DECL_EXPORT
# else
#  define QTYAML_EXPORT Q_DECL_IMPORT
# endif
#else
# define QTYAML_EXPORT
#endif
