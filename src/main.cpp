#include "sensor_view.h"
#include <QApplication>
#include <boost/array.hpp>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Widget w;
    w.showMaximized();
    return a.exec();
}
