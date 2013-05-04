#-------------------------------------------------
#
# Project created by QtCreator 2013-04-16T08:21:29
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = sensor_view
TEMPLATE = app


SOURCES += main.cpp\
        sensor_view.cpp \
    sensor_view_widget.cpp \
    viewpic.cpp

HEADERS  += sensor_view.h \
    sensor_view_widget.h \
    viewpic.h

FORMS    += widget.ui

RESOURCES += ../res/res.qrc

INCLUDEPATH += $$(BOOST_ROOT)
LIBPATH += $(BOOST_ROOT)/stage/lib
