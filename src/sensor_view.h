#ifndef SENSOR_VIEW_H
#define SENSOR_VIEW_H

#include <QWidget>
#include "ui_widget.h"
class QFileSystemModel;

class Widget : public QWidget, public Ui::Widget
{
    Q_OBJECT
    
public:
    Widget(QString list_dir, QWidget *parent = NULL);
    ~Widget();

private slots:
    void on_m_tree_view_doubleClicked(const QModelIndex &index);

private:
    QFileSystemModel* m_model;
};

#endif // SENSOR_VIEW_H
