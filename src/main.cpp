#include "sensor_view.h"
#include <QApplication>
#include <QString>
#include <QDir>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    QString list_dir = QDir::home().absolutePath();
    if(argc > 1) list_dir = argv[1];

    Widget w(list_dir);
    w.showMaximized();

    return a.exec();
}
